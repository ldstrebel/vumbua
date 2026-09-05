"""Attribution harness for Session 12 — every assertion is derived from the config.

Run:
    python sessions/s12-devin/test_attribution.py          # run the harness
    python sessions/s12-devin/test_attribution.py --list   # list generated assertions

The shared-mic assertions are GENERATED from `s12-session-config.json`. Because the
config declares that the mic labeled "Luke S" carries both the GM and Kristina's
Aggie, the harness requires at least one `Luke S -> Aggie` segment — the
decomposition is mandatory, not optional. A session whose config declares no
shared mics generates no such assertion, so the harness never guesses in either
direction.
"""

import collections
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

KIT_DIR = os.path.dirname(os.path.abspath(__file__))
SESSIONS_DIR = os.path.dirname(KIT_DIR)
SCRIPTS_DIR = os.path.join(SESSIONS_DIR, "scripts")
SESSION_ID = "s12"

sys.path.insert(0, SCRIPTS_DIR)
import session_config as sc  # noqa: E402

CONFIG = sc.load_session_config(SESSION_ID, sessions_dir=SESSIONS_DIR)
ATTRIBUTION = {}
WORK_DIR = None


def run_stage(script, args, expect_success=True):
    result = subprocess.run(
        [sys.executable, os.path.join(SCRIPTS_DIR, script)] + args,
        capture_output=True,
        text=True,
    )
    if expect_success and result.returncode != 0:
        raise AssertionError(
            f"{script} {' '.join(args)} failed ({result.returncode}):\n"
            f"{result.stdout}\n{result.stderr}"
        )
    return result


def setUpModule():
    """Run the real pipeline stages into a scratch dir and load the output."""
    global WORK_DIR, ATTRIBUTION
    WORK_DIR = tempfile.mkdtemp(prefix="s12-attribution-")
    run_stage("prep_raw.py", [SESSION_ID, "--out-dir", WORK_DIR])
    run_stage(
        "attribute_speakers.py",
        [SESSION_ID, "--index-dir", WORK_DIR, "--out-dir", WORK_DIR],
    )
    with open(os.path.join(WORK_DIR, f"{SESSION_ID}-attribution.json"), encoding="utf-8") as f:
        ATTRIBUTION = json.load(f)


def segments(**match):
    return [
        segment
        for segment in ATTRIBUTION["segments"]
        if all(segment.get(key) == value for key, value in match.items())
    ]


class TestConfigGate(unittest.TestCase):
    """The config is a hard prerequisite: no config, no pipeline."""

    def test_prep_raw_refuses_without_a_config(self):
        result = run_stage("prep_raw.py", ["s99"], expect_success=False)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("BLOCKED", result.stderr)

    def test_attribution_refuses_without_a_config(self):
        result = run_stage("attribute_speakers.py", ["s99"], expect_success=False)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("BLOCKED", result.stderr)

    def test_pipeline_refuses_a_config_without_a_gm(self):
        with open(CONFIG.path, encoding="utf-8") as handle:
            data = json.load(handle)
        data.pop("gm")
        path = os.path.join(WORK_DIR, "no-gm-config.json")
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(data, handle)
        for script in ("prep_raw.py", "attribute_speakers.py"):
            with self.subTest(script=script):
                result = run_stage(
                    script, [SESSION_ID, "--config", path], expect_success=False
                )
                self.assertEqual(result.returncode, 2)
                self.assertIn("`gm` is required", result.stderr)


class TestConfigDrivenAttribution(unittest.TestCase):
    """Attribution may only ever use identities the config declares."""

    def test_gm_identity_comes_only_from_the_declared_gm(self):
        for segment in segments(identity=sc.GM_IDENTITY):
            self.assertEqual(segment["person"], CONFIG.gm)

    def test_no_segment_invents_an_undeclared_identity(self):
        for segment in ATTRIBUTION["segments"]:
            if segment["kind"] in ("needs_decomposition", "npc"):
                continue
            declared = [i.identity for i in CONFIG.declared_identities(segment["stream"])]
            self.assertIn(segment["identity"], declared, segment)

    def test_npc_segments_are_voiced_by_the_gm(self):
        for segment in segments(kind="npc"):
            self.assertEqual(segment["voiced_by"], sc.GM_IDENTITY)
            self.assertEqual(segment["person"], CONFIG.gm)
            self.assertNotIn(segment["identity"], CONFIG.characters)

    def test_no_violations_reported(self):
        self.assertEqual(ATTRIBUTION["violations"], [])

    def test_a_declared_character_cannot_be_laundered_through_the_npc_path(self):
        """`NPC:Aggie` must be rejected, not silently stripped of its person."""
        decisions_path = os.path.join(SESSIONS_DIR, ATTRIBUTION["decisions_file"])
        with open(decisions_path, encoding="utf-8") as handle:
            decisions = json.load(handle)
        mic_label = CONFIG.shared_mics[0].mic_label
        lines = decisions["mics"][mic_label]["lines"]
        character = next(iter(CONFIG.characters))
        first = lines[next(iter(lines))]
        first[0]["identity"] = f"NPC:{character}"
        path = os.path.join(WORK_DIR, "npc-launder-decisions.json")
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(decisions, handle)
        scratch = os.path.join(WORK_DIR, "npc-launder")
        result = run_stage(
            "attribute_speakers.py",
            [SESSION_ID, "--index-dir", WORK_DIR, "--out-dir", scratch, "--decisions", path],
            expect_success=False,
        )
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("player character declared in the session config", result.stdout + result.stderr)


class TestRenderedClean(unittest.TestCase):
    """The rendered clean transcript must be complete and lossless."""

    @classmethod
    def setUpClass(cls):
        cls.path = os.path.join(WORK_DIR, f"{SESSION_ID}-clean-attributed.md")
        run_stage("render_clean.py", [
            SESSION_ID, "--index-dir", WORK_DIR,
            "--attribution", os.path.join(WORK_DIR, f"{SESSION_ID}-attribution.json"),
            "--out", cls.path,
        ])
        with open(cls.path, encoding="utf-8") as handle:
            cls.rendered = handle.read()

    def test_every_shared_mic_line_is_decomposed(self):
        self.assertEqual(ATTRIBUTION["unresolved_shared_mic_lines"], [])

    def test_render_carries_every_character_of_the_indexed_transcript(self):
        """Zero-loss: the rendered text is a permutation of the indexed text."""
        squash = lambda text: collections.Counter(re.sub(r"[^a-z0-9]+", "", text.lower()))
        indexed = os.path.join(WORK_DIR, f"{SESSION_ID}-raw-indexed.md")
        bodies = []
        with open(indexed, encoding="utf-8") as handle:
            for raw in handle:
                match = re.match(r"^L\d+: \*\*.+?:\*\* (.*)$", raw.rstrip("\n"))
                if match:
                    bodies.append(match.group(1))
        missing = squash("".join(bodies)) - squash(self.rendered)
        self.assertEqual(dict(missing), {})

    def test_shared_mic_speech_is_labelled_with_its_person(self):
        mic = CONFIG.shared_mics[0]
        for identity in mic.identities:
            if identity.is_gm:
                continue
            self.assertIn(
                f"[[{identity.identity}]] (PC, {identity.person} on {mic.mic_label}'s mic)",
                self.rendered,
            )


class TestOutOfCharacter(unittest.TestCase):
    """Table talk is a fact about the table, so it applies to every stream at once."""

    @classmethod
    def setUpClass(cls):
        cls.path = os.path.join(WORK_DIR, f"{SESSION_ID}-clean-ooc.md")
        run_stage("render_clean.py", [
            SESSION_ID, "--index-dir", WORK_DIR,
            "--attribution", os.path.join(WORK_DIR, f"{SESSION_ID}-attribution.json"),
            "--out", cls.path,
        ])
        with open(cls.path, encoding="utf-8") as handle:
            cls.entries = [line for line in handle if line.startswith("**[[")]

    def test_declared_ranges_reach_every_stream(self):
        """A range is useless if only the mic that was audited line-by-line honours it."""
        self.assertTrue(ATTRIBUTION["ooc_ranges"])
        people = {segment["person"] for segment in ATTRIBUTION["segments"]
                  if segment.get("ooc")}
        self.assertIn(CONFIG.gm, people)
        for person in CONFIG.players:
            if CONFIG.has_own_mic(person):
                self.assertIn(person, people, f"{person} never reads as out of character")

    def test_no_character_speaks_during_declared_table_talk(self):
        """The complaint this fixes: character names all over the pre-session chatter."""
        ranges = [(r["from"], r["to"]) for r in ATTRIBUTION["ooc_ranges"]]
        for entry in self.entries:
            match = re.match(r"^\*\*(\[\[.+?\]\] \(.+?\))\*\* \[L(\d+)", entry)
            if not match:
                continue
            line = int(match.group(2))
            if not any(start <= line <= end for start, end in ranges):
                continue
            self.assertIn("out of character", match.group(1), entry)

    def test_a_person_is_never_labelled_as_their_character_while_out_of_character(self):
        for segment in ATTRIBUTION["segments"]:
            if segment.get("ooc") and segment.get("character"):
                self.assertNotIn(
                    f"[[{segment['character']}]] (PC, {segment['person']} ",
                    "".join(e for e in self.entries
                            if f"[L{segment['line']:04d}" in e),
                )


class TestStitchedTurns(unittest.TestCase):
    """Interrupted fragments must read as sentences without moving anything."""

    @classmethod
    def setUpClass(cls):
        cls.stitched = cls.render("stitched", [])
        cls.raw = cls.render("unstitched", ["--no-stitch"])

    @staticmethod
    def render(name, extra):
        path = os.path.join(WORK_DIR, f"{SESSION_ID}-clean-{name}.md")
        run_stage("render_clean.py", [
            SESSION_ID, "--index-dir", WORK_DIR,
            "--attribution", os.path.join(WORK_DIR, f"{SESSION_ID}-attribution.json"),
            "--out", path,
        ] + extra)
        with open(path, encoding="utf-8") as handle:
            return handle.read()

    def entries(self, rendered):
        return [line for line in rendered.splitlines() if line.startswith("**[[")]

    def spoken(self, rendered):
        """Just the words, without the speaker labels and line anchors."""
        return " ".join(entry.split("]: ", 1)[-1] for entry in self.entries(rendered))

    def test_stitching_joins_fragments_a_speaker_was_interrupted_mid_sentence(self):
        # Holly across L0107 "Wow," / L0110 "that's" / L0112 "annoying.", cut apart by
        # the GM's "Yeah." and "Super" in between.
        self.assertIn("[L0107–L0112]: Wow, that's annoying.", self.stitched)
        self.assertIn("[L0110]: that's", self.raw)

    def test_stitching_only_reduces_the_entry_count(self):
        self.assertLess(len(self.entries(self.stitched)), len(self.entries(self.raw)))

    def test_stitching_never_reorders_the_transcript(self):
        anchors = [int(m) for m in re.findall(r"\*\* \[L(\d+)", self.stitched)]
        self.assertEqual(anchors, sorted(anchors))

    def test_stitching_keeps_every_word(self):
        squash = lambda text: collections.Counter(re.sub(r"[^a-z0-9]+", "", text.lower()))
        self.assertEqual(
            dict(squash(self.spoken(self.raw)) - squash(self.spoken(self.stitched))), {})
        self.assertEqual(
            dict(squash(self.spoken(self.stitched)) - squash(self.spoken(self.raw))), {})


class TestStoryboardInserts(unittest.TestCase):
    """Out-of-audio storyboard canon: declared, labelled, and never guessed."""

    SPEC = os.path.join(KIT_DIR, f"{SESSION_ID}-vision-inserts.json")

    @classmethod
    def setUpClass(cls):
        cls.path = os.path.join(WORK_DIR, f"{SESSION_ID}-clean-with-vision.md")
        run_stage("render_clean.py", cls.args(cls.SPEC, cls.path))
        with open(cls.path, encoding="utf-8") as handle:
            cls.rendered = handle.read()
        with open(cls.SPEC, encoding="utf-8") as handle:
            cls.spec = json.load(handle)

    @staticmethod
    def args(spec, out):
        return [
            SESSION_ID, "--index-dir", WORK_DIR,
            "--attribution", os.path.join(WORK_DIR, f"{SESSION_ID}-attribution.json"),
            "--inserts", spec, "--out", out,
        ]

    def variant(self, mutate, name):
        """Render with a mutated inserts spec; return the failed CompletedProcess."""
        spec = json.loads(json.dumps(self.spec))
        mutate(spec)
        path = os.path.join(WORK_DIR, f"{name}.json")
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(spec, handle)
        result = run_stage(
            "render_clean.py",
            self.args(path, os.path.join(WORK_DIR, f"{name}.md")),
            expect_success=False,
        )
        self.assertNotEqual(result.returncode, 0, result.stdout)
        return result.stdout + result.stderr

    def test_inserts_are_marked_as_never_spoken_on_a_mic(self):
        for line in self.rendered.splitlines():
            if "storyboard p" in line:
                self.assertNotIn("'s mic)", line, line)
        self.assertIn("[vision]", self.rendered)

    def test_inserts_do_not_disturb_the_audio_parity(self):
        """Adding canon may only add: every indexed word must still be present."""
        squash = lambda text: collections.Counter(re.sub(r"[^a-z0-9]+", "", text.lower()))
        indexed = os.path.join(WORK_DIR, f"{SESSION_ID}-raw-indexed.md")
        bodies = []
        with open(indexed, encoding="utf-8") as handle:
            for raw in handle:
                match = re.match(r"^L\d+: \*\*.+?:\*\* (.*)$", raw.rstrip("\n"))
                if match:
                    bodies.append(match.group(1))
        self.assertEqual(dict(squash("".join(bodies)) - squash(self.rendered)), {})

    def test_an_unmapped_storyboard_voice_is_an_error(self):
        output = self.variant(lambda spec: spec["speakers"].pop("Empress"), "unmapped")
        self.assertIn("has no entry in `speakers`", output)

    def test_a_declared_character_cannot_be_inserted_as_an_npc(self):
        character = next(iter(CONFIG.characters))
        output = self.variant(
            lambda spec: spec["speakers"].update({"Empress": f"NPC:{character}"}),
            "insert-launder",
        )
        self.assertIn("cannot be attributed as an NPC", output)

    def test_an_undeclared_identity_cannot_be_inserted(self):
        output = self.variant(
            lambda spec: spec["speakers"].update({"Empress": "Somebody Else"}),
            "insert-undeclared",
        )
        self.assertIn("neither the GM", output)


def solo_stream_assertion(person, character):
    def test(self):
        found = segments(stream=person)
        self.assertTrue(found, f"no segments attributed to stream {person!r}")
        for segment in found:
            self.assertEqual(segment["character"], character, segment)
            self.assertFalse(segment["shared_mic"], segment)

    test.__doc__ = (
        f"config declares {person} plays {character} on their own mic -> "
        f"every {person} segment is {character}"
    )
    return test


def shared_mic_assertion(mic_label, identity):
    def test(self):
        found = [
            segment
            for segment in segments(stream=mic_label, shared_mic=True)
            if segment.get("character") == identity.identity
        ]
        self.assertTrue(
            found,
            f"config declares mic {mic_label!r} carries {identity.person}'s "
            f"{identity.identity}, so the attribution run must decompose at least one "
            f"{identity.identity} segment out of that stream — found none.",
        )
        for segment in found:
            self.assertEqual(segment["person"], identity.person, segment)

    test.__doc__ = (
        f"config declares mic {mic_label} carries {identity.identity} "
        f"({identity.person}) -> >=1 {mic_label} -> {identity.identity} segment"
    )
    return test


def shared_mic_gm_assertion(mic_label):
    def test(self):
        found = [
            segment
            for segment in segments(stream=mic_label, shared_mic=True)
            if segment.get("identity") == sc.GM_IDENTITY
        ]
        self.assertTrue(found, f"no GM-narration segments decomposed out of {mic_label!r}")

    test.__doc__ = f"config declares mic {mic_label} carries the GM -> >=1 GM segment"
    return test


class TestDeclaredStreams(unittest.TestCase):
    """Generated from the session config — see _generate_stream_tests."""


def _generate_stream_tests():
    """Build one assertion per stream the config declares."""
    generated = []
    for person, character in CONFIG.players.items():
        if CONFIG.is_shared_mic(person) or person == CONFIG.gm or not CONFIG.has_own_mic(person):
            continue
        name = f"test_solo_stream_{person.replace(' ', '_').lower()}_is_{character.lower()}"
        setattr(TestDeclaredStreams, name, solo_stream_assertion(person, character))
        generated.append(name)

    for mic in CONFIG.shared_mics:
        slug = mic.mic_label.replace(" ", "_").lower()
        for identity in mic.identities:
            if identity.is_gm:
                name = f"test_shared_mic_{slug}_yields_gm_narration"
                setattr(TestDeclaredStreams, name, shared_mic_gm_assertion(mic.mic_label))
            else:
                name = f"test_shared_mic_{slug}_yields_{identity.identity.lower()}"
                setattr(
                    TestDeclaredStreams, name, shared_mic_assertion(mic.mic_label, identity)
                )
            generated.append(name)
    return generated


GENERATED = _generate_stream_tests()


def list_assertions():
    print(f"Assertions generated from {os.path.relpath(CONFIG.path, SESSIONS_DIR)}:")
    for name in GENERATED:
        print(f"  {name}\n      {getattr(TestDeclaredStreams, name).__doc__}")
    if not CONFIG.shared_mics:
        print("  (config declares no shared mics -> no decomposition assertions)")


if __name__ == "__main__":
    if "--list" in sys.argv:
        list_assertions()
    else:
        unittest.main(verbosity=2)
