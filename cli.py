import argparse
import datetime
from pathlib import Path

from collector.collector import collect_logs
from bundler.zipper import create_zip
from utils.logger import setup_logger

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

    args = parser.parse_args()
    logger = setup_logger(args.verbose)


    if args.command == "collect":

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        bundle_dir = Path(f"output/bundle_{timestamp}")

        logger.info(f"[+] Collecting logs from: {args.source}")

        collected_files = collect_logs(
            args.source,
            bundle_dir
        )

        zip_name = f"output/log_bundle_{timestamp}.zip"

        create_zip(bundle_dir, zip_name)

        logger.info(f"[+] Files collected: {len(collected_files)}")
        logger.info(f"[+] Bundle created: {zip_name}")

if __name__ == "__main__":
    main()