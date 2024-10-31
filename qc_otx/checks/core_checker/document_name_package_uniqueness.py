# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging, os

from typing import List

from lxml import etree

from qc_baselib import IssueSeverity, StatusType

from qc_otx import constants
from qc_otx.checks import models


CHECKER_ID = "check_asam_otx_core_chk_002_document_name_package_uniqueness"
CHECKER_DESCRIPTION = "The value of the <otx> attribute name shall be unique within the scope of all OTX documents belonging to the same package."
CHECKER_PRECONDITIONS = set()
RULE_UID = "asam.net:otx:1.0.0:core.chk_002.document_name_package_uniqueness"


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

    root = checker_data.input_file_xml_root.getroot()

    document_name = root.get("name")
    if document_name is None:
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )

        checker_data.result.add_checker_summary(
            constants.BUNDLE_NAME,
            CHECKER_ID,
            "No name attribute in otx root node. Skip the check.",
        )

        return

    package_name = root.get("package")
    if package_name is None:
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )

        checker_data.result.add_checker_summary(
            constants.BUNDLE_NAME,
            CHECKER_ID,
            "No package attribute in otx root node. Skip the check.",
        )

        return

    document_package_dot_name = package_name + "." + document_name
    input_file_path = checker_data.config.get_config_param("InputFile")

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
        os.chdir(previous_wd)

        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )

        checker_data.result.add_checker_summary(
            constants.BUNDLE_NAME,
            CHECKER_ID,
            f"The package root folder {package_root} does not exist. Skip the check.",
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
            checker_id=CHECKER_ID,
            description="<otx> attribute name re-used in the same package",
            level=IssueSeverity.ERROR,
            rule_uid=RULE_UID,
        )

    os.chdir(previous_wd)
