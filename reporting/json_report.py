import json


def write_json_report(
    metadata_results,
    ioc_results,
    sensitive_results,
    entropy_results,
    output_file
):

    report = {

        "metadata": metadata_results,

        "ioc_findings": ioc_results,

        "sensitive_data_findings": sensitive_results,
        "entropy_results": entropy_results
    }

    with open(output_file, "w", encoding="utf-8") as f:

        json.dump(
            report,
            f,
            indent=4
        )