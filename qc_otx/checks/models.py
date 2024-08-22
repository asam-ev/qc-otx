from dataclasses import dataclass
from lxml import etree
from typing import Union, List

from qc_baselib import Configuration, Result


@dataclass
class QueueNode:
    element: etree._ElementTree
    xpath: Union[str, None]


@dataclass
class AttributeInfo:
    name: str
    value: str
    xpath: str


@dataclass
class CheckerData:
    input_file_xml_root: etree._ElementTree
    config: Configuration
    result: Result
    schema_version: str


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
