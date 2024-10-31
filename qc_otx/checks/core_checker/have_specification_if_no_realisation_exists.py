# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging


from qc_baselib import IssueSeverity

from qc_otx import constants
from qc_otx.checks import models

CHECKER_ID = "check_asam_otx_core_chk_007_have_specification_if_no_realisation_exists"
CHECKER_DESCRIPTION = "For all elements with specification and realisation parts in an OTX document: if there is no <realisation> given, the according <specification> element should exist and have content (no empty string)."
CHECKER_PRECONDITIONS = set()
RULE_UID = "asam.net:otx:1.0.0:core.chk_007.have_specification_if_no_realisation_exists"


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
                checker_id=CHECKER_ID,
                description="Empty realisation has content in specification",
                level=IssueSeverity.WARNING,
                rule_uid=RULE_UID,
            )

            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                issue_id=issue_id,
                xpath=current_xpath,
                description=f"Node {current_xpath} has no realisation and no specification or empty string in specification",
            )
