import logging

from dataclasses import dataclass
from typing import List

from lxml import etree

from qc_baselib import Configuration, Result, IssueSeverity

from qc_otx import constants
from qc_otx.checks import utils, models

from qc_otx.checks.core_checker import core_constants
from pathlib import Path


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements core checker rule Core_Chk001
    Criterion:
    For OTX documents stored in a file system, the attribute name of the <otx>
    root element should match the filename of the containing file
    (without the extension “.otx”).
    Severity:
    Warning
    """
    logging.info("Executing document_name_matches_filename check")

    rule_uid = checker_data.result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=core_constants.CHECKER_ID,
        emanating_entity="asam.net",
        standard="otx",
        definition_setting="1.0.0",
        rule_full_name="core.chk_001.document_name_matches_filename",
    )

    root = checker_data.input_file_xml_root
    root_attrib = root.getroot().attrib

    if "name" not in root_attrib:
        logging.error("No name attribute find in otx root node. Abort...")
        return

    document_name = root_attrib["name"]
    config_file_path = checker_data.config.get_config_param("InputFile")
    filename = Path(config_file_path).stem

    is_valid = document_name == filename

    if not is_valid:

        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=core_constants.CHECKER_ID,
            description="Issue flagging when document name does not match file name",
            level=IssueSeverity.WARNING,
            rule_uid=rule_uid,
        )

        checker_data.result.add_xml_location(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=core_constants.CHECKER_ID,
            issue_id=issue_id,
            xpath="/otx",
            description=f"Invalid otx name {document_name} detected. Do not match filename {filename}",
        )
