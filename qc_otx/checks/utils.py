# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

from lxml import etree
from typing import Optional, List, Dict
from qc_otx.checks import models
import re
import logging


def get_data_model_version(root: etree._Element):
    """Get data model version from input root. The data model version is the number indicated as
    in the attribute  xmlns as "http://iso.org/OTX/<version >"

    Args:
        root (etree._Element): the xml root to get data model version

    Returns:
        _type_: the read data model version. None if attribute xmlns is not found
    """
    xmlns_version = None
    xmlns_regex = "http://iso.org/OTX/*"
    for key, value in root.nsmap.items():
        if re.match(xmlns_regex, value):
            xmlns_version = value.replace(xmlns_regex[:-1], "")
            break
    return xmlns_version


def get_all_attributes(
    tree: etree._ElementTree, root: etree._Element
) -> List[models.AttributeInfo]:
    """Function to get all attributes in input xml document

    Args:
        tree (etree._ElementTree): the xml tree to analyse
        root (etree._Element): the root node of the xml to analyse

    Returns:
        _type_: _description_
    """
    attributes = []
    stack = [
        models.QueueNode(root, tree.getpath(root))
    ]  # Initialize stack with the root element

    while stack:
        current_node = stack.pop()
        current_element = current_node.element
        current_xpath = current_node.xpath

        # Process attributes of the current element
        for attr, value in current_element.attrib.items():
            attributes.append(models.AttributeInfo(attr, value, current_xpath))

        # Push children to the stack for further processing
        stack.extend(
            reversed(
                [
                    models.QueueNode(x, tree.getpath(x))
                    for x in current_element.getchildren()
                ]
            )
        )

    return attributes


def get_standard_schema_version(root: etree._ElementTree) -> Optional[str]:
    root_attrib = root.getroot().attrib
    return root_attrib["version"]


def compare_versions(version1: str, version2: str) -> int:
    """Compare two version strings like "X.x.x"
        This function is to avoid comparing version string basing on lexicographical order
        that could cause problem. E.g.
        1.10.0 > 1.2.0 but lexicographical comparison of string would return the opposite

    Args:
        version1 (str): First string to compare
        version2 (str): Second string to compare

    Returns:
        int: 1 if version1 is bigger than version2. 0 if the version are the same. -1 otherwise
    """
    v1_components = list(map(int, version1.split(".")))
    v2_components = list(map(int, version2.split(".")))

    max_length = max(len(v1_components), len(v2_components))

    # extend the length of the shorter components with zero
    if len(v1_components) < max_length:
        for _ in range(len(v1_components), max_length):
            v1_components.append(0)

    if len(v2_components) < max_length:
        for _ in range(len(v2_components), max_length):
            v2_components.append(0)

    # Compare each component until one is greater or they are equal
    for v1, v2 in zip(v1_components, v2_components):
        if v1 < v2:
            return -1
        elif v1 > v2:
            return 1

    return 0


def get_state_machine(input_node: etree._Element, nsmap: Dict) -> models.StateMachine:

    smp_id = input_node.get("id")
    smp_name = input_node.get("name")

    smp_realisation = input_node.xpath("./smp:realisation", namespaces=nsmap)
    logging.debug(f"smp_realisation: {smp_realisation}")

    if smp_realisation is None or len(smp_realisation) != 1:
        logging.error(
            f"Invalid realisation found in current state machine procedure named {smp_name} with id {smp_id}"
        )
        return

    smp_realisation = smp_realisation[0]
    initial_state_name = smp_realisation.get("initialState")
    completed_state_name = smp_realisation.get("completedState")
    logging.debug(f"initial_state_name: {initial_state_name}")
    logging.debug(f"completed_state_name: {completed_state_name}")

    smp_states = smp_realisation.xpath("./smp:states/smp:state", namespaces=nsmap)

    logging.debug(f"smp_states: {smp_states}")

    sm_state_list = []

    for smp_state in smp_states:
        state_name = smp_state.get("name")
        state_id = smp_state.get("id")
        is_initial = state_name == initial_state_name
        is_completed = state_name == completed_state_name

        state_transitions = smp_state.xpath(
            "./smp:transitions/smp:transition", namespaces=nsmap
        )
        transitions = []
        for state_transition in state_transitions:
            current_id = state_transition.get("id")
            current_name = state_transition.get("name")
            current_target = state_transition.get("target")
            transitions.append(
                models.SMTransition(
                    current_id, current_name, current_target, state_transition
                )
            )

        target_state_ids = []

        for transition in transitions:
            if transition.target is not None:
                target_state_ids.append(transition.id)

        logging.debug(f"transitions: {transitions}")

        state_triggers = smp_state.xpath("./smp:triggers/smp:trigger", namespaces=nsmap)
        logging.debug(f"state_triggers: {state_triggers}")

        triggers = []
        for state_trigger in state_triggers:
            logging.debug(f"state_trigger: {state_trigger}")
            current_id = state_trigger.get("id")
            current_name = state_trigger.get("name")
            triggers.append(models.SMTrigger(current_id, current_name, state_trigger))

        current_sm_state = models.SMState(
            state_id,
            state_name,
            is_initial,
            is_completed,
            transitions,
            target_state_ids,
            triggers,
            smp_state,
        )

        sm_state_list.append(current_sm_state)

    state_machine_object = models.StateMachine(
        smp_id, smp_name, sm_state_list, input_node
    )

    return state_machine_object


def get_state_machine_procedures(tree: etree._ElementTree, nsmap: Dict) -> List:
    return tree.xpath("//*[@xsi:type='smp:StateMachineProcedure']", namespaces=nsmap)


def get_namespace_map(tree: etree._ElementTree) -> Dict:
    root = tree.getroot()
    return {k: v for k, v in root.nsmap.items() if k is not None}
