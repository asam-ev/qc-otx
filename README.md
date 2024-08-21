# asam-qc-otx

This project implements the [OTX Checker](checker_bundle_doc.md) for the ASAM Quality Checker project.

OTX stands for [Open Test sequence eXchange](https://report.asam.net/otx-iso-13209-open-test-sequence-exchange-format).

- [asam-qc-otx](#asam-qc-otx)
  - [Installation and usage](#installation-and-usage)
    - [Installation using pip](#installation-using-pip)
    - [Installation from source](#installation-from-source)
      - [Default Python](#default-python)
      - [Poetry](#poetry)
  - [Register Checker Bundle to ASAM Quality Checker Framework](#register-checker-bundle-to-asam-quality-checker-framework)
    - [Linux Manifest Template](#linux-manifest-template)
  - [Tests](#tests)
    - [Install using pip](#install-using-pip)
    - [Install using poetry](#install-using-poetry)
    - [Execute tests](#execute-tests)
  - [Contributing](#contributing)


## Installation and usage

asam-qc-otx can be installed using pip or from source.

### Installation using pip

asam-qc-otx can be installed using pip.

```bash
pip install asam-qc-otx@git+https://github.com/asam-ev/qc-otx@main
```

**Note**: To install from different sources, you can replace `@main` with
your desired target. For example, `develop` branch as `@develop`.

To run the application:

```bash
qc_otx --help
usage: QC OTX Checker [-h] (-d | -c CONFIG_PATH)
This is a collection of scripts for checking validity of Open Test sequence eXchange format (.otx) files.
options:
  -h, --help            show this help message and exit
  -d, --default_config
  -c CONFIG_PATH, --config_path CONFIG_PATH
```

The following commands are equivalent:

```bash
qc_otx --help
python qc_otx/main.py --help
python -m qc_otx.main --help
```

### Installation from source

After cloning the repository, there are two options to install from source.

1. Default Python on the machine
2. [Poetry](https://python-poetry.org/)

#### Default Python

```bash
pip install -r requirements.txt
```

This will install the needed dependencies to your local Python.

#### Poetry

```bash
poetry install
```

After installing from source, the usage are similar to above.

```bash
qc_otx --help
python qc_otx/main.py --help
python -m qc_otx.main --help
```

## Register Checker Bundle to ASAM Quality Checker Framework

Manifest file templates are provided in the [manifest_templates](manifest_templates/) folder to register the ASAM OpenDrive Checker Bundle with the [ASAM Quality Checker Framework](https://github.com/asam-ev/qc-framework/tree/main).

### Linux Manifest Template

To register this Checker Bundle in Linux, use the [linux_manifest.json](manifest_templates/linux_manifest.json) template file. Replace the path to the Python executable `/home/user/.venv/bin/python` in the `exec_command` with the path to the Python executable where the Checker Bundle is installed.

## Tests

To run the tests, you need to install the extra test dependency after installing from source.

### Install using pip

```bash
pip install -r requirements-tests.txt
```

### Install using poetry

```bash
poetry install --with dev
```

### Execute tests

```bash
python -m pytest -vv
```

or

```bash
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

```bash
pip install -r requirements-dev.txt
```

or

```bash
poetry install --with dev
```

You need to have pre-commit installed and install the hooks:

```
pre-commit install
```
