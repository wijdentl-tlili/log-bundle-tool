from analyzer.metadata import sha256_file


def generate_sha256_report(files, output_file):

    with open(output_file, "w") as report:

        report.write("=== SHA256 REPORT ===\n\n")

        for file in files:

            file_hash = sha256_file(file)

            report.write(f"FILE: {file.name}\n")
            report.write(f"SHA256: {file_hash}\n")
            report.write("\n")