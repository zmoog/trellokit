# trellokit

[![PyPI](https://img.shields.io/pypi/v/trellokit.svg)](https://pypi.org/project/trellokit/)
[![Changelog](https://img.shields.io/github/v/release/zmoog/trellokit?include_prereleases&label=changelog)](https://github.com/zmoog/trellokit/releases)
[![Tests](https://github.com/zmoog/trellokit/workflows/Test/badge.svg)](https://github.com/zmoog/trellokit/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/zmoog/trellokit/blob/master/LICENSE)

CLI tool and Python library to access and use Trello API

## Installation

Install this tool using `pip`:

    pip install trellokit

## Usage

For help, run:

    trellokit --help

You can also use:

    python -m trellokit --help

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd trellokit
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
