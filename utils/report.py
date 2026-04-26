from pathlib import Path
from utils.hashing import sha256_file

def generate_report(files, report_path):

    with open(report_path, "w") as report:

        report.write("=== LOG BUNDLE REPORT ===\n\n")

        for file in files:

            file_hash = sha256_file(file)

            report.write(f"FILE: {file}\n")
            report.write(f"SHA256: {file_hash}\n")
            report.write("\n")