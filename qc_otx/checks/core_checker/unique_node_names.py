import logging, os

from typing import List

from lxml import etree

from qc_baselib import Result, IssueSeverity

from qc_otx import constants
from qc_otx.checks import models

from qc_otx.checks.core_checker import core_constants


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Rule ID: asam.net:otx:1.0.0:core.chk_010.unique_node_names

    Description: The value of a nodes name attribute should be unique among all nodes in a procedure.

    Severity: WARNING

    Version range: [1.0.0, )

    Remark:
        None

    More info at
        -
    """
    logging.info("Executing unique_node_names check")

    issue_severity = IssueSeverity.WARNING

    rule_uid = checker_data.result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=core_constants.CHECKER_ID,
        emanating_entity="asam.net",
        standard="otx",
        definition_setting="1.0.0",
        rule_full_name="core.chk_010.unique_node_names",
    )

    tree = checker_data.input_file_xml_root
    root = tree.getroot()
    # Use XPath to find all nodes procedure
    procedure_nodes = tree.xpath("//procedure")

    for procedure_node in procedure_nodes:
        procedure_name = procedure_node.get("name")

        # Define the XPath expression to find all elements with a "name" attribute
        xpath_expr = ".//*[@name]"

        # Use XPath to find all matching elements from the given procedure node
        result = procedure_node.xpath(xpath_expr)

        # Dictionary to store the found names and their corresponding XPath expressions
        name_map = dict()

        # Build the XPaths for elements and check for duplicates
        for elem in result:
            name = elem.get("name")
            if name is None:
                continue
            xpath = tree.getpath(elem)

            if name not in name_map:
                name_map[name] = []

            name_map[name].append(xpath)

        for name, xpaths in name_map.items():
            if len(xpaths) <= 1:
                continue

            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=core_constants.CHECKER_ID,
                description="Issue flagging when nodes with same attribute name are found in a procedure",
                level=issue_severity,
                rule_uid=rule_uid,
            )

            error_string = f"Duplicated name {name}"
            for xpath in xpaths:
                error_string += f" defined at {xpath}"

            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=core_constants.CHECKER_ID,
                issue_id=issue_id,
                xpath=xpaths,
                description=f"Procedure {procedure_name} contains duplicated name. {error_string}",
            )
