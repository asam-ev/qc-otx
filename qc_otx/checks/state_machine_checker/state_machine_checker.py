import logging

from lxml import etree

from qc_baselib import Configuration, Result, StatusType

from qc_otx import constants
from qc_otx.checks import utils, models

from qc_otx.checks.state_machine_checker import (
    state_machine_constants,
    no_procedure_realization,
    mandatory_target_state,
    no_target_state_for_completed_state,
    mandatory_transition,
    mandatory_trigger,
    distinguished_initial_and_completed_state,
)


def run_checks(checker_data: models.CheckerData) -> None:
    logging.info("Executing state_machine checks")

    checker_data.result.register_checker(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=state_machine_constants.CHECKER_ID,
        description="Check if state_machine properties of input file are properly set",
        summary="",
    )

    rule_list = [
        no_procedure_realization.check_rule,  # Chk001
        mandatory_target_state.check_rule,  # Chk002
        no_target_state_for_completed_state.check_rule,  # Chk003
        mandatory_transition.check_rule,  # Chk004
        mandatory_trigger.check_rule,  # Chk005
        distinguished_initial_and_completed_state.check_rule,  # Chk006
    ]

    for rule in rule_list:
        rule(checker_data=checker_data)

    logging.info(
        f"Issues found - {checker_data.result.get_checker_issue_count(checker_bundle_name=constants.BUNDLE_NAME, checker_id=state_machine_constants.CHECKER_ID)}"
    )

    checker_data.result.set_checker_status(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=state_machine_constants.CHECKER_ID,
        status=StatusType.COMPLETED,
    )
