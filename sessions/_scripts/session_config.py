"""Per-session config: the hard prerequisite gate for the transcript pipeline.

The GM identity and any mic sharing are USER-PROVIDED FACTS. They are declared in
`sN-session-config.json` before any analysis runs and are never inferred from a
transcript. Every stage that needs to know who the GM is, or which identities a
diarized stream carries, loads them from here.

Config discovery order (first hit wins), relative to `sessions/`:
    1. `sN-devin/sN-session-config.json`
    2. `config/sN-session-config.json`
    3. `data/index/sN-session-config.json`

Schema (see `sessions/s12-devin/s12-session-config.json` for a filled example):

    {
      "session_id": "s12",
      "gm": "Luke S",
      "players": { "<person label>": "<character>", ... },
      "shared_mics": [
        {
          "mic_label": "Luke S",
          "note": "...",
          "carries": [
            { "person": "Luke S",   "identity": "GM",    "kind": "gm" },
            { "person": "Kristina", "identity": "Aggie", "kind": "player_character" }
          ]
        }
      ],
      "raw_speaker_labels": { "<garbled label>": "<canonical person label>", ... }
    }

`raw_speaker_labels` is spelling normalization for PERSON labels only. Diarization
is per-mic, not per-person: a raw label names a microphone stream, so it may carry
several identities — but only the ones declared in `shared_mics`.
"""

import json
import os
import sys

GM_IDENTITY = "GM"
GM_KIND = "gm"
PLAYER_KIND = "player_character"
VALID_KINDS = (GM_KIND, PLAYER_KIND)

CONFIG_SEARCH_DIRS = (
    os.path.join("{session_id}-devin"),
    "config",
    os.path.join("data", "index"),
)


class SessionConfigError(Exception):
    """Raised when a session config is missing, unreadable, or incomplete."""


class Identity:
    """One identity carried by a microphone stream."""

    def __init__(self, person, identity, kind):
        self.person = person
        self.identity = identity
        self.kind = kind

    @property
    def is_gm(self):
        return self.kind == GM_KIND

    @property
    def character(self):
        return None if self.is_gm else self.identity

    def __repr__(self):
        return f"Identity(person={self.person!r}, identity={self.identity!r}, kind={self.kind!r})"


class SharedMic:
    """A microphone stream declared to carry more than one identity."""

    def __init__(self, mic_label, identities, note=""):
        self.mic_label = mic_label
        self.identities = identities
        self.note = note

    def identity_labels(self):
        return [i.identity for i in self.identities]

    def player_identities(self):
        return [i for i in self.identities if i.kind == PLAYER_KIND]

    def __repr__(self):
        return f"SharedMic(mic_label={self.mic_label!r}, identities={self.identity_labels()!r})"


class SessionConfig:
    def __init__(self, session_id, gm, players, shared_mics, raw_speaker_labels, path):
        self.session_id = session_id
        self.gm = gm
        self.players = players
        self.shared_mics = shared_mics
        self.raw_speaker_labels = raw_speaker_labels
        self.path = path

    # -- person / identity lookups ------------------------------------------

    @property
    def person_labels(self):
        return [self.gm] + [p for p in self.players if p != self.gm]

    @property
    def characters(self):
        return list(self.players.values())

    def canonical_person(self, raw_label):
        """Normalize a raw diarization label to a canonical person label."""
        return self.raw_speaker_labels.get(raw_label, raw_label)

    def shared_mic(self, person):
        for mic in self.shared_mics:
            if mic.mic_label == person:
                return mic
        return None

    def is_shared_mic(self, person):
        return self.shared_mic(person) is not None

    def carrying_mic(self, person):
        """The shared mic a person rides, when they have no stream of their own."""
        for mic in self.shared_mics:
            if mic.mic_label == person:
                continue
            if any(identity.person == person for identity in mic.identities):
                return mic
        return None

    def has_own_mic(self, person):
        return self.carrying_mic(person) is None

    def solo_identity(self, person):
        """The single identity a non-shared stream carries."""
        if person == self.gm:
            return Identity(person, GM_IDENTITY, GM_KIND)
        if person in self.players:
            return Identity(person, self.players[person], PLAYER_KIND)
        return None

    def declared_identities(self, person):
        """Every identity a stream may be decomposed into, per the config."""
        mic = self.shared_mic(person)
        if mic:
            return list(mic.identities)
        solo = self.solo_identity(person)
        return [solo] if solo else []

    def identity(self, person, identity_label):
        for candidate in self.declared_identities(person):
            if candidate.identity == identity_label:
                return candidate
        return None


# -- loading & validation ---------------------------------------------------


def default_sessions_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def config_search_paths(session_id, sessions_dir=None):
    sessions_dir = sessions_dir or default_sessions_dir()
    filename = f"{session_id}-session-config.json"
    return [
        os.path.join(sessions_dir, template.format(session_id=session_id), filename)
        for template in CONFIG_SEARCH_DIRS
    ]


def find_config_path(session_id, sessions_dir=None):
    for path in config_search_paths(session_id, sessions_dir):
        if os.path.exists(path):
            return path
    return None


def _parse_shared_mics(raw, players, gm, violations):
    if raw is None:
        violations.append(
            "`shared_mics` is missing — declare `[]` to state that no mics are shared."
        )
        return []
    if not isinstance(raw, list):
        violations.append("`shared_mics` must be a list.")
        return []

    known_people = dict(players)
    known_people.setdefault(gm, None)
    mics = []
    for index, entry in enumerate(raw):
        where = f"shared_mics[{index}]"
        if not isinstance(entry, dict):
            violations.append(f"{where} must be an object.")
            continue
        mic_label = entry.get("mic_label")
        if not mic_label:
            violations.append(f"{where}.mic_label is required.")
            continue
        if mic_label not in known_people:
            violations.append(
                f"{where}.mic_label {mic_label!r} is not the GM or a declared player."
            )
        carries = entry.get("carries")
        if not isinstance(carries, list) or len(carries) < 2:
            violations.append(
                f"{where}.carries must list the 2+ identities the mic carries."
            )
            continue

        identities = []
        for slot, carried in enumerate(carries):
            slot_where = f"{where}.carries[{slot}]"
            if not isinstance(carried, dict):
                violations.append(f"{slot_where} must be an object.")
                continue
            person = carried.get("person")
            identity_label = carried.get("identity")
            kind = carried.get("kind")
            if not person or not identity_label or not kind:
                violations.append(
                    f"{slot_where} requires `person`, `identity`, and `kind`."
                )
                continue
            if kind not in VALID_KINDS:
                violations.append(
                    f"{slot_where}.kind {kind!r} must be one of {list(VALID_KINDS)}."
                )
                continue
            if kind == GM_KIND:
                if person != gm:
                    violations.append(
                        f"{slot_where} declares {person!r} as GM, but `gm` is {gm!r}."
                    )
                if identity_label != GM_IDENTITY:
                    violations.append(
                        f"{slot_where}.identity must be {GM_IDENTITY!r} for a gm slot."
                    )
            else:
                if person not in players:
                    violations.append(
                        f"{slot_where}.person {person!r} is not in `players`."
                    )
                elif players[person] != identity_label:
                    violations.append(
                        f"{slot_where}.identity {identity_label!r} does not match "
                        f"`players[{person!r}]` = {players[person]!r}."
                    )
            identities.append(Identity(person, identity_label, kind))

        mics.append(SharedMic(mic_label, identities, entry.get("note", "")))
    return mics


def _parse_raw_speaker_labels(raw, person_labels, violations):
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        violations.append("`raw_speaker_labels` must be an object.")
        return {}
    labels = {}
    for key, value in raw.items():
        if key.startswith("_"):
            continue
        if not isinstance(value, str):
            violations.append(f"`raw_speaker_labels[{key!r}]` must be a string.")
            continue
        if value not in person_labels:
            violations.append(
                f"`raw_speaker_labels[{key!r}]` maps to {value!r}, which is not a "
                "declared person label. This map normalizes spelling of PERSON "
                "labels only — character routing belongs in `players`/`shared_mics`."
            )
        labels[key] = value
    return labels


def load_session_config(session_id, sessions_dir=None, config_path=None):
    """Load and validate a session config, or raise SessionConfigError."""
    path = config_path or find_config_path(session_id, sessions_dir)
    if not path:
        searched = "\n".join(
            f"    - {p}" for p in config_search_paths(session_id, sessions_dir)
        )
        raise SessionConfigError(
            f"No session config found for {session_id!r}. Searched:\n{searched}\n"
            "Before any analysis, obtain and record the GM and shared-mic config "
            "from the user (see `.agent/workflows/add-session.md` Step 0). The "
            "pipeline never infers the GM or mic sharing from the transcript."
        )
    if not os.path.exists(path):
        raise SessionConfigError(f"Session config not found at {path}.")

    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as exc:
        raise SessionConfigError(f"{path} is not valid JSON: {exc}") from exc

    violations = []
    if data.get("session_id") != session_id:
        violations.append(
            f"`session_id` is {data.get('session_id')!r}, expected {session_id!r}."
        )

    gm = data.get("gm")
    if not gm or not isinstance(gm, str):
        violations.append(
            "`gm` is required: the person label that is the GM. Ask the user — "
            "never infer it from the transcript."
        )
        gm = gm if isinstance(gm, str) else ""

    players = data.get("players")
    if not isinstance(players, dict) or not players:
        violations.append("`players` must be a non-empty person-label -> character map.")
        players = {}
    else:
        for person, character in players.items():
            if not isinstance(character, str) or not character:
                violations.append(f"`players[{person!r}]` must be a character name.")
        characters = [c for c in players.values() if isinstance(c, str)]
        duplicates = {c for c in characters if characters.count(c) > 1}
        if duplicates:
            violations.append(f"Duplicate characters in `players`: {sorted(duplicates)}.")

    shared_mics = _parse_shared_mics(data.get("shared_mics"), players, gm, violations)
    person_labels = [gm] + list(players)
    raw_speaker_labels = _parse_raw_speaker_labels(
        data.get("raw_speaker_labels"), person_labels, violations
    )

    if violations:
        detail = "\n".join(f"    - {v}" for v in violations)
        raise SessionConfigError(
            f"{path} is not a usable session config:\n{detail}"
        )

    return SessionConfig(
        session_id=session_id,
        gm=gm,
        players=players,
        shared_mics=shared_mics,
        raw_speaker_labels=raw_speaker_labels,
        path=path,
    )


def gate(session_id, stage, sessions_dir=None, config_path=None):
    """Hard prerequisite gate. Returns the config or exits with status 2."""
    try:
        return load_session_config(session_id, sessions_dir, config_path)
    except SessionConfigError as exc:
        print(f"❌ BLOCKED — {stage} cannot run for {session_id}.", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        sys.exit(2)


def describe(config):
    lines = [
        f"Session config: {config.path}",
        f"  GM: {config.gm}",
        "  Players: "
        + ", ".join(f"{person} ({character})" for person, character in config.players.items()),
    ]
    if config.shared_mics:
        for mic in config.shared_mics:
            carried = ", ".join(
                f"{i.identity} [{i.person}]" for i in mic.identities
            )
            lines.append(f"  Shared mic {mic.mic_label!r} carries: {carried}")
    else:
        lines.append("  Shared mics: none declared")
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python session_config.py <session_id> [--config PATH]")
        sys.exit(1)
    override = None
    if "--config" in sys.argv:
        override = sys.argv[sys.argv.index("--config") + 1]
    print(describe(gate(sys.argv[1], "session-config check", config_path=override)))
