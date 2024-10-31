# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging

from qc_baselib import IssueSeverity

from qc_otx import constants
from qc_otx.checks import models

CHECKER_ID = "check_asam_otx_core_chk_009_mandatory_constant_initialization"
CHECKER_DESCRIPTION = "Constant declarations shall always be initialized."
CHECKER_PRECONDITIONS = set()
RULE_UID = "asam.net:otx:1.0.0:core.chk_009.mandatory_constant_initialization"


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements core checker rule Core_Chk009
    Criterion: Constant declarations shall always be initialized.
    Severity: Critical
    """
    logging.info("Executing mandatory_constant_initialization check")

    tree = checker_data.input_file_xml_root
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
                checker_id=CHECKER_ID,
                description="Constant declaration without initialization",
                level=IssueSeverity.ERROR,
                rule_uid=RULE_UID,
            )

            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                issue_id=issue_id,
                xpath=current_xpath,
                description=f"Constant {constant_name} at {current_xpath} is not initialized",
            )
