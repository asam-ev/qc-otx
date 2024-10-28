# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging


from qc_baselib import IssueSeverity, StatusType

from qc_otx import constants
from qc_otx.checks import models

from pathlib import Path

CHECKER_ID = "check_asam_otx_core_chk_001_document_name_matches_filename"
CHECKER_DESCRIPTION = "For OTX documents stored in a file system, the attribute name of the <otx> root element should match the filename of the containing file (without the extension '.otx')."
CHECKER_PRECONDITIONS = set()
RULE_UID = "asam.net:otx:1.0.0:core.chk_001.document_name_matches_filename"


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

    root = checker_data.input_file_xml_root
    root_attrib = root.getroot().attrib

    if "name" not in root_attrib:
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )

        checker_data.result.add_checker_summary(
            constants.BUNDLE_NAME,
            CHECKER_ID,
            "No name attribute in otx root node. Skip the check.",
        )

        return

    document_name = root_attrib["name"]
    config_file_path = checker_data.config.get_config_param("InputFile")
    filename = Path(config_file_path).stem

    is_valid = document_name == filename

    if not is_valid:

        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            description="Document name not matching file name",
            level=IssueSeverity.WARNING,
            rule_uid=RULE_UID,
        )

        checker_data.result.add_xml_location(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            issue_id=issue_id,
            xpath="/otx",
            description=f"Invalid otx name {document_name} detected. Do not match filename {filename}",
        )
