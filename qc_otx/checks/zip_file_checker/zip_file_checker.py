import logging

from lxml import etree

from qc_baselib import Configuration, Result, StatusType

from qc_otx import constants
from qc_otx.checks import utils, models

from qc_otx.checks.zip_file_checker import (
    zip_file_constants,
    type_safe_zip_file,
    type_safe_unzip_file,
)


def run_checks(checker_data: models.CheckerData) -> None:
    logging.info("Executing zip_file checks")

    checker_data.result.register_checker(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=zip_file_constants.CHECKER_ID,
        description="Check if zip_file properties of input file are properly set",
        summary="",
    )

    rule_list = [
        type_safe_zip_file.check_rule,  # Chk001
        type_safe_unzip_file.check_rule,  # Chk002
    ]

    for rule in rule_list:
        rule(checker_data=checker_data)

    logging.info(
        f"Issues found - {checker_data.result.get_checker_issue_count(checker_bundle_name=constants.BUNDLE_NAME, checker_id=zip_file_constants.CHECKER_ID)}"
    )

    checker_data.result.set_checker_status(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=zip_file_constants.CHECKER_ID,
        status=StatusType.COMPLETED,
    )
