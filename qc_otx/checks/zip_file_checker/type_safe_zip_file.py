import logging

from qc_baselib import IssueSeverity

from qc_otx import constants
from qc_otx.checks import models

from qc_otx.checks.zip_file_checker import zip_file_constants


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Rule ID: asam.net:otx:1.0.0:zip_file.chk_002.type_safe_zip_file

    Description: In a ZipFile action, the list described by ListTerm <extensions> shall
                 have a data type of <String>.
    Severity: ERROR

    Version range: [1.0.0, )

    Remark:
        None

    """
    logging.info("Executing correct_target_for_structure_element check")

    issue_severity = IssueSeverity.ERROR

    rule_uid = checker_data.result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=zip_file_constants.CHECKER_ID,
        emanating_entity="asam.net",
        standard="otx",
        definition_setting="1.0.0",
        rule_full_name="zip_file.chk_002.type_safe_zip_file",
    )

    tree = checker_data.input_file_xml_root
    root = tree.getroot()
    nsmap = {k: v for k, v in root.nsmap.items() if k is not None}

    if "xsi" not in nsmap or "zip" not in nsmap:
        return
    zip_nodes = tree.xpath("//*[@xsi:type='zip:ZipFile']", namespaces=nsmap)

    logging.debug(f"zip_nodes {zip_nodes}")

    for zip_node in zip_nodes:
        list_children = zip_node.xpath(
            ".//*[@xsi:type='ListLiteral']", namespaces=nsmap
        )
        logging.debug(f"list_children : {list_children}")
        if list_children is None or len(list_children) == 0:
            continue

        for current_list in list_children:
            logging.debug(f"current_list : {current_list}")

            type_children = current_list.xpath(".//*[@xsi:type]", namespaces=nsmap)

            logging.debug(f"type_children : {type_children}")
            if type_children is None:
                continue

            string_type_num = 0

            for type_child in type_children:
                xsi_ns = "{" + nsmap["xsi"] + "}"
                current_type = type_child.get(f"{xsi_ns}type")
                logging.debug(f"type_child : {type_child.attrib}")
                if current_type is None:
                    continue
                logging.debug(f"current_type : {current_type}")
                if current_type == "String":
                    string_type_num += 1

            has_issue = string_type_num == 0
            if has_issue:
                current_xpath = tree.getelementpath(current_list)
                issue_id = checker_data.result.register_issue(
                    checker_bundle_name=constants.BUNDLE_NAME,
                    checker_id=zip_file_constants.CHECKER_ID,
                    description="Issue flagging when the list in an ZipFile action does not contain type String",
                    level=issue_severity,
                    rule_uid=rule_uid,
                )

                checker_data.result.add_xml_location(
                    checker_bundle_name=constants.BUNDLE_NAME,
                    checker_id=zip_file_constants.CHECKER_ID,
                    issue_id=issue_id,
                    xpath=current_xpath,
                    description=f"Zip action does not contain any String type",
                )