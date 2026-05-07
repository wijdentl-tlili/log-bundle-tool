import argparse
import datetime
from pathlib import Path

from collector.collector import collect_logs
from bundler.zipper import create_zip

from utils.logger import setup_logger

from analyzer.metadata import get_file_metadata
from analyzer.ioc_scanner import scan_file
from analyzer.sensitive_detector import detect_sensitive_data
from analyzer.redactor import redact_content

from reporting.json_report import write_json_report
from reporting.html_report import generate_html_report


def main():

    parser = argparse.ArgumentParser(
        description="Log Bundle Tool"
    )

    parser.add_argument(
        "command",
        choices=["collect"],
        help="Command to execute"
    )

    parser.add_argument(
        "--source",
        required=True,
        help="Directory containing logs"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "--extensions",
        nargs="+",
        default=[".log", ".txt"],
        help="Extensions to collect"
    )

    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="Disable recursive scanning"
    )

    args = parser.parse_args()

    logger = setup_logger(args.verbose)

    if args.command == "collect":

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        bundle_dir = Path(f"output/bundle_{timestamp}")

        logger.info(f"Collecting logs from: {args.source}")

        collected_files = collect_logs(
            args.source,
            bundle_dir,
            args.extensions,
            recursive=not args.no_recursive
        )

        logger.info(f"Collected {len(collected_files)} files")

        metadata_results = []
        ioc_results = []
        sensitive_results = []

        for file in collected_files:

            logger.info(f"Analyzing: {file.name}")

            # Metadata
            metadata = get_file_metadata(file)
            metadata_results.append(metadata)

            # Read file content
            with open(file, "r", errors="ignore") as f:
                content = f.read()

            # IOC Scan
            iocs = scan_file(file)

            if iocs:
                ioc_results.append({
                    "file": file.name,
                    "findings": iocs
                })

            # Sensitive Data Detection
            sensitive = detect_sensitive_data(content)

            if sensitive:
                sensitive_results.append({
                    "file": file.name,
                    "findings": sensitive
                })

            # Redaction
            redacted_content = redact_content(content)

            redacted_path = bundle_dir / f"redacted_{file.name}"

            with open(redacted_path, "w", encoding="utf-8") as redacted_file:
                redacted_file.write(redacted_content)

        # JSON Report
        json_report_path = bundle_dir / "forensic_report.json"

        write_json_report(
            metadata_results,
            ioc_results,
            sensitive_results,
            json_report_path
        )

        # HTML Report
        html_report_path = bundle_dir / "forensic_report.html"

        generate_html_report(
            metadata_results,
            ioc_results,
            sensitive_results,
            html_report_path
        )

        # ZIP Bundle
        zip_name = f"output/log_bundle_{timestamp}.zip"

        create_zip(bundle_dir, zip_name)

        logger.info(f"Bundle created: {zip_name}")


if __name__ == "__main__":
    main()