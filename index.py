import os


def read_index():
    index_file = os.path.join(".git", "index")
    if not os.path.exists(index_file):
        return []
    with open(index_file, "rb") as f:
        raw = f.read()
    # parse index header
    header = raw[:12]
    signature = raw[:4]
    assert signature == b"DIRC"
    version = int.from_bytes(header[4:8], "big")
    assert version == 2
    count = int.from_bytes(header[8:12], "big")
    # get index entries
    entries = []
    content = raw[12:]
    idx = 0
    for i in range(count):
        # read creation time as a unix timestamp
        ctime_s = int.from_bytes(content[idx : idx + 4], "big")
        idx += 4
        # read creation time nanoseconds
        ctime_ns = int.from_bytes(content[idx : idx + 4], "big")
        idx += 4
        # read modification time, same format as before
        mtime_s = int.from_bytes(content[idx : idx + 4], "big")
        idx += 4
        mtime_ns = int.from_bytes(content[idx : idx + 4], "big")
        idx += 4
        # read device ID
        dev = int.from_bytes(content[idx : idx + 4], "big")
        idx += 4
        # read Inode
        ino = int.from_bytes(content[idx : idx + 4], "big")
        idx += 4
        # read 32-bit mode, first 2 bytes unused
        unused = int.from_bytes(content[idx : idx + 2], "big")
        idx += 2
        # first 2 bytes must be 0
        assert 0 == unused
