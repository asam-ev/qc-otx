import logging, os

from typing import List

from lxml import etree

from qc_baselib import Result, IssueSeverity

from qc_otx import constants
from qc_otx.checks import models

from qc_otx.checks.core_checker import core_constants


def _is_prefix_never_used_in_attributes(attributes: List, prefix: str) -> bool:
    # Check if the prefix is never used in any attribute value
    for attr in attributes:
        if ":" in attr and prefix in attr.split(":")[0]:
            return False  # Found the prefix in an attribute value
    return True  # Prefix is never used in any attribute value


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements core checker rule Core_Chk004
    Criterion: An imported OTX document should be used at least once in the importing document.
    Severity: Warning

    """
    logging.info("Executing no_unused_imports check")

    rule_uid = checker_data.result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=core_constants.CHECKER_ID,
        emanating_entity="asam.net",
        standard="otx",
        definition_setting="1.0.0",
        rule_full_name="core.chk_004.no_unused_imports",
    )

    tree = checker_data.input_file_xml_root
    root = tree.getroot()

    import_nodes = root.findall(".//import", namespaces=root.nsmap)
    print(import_nodes)
    xpath_query = "//@*"
    otx_document_attributes = root.xpath(xpath_query)

    for import_node in import_nodes:
        import_prefix = import_node.get("prefix")
        import_package = import_node.get("package")
        import_document = import_node.get("document")
        import_path = tree.getpath(import_node)
        if _is_prefix_never_used_in_attributes(otx_document_attributes, import_prefix):
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=core_constants.CHECKER_ID,
                description="Issue flagging when an imported otx document is never used in the current otx",
                level=IssueSeverity.WARNING,
                rule_uid=rule_uid,
            )

            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=core_constants.CHECKER_ID,
                issue_id=issue_id,
                xpath=import_path,
                description=f"Imported otx document [package: {import_package}, document:{import_document}, prefix:{import_prefix}] is never used in current document",
            )
