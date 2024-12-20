# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import pytest
import test_utils
from qc_baselib import Result, IssueSeverity, StatusType
from qc_otx.checks import state_machine_checker


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
        result.get_checker_status(
            state_machine_checker.no_procedure_realization.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

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

    assert (
        result.get_checker_status(
            state_machine_checker.no_procedure_realization.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

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
        result.get_checker_status(
            state_machine_checker.mandatory_target_state.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

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

    assert (
        result.get_checker_status(
            state_machine_checker.mandatory_target_state.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    state_machine_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:state_machine.chk_002.mandatory_target_state"
    )
    assert len(state_machine_issues) == 1
    assert state_machine_issues[0].level == IssueSeverity.ERROR

    test_utils.cleanup_files()


def test_chk003_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/StateMachine_Chk003/"
    target_file_name = f"positive.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            state_machine_checker.no_target_state_for_completed_state.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:otx:1.0.0:state_machine.chk_003.no_target_state_for_completed_state"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_chk003_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/StateMachine_Chk003/"
    target_file_name = f"negative.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            state_machine_checker.no_target_state_for_completed_state.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    state_machine_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:state_machine.chk_003.no_target_state_for_completed_state"
    )
    assert len(state_machine_issues) == 1
    assert state_machine_issues[0].level == IssueSeverity.WARNING

    test_utils.cleanup_files()


def test_chk004_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/StateMachine_Chk004/"
    target_file_name = f"positive.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(state_machine_checker.mandatory_trigger.CHECKER_ID)
        == StatusType.COMPLETED
    )

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:otx:1.0.0:state_machine.chk_004.mandatory_trigger"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_chk004_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/StateMachine_Chk004/"
    target_file_name = f"negative.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(state_machine_checker.mandatory_trigger.CHECKER_ID)
        == StatusType.COMPLETED
    )

    state_machine_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:state_machine.chk_004.mandatory_trigger"
    )
    assert len(state_machine_issues) == 1
    assert state_machine_issues[0].level == IssueSeverity.ERROR

    test_utils.cleanup_files()


def test_chk005_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/StateMachine_Chk005/"
    target_file_name = f"positive.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(state_machine_checker.mandatory_transition.CHECKER_ID)
        == StatusType.COMPLETED
    )

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:otx:1.0.0:state_machine.chk_005.mandatory_transition"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_chk005_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/StateMachine_Chk005/"
    target_file_name = f"negative.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(state_machine_checker.mandatory_transition.CHECKER_ID)
        == StatusType.COMPLETED
    )

    state_machine_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:state_machine.chk_005.mandatory_transition"
    )
    assert len(state_machine_issues) == 1
    assert state_machine_issues[0].level == IssueSeverity.ERROR

    test_utils.cleanup_files()


def test_chk006_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/StateMachine_Chk006/"
    target_file_name = f"positive.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            state_machine_checker.distinguished_initial_and_completed_state.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:otx:1.0.0:state_machine.chk_006.distinguished_initial_and_completed_state"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_chk006_positive_no_completed(
    monkeypatch,
) -> None:
    base_path = "tests/data/StateMachine_Chk006/"
    target_file_name = f"positive_no_completed.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            state_machine_checker.distinguished_initial_and_completed_state.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:otx:1.0.0:state_machine.chk_006.distinguished_initial_and_completed_state"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_chk006_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/StateMachine_Chk006/"
    target_file_name = f"negative.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            state_machine_checker.distinguished_initial_and_completed_state.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    state_machine_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:state_machine.chk_006.distinguished_initial_and_completed_state"
    )
    assert len(state_machine_issues) == 1
    assert state_machine_issues[0].level == IssueSeverity.ERROR

    test_utils.cleanup_files()
