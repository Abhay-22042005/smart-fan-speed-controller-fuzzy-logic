import unittest

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from main import calculate_fan_speed, create_membership_figure


class FuzzyControllerTests(unittest.TestCase):
    def test_low_medium_and_high_temperatures(self) -> None:
        expected_categories = {
            20: "Low",
            27.5: "Medium",
            35: "High",
        }

        for temperature, expected_category in expected_categories.items():
            with self.subTest(temperature=temperature):
                speed, category = calculate_fan_speed(temperature)
                self.assertEqual(category, expected_category)
                self.assertGreaterEqual(speed, 0)
                self.assertLessEqual(speed, 100)

    def test_boundary_temperatures_are_supported(self) -> None:
        self.assertEqual(calculate_fan_speed(15), (15.0, "Low"))
        self.assertEqual(calculate_fan_speed(40), (85.0, "High"))

    def test_speed_does_not_decrease_as_temperature_rises(self) -> None:
        speeds = [
            calculate_fan_speed(15 + step / 10)[0]
            for step in range(251)
        ]

        self.assertTrue(
            all(left <= right for left, right in zip(speeds, speeds[1:]))
        )

    def test_invalid_temperatures_are_rejected(self) -> None:
        invalid_values = (
            "",
            "not a number",
            None,
            14,
            41,
            float("nan"),
            float("inf"),
        )

        for temperature in invalid_values:
            with self.subTest(temperature=temperature):
                with self.assertRaises(ValueError):
                    calculate_fan_speed(temperature)

    def test_membership_graphs_show_all_sets_and_labels(self) -> None:
        figure = create_membership_figure()
        try:
            self.assertEqual(len(figure.axes), 2)
            temperature_axes, speed_axes = figure.axes
            self.assertEqual(
                temperature_axes.get_title(),
                "Temperature Membership Functions",
            )
            self.assertEqual(
                speed_axes.get_title(),
                "Fan-Speed Membership Functions",
            )
            self.assertEqual(temperature_axes.get_xlabel(), "Temperature (\u00b0C)")
            self.assertEqual(speed_axes.get_xlabel(), "Fan speed (%)")

            for axes in figure.axes:
                self.assertEqual(axes.get_ylabel(), "Membership degree")
                self.assertEqual(
                    [line.get_label() for line in axes.lines],
                    ["Low", "Medium", "High"],
                )
                self.assertGreaterEqual(float(axes.get_ylim()[0]), 0)
                self.assertGreaterEqual(float(axes.get_ylim()[1]), 1)
                for line in axes.lines:
                    self.assertTrue(all(0 <= value <= 1 for value in line.get_ydata()))
        finally:
            plt.close(figure)


if __name__ == "__main__":
    unittest.main()
