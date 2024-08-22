import logging, os, re

from typing import List

from lxml import etree

from qc_baselib import Result, IssueSeverity

from qc_otx import constants
from qc_otx.checks import models, utils

from qc_otx.checks.core_checker import core_constants


RULE_SEVERITY = IssueSeverity.ERROR


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

    rule_uid = checker_data.result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=core_constants.CHECKER_ID,
        emanating_entity="asam.net",
        standard="otx",
        definition_setting="1.0.0",
        rule_full_name="core.chk_006.match_of_imported_document_data_model_version",
    )

    input_file_path = checker_data.config.get_config_param("InputFile")
    tree = checker_data.input_file_xml_root
    root = tree.getroot()

    source_data_model_version = utils.get_data_model_version(root)
    if source_data_model_version is None:
        logging.error(
            "xmlns version not found in current document root. Skipping check.."
        )
        return
    logging.debug(f"source_data_model_version: {source_data_model_version}")

    import_nodes = root.findall(".//import", namespaces=root.nsmap)

    if import_nodes is None:
        logging.error("No import nodes found. Skipping check..")
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
                checker_id=core_constants.CHECKER_ID,
                description="Issue flagging when data model version of imported document is different than the one in current document",
                level=RULE_SEVERITY,
                rule_uid=rule_uid,
            )

            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=core_constants.CHECKER_ID,
                issue_id=issue_id,
                xpath=current_xpath,
                description=f"Imported document {current_document} data model version {current_data_model_version} different than current model version {source_data_model_version}",
            )

    os.chdir(previous_wd)
