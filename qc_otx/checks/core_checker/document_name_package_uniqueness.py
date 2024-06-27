import logging, os

from dataclasses import dataclass
from typing import List

from lxml import etree

from qc_baselib import Configuration, Result, IssueSeverity

from qc_otx import constants
from qc_otx.checks import utils, models

from qc_otx.checks.core_checker import core_constants
from pathlib import Path


def find_otx_files(directory: str) -> List:
    """Recursively find all OTX files in the given directory."""
    otx_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".otx"):
                otx_files.append(os.path.join(root, file))
    return otx_files


def get_package_dot_name_attributes(xml_files: List) -> List:
    """Parse XML files and collect 'name' and `package` attributes from root elements.
    Resulting list will contains name and package in the form: "package.name"
    """
    package_dot_name_attributes = []
    for file in xml_files:
        try:
            tree = etree.parse(file)
            root = tree.getroot()
            name_attr = root.get("name")
            package_attr = root.get("package")
            package_dot_name = package_attr + "." + name_attr
            if package_attr and name_attr:
                package_dot_name_attributes.append(package_dot_name)
        except etree.XMLSyntaxError:
            print(f"Failed to parse XML file: {file}")
        except Exception as e:
            print(f"An error occurred: {e}")
    return package_dot_name_attributes


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements core checker rule Core_Chk002
    Criterion: The value of the <otx> attribute name shall be unique
    within the scope of all OTX documents belonging to the same package.
    Severity: Critical

    """
    logging.info("Executing document_name_package_uniqueness check")

    rule_uid = checker_data.result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=core_constants.CHECKER_ID,
        emanating_entity="asam.net",
        standard="otx",
        definition_setting="1.0.0",
        rule_full_name="core.chk_002.document_name_package_uniqueness",
    )

    root = checker_data.input_file_xml_root.getroot()

    document_name = root.get("name")
    if document_name is None:
        logging.error("No name attribute find in otx root node. Abort...")
        return

    package_name = root.get("package")
    if package_name is None:
        logging.error("No package attribute find in otx root node. Abort...")
        return

    document_package_dot_name = package_name + "." + document_name
    input_file_path = checker_data.config.get_config_param("OtxFile")

    # Store previous working directory and move to config path dir for relative package paths
    previous_wd = os.getcwd()
    os.chdir(os.path.dirname(input_file_path))

    # Split package path by "."
    package_splits = package_name.split(".")

    # For each element of the package full path
    # Create relative path with .. -> to have the path to the root of the package
    # Substitute . with / for having the path of the current config, for filtering results
    current_filename_package_path = ""
    package_root = ""
    for package_dir in package_splits:
        current_filename_package_path = os.path.join(
            current_filename_package_path, package_dir
        )
        package_root = os.path.join(package_root, "..")

    current_filename_package_path = os.path.join(
        current_filename_package_path, os.path.basename(input_file_path)
    )
    package_root = os.path.join(package_root, package_splits[0])

    if not os.path.exists(package_root):
        logging.error(
            f"Error in setting package root {package_root}. Folder not found. Abort..."
        )
        return
    # Collect all otx file path from package root
    package_otx_files = find_otx_files(package_root)

    # Filtering out current document name from otx file list
    package_otx_files = [
        x for x in package_otx_files if current_filename_package_path not in x
    ]

    # Collect all otx names in the form package.name
    package_dot_names = get_package_dot_name_attributes(package_otx_files)

    is_valid = document_package_dot_name not in package_dot_names

    if not is_valid:
        checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=core_constants.CHECKER_ID,
            description="Issue flagging when otx name is reused in the same package",
            level=IssueSeverity.ERROR,
            rule_uid=rule_uid,
        )

    os.chdir(previous_wd)
