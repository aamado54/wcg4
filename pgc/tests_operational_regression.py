import json
import tempfile
from pathlib import Path

from django.test import TestCase

from pgc.operational_baseline import load_baseline_file, save_baseline_file


class OperationalBaselineFileTests(TestCase):
    def test_save_and_load_roundtrip(self):
        payload = {
            "version": 1,
            "tag": "sep-save",
            "year": 2026,
            "month": 9,
            "mode": "modo2",
            "results": [],
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "baseline.json"
            save_baseline_file(payload, path)
            loaded = load_baseline_file(path)
            self.assertEqual(loaded["tag"], "sep-save")
            self.assertEqual(json.loads(path.read_text())["month"], 9)
