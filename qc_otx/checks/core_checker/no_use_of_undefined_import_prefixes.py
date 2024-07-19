import logging, os

from typing import List

from lxml import etree

from qc_baselib import Result, IssueSeverity

from qc_otx import constants
from qc_otx.checks import models, utils

from qc_otx.checks.core_checker import core_constants

RULE_SEVERITY = IssueSeverity.ERROR

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

    rule_uid = checker_data.result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=core_constants.CHECKER_ID,
        emanating_entity="asam.net",
        standard="otx",
        definition_setting="1.0.0",
        rule_full_name="core.chk_005.no_use_of_undefined_import_prefixes",
    )

    tree = checker_data.input_file_xml_root
    root = tree.getroot()

    import_nodes = root.findall(".//import", namespaces=root.nsmap)

    if import_nodes is None:
        logging.error("No import nodes found. Skipping check..")
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
                checker_id=core_constants.CHECKER_ID,
                description="Issue flagging when prefix definition does not exists in an import element",
                level=RULE_SEVERITY,
                rule_uid=rule_uid,
            )

            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=core_constants.CHECKER_ID,
                issue_id=issue_id,
                xpath=otx_link.xpath,
                description=f"Imported prefix {current_prefix} not found across import elements",
            )
