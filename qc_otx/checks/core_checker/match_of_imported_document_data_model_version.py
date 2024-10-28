# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging, os

from lxml import etree

from qc_baselib import IssueSeverity, StatusType

from qc_otx import constants
from qc_otx.checks import models, utils


CHECKER_ID = "check_asam_otx_core_chk_006_match_of_imported_document_data_model_version"
CHECKER_DESCRIPTION = "An imported OTX document (imported by an <import> element) shall be bound to the same data model version as the importing document."
CHECKER_PRECONDITIONS = set()
RULE_UID = (
    "asam.net:otx:1.0.0:core.chk_006.match_of_imported_document_data_model_version"
)


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements core checker rule Core_Chk006
    Criterion: An imported OTX document (imported by an <import> element)
                shall be bound to the same data model version as the importing document.
                For this, the OTX XSD namespaces claimed by the <otx> root elements
                of both documents (attribute xmlns = "http://iso.org/OTX/<version > ") shall be identical.

    Severity: Critical

    """
    logging.info("Executing match_of_imported_document_data_model_version check")

    input_file_path = checker_data.config.get_config_param("InputFile")
    tree = checker_data.input_file_xml_root
    root = tree.getroot()

    source_data_model_version = utils.get_data_model_version(root)
    if source_data_model_version is None:
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )

        checker_data.result.add_checker_summary(
            constants.BUNDLE_NAME,
            CHECKER_ID,
            f"xmlns version not found in current document root. Skip the check.",
        )

        return

    logging.debug(f"source_data_model_version: {source_data_model_version}")

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

    # Store previous working directory and move to config path dir for relative package paths
    previous_wd = os.getcwd()
    os.chdir(os.path.dirname(input_file_path))

    for import_node in import_nodes:

        current_document = import_node.get("document")
        if current_document is None:
            continue

        current_document_filepath = current_document + ".otx"
        current_xpath = tree.getpath(import_node)

        if not os.path.exists(current_document_filepath):
            continue

        current_imported_document_root = etree.parse(current_document_filepath)
        current_data_model_version = utils.get_data_model_version(
            current_imported_document_root.getroot()
        )
        logging.debug(
            f"Current document {current_document} - data model version {current_data_model_version}"
        )
        has_issue = current_data_model_version != source_data_model_version

        if has_issue:
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                description="Imported document data model version is different than the one in the current document",
                level=IssueSeverity.ERROR,
                rule_uid=RULE_UID,
            )

            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                issue_id=issue_id,
                xpath=current_xpath,
                description=f"Imported document {current_document} data model version {current_data_model_version} different than current model version {source_data_model_version}",
            )

    os.chdir(previous_wd)
