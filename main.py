#!/usr/bin/env python3

import json

import click
from InquirerPy import inquirer
from tabulate import tabulate

from gross_net_calculator.gross_net_calculator import GrossNetCalculator


def load_config() -> dict:
    """
    Load the configuration options from the 'config/options.json' file.

    Returns:
        dict: A dictionary containing the configuration options.

    Raises:
        FileNotFoundError: If the 'config/options.json' file does not exist.
        json.JSONDecodeError: If the file does not contain valid JSON.

    """
    try:
        with open("config/options.json") as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError("The 'config/options.json' file does not exist.") from e
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            "The 'config/options.json' file contains invalid JSON.", e.doc, e.pos
        ) from e


def format_salary(salary) -> str:
    """
    Format the given salary into a formatted string representation.

    Parameters:
    - salary (str): The salary to be formatted.

    Returns:
    str: The formatted salary string.

    Example:
    >>> format_salary("10'000")
    '10.000 CHF'
    >>> format_salary("5'000.00")
    '5.000,00 CHF'
    >>> format_salary(None)
    'Salary information not available'
    """
    if salary is None:
        return "Salary information not available"

    # Remove any apostrophes and replace them with a dot
    formatted_salary = salary.replace("'", ".")

    # Replace the dot before the last two digits with a comma
    if "." in formatted_salary:
        parts = formatted_salary.split(".")
        if len(parts[-1]) == 2:
            formatted_salary = ".".join(parts[:-1]) + "," + parts[-1]

    # Add the currency
    formatted_salary += " CHF"

    return formatted_salary


def get_user_inputs(config) -> dict:
    """
    This function prompts the user to enter information such as church membership, status,
    children, and canton of residence. It uses the InquirerPy library to display a series of
    select prompts to the user and returns the user's inputs as a dictionary.

    Parameters:
    - config (dict): A dictionary containing the configuration options for the prompts.

    Returns:
    dict: A dictionary containing the user's inputs, with the following keys:
        - 'church_member' (str): The user's church membership status ('Yes' or 'No').
        - 'status' (str): The user's status.
        - 'children' (str): The number of children.
        - 'canton' (str): The user's canton of residence.

    Raises:
    ValueError: If the config dictionary does not contain all the required keys
    ('status', 'children', 'canton').

    Example:
    config = {
        'status': ['Single', 'Married'],
        'children': ['0', '1', '2', '3+'],
        'canton': ['Zurich', 'Bern', 'Lucerne']
    }
    user_inputs = get_user_inputs(config)
    print(user_inputs)
    # Output: {'church_member': 'Yes', 'status': 'Married', 'children': '2', 'canton': 'Zurich'}
    """
    required_keys = ["status", "children", "canton"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required key in config: {key}")

    church_member = inquirer.select(
        message="Church member (Yes/No):",
        choices=["Yes", "No"],
    ).execute()
    status = inquirer.select(
        message="Status:",
        choices=config["status"],
    ).execute()
    children = inquirer.select(
        message="Children:",
        choices=config["children"],
    ).execute()
    canton = inquirer.select(
        message="Canton of residence:",
        choices=config["canton"],
    ).execute()

    return {
        "church_member": church_member,
        "status": status,
        "children": children,
        "canton": canton,
    }


@click.command()
@click.option("--wage", prompt="Gross monthly wage in CHF", type=float)
@click.option("--age", prompt="Age in years", type=int)
def cli(wage, age) -> None:
    """
    This function is the entry point for the command-line interface (CLI) of
    the gross net calculator for Switzerland.

    Parameters:
    - wage (float): The gross monthly wage in CHF.
    - age (int): The age in years.

    Returns:
    None

    Raises:
    ValueError: If the age is not between 0 and 67, or if the wage is not a positive number.

    Usage:
    The user will be prompted to enter additional information such as church membership, status,
    children, and canton of residence. The function will then calculate the net salary based on
    the provided inputs and display the results in a tabular format.

    Example:
    cli(wage=5000, age=30)
    """
    try:
        config = load_config()
        # Validate user inputs for age and wage
        if age < 0 or age > 67:
            raise ValueError("Age must be between 0 and 67")
        if wage <= 0:
            raise ValueError("Wage must be a positive number")
        user_inputs = get_user_inputs(config)

        calculator = GrossNetCalculator(load_config)
        results = {}
        if user_inputs["canton"].lower() == "all":
            results = calculator.fetch_net_wages_for_all_cantons(
                gross=f"{wage}",
                age=f"{age}",
                church_member=f"{user_inputs['church_member']}",
                status=f"{user_inputs['status']}",
                children=f"{user_inputs['children']}",
            )
        else:
            net_salary = calculator.calculate_net_salary(
                gross=f"{wage}",
                age=f"{age}",
                church_member=f"{user_inputs['church_member']}",
                status=f"{user_inputs['status']}",
                children=f"{user_inputs['children']}",
                canton=f"{user_inputs['canton']}",
            )
            results[user_inputs["canton"]] = net_salary

        # Convert the results dictionary into a list of lists for tabulate
        data = [[canton, format_salary(salary)] for canton, salary in results.items()]

        print(tabulate(data, headers=["Canton", "Net Salary"], tablefmt="pretty", stralign="left"))

        calculator.close()

    except Exception as e:
        print("END WITH ERROR: " + str(e))
        raise SystemExit(e) from e


if __name__ == "__main__":
    cli()
