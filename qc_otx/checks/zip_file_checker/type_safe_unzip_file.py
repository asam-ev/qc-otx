import logging

from qc_baselib import IssueSeverity

from qc_otx import constants
from qc_otx.checks import models

from qc_otx.checks.zip_file_checker import zip_file_constants


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Rule ID: asam.net:otx:1.0.0:zip_file.chk_001.type_safe_unzip_file

    Description: In an UnZipFile action, the list described by ListTerm <extensions> shall
                 have a data type of <String>.
    Severity: ERROR

    Version range: [1.0.0, )

    Remark:
        None

    """
    logging.info("Executing type_safe_unzip_file check")

    issue_severity = IssueSeverity.ERROR

    rule_uid = checker_data.result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=zip_file_constants.CHECKER_ID,
        emanating_entity="asam.net",
        standard="otx",
        definition_setting="1.0.0",
        rule_full_name="zip_file.chk_001.type_safe_unzip_file",
    )

    tree = checker_data.input_file_xml_root
    root = tree.getroot()
    nsmap = {k: v for k, v in root.nsmap.items() if k is not None}

    if "xsi" not in nsmap or "zip" not in nsmap:
        return
    unzip_nodes = tree.xpath("//*[@xsi:type='zip:UnZipFile']", namespaces=nsmap)

    logging.debug(f"unzip_nodes {unzip_nodes}")

    for unzip_node in unzip_nodes:
        list_children = unzip_node.xpath(
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
                string_type_num += current_type == "String"

            has_issue = string_type_num == 0
            if has_issue:
                current_xpath = tree.getpath(current_list)
                issue_id = checker_data.result.register_issue(
                    checker_bundle_name=constants.BUNDLE_NAME,
                    checker_id=zip_file_constants.CHECKER_ID,
                    description="Issue flagging when the list in an UnzipFile action does not contain type String",
                    level=issue_severity,
                    rule_uid=rule_uid,
                )

                checker_data.result.add_xml_location(
                    checker_bundle_name=constants.BUNDLE_NAME,
                    checker_id=zip_file_constants.CHECKER_ID,
                    issue_id=issue_id,
                    xpath=current_xpath,
                    description=f"Unzip action does not contain any String type",
                )
