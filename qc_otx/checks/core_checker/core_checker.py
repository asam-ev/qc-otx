import logging

from lxml import etree

from qc_baselib import Configuration, Result, StatusType

from qc_otx import constants
from qc_otx.checks import utils, models

from qc_otx.checks.core_checker import core_constants, document_name_matches_filename


def run_checks(checker_data: models.CheckerData) -> None:
    logging.info("Executing core checks")

    checker_data.result.register_checker(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=core_constants.CHECKER_ID,
        description="Check if core properties of input file are properly set",
        summary="",
    )

    rule_list = [document_name_matches_filename.check_rule]

    for rule in rule_list:
        rule(checker_data=checker_data)

    logging.info(
        f"Issues found - {checker_data.result.get_checker_issue_count(checker_bundle_name=constants.BUNDLE_NAME, checker_id=core_constants.CHECKER_ID)}"
    )

    checker_data.result.set_checker_status(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=core_constants.CHECKER_ID,
        status=StatusType.COMPLETED,
    )
