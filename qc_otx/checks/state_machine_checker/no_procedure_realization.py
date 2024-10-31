# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging

from qc_baselib import IssueSeverity, StatusType

from qc_otx import constants
from qc_otx.checks import models, utils


CHECKER_ID = "check_asam_otx_state_machine_chk_001_no_procedure_realization"
CHECKER_DESCRIPTION = "A StateMachineProcedure shall not have a ProcedureRealisation."
CHECKER_PRECONDITIONS = set()
RULE_UID = "asam.net:otx:1.0.0:state_machine.chk_001.no_procedure_realization"


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Rule ID: asam.net:otx:1.0.0:state_machine.chk_001.no_procedure_realization

    Description: A StateMachineProcedure shall not have a ProcedureRealisation.
    Severity: ERROR

    Version range: [1.0.0, )

    Remark:
        None

    """
    logging.info("Executing no_procedure_realization check")

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

    for state_machine_procedure in state_machine_procedures:
        realisations = state_machine_procedure.xpath(
            "./otx:realisation", namespaces=nsmap
        )

        logging.debug(f"realisations: {realisations}")

        has_issue = realisations is not None and len(realisations) != 0
        if has_issue:
            current_xpath = tree.getelementpath(state_machine_procedure)
            procedure_realisation_xpath = tree.getpath(realisations[0])
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                description="StateMachineProcedure has a ProcedureRealisation",
                level=IssueSeverity.ERROR,
                rule_uid=RULE_UID,
            )

            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                issue_id=issue_id,
                xpath=current_xpath,
                description=f"State machine {state_machine_procedure.get('id')} has a ProcedureRealisation at {procedure_realisation_xpath}",
            )
