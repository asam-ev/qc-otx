import logging

from qc_baselib import IssueSeverity

from qc_otx import constants
from qc_otx.checks import models, utils

from qc_otx.checks.state_machine_checker import state_machine_constants


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Rule ID: asam.net:otx:1.0.0:state_machine.chk_006.distinguished_initial_and_completed_state

    Description: Each state except the completed state shall have a target state.
    Severity: ERROR

    Version range: [1.0.0, )

    Remark:
        None

    """
    logging.info("Executing distinguished_initial_and_completed_state check")

    issue_severity = IssueSeverity.ERROR

    rule_uid = checker_data.result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=state_machine_constants.CHECKER_ID,
        emanating_entity="asam.net",
        standard="otx",
        definition_setting="1.0.0",
        rule_full_name="state_machine.chk_006.distinguished_initial_and_completed_state",
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

        smp_realisation = state_machine_procedure.xpath(
            "./smp:realisation", namespaces=nsmap
        )
        logging.debug(f"smp_realisation: {smp_realisation}")

        if smp_realisation is None or len(smp_realisation) != 1:
            logging.error(
                f"Invalid realisation found in current state machine procedure"
            )
            return

        smp_realisation = smp_realisation[0]

        has_issue = smp_realisation.get("initialState") == smp_realisation.get(
            "completedState"
        )
        if has_issue:
            current_xpath = tree.getelementpath(smp_realisation)
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=state_machine_constants.CHECKER_ID,
                description="Issue flagging when initialState and completedState cannot be distinguished",
                level=issue_severity,
                rule_uid=rule_uid,
            )

            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=state_machine_constants.CHECKER_ID,
                issue_id=issue_id,
                xpath=current_xpath,
                description=f"State machine realisation cannot distinguish between initial and completed state",
            )
