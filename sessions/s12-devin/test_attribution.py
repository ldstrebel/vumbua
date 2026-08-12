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

import json
import os
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
        data = json.load(open(CONFIG.path, encoding="utf-8"))
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
