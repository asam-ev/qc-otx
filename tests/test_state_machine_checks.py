import os
import pytest
import test_utils
from qc_otx import constants
from qc_otx.checks.core_checker import core_constants
from qc_baselib import Result, IssueSeverity


def test_chk001_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/StateMachine_Chk001/"
    target_file_name = f"positive.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:otx:1.0.0:state_machine.chk_001.no_procedure_realization"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_chk001_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/StateMachine_Chk001/"
    target_file_name = f"negative.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    state_machine_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:state_machine.chk_001.no_procedure_realization"
    )
    assert len(state_machine_issues) == 1
    assert state_machine_issues[0].level == IssueSeverity.ERROR

    test_utils.cleanup_files()


def test_chk002_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/StateMachine_Chk002/"
    target_file_name = f"positive.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:otx:1.0.0:state_machine.chk_002.mandatory_target_state"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_chk002_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/StateMachine_Chk002/"
    target_file_name = f"negative.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    state_machine_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:state_machine.chk_002.mandatory_target_state"
    )
    assert len(state_machine_issues) == 1
    assert state_machine_issues[0].level == IssueSeverity.ERROR

    test_utils.cleanup_files()
