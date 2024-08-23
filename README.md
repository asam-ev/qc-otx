# asam-qc-otx

This project implements the [OTX Checker](checker_bundle_doc.md) for the ASAM Quality Checker project.

OTX stands for [Open Test sequence eXchange](https://report.asam.net/otx-iso-13209-open-test-sequence-exchange-format).

- [asam-qc-otx](#asam-qc-otx)
  - [Installation and usage](#installation-and-usage)
    - [Installation using pip](#installation-using-pip)
    - [Installation from source](#installation-from-source)
  - [Register Checker Bundle to ASAM Quality Checker Framework](#register-checker-bundle-to-asam-quality-checker-framework)
    - [Linux Manifest Template](#linux-manifest-template)
    - [Windows Manifest Template](#windows-manifest-template)
  - [Tests](#tests)
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

After cloning the repository, the project can be installed using [Poetry](https://python-poetry.org/).

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

To register this Checker Bundle in Linux, use the [linux_otx_manifest.json](manifest_templates/linux_otx_manifest.json) template file.

If the asam-qc-opendrive is installed in a virtual environment, the `exec_command` needs to be adjusted as follows:

```json
"exec_command": "source <venv>/bin/activate && cd $ASAM_QC_FRAMEWORK_WORKING_DIR && qc_otx -c $ASAM_QC_FRAMEWORK_CONFIG_FILE"
```

Replace `<venv>/bin/activate` by the path to your virtual environment.

### Windows Manifest Template

To register this Checker Bundle in Windows, use the [windows_otx_manifest.json](manifest_templates/windows_otx_manifest.json) template file.

If the asam-qc-opendrive is installed in a virtual environment, the `exec_command` needs to be adjusted as follows:

```json
"exec_command": "C:\\> <venv>\\Scripts\\activate.bat && cd %ASAM_QC_FRAMEWORK_WORKING_DIR% && qc_otx -c %ASAM_QC_FRAMEWORK_CONFIG_FILE%"
```

Replace `C:\\> <venv>\\Scripts\\activate.bat` by the path to your virtual environment.

## Tests

To run the tests, you need to install the extra test dependency after installing from source.

```bash
poetry install --with dev
```

To execute tests:

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
poetry install --with dev
```

You need to have pre-commit installed and install the hooks:

```
pre-commit install
```
