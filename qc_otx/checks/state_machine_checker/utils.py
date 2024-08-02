from qc_otx.checks.state_machine_checker import models as state_machine_models

from lxml import etree
import logging
from typing import List, Dict


def get_state_machine(
    input_node: etree._Element, nsmap: Dict
) -> state_machine_models.StateMachine:

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
                state_machine_models.SMTransition(
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
            triggers.append(
                state_machine_models.SMTrigger(current_id, current_name, state_trigger)
            )

        current_sm_state = state_machine_models.SMState(
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

    state_machine_object = state_machine_models.StateMachine(
        smp_id, smp_name, sm_state_list, input_node
    )

    return state_machine_object
