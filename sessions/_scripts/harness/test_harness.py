"""Automated Unit Tests for the Vumbua Editorial Harness."""

import unittest
from sessions.scripts.harness.leak_detector import LeakDetector
from sessions.scripts.harness.echo_detector import EchoDetector
from sessions.scripts.harness.style_analyzer import StyleAnalyzer
from sessions.scripts.harness.lore_guardian import LoreGuardian
from sessions.scripts.harness.context_bridge import ContextBridge


class TestEditorialHarness(unittest.TestCase):
    def setUp(self):
        self.leak_detector = LeakDetector()
        self.echo_detector = EchoDetector(proximity_window_words=50)
        self.style_analyzer = StyleAnalyzer()
        self.lore_guardian = LoreGuardian()

    def test_leak_detector_catches_player_name(self):
        bad_text = 'Ignatius walked forward. Luke told everyone to roll for initiative.'
        res = self.leak_detector.scan_text(bad_text)
        self.assertFalse(res["passed"])
        types = [v["type"] for v in res["violations"]]
        self.assertIn("PLAYER_NAME_LEAK", types)

    def test_leak_detector_catches_mechanics(self):
        bad_text = 'Iggy checked his character sheet and spent an armor slot.'
        res = self.leak_detector.scan_text(bad_text)
        self.assertFalse(res["passed"])
        types = [v["type"] for v in res["violations"]]
        self.assertIn("MECHANICS_LEAK", types)

    def test_leak_detector_catches_embedded_italic_dialogue(self):
        bad_text = '*I really think we should go back,* Pip said with a shudder.'
        res = self.leak_detector.scan_text(bad_text)
        self.assertFalse(res["passed"])
        types = [v["type"] for v in res["violations"]]
        self.assertIn("EMBEDDED_ITALIC_DIALOGUE", types)

    def test_lore_guardian_catches_phonetic_drift(self):
        bad_text = 'Ignatius turned toward Vanball and asked for advice.'
        res = self.lore_guardian.scan_text(bad_text)
        self.assertFalse(res["passed"])
        err_types = [e["type"] for e in res["errors"]]
        self.assertIn("PHONETIC_DRIFT", err_types)

    def test_lore_guardian_catches_tense_slip(self):
        bad_text = 'Britt turns toward the forest and watches the leaves fall.'
        res = self.lore_guardian.scan_text(bad_text)
        warn_types = [w["type"] for w in res["warnings"]]
        self.assertIn("TENSE_SLIPPAGE", warn_types)

    def test_echo_detector_catches_proximity_echo(self):
        repetitive_text = (
            "Through the shattered archway, Ignatius stepped with caution. "
            "The ancient stones were covered in dark green moss. "
            "Through the shattered archway, he could see the distant harbor."
        )
        res = self.echo_detector.scan_text(repetitive_text)
        self.assertGreater(res["echoes_found"], 0)

    def test_style_analyzer_metrics(self):
        sample_prose = (
            'The copper boiler hummed beneath the iron deck, vibrating through the soles of Lomi’s boots. '
            '"Are we ready to engage the main conduits?" Ignatius asked, wiping soot from his jaw. '
            '"Not quite yet," Lomi replied, adjusting his woolen cap. The smell of ozone and sulfur hung thick in the air.'
        )
        res = self.style_analyzer.generate_style_report(sample_prose)
        self.assertGreater(res["pacing"]["sentence_count"], 0)
        self.assertGreater(res["dialogue_ratio"]["dialogue_pct"], 0)
        self.assertGreater(res["sensory_palette"]["covered_registers"], 0)

    def test_context_bridge_format(self):
        bridge = ContextBridge()
        state = {
            "location_and_environment": "Apex Arena, basalt canyon, heavy morning rain",
            "characters_present": [
                {"name": "Ignatius", "status": "exhausted, crown glowing"},
                {"name": "Lomi", "status": "riding Ignatius's shoulders"}
            ],
            "key_items_or_props": ["Spirit Tortoise vial", "copper slates"],
            "immediate_preceding_action": "Ignatius crossed the rapids while Lomi held on tightly.",
            "emotional_tone_or_tension": "Elated relief after surviving the trials"
        }
        formatted = bridge.format_bridge_prompt(state)
        self.assertIn("Apex Arena", formatted)
        self.assertIn("Ignatius", formatted)
        self.assertIn("Spirit Tortoise vial", formatted)


if __name__ == "__main__":
    unittest.main()
