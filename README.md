# Gross Net Calculator Switzerland

The CLI-based tool is designed to help users calculate **approximate** monthly net salary from their gross income in Switzerland. 
This tool utilizes Selenium, a web browser automation tool, to replicate user interactions with the **Lohncomputer** website.

![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Project Overview

This Gross Net Calculator is tailored for Swiss residents, offering detailed net salary calculations from gross income. 
It employs Python and integrates libraries like `click`, `InquirerPy`, `tabulate`, and `selenium` for a seamless command-line experience. 
The application uniquely utilizes Selenium to emulate user interactions with the [Lohncomputer](http://www.lohncomputer.ch) website, 
ensuring accurate and current data for calculating net salaries based on various personal and regional parameters.

## Demo

![App Demo](https://cdn.loncar.net/gross-net-calculator-switzerland.gif)

## Built With

- **[Python](https://www.python.org/)** - The core programming language used.
- **[Poetry](https://python-poetry.org/)** - Dependency Management and Packaging.
- **[Click](https://click.palletsprojects.com/)** - Creates a command-line interface.
- **[InquirerPy](https://github.com/kazhala/InquirerPy)** - Simplifies creating interactive CLI prompts.
- **[Tabulate](https://pypi.org/project/tabulate/)** - Formats tabular data.
- **[Selenium](https://www.selenium.dev/)** - Automates web browser interaction.

## Getting Started

These instructions will guide you through setting up the project on your local machine for development and testing purposes.

### Prerequisites

- Python 3.11
- [Poetry](https://python-poetry.org/docs/#installation) for managing dependencies

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/loncarales/gross-net-calculator-switzerland.git
cd gross-net-calculator-switzerland
```

2. **Use Makefile for setup**

The project includes a Makefile to simplify common tasks such as installing dependencies, running tests, and formatting/linting code.

To install the project dependencies, run:

```bash
make install
```
## Usage

Run the Gross Net Calculator using the Makefile:

```bash
make run
```

You will be prompted to enter your gross monthly wage in CHF and your age in years. 
Then, you will be asked to provide additional information such as church membership, status, children, and canton of residence. 
The program will automate interactions with the Lohncomputer website to provide accurate net salary calculations 
based on the provided inputs and display the results in a tabular format.

### Makefile Commands

The Makefile provides convenient commands for development and testing:

* Install Dependencies: `make install`
* Run Application: `make run`
* Run Tests: `make test`
* Generate Coverage Report: `make coverage`
* Format Code: `make format`
* Lint Code: `make lint`

## Contributing

Contributions to this project are welcome! Please feel free to report bugs, suggest features, improve documentation, or submit pull requests. Follow the standard fork-and-pull request workflow.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details.

## Acknowledgments

* Special thanks to all the open-source libraries and contributors that make this project possible.
* Gratitude to the community for their valuable feedback and suggestions.

<div align="center">

Developed with ❤️ by Aleš Lončar

</div>