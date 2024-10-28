# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging

from qc_baselib import IssueSeverity

from qc_otx import constants
from qc_otx.checks import models


CHECKER_ID = "check_asam_otx_data_type_chk_001_accessing_structure_elements"
CHECKER_DESCRIPTION = "Accessing structure elements is only allowed via StepByName using matching string literals."
CHECKER_PRECONDITIONS = set()
RULE_UID = "asam.net:otx:1.0.0:data_type.chk_001.accessing_structure_elements"


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Rule ID: asam.net:otx:1.0.0:data_type.chk_001.accessing_structure_elements

    Description: Accessing structure elements is only allowed via StepByName using matching string literals.
    Severity: ERROR

    Version range: [1.0.0, )

    Remark:
        None

    """
    logging.info("Executing accessing_structure_elements check")

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

    step_by_name_nodes = tree.xpath("//stepByName")

    for step_by_name_node in step_by_name_nodes:
        logging.debug(f"step_by_name_node: {step_by_name_node}")
        current_value = step_by_name_node.get("value")

        current_result = step_by_name_node.getparent().getparent()
        current_result_name = current_result.get("name")
        if current_result_name is None:
            continue

        logging.debug(f"current_value {current_value}")
        if current_result_name not in variable_type_dict:
            continue

        current_variable_type = variable_type_dict[current_result_name]
        logging.debug(f"current_variable_type {current_variable_type}")

        if current_variable_type not in signature_dict:
            continue

        has_issue = current_value not in signature_dict[current_variable_type]

        if has_issue:
            current_xpath = tree.getelementpath(step_by_name_node)
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                description="StepByName node accessing invalid fields",
                level=IssueSeverity.ERROR,
                rule_uid=RULE_UID,
            )

            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                issue_id=issue_id,
                xpath=current_xpath,
                description=f"Accessing {current_value} for variable {current_result_name} of type {current_variable_type} is not present in type definition",
            )
