# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging

from qc_baselib import IssueSeverity, StatusType

from qc_otx import constants
from qc_otx.checks import models, utils

CHECKER_ID = "check_asam_otx_core_chk_005_no_use_of_undefined_import_prefixes"
CHECKER_DESCRIPTION = "If an imported name is accessed by prefix in an OtxLink type attribute, the corresponding prefix definition shall exist in an <import> element."
CHECKER_PRECONDITIONS = set()
RULE_UID = "asam.net:otx:1.0.0:core.chk_005.no_use_of_undefined_import_prefixes"


OTX_LINK_ATTRIBUTES = set()
OTX_LINK_ATTRIBUTES.add("implements")
OTX_LINK_ATTRIBUTES.add("validFor")
OTX_LINK_ATTRIBUTES.add("procedure")
OTX_LINK_ATTRIBUTES.add("valueOf")
OTX_LINK_ATTRIBUTES.add("mutexLock")


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements core checker rule Core_Chk005
    Criterion: If an imported name is accessed by prefix in an OtxLink type attribute,
                the corresponding prefix definition shall exist in an <import> element.
    Severity: Critical

    """
    logging.info("Executing no_use_of_undefined_import_prefixes check")

    tree = checker_data.input_file_xml_root
    root = tree.getroot()

    import_nodes = root.findall(".//import", namespaces=root.nsmap)

    if import_nodes is None:
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )

        checker_data.result.add_checker_summary(
            constants.BUNDLE_NAME,
            CHECKER_ID,
            f"No import nodes found. Skip the check.",
        )

        return

    import_prefixes = [x.get("prefix") for x in import_nodes]

    attributes = utils.get_all_attributes(tree, root)
    otx_link_attributes = [x for x in attributes if x.name in OTX_LINK_ATTRIBUTES]

    logging.debug(f"attributes: {attributes}")
    logging.debug(f"import_prefixes: {import_prefixes}")
    logging.debug(f"otx_link_attributes: {otx_link_attributes}")

    for otx_link in otx_link_attributes:
        if ":" not in otx_link.value:
            continue
        current_value_split = otx_link.value.split(":")
        if len(current_value_split) == 0:
            continue
        current_prefix = current_value_split[0]

        has_issue = current_prefix not in import_prefixes

        if has_issue:
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                description="Prefix definition does not exists in an <import> element",
                level=IssueSeverity.ERROR,
                rule_uid=RULE_UID,
            )

            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                issue_id=issue_id,
                xpath=otx_link.xpath,
                description=f"Imported prefix {current_prefix} not found across import elements",
            )
