# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import pytest
import test_utils
from qc_baselib import Result, IssueSeverity, StatusType
from qc_otx.checks import core_checker


def test_chk001_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk001/"
    target_file_name = f"Core_Chk001_positive.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            core_checker.document_name_matches_filename.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:otx:1.0.0:core.chk_001.document_name_matches_filename"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_chk001_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk001/"
    target_file_name = f"Core_Chk001_negative.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            core_checker.document_name_matches_filename.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_001.document_name_matches_filename"
    )
    assert len(core_issues) == 1
    assert core_issues[0].level == IssueSeverity.WARNING

    test_utils.cleanup_files()


def test_chk002_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk002/positive/package1"
    target_file_name = f"Core_Chk002_positive.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            core_checker.document_name_package_uniqueness.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_002.document_name_package_uniqueness"
    )
    assert len(core_issues) == 0
    test_utils.cleanup_files()


def test_chk002_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk002/negative/package1"
    target_file_name = f"Core_Chk002_negative.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            core_checker.document_name_package_uniqueness.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_002.document_name_package_uniqueness"
    )
    assert len(core_issues) == 1
    assert core_issues[0].level == IssueSeverity.ERROR

    test_utils.cleanup_files()


def test_chk003_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk003"
    target_file_name = f"Core_Chk003_positive.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(core_checker.no_dead_import_links.CHECKER_ID)
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_003.no_dead_import_links"
    )
    assert len(core_issues) == 0
    test_utils.cleanup_files()


def test_chk003_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk003"
    target_file_name = f"Core_Chk003_negative.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(core_checker.no_dead_import_links.CHECKER_ID)
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_003.no_dead_import_links"
    )
    assert len(core_issues) == 1
    assert core_issues[0].level == IssueSeverity.ERROR

    test_utils.cleanup_files()


def test_chk004_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk004"
    target_file_name = f"Core_Chk004_positive.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(core_checker.no_unused_imports.CHECKER_ID)
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_004.no_unused_imports"
    )
    assert len(core_issues) == 0
    test_utils.cleanup_files()


def test_chk004_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk004"
    target_file_name = f"Core_Chk004_negative.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(core_checker.no_unused_imports.CHECKER_ID)
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_004.no_unused_imports"
    )
    assert len(core_issues) == 1
    assert core_issues[0].level == IssueSeverity.WARNING

    test_utils.cleanup_files()


def test_chk005_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk005"
    target_file_name = f"Core_Chk005_positive.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            core_checker.no_use_of_undefined_import_prefixes.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_005.no_use_of_undefined_import_prefixes"
    )
    assert len(core_issues) == 0
    test_utils.cleanup_files()


def test_chk005_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk005"
    target_file_name = f"Core_Chk005_negative.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            core_checker.no_use_of_undefined_import_prefixes.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_005.no_use_of_undefined_import_prefixes"
    )
    assert len(core_issues) == 1
    assert core_issues[0].level == IssueSeverity.ERROR
    assert "foo" in core_issues[0].locations[0].description

    test_utils.cleanup_files()


def test_chk006_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk006"
    target_file_name = f"Core_Chk006_positive.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            core_checker.match_of_imported_document_data_model_version.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_006.match_of_imported_document_data_model_version"
    )
    assert len(core_issues) == 0
    test_utils.cleanup_files()


def test_chk006_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk006"
    target_file_name = f"Core_Chk006_negative.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            core_checker.match_of_imported_document_data_model_version.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_006.match_of_imported_document_data_model_version"
    )
    assert len(core_issues) == 1
    assert core_issues[0].level == IssueSeverity.ERROR
    assert "1.0.0" in core_issues[0].locations[0].description

    test_utils.cleanup_files()


def test_chk007_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk007"
    target_file_name = f"Core_Chk007_positive.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            core_checker.have_specification_if_no_realisation_exists.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_007.have_specification_if_no_realisation_exists"
    )
    assert len(core_issues) == 0
    test_utils.cleanup_files()


def test_chk007_positive_no_specification(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk007"
    target_file_name = f"Core_Chk007_positive_no_specification.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            core_checker.have_specification_if_no_realisation_exists.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_007.have_specification_if_no_realisation_exists"
    )
    assert len(core_issues) == 0
    test_utils.cleanup_files()


def test_chk007_positive_no_realisation(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk007"
    target_file_name = f"Core_Chk007_positive_no_realisation.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            core_checker.have_specification_if_no_realisation_exists.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_007.have_specification_if_no_realisation_exists"
    )
    assert len(core_issues) == 0
    test_utils.cleanup_files()


def test_chk007_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk007"
    target_file_name = f"Core_Chk007_negative.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            core_checker.have_specification_if_no_realisation_exists.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_007.have_specification_if_no_realisation_exists"
    )
    assert len(core_issues) == 1
    assert core_issues[0].level == IssueSeverity.WARNING

    test_utils.cleanup_files()


def test_chk007_negative_no_specification(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk007"
    target_file_name = f"Core_Chk007_negative_no_specification.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            core_checker.have_specification_if_no_realisation_exists.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_007.have_specification_if_no_realisation_exists"
    )
    assert len(core_issues) == 1
    assert core_issues[0].level == IssueSeverity.WARNING

    test_utils.cleanup_files()


def test_chk007_negative_empty_string(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk007"
    target_file_name = f"Core_Chk007_negative_empty_string.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            core_checker.have_specification_if_no_realisation_exists.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_007.have_specification_if_no_realisation_exists"
    )
    assert len(core_issues) == 1
    assert core_issues[0].level == IssueSeverity.WARNING

    test_utils.cleanup_files()


def test_chk008_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk008"
    target_file_name = f"Core_Chk008_positive.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(core_checker.public_main_procedure.CHECKER_ID)
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_008.public_main_procedure"
    )
    assert len(core_issues) == 0
    test_utils.cleanup_files()


def test_chk008_positive_two_mains(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk008"
    target_file_name = f"Core_Chk008_positive_two_mains.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(core_checker.public_main_procedure.CHECKER_ID)
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_008.public_main_procedure"
    )
    assert len(core_issues) == 0
    test_utils.cleanup_files()


def test_chk008_positive_no_main(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk008"
    target_file_name = f"Core_Chk008_positive_no_main.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(core_checker.public_main_procedure.CHECKER_ID)
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_008.public_main_procedure"
    )
    assert len(core_issues) == 0
    test_utils.cleanup_files()


def test_chk008_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk008"
    target_file_name = f"Core_Chk008_negative.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(core_checker.public_main_procedure.CHECKER_ID)
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_008.public_main_procedure"
    )
    assert len(core_issues) == 1
    assert core_issues[0].level == IssueSeverity.ERROR

    test_utils.cleanup_files()


def test_chk008_negative_two_mains(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk008"
    target_file_name = f"Core_Chk008_negative_two_mains.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(core_checker.public_main_procedure.CHECKER_ID)
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_008.public_main_procedure"
    )
    assert len(core_issues) == 1
    assert core_issues[0].level == IssueSeverity.ERROR

    test_utils.cleanup_files()


def test_chk008_negative_no_visibility(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk008"
    target_file_name = f"Core_Chk008_negative_no_visibility.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(core_checker.public_main_procedure.CHECKER_ID)
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_008.public_main_procedure"
    )
    assert len(core_issues) == 1
    assert core_issues[0].level == IssueSeverity.ERROR

    test_utils.cleanup_files()


def test_chk009_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk009"
    target_file_name = f"Core_Chk009_positive.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            core_checker.mandatory_constant_initialization.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_009.mandatory_constant_initialization"
    )
    assert len(core_issues) == 0
    test_utils.cleanup_files()


def test_chk009_positive_multiple(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk009"
    target_file_name = f"Core_Chk009_positive_multiple.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            core_checker.mandatory_constant_initialization.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_009.mandatory_constant_initialization"
    )
    assert len(core_issues) == 0
    test_utils.cleanup_files()


def test_chk009_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk009"
    target_file_name = f"Core_Chk009_negative.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            core_checker.mandatory_constant_initialization.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_009.mandatory_constant_initialization"
    )
    assert len(core_issues) == 1
    assert core_issues[0].level == IssueSeverity.ERROR

    test_utils.cleanup_files()


def test_chk009_negative_multiple(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk009"
    target_file_name = f"Core_Chk009_negative_multiple.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            core_checker.mandatory_constant_initialization.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_009.mandatory_constant_initialization"
    )
    assert len(core_issues) == 1
    assert core_issues[0].level == IssueSeverity.ERROR

    test_utils.cleanup_files()


def test_chk009_negative_multiple_errors(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk009"
    target_file_name = f"Core_Chk009_negative_multiple_errors.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            core_checker.mandatory_constant_initialization.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_009.mandatory_constant_initialization"
    )
    assert len(core_issues) == 2
    assert core_issues[0].level == IssueSeverity.ERROR
    assert core_issues[1].level == IssueSeverity.ERROR

    test_utils.cleanup_files()


def test_chk010_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk010"
    target_file_name = f"Core_Chk010_positive.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(core_checker.unique_node_names.CHECKER_ID)
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_010.unique_node_names"
    )
    assert len(core_issues) == 0
    test_utils.cleanup_files()


def test_chk010_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/Core_Chk010"
    target_file_name = f"Core_Chk010_negative.otx"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(core_checker.unique_node_names.CHECKER_ID)
        == StatusType.COMPLETED
    )

    core_issues = result.get_issues_by_rule_uid(
        "asam.net:otx:1.0.0:core.chk_010.unique_node_names"
    )
    assert len(core_issues) == 3

    assert "Procedure main" in core_issues[0].locations[0].description
    assert "Procedure main" in core_issues[1].locations[0].description
    assert "Procedure computeDelta" in core_issues[2].locations[0].description

    assert core_issues[0].level == IssueSeverity.WARNING
    assert core_issues[1].level == IssueSeverity.WARNING
    assert core_issues[2].level == IssueSeverity.WARNING

    test_utils.cleanup_files()
