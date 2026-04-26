import zipfile
from pathlib import Path

def create_zip(bundle_directory, output_zip):

    bundle_path = Path(bundle_directory)

    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:

        for file in bundle_path.rglob("*"):

            if file.is_file():
                zipf.write(file, arcname=file.name)

    return output_zip