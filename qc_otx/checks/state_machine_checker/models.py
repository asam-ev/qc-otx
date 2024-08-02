from dataclasses import dataclass

from typing import List, Union
from lxml import etree


@dataclass
class SMTrigger:
    id: str
    name: Union[str, None]
    xml_element: etree._Element


@dataclass
class SMTransition:
    id: str
    name: Union[str, None]
    target: Union[str, None]
    xml_element: etree._Element


@dataclass
class SMState:
    id: str
    name: Union[str, None]
    is_initial: bool
    is_completed: bool
    transitions: List[SMTransition]
    target_state_ids: List[str]
    triggers: List[SMTrigger]
    xml_element: etree._Element


@dataclass
class StateMachine:
    id: str
    name: str
    states: List[SMState]
    xml_element: etree._Element
