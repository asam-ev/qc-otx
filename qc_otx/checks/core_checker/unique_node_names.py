# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging

from qc_baselib import IssueSeverity

from qc_otx import constants
from qc_otx.checks import models

CHECKER_ID = "check_asam_otx_core_chk_010_unique_node_names"
CHECKER_DESCRIPTION = "The value of a nodes name attribute should be unique among all nodes in a procedure."
CHECKER_PRECONDITIONS = set()
RULE_UID = "asam.net:otx:1.0.0:core.chk_010.unique_node_names"


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

    tree = checker_data.input_file_xml_root
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
                checker_id=CHECKER_ID,
                description="Nodes with same attribute name found in a procedure",
                level=IssueSeverity.WARNING,
                rule_uid=RULE_UID,
            )

            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                issue_id=issue_id,
                xpath=xpaths,
                description=f"Procedure {procedure_name} contains duplicated name.",
            )
