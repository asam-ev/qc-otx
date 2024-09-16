import logging

from qc_baselib import IssueSeverity

from qc_otx import constants
from qc_otx.checks import models


CHECKER_ID = "check_asam_otx_core_chk_008_public_main_procedure"
CHECKER_DESCRIPTION = "he value of <procedure> attribute visibility shall always be 'PUBLIC' if the procedure name is 'main'."
CHECKER_PRECONDITIONS = set()
RULE_UID = "asam.net:otx:1.0.0:core.chk_008.public_main_procedure"


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements core checker rule Core_Chk008
    Criterion: The value of <procedure> attribute visibility shall always be "PUBLIC" if the procedure name is "main".
    ​Severity: Critical
    """
    logging.info("Executing public_main_procedure check")

    tree = checker_data.input_file_xml_root

    # Use XPath to find all nodes procedures
    procedure_nodes = tree.xpath(f"//procedure")

    for procedure_node in procedure_nodes:
        procedure_name = procedure_node.get("name")
        procedure_visibility = procedure_node.get("visibility")

        # Visibility defaults to private if not specified
        if procedure_visibility is None:
            procedure_visibility = "PRIVATE"

        has_issue = procedure_name == "main" and procedure_visibility != "PUBLIC"

        if has_issue:
            current_xpath = tree.getpath(procedure_node)
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                description="Issue flagging when procedure called main has not PUBLIC visibility",
                level=IssueSeverity.ERROR,
                rule_uid=RULE_UID,
            )

            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                issue_id=issue_id,
                xpath=current_xpath,
                description=f"Procedure at {current_xpath} is called main but its visibility is not PUBLIC",
            )
