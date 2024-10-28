# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging

from qc_baselib import IssueSeverity

from qc_otx import constants
from qc_otx.checks import models


CHECKER_ID = "check_asam_otx_data_type_chk_008_correct_target_for_structure_element"
CHECKER_DESCRIPTION = "When referring to a structure element, an existing <element> name of the referenced StructureSignature shall be used."
CHECKER_PRECONDITIONS = set()
RULE_UID = "asam.net:otx:1.0.0:data_type.chk_008.correct_target_for_structure_element"


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Rule ID: asam.net:otx:1.0.0:data_type.chk_008.correct_target_for_structure_element

    Description: When referring to a structure element, an existing <element> name of the referenced StructureSignature shall be used.
    Severity: ERROR

    Version range: [1.0.0, )

    Remark:
        None

    """
    logging.info("Executing correct_target_for_structure_element check")

    tree = checker_data.input_file_xml_root

    # Use XPath to find all nodes procedure
    signature_nodes = tree.xpath("//signature")

    signature_dict = dict()
    for signature in signature_nodes:

        field_list = []
        fields = signature.xpath(".//*[local-name()='element']")
        for field in fields:
            field_list.append(field.get("name"))

        signature_dict[signature.get("name")] = field_list

    logging.debug(f"signature_dict {signature_dict}")

    variable_nodes = tree.xpath("//variable")
    variable_type_dict = dict()
    for variable in variable_nodes:
        variable_type = variable.xpath(".//*[@structureType]")
        if len(variable_type) == 0:
            continue
        variable_type_dict[variable.get("name")] = variable_type[0].get("structureType")

    logging.debug(f"variable_type_dict {variable_type_dict}")

    for structure_name in variable_type_dict.keys():
        logging.debug(f"structure_name: {structure_name}")

        structure_instances = tree.xpath(f"//*[@name='{structure_name}']")

        logging.debug(f"structure_instances: {structure_instances}")

        for structure_instance in structure_instances:
            structure_accesses = structure_instance.xpath(".//*[@value]")

            for structure_access in structure_accesses:
                current_value = structure_access.get("value")
                if current_value is None:
                    continue
                logging.debug(f"current_value: {current_value}")

                current_variable_type = variable_type_dict[structure_name]
                logging.debug(f"current_variable_type: {current_variable_type}")

                has_issue = current_value not in signature_dict[current_variable_type]

                if has_issue:
                    current_xpath = tree.getpath(structure_instance)
                    issue_id = checker_data.result.register_issue(
                        checker_bundle_name=constants.BUNDLE_NAME,
                        checker_id=CHECKER_ID,
                        description="Invalid names used while accessing structure element",
                        level=IssueSeverity.ERROR,
                        rule_uid=RULE_UID,
                    )

                    checker_data.result.add_xml_location(
                        checker_bundle_name=constants.BUNDLE_NAME,
                        checker_id=CHECKER_ID,
                        issue_id=issue_id,
                        xpath=current_xpath,
                        description=f"Accessing {current_value} for variable {structure_name} of type {current_variable_type} is not present in type definition",
                    )
