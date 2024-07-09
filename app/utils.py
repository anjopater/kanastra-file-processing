import hashlib

def compute_file_hash(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
    except FileNotFoundError:
        print(f"File {file_path} not found when computing hash")
        raise
    return sha256.hexdigest()
