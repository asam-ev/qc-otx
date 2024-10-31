# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging

from qc_baselib import IssueSeverity, StatusType

from qc_otx import constants
from qc_otx.checks import models, utils


CHECKER_ID = (
    "check_asam_otx_state_machine_chk_006_distinguished_initial_and_completed_state"
)
CHECKER_DESCRIPTION = "The values of the mandatory initialState and optional completedState attributes shall be distinguished."
CHECKER_PRECONDITIONS = set()
RULE_UID = (
    "asam.net:otx:1.0.0:state_machine.chk_006.distinguished_initial_and_completed_state"
)


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Rule ID: asam.net:otx:1.0.0:state_machine.chk_006.distinguished_initial_and_completed_state

    Description: The values of the mandatory initialState and optional completedState attributes shall be distinguished.
    Severity: ERROR

    Version range: [1.0.0, )

    Remark:
        None

    """
    logging.info("Executing distinguished_initial_and_completed_state check")

    tree = checker_data.input_file_xml_root
    nsmap = utils.get_namespace_map(tree)

    if "smp" not in nsmap:
        logging.error(
            'No state machine procedure prefix "smp" found in document namespaces. Abort state machine procedure checks...'
        )

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

        smp_realisation = state_machine_procedure.xpath(
            "./smp:realisation", namespaces=nsmap
        )
        logging.debug(f"smp_realisation: {smp_realisation}")

        if smp_realisation is None or len(smp_realisation) != 1:
            continue

        smp_realisation = smp_realisation[0]

        has_issue = smp_realisation.get("initialState") == smp_realisation.get(
            "completedState"
        )
        if has_issue:
            current_xpath = tree.getelementpath(smp_realisation)
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                description="initialState and completedState cannot be distinguished",
                level=IssueSeverity.ERROR,
                rule_uid=RULE_UID,
            )

            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                issue_id=issue_id,
                xpath=current_xpath,
                description=f"State machine realisation cannot distinguish between initial and completed state",
            )
