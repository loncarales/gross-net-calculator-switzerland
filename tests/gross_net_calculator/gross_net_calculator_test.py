import unittest
from unittest.mock import MagicMock, patch

from gross_net_calculator.gross_net_calculator import GrossNetCalculator


class TestGrossNetCalculator(unittest.TestCase):
    def setUp(self):
        self.config_loader_mock = MagicMock()
        self.calculator = GrossNetCalculator(self.config_loader_mock)

    @patch("gross_net_calculator.gross_net_calculator.webdriver.Firefox")
    def test_init(self, firefox_mock):
        self.config_loader_mock.return_value = {"canton": ["All", "Commuters"]}
        self.calculator = GrossNetCalculator(self.config_loader_mock)
        firefox_mock.assert_called_once()

    @patch("gross_net_calculator.gross_net_calculator.webdriver.Firefox")
    def test_close(self, firefox_mock):
        mock_driver = MagicMock()
        firefox_mock.return_value = mock_driver
        self.calculator = GrossNetCalculator(self.config_loader_mock)

        self.calculator.close()

        mock_driver.quit.assert_called_once()

    @patch("gross_net_calculator.gross_net_calculator.webdriver.Firefox")
    def test_fetches_net_wages_for_all_cantons(self, firefox_mock):
        mock_driver = MagicMock()
        mock_driver.find_element = MagicMock()  # Mock the find_element method on the mock_driver
        firefox_mock.return_value = mock_driver

        self.calculator = GrossNetCalculator(
            self.config_loader_mock
        )  # Ensure calculator uses the mocked driver
        self.calculator.fetch_net_wages_for_all_cantons(5000, 30, "Yes", "Single", "No children")

        # Assert find_element was called on the mock_driver
        mock_driver.find_element.assert_called()

    @patch("gross_net_calculator.gross_net_calculator.webdriver.Firefox")
    def test_calculates_net_salary(self, firefox_mock):
        mock_driver = MagicMock()
        mock_driver.find_element = MagicMock()  # Mock the find_element method on the mock_driver
        firefox_mock.return_value = mock_driver

        self.calculator = GrossNetCalculator(
            self.config_loader_mock
        )  # Ensure calculator uses the mocked driver
        self.calculator.calculate_net_salary(5000, 30, "Yes", "Single", "No children", "Zurich")
        # Assert find_element was called on the mock_driver
        firefox_mock().find_element.assert_called()


if __name__ == "__main__":
    unittest.main()
