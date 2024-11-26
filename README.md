# asam-qc-otx

This project implements the [OTX Checker Bundle](checker_bundle_doc.md) for the ASAM Quality Checker project.

The ASAM Quality Checker OTX library contains a short representative list of check examples for [Open Test sequence eXchange (OTX)](https://report.asam.net/otx-iso-13209-open-test-sequence-exchange-format)
to showcase the functionality and implementation (it shall not be a reference implementation) for the ASAM Quality Checker project. 

- [asam-qc-otx](#asam-qc-otx)
  - [Installation and usage](#installation-and-usage)
    - [Installation using pip](#installation-using-pip)
    - [Installation from source](#installation-from-source)
  - [Register Checker Bundle to ASAM Quality Checker Framework](#register-checker-bundle-to-asam-quality-checker-framework)
    - [Linux Manifest Template](#linux-manifest-template)
    - [Windows Manifest Template](#windows-manifest-template)
    - [Example Configuration File](#example-configuration-file)
  - [Tests](#tests)
  - [Contributing](#contributing)


## Installation and usage

asam-qc-otx can be installed using pip or from source.

### Installation using pip

asam-qc-otx can be installed using pip.

**From PyPi repository**

```bash
pip install asam-qc-otx
```

**From GitHub repository**

```bash
pip install asam-qc-otx@git+https://github.com/asam-ev/qc-otx@main
```

The above command will install `asam-qc-otx` from the `main` branch. If you want to install `asam-qc-otx` from another branch or tag, replace `@main` with the desired branch or tag.

**From a local repository**

```bash
pip install /home/user/qc-otx
```

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

Manifest file templates are provided in the [manifest_templates](manifest_templates/) folder to register the ASAM OTX Checker Bundle with the [ASAM Quality Checker Framework](https://github.com/asam-ev/qc-framework/tree/main).

### Linux Manifest Template

To register this Checker Bundle in Linux, use the [linux_otx_manifest.json](manifest_templates/linux_otx_manifest.json) template file.

If the asam-qc-otx is installed in a virtual environment, the `exec_command` needs to be adjusted as follows:

```json
"exec_command": "source <venv>/bin/activate && cd $ASAM_QC_FRAMEWORK_WORKING_DIR && qc_otx -c $ASAM_QC_FRAMEWORK_CONFIG_FILE"
```

Replace `<venv>/bin/activate` by the path to your virtual environment.

### Windows Manifest Template

To register this Checker Bundle in Windows, use the [windows_otx_manifest.json](manifest_templates/windows_otx_manifest.json) template file.

If the asam-qc-otx is installed in a virtual environment, the `exec_command` needs to be adjusted as follows:

```json
"exec_command": "C:\\> <venv>\\Scripts\\activate.bat && cd %ASAM_QC_FRAMEWORK_WORKING_DIR% && qc_otx -c %ASAM_QC_FRAMEWORK_CONFIG_FILE%"
```

Replace `C:\\> <venv>\\Scripts\\activate.bat` by the path to your virtual environment.

### Example Configuration File

An example configuration file for using this Checker Bundle within the ASAM Quality Checker Framework is as follows.

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<Config>

    <Param name="InputFile" value="test.otx" />

    <CheckerBundle application="otxBundle">
        <Param name="resultFile" value="otx_bundle_report.xqar" />
        <Checker checkerId="check_asam_otx_core_chk_001_document_name_matches_filename" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_otx_core_chk_002_document_name_package_uniqueness" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_otx_core_chk_003_no_dead_import_links" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_otx_core_chk_004_no_unused_imports" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_otx_core_chk_005_no_use_of_undefined_import_prefixes" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_otx_core_chk_006_match_of_imported_document_data_model_version" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_otx_core_chk_007_have_specification_if_no_realisation_exists" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_otx_core_chk_008_public_main_procedure" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_otx_core_chk_009_mandatory_constant_initialization" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_otx_core_chk_010_unique_node_names" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_otx_data_type_chk_001_accessing_structure_elements" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_otx_data_type_chk_008_correct_target_for_structure_element" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_otx_zip_file_chk_002_type_safe_zip_file" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_otx_zip_file_chk_001_type_safe_unzip_file" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_otx_state_machine_chk_001_no_procedure_realization" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_otx_state_machine_chk_002_mandatory_target_state" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_otx_state_machine_chk_003_no_target_state_for_completed_state" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_otx_state_machine_chk_005_mandatory_transition" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_otx_state_machine_chk_004_mandatory_trigger" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_otx_state_machine_chk_006_distinguished_initial_and_completed_state" maxLevel="1" minLevel="3" />
    </CheckerBundle>

    <ReportModule application="TextReport">
        <Param name="strInputFile" value="Result.xqar" />
        <Param name="strReportFile" value="Report.txt" />
    </ReportModule>

</Config>
```

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

**To implement a new checker:**

1. Create a new Python module for each checker.
2. Specify the following global variables for the Python module

| Variable | Meaning |
| --- | --- |
| `CHECKER_ID` | The ID of the checker |
| `CHECKER_DESCRIPTION` | The description of the checker |
| `CHECKER_PRECONDITIONS` | A set of other checkers in which if any of them raise an issue, the current checker will be skipped |
| `RULE_UID` | The rule UID of the rule that the checker will check |

3. Implement the checker logic in the following function:

```python
def check_rule(checker_data: models.CheckerData) -> None:
    pass
```

4. Register the checker module in the following function in [main.py](qc_otx/main.py).

```python
def run_checks(config: Configuration, result: Result) -> None:
    ...
    # Add the following line to register your checker module
    execute_checker(your_checker_module, checker_data)
    ...
```

All the checkers in this checker bundle are implemented in this way. Take a look at some of them before implementing your first checker.
