# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging, os

from qc_baselib import IssueSeverity

from qc_otx import constants
from qc_otx.checks import models

CHECKER_ID = "check_asam_otx_core_chk_003_no_dead_import_links"
CHECKER_DESCRIPTION = "Imported OTX documents (referenced by package name and document name via <import> elements) should exist and should be accessible."
CHECKER_PRECONDITIONS = set()
RULE_UID = "asam.net:otx:1.0.0:core.chk_003.no_dead_import_links"


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements core checker rule Core_Chk003
    Criterion: Imported OTX documents (referenced by package name and document name via <import> elements)
    should exist and should be accessible.
    Severity: Critical
    """

    logging.info("Executing no_dead_import_links check")

    tree = checker_data.input_file_xml_root
    root = tree.getroot()
    input_file_path = checker_data.config.get_config_param("InputFile")

    import_nodes = root.findall(".//import", namespaces=root.nsmap)

    # Store previous working directory and move to config path dir for relative package paths
    previous_wd = os.getcwd()
    os.chdir(os.path.dirname(input_file_path))

    for import_node in import_nodes:
        import_prefix = import_node.get("prefix")
        import_package = import_node.get("package")
        import_document = import_node.get("document")
        logging.debug(
            f"import_prefix: {import_prefix} - import_package {import_package} - import_document {import_document}"
        )
        import_xpath = tree.getpath(import_node)
        # Import path checked in the same input file directory following
        # Recommendation: Use only references inside the same package.
        full_imported_path = os.path.join(import_document + ".otx")

        logging.debug(f"cwd: {os.getcwd()}")
        logging.debug(f"full_imported_path: {full_imported_path}")
        # Check if file exists
        import_file_exists = os.path.exists(full_imported_path)

        if not import_file_exists:
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                description="Imported otx document does not exists at specified package",
                level=IssueSeverity.ERROR,
                rule_uid=RULE_UID,
            )

            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                issue_id=issue_id,
                xpath=import_xpath,
                description=f"Imported otx document [package: {import_package}, document:{import_document}, prefix:{import_prefix}] does not exists",
            )

    os.chdir(previous_wd)
