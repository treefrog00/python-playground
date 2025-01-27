import unittest
import datetime
from wiggles_finder import munge_wiggles_data


class MockRecord:
    def __init__(self, distance, timestamp, lat=None, lon=None):
        self._values = {
            "distance": distance,
            "timestamp": timestamp,
            "position_lat": int(lat * ((2**32) / 360)) if lat is not None else None,
            "position_long": int(lon * ((2**32) / 360)) if lon is not None else None,
        }

    def get_value(self, field):
        return self._values.get(field)

    def has_field(self, field):
        return self._values.get(field) is not None


class MockFitData:
    def __init__(self, records):
        self.records = records


class TestWigglesFinder(unittest.TestCase):
    def test_straight_line_north(self):
        # Moving north in a straight line
        records = [
            MockRecord(0, datetime.datetime(2025, 1, 18, 11, 34, 16), lat=0.0, lon=0.0),
            MockRecord(
                100, datetime.datetime(2025, 1, 18, 11, 34, 26), lat=0.001, lon=0.0
            ),
            MockRecord(
                200, datetime.datetime(2025, 1, 18, 11, 34, 36), lat=0.002, lon=0.0
            ),
        ]
        mock_fit_data = MockFitData(records)
        mock_fit_data.session_metadata = {"sport": "running"}

        result = munge_wiggles_data(mock_fit_data)

        # Should be a single group since direction never changes
        self.assertEqual(len(result), 1)
        row = result.to_dict(as_series=False)
        self.assertEqual(row["start_index"][0], 0)
        self.assertEqual(row["end_index"][0], 2)
        self.assertEqual(row["segment_distance_m"][0], 200)

    def test_zigzag_pattern(self):
        # Moving in a zigzag pattern, only lat or lon changes
        # so it will be a single segment
        records = [
            MockRecord(0, datetime.datetime(2025, 1, 18, 11, 34, 16), lat=0.0, lon=0.0),
            MockRecord(
                100, datetime.datetime(2025, 1, 18, 11, 34, 26), lat=0.001, lon=0.001
            ),
            MockRecord(
                200, datetime.datetime(2025, 1, 18, 11, 34, 36), lat=0.0, lon=0.002
            ),
            MockRecord(
                300, datetime.datetime(2025, 1, 18, 11, 34, 46), lat=0.001, lon=0.003
            ),
        ]
        mock_fit_data = MockFitData(records)
        mock_fit_data.session_metadata = {"sport": "running"}

        result = munge_wiggles_data(mock_fit_data)

        self.assertEqual(len(result), 1)

        row = result.to_dict(as_series=False)

        # Check segment distances
        self.assertEqual(row["segment_distance_m"][0], 300)

    def test_backwards_and_forwards_pattern(self):
        # Moving back and forth to the same spot
        records = [
            MockRecord(0, datetime.datetime(2025, 1, 18, 11, 34, 16), lat=0.0, lon=0.0),
            MockRecord(
                100, datetime.datetime(2025, 1, 18, 11, 34, 26), lat=0.001, lon=0.001
            ),
            MockRecord(
                200, datetime.datetime(2025, 1, 18, 11, 34, 36), lat=0.0, lon=0.0
            ),  # Direction change
            MockRecord(
                300, datetime.datetime(2025, 1, 18, 11, 34, 46), lat=0.001, lon=0.001
            ),  # Direction change
        ]
        mock_fit_data = MockFitData(records)
        mock_fit_data.session_metadata = {"sport": "running"}

        result = munge_wiggles_data(mock_fit_data)

        # Should have 3 groups due to direction changes
        self.assertEqual(len(result), 3)

        row = result.to_dict(as_series=False)

        # Check segment distances
        self.assertEqual(row["segment_distance_m"][0], 100)
        self.assertEqual(row["segment_distance_m"][1], 100)
        self.assertEqual(row["segment_distance_m"][2], 100)

    def test_missing_position_data(self):
        # Some records missing position data
        records = [
            MockRecord(0, datetime.datetime(2025, 1, 18, 11, 34, 16), lat=0.0, lon=0.0),
            MockRecord(
                100, datetime.datetime(2025, 1, 18, 11, 34, 26)
            ),  # Missing position
            MockRecord(
                200, datetime.datetime(2025, 1, 18, 11, 34, 36), lat=0.002, lon=0.0
            ),
        ]
        mock_fit_data = MockFitData(records)
        mock_fit_data.session_metadata = {"sport": "running"}

        result = munge_wiggles_data(mock_fit_data)

        # Should still process the data without errors
        self.assertTrue(len(result) > 0)

    def test_speed_calculation(self):
        # Test speed calculations and categories
        records = [
            MockRecord(0, datetime.datetime(2025, 1, 18, 11, 34, 16), lat=0.0, lon=0.0),
            # Slow speed: 0.5 km/h
            MockRecord(
                1000, datetime.datetime(2025, 1, 18, 13, 34, 16), lat=0.1, lon=0.1
            ),  # 1 km in 2 hours = 0.5 km/h
            # Medium speed: ~15 km/h
            MockRecord(
                6000, datetime.datetime(2025, 1, 18, 14, 34, 16), lat=0, lon=0
            ),  # 5 km in 1 hour = 5 km/h
            # Suspicious speed: ~30 km/h
            MockRecord(
                21000, datetime.datetime(2025, 1, 18, 14, 44, 16), lat=0.1, lon=0.1
            ),  # 15 km in 10 minutes = 90 km/h
        ]
        mock_fit_data = MockFitData(records)
        mock_fit_data.session_metadata = {"sport": "hiking"}

        result = munge_wiggles_data(mock_fit_data)

        # Convert to dict for easier testing
        row = result.to_dict(as_series=False)
        # Test speed categories
        self.assertEqual(
            row["speed_category"][0], "slow"
        )  # First segment should be slow
        self.assertEqual(
            row["speed_category"][1], "medium"
        )  # Second segment should be medium
        self.assertEqual(
            row["speed_category"][2], "suspicious"
        )  # Third segment should be suspicious

        # Test speed calculations
        self.assertAlmostEqual(row["speed_kmh"][0], 0.5)
        self.assertAlmostEqual(row["speed_kmh"][1], 5)
        self.assertAlmostEqual(row["speed_kmh"][2], 90)


if __name__ == "__main__":
    unittest.main()
