import logging

from lxml import etree

from qc_baselib import Configuration, Result, StatusType

from qc_otx import constants
from qc_otx.checks import utils, models

from qc_otx.checks.data_type_checker import (
    data_type_constants,
    accessing_structure_elements,
)


def run_checks(checker_data: models.CheckerData) -> None:
    logging.info("Executing data_type checks")

    checker_data.result.register_checker(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=data_type_constants.CHECKER_ID,
        description="Check if data_type properties of input file are properly set",
        summary="",
    )

    rule_list = [
        accessing_structure_elements.check_rule,  # Chk001
    ]

    for rule in rule_list:
        rule(checker_data=checker_data)

    logging.info(
        f"Issues found - {checker_data.result.get_checker_issue_count(checker_bundle_name=constants.BUNDLE_NAME, checker_id=data_type_constants.CHECKER_ID)}"
    )

    checker_data.result.set_checker_status(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=data_type_constants.CHECKER_ID,
        status=StatusType.COMPLETED,
    )
