import logging, os

from typing import List

from lxml import etree

from qc_baselib import Result, IssueSeverity

from qc_otx import constants
from qc_otx.checks import models

from qc_otx.checks.core_checker import core_constants


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements core checker rule Core_Chk008
    Criterion: The value of <procedure> attribute visibility shall always be "PUBLIC" if the procedure name is "main".
    ​Severity: Critical
    """
    logging.info("Executing public_main_procedure check")

    issue_severity = IssueSeverity.ERROR

    rule_uid = checker_data.result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=core_constants.CHECKER_ID,
        emanating_entity="asam.net",
        standard="otx",
        definition_setting="1.0.0",
        rule_full_name="core.chk_008.public_main_procedure",
    )

    tree = checker_data.input_file_xml_root
    root = tree.getroot()

    # Use XPath to find all nodes procedures
    procedure_nodes = tree.xpath(f"//procedure")

    for procedure_node in procedure_nodes:
        procedure_name = procedure_node.get("name")
        procedure_visibility = procedure_node.get("visibility")

        # Visibility defaults to private if not specified
        if procedure_visibility is None:
            procedure_visibility = "PRIVATE"

        has_issue = procedure_name == "main" and procedure_visibility != "PUBLIC"

        if has_issue:
            current_xpath = tree.getpath(procedure_node)
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=core_constants.CHECKER_ID,
                description="Issue flagging when procedure called main has not PUBLIC visibility",
                level=issue_severity,
                rule_uid=rule_uid,
            )

            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=core_constants.CHECKER_ID,
                issue_id=issue_id,
                xpath=current_xpath,
                description=f"Procedure at {current_xpath} is called main but its visibility is not PUBLIC",
            )
