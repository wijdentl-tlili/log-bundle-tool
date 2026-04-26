import os
import shutil
from pathlib import Path

LOG_EXTENSIONS = [".log", ".txt"]

def collect_logs(source_directory, bundle_directory):
    source_path = Path(source_directory)
    bundle_path = Path(bundle_directory)

    # Create bundle directory if not exists
    bundle_path.mkdir(parents=True, exist_ok=True)

    collected_files = []

    for root, dirs, files in os.walk(source_path):

        for file in files:
            file_path = Path(root) / file

            # Collect only log-like files
            if file_path.suffix.lower() in LOG_EXTENSIONS:

                destination = bundle_path / file

                try:
                    shutil.copy2(file_path, destination)
                    collected_files.append(str(destination))

                except Exception as e:
                    print(f"[ERROR] Failed to copy {file_path}: {e}")

    return collected_files