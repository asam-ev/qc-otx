# qc-otx

The ASAM Quality Checker OTX library contains a short representative list of check examples for [Open Test sequence eXchange (OTX)](https://report.asam.net/otx-iso-13209-open-test-sequence-exchange-format)
to showcase the functionality and implementation (it shall not be a reference implementation) for the ASAM Quality Checker project. 

## Installation

There are two options of usage of the project:

1. Default python on the machine
2. [Poetry](https://python-poetry.org/)

To install the project, run:

**Default python**

```
pip install -r requirements.txt
```

This will install the needed dependencies to your local Python.

**Poetry**

```
poetry install
```

## Usage

The checker can be used as a Python script:

**Default python**

```
python main.py --help
usage: QC OTX Checker [-h] (-d | -c CONFIG_PATH)
This is a collection of scripts for checking validity of Open Test sequence eXchange format (.otx) files.
options:
  -h, --help            show this help message and exit
  -d, --default_config
  -c CONFIG_PATH, --config_path CONFIG_PATH
```

**Poetry**

```
poetry run python main.py --help
usage: QC OTX Checker [-h] (-d | -c CONFIG_PATH)
This is a collection of scripts for checking validity of Open Test sequence eXchange format (.otx) files.
options:
  -h, --help            show this help message and exit
  -d, --default_config
  -c CONFIG_PATH, --config_path CONFIG_PATH
```

### Example

- No issues found

- Issues found on file

## Tests

To run the tests, you need to have installed the main dependencies mentioned
at [Installation](#installation).

**Install Python tests and development dependencies:**

**Default python**

```
pip install -r requirements-tests.txt
```

**Poetry**

```
poetry install --with dev
```

**Execute tests:**

**Default python**

```
python -m pytest -vv
```

**Poetry**

```
poetry run pytest -vv
```

They should output something similar to:

```
===================== test session starts =====================
platform linux -- Python 3.11.9, pytest-8.2.2, pluggy-1.5.0
```

You can check more options for pytest at its [own documentation](https://docs.pytest.org/).

## Contributing

For contributing, you need to install the development requirements besides the
test and installation requirements, for that run:

```
pip install -r requirements-dev.txt
```

You need to have pre-commit installed and install the hooks:

```
pre-commit install
```
