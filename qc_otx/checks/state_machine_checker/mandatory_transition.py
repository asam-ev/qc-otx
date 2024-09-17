import logging

from qc_baselib import IssueSeverity, StatusType

from qc_otx import constants
from qc_otx.checks import models, utils


CHECKER_ID = "check_asam_otx_state_machine_chk_005_mandatory_transition"
CHECKER_DESCRIPTION = (
    "Each state except the completed state shall have at least one transition."
)
CHECKER_PRECONDITIONS = set()
RULE_UID = "asam.net:otx:1.0.0:state_machine.chk_005.mandatory_transition"


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

    tree = checker_data.input_file_xml_root
    nsmap = utils.get_namespace_map(tree)

    if "smp" not in nsmap:
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )

        checker_data.result.add_checker_summary(
            constants.BUNDLE_NAME,
            CHECKER_ID,
            f"No state machine procedure prefix 'smp' found in document namespaces. Skip the check.",
        )

        return

    state_machine_procedures = utils.get_state_machine_procedures(tree, nsmap)

    if state_machine_procedures is None:
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )

        checker_data.result.add_checker_summary(
            constants.BUNDLE_NAME,
            CHECKER_ID,
            f"State machine procedures not found. Skip the check.",
        )

        return

    logging.debug(f"state_machine_procedures: {state_machine_procedures}")

    # smp = "state machine procedure"
    for state_machine_procedure in state_machine_procedures:

        state_machine = utils.get_state_machine(state_machine_procedure, nsmap)

        if state_machine is None:
            checker_data.result.set_checker_status(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                status=StatusType.SKIPPED,
            )

            checker_data.result.add_checker_summary(
                constants.BUNDLE_NAME,
                CHECKER_ID,
                f"State machine not found. Skip the check.",
            )

            return

        for sm_state in state_machine.states:
            has_issue = not sm_state.is_completed and len(sm_state.transitions) == 0
            if has_issue:
                current_xpath = tree.getelementpath(sm_state.xml_element)
                issue_id = checker_data.result.register_issue(
                    checker_bundle_name=constants.BUNDLE_NAME,
                    checker_id=CHECKER_ID,
                    description="Non completed state has no transition",
                    level=IssueSeverity.ERROR,
                    rule_uid=RULE_UID,
                )

                checker_data.result.add_xml_location(
                    checker_bundle_name=constants.BUNDLE_NAME,
                    checker_id=CHECKER_ID,
                    issue_id=issue_id,
                    xpath=current_xpath,
                    description=f"State {sm_state.name} with id {sm_state.id} does not have any transition",
                )
