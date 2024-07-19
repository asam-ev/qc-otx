from lxml import etree
from typing import Union, List
from qc_otx.checks.models import QueueNode, AttributeInfo


def get_all_attributes(
    tree: etree._ElementTree, root: etree._Element
) -> List[AttributeInfo]:
    """Function to get all attributes in input xml document

    Args:
        tree (etree._ElementTree): the xml tree to analyse
        root (etree._Element): the root node of the xml to analyse

    Returns:
        _type_: _description_
    """
    attributes = []
    stack = [
        QueueNode(root, tree.getpath(root))
    ]  # Initialize stack with the root element

    while stack:
        current_node = stack.pop()
        current_element = current_node.element
        current_xpath = current_node.xpath

        # Process attributes of the current element
        for attr, value in current_element.attrib.items():
            attributes.append(AttributeInfo(attr, value, current_xpath))

        # Push children to the stack for further processing
        stack.extend(
            reversed(
                [QueueNode(x, tree.getpath(x)) for x in current_element.getchildren()]
            )
        )

    return attributes


def get_standard_schema_version(root: etree._ElementTree) -> Union[str, None]:
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

    # Compare each component until one is greater or they are equal
    for v1, v2 in zip(v1_components, v2_components):
        if v1 < v2:
            return -1
        elif v1 > v2:
            return 1

    # If all components are equal, compare based on length
    if len(v1_components) < len(v2_components):
        return -1
    elif len(v1_components) > len(v2_components):
        return 1
    else:
        return 0
