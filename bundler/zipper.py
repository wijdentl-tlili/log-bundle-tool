from pathlib import Path
import zipfile

def create_zip(source_directory, zip_name):

    source_path = Path(source_directory)

    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:

        for file in source_path.rglob("*"):

            if file.is_file():

                zipf.write(file, arcname=file.name)

    return zip_name