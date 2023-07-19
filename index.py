import os


def read_index():
    index_file = os.path.join(".git", "index")
    if not os.path.exists(index_file):
        return []
    with open(index_file, "rb") as f:
        raw = f.read()
    header = raw[:12]
    signature = raw[:4]
    assert signature == b"DIRC"
    version = int.from_bytes(header[4:8], "big")
    assert version == 2
    count = int.from_bytes(header[8:12], "big")
