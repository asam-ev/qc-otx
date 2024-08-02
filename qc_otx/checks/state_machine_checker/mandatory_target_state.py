import logging

from qc_baselib import IssueSeverity

from qc_otx import constants
from qc_otx.checks import models

from qc_otx.checks.state_machine_checker import state_machine_constants

from qc_otx.checks.state_machine_checker import utils as state_machine_utils

logging.basicConfig(level=logging.DEBUG)


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Rule ID: asam.net:otx:1.0.0:state_machine.chk_002.mandatory_target_state

    Description: Each state except the completed state shall have a target state.
    Severity: ERROR

    Version range: [1.0.0, )

    Remark:
        None

    """
    logging.info("Executing mandatory_target_state check")

    issue_severity = IssueSeverity.ERROR

    rule_uid = checker_data.result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=state_machine_constants.CHECKER_ID,
        emanating_entity="asam.net",
        standard="otx",
        definition_setting="1.0.0",
        rule_full_name="state_machine.chk_002.mandatory_target_state",
    )

    tree = checker_data.input_file_xml_root
    root = tree.getroot()
    nsmap = {k: v for k, v in root.nsmap.items() if k is not None}

    if "smp" not in nsmap:
        logging.error(
            'No state machine procedure prefix "smp" found in document namespaces. Abort state machine procedure checks...'
        )
        return

    state_machine_procedures = tree.xpath(
        "//*[@xsi:type='smp:StateMachineProcedure']", namespaces=nsmap
    )

    if state_machine_procedures is None:
        return

    logging.debug(f"state_machine_procedures: {state_machine_procedures}")

    # smp = "state machine procedure"
    for state_machine_procedure in state_machine_procedures:

        state_machine = state_machine_utils.get_state_machine(
            state_machine_procedure, nsmap
        )

        if state_machine is None:
            return

        for sm_state in state_machine.states:
            has_issue = (
                not sm_state.is_completed and len(sm_state.target_state_ids) == 0
            )
            if has_issue:
                current_xpath = tree.getpath(sm_state.xml_element)
                issue_id = checker_data.result.register_issue(
                    checker_bundle_name=constants.BUNDLE_NAME,
                    checker_id=state_machine_constants.CHECKER_ID,
                    description="Issue flagging when a non completed state has no target state",
                    level=issue_severity,
                    rule_uid=rule_uid,
                )

                checker_data.result.add_xml_location(
                    checker_bundle_name=constants.BUNDLE_NAME,
                    checker_id=state_machine_constants.CHECKER_ID,
                    issue_id=issue_id,
                    xpath=current_xpath,
                    description=f"State {sm_state.name} wiht id {sm_state.id} does not have any target state",
                )
