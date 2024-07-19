from dataclasses import dataclass
from lxml import etree
from typing import Union

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
