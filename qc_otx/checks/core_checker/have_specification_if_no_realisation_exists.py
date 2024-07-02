import logging, os

from typing import List

from lxml import etree

from qc_baselib import Result, IssueSeverity

from qc_otx import constants
from qc_otx.checks import models

from qc_otx.checks.core_checker import core_constants

NODES_WITH_SPECIFICATION_AND_REALISATION = [
    "declaration",
    "procedure",
    "signature",
    "validity",
]


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements core checker rule Core_Chk007
    Criterion: For all elements with specification and realisation parts in an OTX document:
    if there is no <realisation> given, the according <specification> element should exist
    and have content (no empty string).
    Severity: Warning
    """
    logging.info("Executing have_specification_if_no_realisation_exists check")

    issue_severity = IssueSeverity.WARNING

    rule_uid = checker_data.result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=core_constants.CHECKER_ID,
        emanating_entity="asam.net",
        standard="otx",
        definition_setting="1.0.0",
        rule_full_name="core.chk_007.have_specification_if_no_realisation_exists",
    )

    tree = checker_data.input_file_xml_root
    root = tree.getroot()

    # Construct the XPath expression using the union operator
    xpath_expr = "|".join(
        [f"//{node}" for node in NODES_WITH_SPECIFICATION_AND_REALISATION]
    )

    # Use XPath to find all matching elements
    result = root.xpath(xpath_expr)

    for node in result:
        has_realisation = node.find("realisation") is not None
        has_specification = node.find("specification") is not None
        specification_has_content = (
            has_specification
            and node.find("specification").text is not None
            and node.find("specification").text != '""'
        )

        is_valid = True

        if not has_realisation:
            is_valid = has_specification and specification_has_content

        current_xpath = tree.getpath(node)

        if not is_valid:
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=core_constants.CHECKER_ID,
                description="Issue to check if empty realisation have content in specification",
                level=issue_severity,
                rule_uid=rule_uid,
            )

            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=core_constants.CHECKER_ID,
                issue_id=issue_id,
                xpath=current_xpath,
                description=f"Node {current_xpath} has no realisation and no specification or empty string in specification",
            )
