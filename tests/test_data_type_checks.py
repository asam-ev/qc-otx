import os
import pytest
import test_utils
from qc_otx import constants
from qc_otx.checks.core_checker import core_constants
from qc_baselib import Result, IssueSeverity


def test_chk001_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/DataType_Chk001/"
    target_file_name = f"positive.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:otx:1.0.0:data_type.chk_001.accessing_structure_elements"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_chk001_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/DataType_Chk001/"
    target_file_name = f"negative.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    data_type_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:data_type.chk_001.accessing_structure_elements"
    )
    assert len(data_type_issues) == 1
    assert data_type_issues[0].level == IssueSeverity.ERROR

    test_utils.cleanup_files()


def test_chk008_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/DataType_Chk008/"
    target_file_name = f"positive.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:otx:1.0.0:data_type.chk_008.correct_target_for_structure_element"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_chk008_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/DataType_Chk008/"
    target_file_name = f"negative.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    data_type_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:data_type.chk_008.correct_target_for_structure_element"
    )
    assert len(data_type_issues) == 2
    assert data_type_issues[0].level == IssueSeverity.ERROR
    assert data_type_issues[1].level == IssueSeverity.ERROR
    assert "MainName" in data_type_issues[0].locations[0].description
    assert "DateOfBirth" in data_type_issues[1].locations[0].description

    test_utils.cleanup_files()
