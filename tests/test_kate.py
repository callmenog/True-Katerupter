import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("kate", ROOT / "Kate.py")
kate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kate)


class KateScanTests(unittest.TestCase):
    def test_scan_lists_networks_for_station_scan(self):
        with patch.object(kate.subprocess, "run") as mock_run:
            mock_run.return_value = type(
                "Result",
                (),
                {"returncode": 0, "stdout": "SSID: TestNet\nSSID: OtherNet\n"},
            )()
            k = kate.Kate()
            result = k.scan("station scan", "wlan0")
            self.assertEqual(result, ["TestNet", "OtherNet"])


if __name__ == "__main__":
    unittest.main()
