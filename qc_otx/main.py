import argparse
import logging
from datetime import datetime
from lxml import etree

from qc_baselib import Configuration, Result
from qc_baselib.models.common import ParamType
from qc_otx import constants
from qc_otx.checks.core_checker import core_checker
from qc_otx.checks.data_type_checker import data_type_checker
from qc_otx.checks.zip_file_checker import zip_file_checker
from qc_otx.checks.state_machine_checker import state_machine_checker
from qc_otx.checks import utils, models

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)


def args_entrypoint() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="QC OTX Checker",
        description="This is a collection of scripts for checking validity of Open Test sequence eXchange (.otx) files.",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--default_config", action="store_true")
    group.add_argument("-c", "--config_path")

    return parser.parse_args()


def main():
    args = args_entrypoint()

    logging.info("Initializing checks")

    if args.default_config:
        raise RuntimeError("Not implemented.")
    else:
        config = Configuration()
        config.load_from_file(xml_file_path=args.config_path)

        result = Result()
        result.register_checker_bundle(
            name=constants.BUNDLE_NAME,
            build_date=datetime.today().strftime("%Y-%m-%d"),
            description="OTX checker bundle",
            version=constants.BUNDLE_VERSION,
            summary="",
        )
        result.set_result_version(version=constants.BUNDLE_VERSION)

        input_file_path = config.get_config_param("InputFile")
        input_param = ParamType(name="InputFile", value=input_file_path)
        result.get_checker_bundle_result(constants.BUNDLE_NAME).params.append(
            input_param
        )

        root = etree.parse(config.get_config_param("InputFile"))
        otx_schema_version = utils.get_standard_schema_version(root)

        checker_data = models.CheckerData(
            input_file_xml_root=root,
            config=config,
            result=result,
            schema_version=otx_schema_version,
        )
        # 1. Run basic checks
        core_checker.run_checks(checker_data)

        # 2. Run data type checks
        data_type_checker.run_checks(checker_data)

        # 3. Run zip file checks
        zip_file_checker.run_checks(checker_data)

        # 4. Run state machine checks
        state_machine_checker.run_checks(checker_data)

        result.write_to_file(
            config.get_checker_bundle_param(
                checker_bundle_name=constants.BUNDLE_NAME, param_name="resultFile"
            )
        )

        # Uncomment the follow line to generate the checker bundle documentation.
        # result.write_markdown_doc("checker_bundle_doc.md")

    logging.info("Done")


if __name__ == "__main__":
    main()
