# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import pytest
import test_utils
from qc_baselib import Result, IssueSeverity, StatusType
from qc_otx.checks import zip_file_checker


def test_chk001_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/ZipFile_Chk001/"
    target_file_name = f"positive.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(zip_file_checker.type_safe_unzip_file.CHECKER_ID)
        == StatusType.COMPLETED
    )

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:otx:1.0.0:zip_file.chk_001.type_safe_unzip_file"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_chk001_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/ZipFile_Chk001/"
    target_file_name = f"negative.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(zip_file_checker.type_safe_unzip_file.CHECKER_ID)
        == StatusType.COMPLETED
    )

    zip_file_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:zip_file.chk_001.type_safe_unzip_file"
    )
    assert len(zip_file_issues) == 1
    assert zip_file_issues[0].level == IssueSeverity.ERROR

    test_utils.cleanup_files()


def test_chk002_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/ZipFile_Chk002/"
    target_file_name = f"positive.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(zip_file_checker.type_safe_zip_file.CHECKER_ID)
        == StatusType.COMPLETED
    )

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:otx:1.0.0:zip_file.chk_002.type_safe_zip_file"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_chk002_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/ZipFile_Chk002/"
    target_file_name = f"negative.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(zip_file_checker.type_safe_zip_file.CHECKER_ID)
        == StatusType.COMPLETED
    )

    zip_file_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:zip_file.chk_002.type_safe_zip_file"
    )
    assert len(zip_file_issues) == 1
    assert zip_file_issues[0].level == IssueSeverity.ERROR

    test_utils.cleanup_files()
