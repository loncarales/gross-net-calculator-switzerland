import json
import unittest
from unittest.mock import MagicMock, mock_open, patch

import pytest
from click.testing import CliRunner

from main import cli, format_salary, get_user_inputs, load_config


class TestMainFunctions(unittest.TestCase):
    def test_load_config_returns_correct_data(self):
        mock_data = {
            "status": ["Single", "Married"],
            "children": ["0", "1", "2", "3+"],
            "canton": ["Zurich", "Bern", "Jura"],
        }
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
            result = load_config()
        assert result == mock_data

    def test_load_config_raises_error_when_invalid_json(self):
        with patch("builtins.open", mock_open(read_data="invalid json")):
            with pytest.raises(json.JSONDecodeError):
                load_config()

    def test_format_salary_returns_correctly_for_valid_input(self):
        assert format_salary("10'000") == "10.000 CHF"
        assert format_salary("5'000.00") == "5.000,00 CHF"

    def test_format_salary_returns_correctly_for_none_input(self):
        assert format_salary(None) == "Salary information not available"

    def test_format_salary_returns_correctly_for_empty_string(self):
        assert format_salary("") == " CHF"

    def test_get_user_inputs_returns_correct_data(self):
        config = {
            "status": ["Single", "Married"],
            "children": ["0", "1", "2", "3+"],
            "canton": ["Zurich", "Bern", "Wallis"],
        }
        mock_select = MagicMock()
        mock_select.execute.side_effect = ["Yes", "Married", "2", "Zurich"]
        with patch("InquirerPy.inquirer.select", return_value=mock_select):
            result = get_user_inputs(config)
        assert result == {
            "church_member": "Yes",
            "status": "Married",
            "children": "2",
            "canton": "Zurich",
        }
        assert mock_select.execute.call_count == 4

    def test_get_user_inputs_handles_no_config(self):
        with pytest.raises(ValueError) as exception_info:
            get_user_inputs({})
        assert str(exception_info.value) == "Missing required key in config: status"

    @patch("main.load_config")
    @patch("main.get_user_inputs")
    @patch("main.GrossNetCalculator")
    def test_cli_calculates_net_salary_for_all_cantons(
        self, mock_calculator, mock_get_user_inputs, mock_load_config
    ):
        runner = CliRunner()
        mock_load_config.return_value = {}
        mock_get_user_inputs.return_value = {
            "church_member": "Yes",
            "status": "Single",
            "children": "0",
            "canton": "all",
        }
        mock_calculator.return_value.fetch_net_wages_for_all_cantons.return_value = {
            "Zurich": "5'000.00",
            "Bern": "4'500.00",
        }

        result = runner.invoke(cli, ["--wage", "5000", "--age", "30"])
        assert result.exit_code == 0

    @patch("main.load_config")
    @patch("main.get_user_inputs")
    @patch("main.GrossNetCalculator")
    def test_cli_calculates_net_salary_for_specific_canton(
        self, mock_calculator, mock_get_user_inputs, mock_load_config
    ):
        runner = CliRunner()
        mock_load_config.return_value = {}
        mock_get_user_inputs.return_value = {
            "church_member": "Yes",
            "status": "Single",
            "children": "0",
            "canton": "Zurich",
        }
        mock_calculator.return_value.calculate_net_salary.return_value = "5'000.00"

        result = runner.invoke(cli, ["--wage", "5000", "--age", "30"])
        assert result.exit_code == 0

    def test_cli_raises_error_for_invalid_age(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--wage", "5000", "--age", "-1"])
        assert result.exit_code != 0

    def test_cli_raises_error_for_invalid_wage(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--wage", "-5000", "--age", "30"])
        assert result.exit_code != 0


if __name__ == "__main__":
    unittest.main()
