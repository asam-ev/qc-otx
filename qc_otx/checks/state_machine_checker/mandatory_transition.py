import logging

from qc_baselib import IssueSeverity

from qc_otx import constants
from qc_otx.checks import models, utils

from qc_otx.checks.state_machine_checker import state_machine_constants


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Rule ID: asam.net:otx:1.0.0:state_machine.chk_005.mandatory_transition

    Criterion: Each state except the completed state shall have at least one transition.
    Severity: Critical

    Version range: [1.0.0, )

    Remark:
        None

    """
    logging.info("Executing mandatory_transition check")

    issue_severity = IssueSeverity.ERROR

    rule_uid = checker_data.result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=state_machine_constants.CHECKER_ID,
        emanating_entity="asam.net",
        standard="otx",
        definition_setting="1.0.0",
        rule_full_name="state_machine.chk_005.mandatory_transition",
    )

    tree = checker_data.input_file_xml_root
    nsmap = utils.get_namespace_map(tree)

    if "smp" not in nsmap:
        logging.error(
            'No state machine procedure prefix "smp" found in document namespaces. Abort state machine procedure checks...'
        )
        return

    state_machine_procedures = utils.get_state_machine_procedures(tree, nsmap)

    if state_machine_procedures is None:
        return

    logging.debug(f"state_machine_procedures: {state_machine_procedures}")

    # smp = "state machine procedure"
    for state_machine_procedure in state_machine_procedures:

        state_machine = utils.get_state_machine(state_machine_procedure, nsmap)

        if state_machine is None:
            return

        for sm_state in state_machine.states:
            has_issue = not sm_state.is_completed and len(sm_state.transitions) == 0
            if has_issue:
                current_xpath = tree.getelementpath(sm_state.xml_element)
                issue_id = checker_data.result.register_issue(
                    checker_bundle_name=constants.BUNDLE_NAME,
                    checker_id=state_machine_constants.CHECKER_ID,
                    description="Issue flagging when a non completed state has no transition",
                    level=issue_severity,
                    rule_uid=rule_uid,
                )

                checker_data.result.add_xml_location(
                    checker_bundle_name=constants.BUNDLE_NAME,
                    checker_id=state_machine_constants.CHECKER_ID,
                    issue_id=issue_id,
                    xpath=current_xpath,
                    description=f"State {sm_state.name} with id {sm_state.id} does not have any transition",
                )
