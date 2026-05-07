from pathlib import Path
import hashlib
import stat
import platform
from datetime import datetime

def sha256_file(file_path):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:

        while chunk := f.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()

def get_file_metadata(file_path):

    path = Path(file_path)

    stats = path.stat()

    if platform.system() == "Windows":
        owner = "N/A"
    else:
        import pwd
        owner = pwd.getpwuid(stats.st_uid).pw_name

    metadata = {

        "file_name": path.name,

        "absolute_path": str(path.resolve()),

        "size_bytes": stats.st_size,

        "sha256": sha256_file(path),

        "created_time": datetime.fromtimestamp(
            stats.st_ctime
        ).isoformat(),

        "modified_time": datetime.fromtimestamp(
            stats.st_mtime
        ).isoformat(),

        "accessed_time": datetime.fromtimestamp(
            stats.st_atime
        ).isoformat(),

        "permissions": stat.filemode(stats.st_mode),

        "owner": owner
    }

    return metadata