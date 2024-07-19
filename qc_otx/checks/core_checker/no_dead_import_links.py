import logging, os

from typing import List

from lxml import etree

from qc_baselib import Result, IssueSeverity

from qc_otx import constants
from qc_otx.checks import models

from qc_otx.checks.core_checker import core_constants


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements core checker rule Core_Chk003
    Criterion: Imported OTX documents (referenced by package name and document name via <import> elements)
    should exist and should be accessible.
    Severity: Critical
    """

    logging.info("Executing no_dead_import_links check")

    rule_uid = checker_data.result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=core_constants.CHECKER_ID,
        emanating_entity="asam.net",
        standard="otx",
        definition_setting="1.0.0",
        rule_full_name="core.chk_003.no_dead_import_links",
    )

    tree = checker_data.input_file_xml_root
    root = tree.getroot()
    input_file_path = checker_data.config.get_config_param("OtxFile")

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
                checker_id=core_constants.CHECKER_ID,
                description="Issue flagging when an imported otx document does not exists at specified package",
                level=IssueSeverity.ERROR,
                rule_uid=rule_uid,
            )

            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=core_constants.CHECKER_ID,
                issue_id=issue_id,
                xpath=import_xpath,
                description=f"Imported otx document [package: {import_package}, document:{import_document}, prefix:{import_prefix}] does not exists",
            )

    os.chdir(previous_wd)
