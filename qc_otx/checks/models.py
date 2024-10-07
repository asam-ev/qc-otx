from dataclasses import dataclass
from lxml import etree
from typing import Union, List, Optional

from qc_baselib import Configuration, Result


@dataclass
class QueueNode:
    element: etree._ElementTree
    xpath: Optional[str]


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
    name: Optional[str]
    xml_element: etree._Element


@dataclass
class SMTransition:
    id: str
    name: Optional[str]
    target: Optional[str]
    xml_element: etree._Element


@dataclass
class SMState:
    id: str
    name: Optional[str]
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
