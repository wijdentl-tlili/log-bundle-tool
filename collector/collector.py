from pathlib import Path
import shutil
import os


def collect_logs(source_directory,
                 destination_directory,
                 extensions,
                 recursive=True):

    source_path = Path(source_directory)
    destination_path = Path(destination_directory)

    destination_path.mkdir(parents=True, exist_ok=True)

    collected_files = []

    for root, dirs, files in os.walk(source_path):

        if not recursive:
            dirs.clear()
        for file in files:

            file_path = Path(root) / file

            if file_path.suffix.lower() in extensions:

                destination_file = destination_path / file

                shutil.copy2(file_path, destination_file)

                collected_files.append(destination_file)

    return collected_files