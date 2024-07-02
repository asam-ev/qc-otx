import logging, os

from typing import List

from lxml import etree

from qc_baselib import Result, IssueSeverity

from qc_otx import constants
from qc_otx.checks import models

from qc_otx.checks.core_checker import core_constants


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

    # Define the type you are looking for
    desired_type = "specification"
    desired_sibling_name = "realisation"

    # Use XPath to find all nodes of the specified type
    specification_nodes = tree.xpath(f"//*[local-name() = '{desired_type}']")

    # Check siblings for each specification node
    for spec_node in specification_nodes:

        current_has_content = spec_node.text is not None

        current_siblings = []
        parent = spec_node.getparent()
        if parent is not None:
            siblings = parent.getchildren()
            for sibling in siblings:
                if sibling != spec_node and sibling.tag.endswith(desired_sibling_name):
                    current_siblings.append(sibling)

        has_issue = len(current_siblings) == 0 and not current_has_content

        current_xpath = tree.getpath(spec_node)
        print("node.text ", spec_node.text)
        print("current_xpath ", current_xpath)
        print("current_has_content ", current_has_content)
        if has_issue:
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=core_constants.CHECKER_ID,
                description="Issue flagging when specification node with no realisation has empty content",
                level=issue_severity,
                rule_uid=rule_uid,
            )

            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=core_constants.CHECKER_ID,
                issue_id=issue_id,
                xpath=current_xpath,
                description=f"Specification node {current_xpath} has no realisation and empty string as content",
            )

        # print("Found a sibling with the name 'realisation':")
        # print(etree.tostring(sibling, pretty_print=True).decode("utf-8"))
