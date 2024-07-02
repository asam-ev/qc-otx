import logging, os

from typing import List

from lxml import etree

from qc_baselib import Result, IssueSeverity

from qc_otx import constants
from qc_otx.checks import models

from qc_otx.checks.core_checker import core_constants


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements core checker rule Core_Chk009
    Criterion: Constant declarations shall always be initialized.
    Severity: Critical
    """
    logging.info("Executing mandatory_constant_initialization check")

    issue_severity = IssueSeverity.ERROR

    rule_uid = checker_data.result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=core_constants.CHECKER_ID,
        emanating_entity="asam.net",
        standard="otx",
        definition_setting="1.0.0",
        rule_full_name="core.chk_009.mandatory_constant_initialization",
    )

    tree = checker_data.input_file_xml_root
    root = tree.getroot()
    # Use XPath to find all nodes constant
    constant_nodes = tree.xpath("//constant")

    for constant_node in constant_nodes:
        constant_name = constant_node.get("name")

        # Define the XPath expression for the sequence of children
        xpath_expr = ".//realisation/dataType/init"

        # Use XPath to find if the sequence exists
        is_valid = constant_node.xpath(xpath_expr)

        if not is_valid:
            current_xpath = tree.getpath(constant_node)
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=core_constants.CHECKER_ID,
                description="Issue flagging when a constant is not initialized",
                level=issue_severity,
                rule_uid=rule_uid,
            )

            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=core_constants.CHECKER_ID,
                issue_id=issue_id,
                xpath=current_xpath,
                description=f"Constant {constant_name} at {current_xpath} is not initialized",
            )
