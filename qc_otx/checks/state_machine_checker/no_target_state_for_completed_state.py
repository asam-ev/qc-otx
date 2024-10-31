# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging

from qc_baselib import IssueSeverity, StatusType

from qc_otx import constants
from qc_otx.checks import models, utils


CHECKER_ID = "check_asam_otx_state_machine_chk_003_no_target_state_for_completed_state"
CHECKER_DESCRIPTION = "After finishing the completed state the procedure is finished and shall return to the caller. Therefore the completed state shall not have a target state."
CHECKER_PRECONDITIONS = set()
RULE_UID = (
    "asam.net:otx:1.0.0:state_machine.chk_003.no_target_state_for_completed_state"
)


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Rule ID: asam.net:otx:1.0.0:state_machine.chk_003.no_target_state_for_completed_state

    Criterion: After finishing the completed state the procedure is finished and shall return to
    the caller. Therefore the completed state shall not have a target state.
    Severity: Warning

    Version range: [1.0.0, )

    Remark:
        None

    """
    logging.info("Executing no_target_state_for_completed_state check")

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
            continue

        completed_state = None
        for sm_state in state_machine.states:
            if sm_state.is_completed:
                completed_state = sm_state
                break

        if completed_state is None:
            continue

        has_issue = len(completed_state.target_state_ids) != 0
        if has_issue:
            current_xpath = tree.getelementpath(completed_state.xml_element)
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                description="completed state has a target state",
                level=IssueSeverity.WARNING,
                rule_uid=RULE_UID,
            )

            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                issue_id=issue_id,
                xpath=current_xpath,
                description=f"Completed state {completed_state.name} with id {completed_state.id} has a target state but it should not",
            )
