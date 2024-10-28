# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import argparse
import logging
from datetime import datetime
from lxml import etree
import types

from qc_baselib import Configuration, Result, StatusType
from qc_baselib.models.common import ParamType
from qc_otx import constants
from qc_otx.checks import core_checker
from qc_otx.checks import data_type_checker
from qc_otx.checks import zip_file_checker
from qc_otx.checks import state_machine_checker
from qc_otx.checks import utils, models

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)


def args_entrypoint() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="QC OTX Checker",
        description="This is a collection of scripts for checking validity of Open Test sequence eXchange (.otx) files.",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-c", "--config_path")

    parser.add_argument("-g", "--generate_markdown", action="store_true")

    return parser.parse_args()


def execute_checker(
    checker: types.ModuleType,
    checker_data: models.CheckerData,
    required_definition_setting: bool = True,
) -> None:
    # Register checker
    checker_data.result.register_checker(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=checker.CHECKER_ID,
        description=checker.CHECKER_DESCRIPTION,
    )

    # Register rule uid
    checker_data.result.register_rule_by_uid(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=checker.CHECKER_ID,
        rule_uid=checker.RULE_UID,
    )

    # Check preconditions. If not satisfied then set status as SKIPPED and return
    if not checker_data.result.all_checkers_completed_without_issue(
        checker.CHECKER_PRECONDITIONS
    ):
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=checker.CHECKER_ID,
            status=StatusType.SKIPPED,
        )

        checker_data.result.add_checker_summary(
            constants.BUNDLE_NAME,
            checker.CHECKER_ID,
            "Preconditions are not satisfied. Skip the check.",
        )

        return

    # Checker definition setting. If not satisfied then set status as SKIPPED and return
    if required_definition_setting:
        schema_version = checker_data.schema_version
        splitted_rule_uid = checker.RULE_UID.split(":")
        if len(splitted_rule_uid) != 4:
            raise RuntimeError(f"Invalid rule uid: {checker.RULE_UID}")

        definition_setting = splitted_rule_uid[2]
        if (
            schema_version is None
            or utils.compare_versions(schema_version, definition_setting) < 0
        ):
            checker_data.result.set_checker_status(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=checker.CHECKER_ID,
                status=StatusType.SKIPPED,
            )

            checker_data.result.add_checker_summary(
                constants.BUNDLE_NAME,
                checker.CHECKER_ID,
                f"Version {schema_version} is lower than definition setting {definition_setting}. Skip the check.",
            )

            return

    # Execute checker
    try:
        checker.check_rule(checker_data)

        # If checker is not explicitly set as SKIPPED, then set it as COMPLETED
        if (
            checker_data.result.get_checker_status(checker.CHECKER_ID)
            != StatusType.SKIPPED
        ):
            checker_data.result.set_checker_status(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=checker.CHECKER_ID,
                status=StatusType.COMPLETED,
            )
    except Exception as e:
        # If any exception occurs during the check, set the status as ERROR
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=checker.CHECKER_ID,
            status=StatusType.ERROR,
        )

        checker_data.result.add_checker_summary(
            constants.BUNDLE_NAME, checker.CHECKER_ID, f"Error: {str(e)}."
        )

        logging.exception(f"An error occurred in {checker.CHECKER_ID}.")


def run_checks(config: Configuration, result: Result) -> None:
    root = etree.parse(config.get_config_param("InputFile"))
    otx_schema_version = utils.get_standard_schema_version(root)

    checker_data = models.CheckerData(
        input_file_xml_root=root,
        config=config,
        result=result,
        schema_version=otx_schema_version,
    )

    # 1. Run basic checks
    # Chk001
    execute_checker(core_checker.document_name_matches_filename, checker_data)
    # Chk002
    execute_checker(core_checker.document_name_package_uniqueness, checker_data)
    # Chk003
    execute_checker(core_checker.no_dead_import_links, checker_data)
    # Chk004
    execute_checker(core_checker.no_unused_imports, checker_data)
    # Chk005
    execute_checker(core_checker.no_use_of_undefined_import_prefixes, checker_data)
    # Chk006
    execute_checker(
        core_checker.match_of_imported_document_data_model_version, checker_data
    )
    # Chk007
    execute_checker(
        core_checker.have_specification_if_no_realisation_exists, checker_data
    )
    # Chk008
    execute_checker(core_checker.public_main_procedure, checker_data)
    # Chk009
    execute_checker(core_checker.mandatory_constant_initialization, checker_data)
    # Chk010
    execute_checker(core_checker.unique_node_names, checker_data)

    # 2. Run data type checks
    # Chk001
    execute_checker(data_type_checker.accessing_structure_elements, checker_data)
    # Chk008
    execute_checker(
        data_type_checker.correct_target_for_structure_element, checker_data
    )

    # 3. Run zip file checks
    # Chk001
    execute_checker(zip_file_checker.type_safe_zip_file, checker_data)
    # Chk002
    execute_checker(zip_file_checker.type_safe_unzip_file, checker_data)

    # 4. Run state machine checks
    # Chk001
    execute_checker(state_machine_checker.no_procedure_realization, checker_data)
    # Chk002
    execute_checker(state_machine_checker.mandatory_target_state, checker_data)
    # Chk003
    execute_checker(
        state_machine_checker.no_target_state_for_completed_state, checker_data
    )
    # Chk004
    execute_checker(state_machine_checker.mandatory_transition, checker_data)
    # Chk005
    execute_checker(state_machine_checker.mandatory_trigger, checker_data)
    # Chk006
    execute_checker(
        state_machine_checker.distinguished_initial_and_completed_state, checker_data
    )


def main():
    args = args_entrypoint()

    logging.info("Initializing checks")

    config = Configuration()
    config.load_from_file(xml_file_path=args.config_path)

    result = Result()
    result.register_checker_bundle(
        name=constants.BUNDLE_NAME,
        description="OTX checker bundle",
        version=constants.BUNDLE_VERSION,
        summary="",
    )
    result.set_result_version(version=constants.BUNDLE_VERSION)

    run_checks(config, result)

    result.copy_param_from_config(config)

    result.write_to_file(
        config.get_checker_bundle_param(
            checker_bundle_name=constants.BUNDLE_NAME, param_name="resultFile"
        ),
        generate_summary=True,
    )

    if args.generate_markdown:
        result.write_markdown_doc("generated_checker_bundle_doc.md")

    logging.info("Done")


if __name__ == "__main__":
    main()
