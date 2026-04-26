from collector.collector import collect_logs
from bundler.zipper import create_zip
from utils.report import generate_report
from pathlib import Path
import datetime

def main():

    source_logs = input("Enter logs directory: ")

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    bundle_dir = f"output/bundle_{timestamp}"

    collected = collect_logs(source_logs, bundle_dir)

    report_path = f"{bundle_dir}/report.txt"

    generate_report(collected, report_path)

    zip_path = f"output/log_bundle_{timestamp}.zip"

    create_zip(bundle_dir, zip_path)

    print("\n[+] Bundle Created Successfully")
    print(f"[+] ZIP: {zip_path}")
    print(f"[+] Files Collected: {len(collected)}")

if __name__ == "__main__":
    main()