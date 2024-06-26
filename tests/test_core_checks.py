import os
import pytest
import test_utils
from qc_otx import constants
from qc_otx.checks.core_checker import core_constants
from qc_baselib import Result, IssueSeverity


def test_valid_xml_document_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/document_name_matches_filename/"
    target_file_name = f"PositiveRootExample.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:otx:1.0.0:core.document_name_matches_filename"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_valid_xml_document_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/document_name_matches_filename/"
    target_file_name = f"NegativeRootExample.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.document_name_matches_filename"
    )
    assert len(core_issues) == 1
    assert core_issues[0].level == IssueSeverity.ERROR

    test_utils.cleanup_files()
