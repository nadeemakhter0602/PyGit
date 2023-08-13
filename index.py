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
        # read Device ID
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
        # get next 2 bytes containing actual mode information
        mode = int.from_bytes(content[idx : idx + 2], "big")
        # read 4-bit object type
        object_type = mode >> 12
        # valid values for object type include:
        # 1000 (regular file), 1010 (symbolic link) and 1110 (gitlink)
        assert object_type in [0b1000, 0b1010, 0b1110]
        # next 3 bits unused, must be zero
        # read 9-bit unix permission
        unix_perm = mode & 0b0000000111111111
        idx += 2
        # read User ID
        uid = int.from_bytes(content[idx : idx + 4], "big")
        idx += 4
        # read Group ID
        gid = int.from_bytes(content[idx : idx + 4], "big")
        idx += 4
        # read on-disk file size, truncated to 32-bit
        fsize = int.from_bytes(content[idx : idx + 4], "big")
        idx += 4
        # object ID in the form of SHA-1 hash of an object
        # size of hash is 20 bytes
        sha = int.from_bytes(content[idx : idx + 20], "big")
        # convert hash bytes to lowercase hex string
        sha = format(sha, "040x")
        idx += 20
        # read 16-bit 'flags'
        flags = int.from_bytes(content[idx : idx + 2], "big")
        # read 1-bit assume-valid flag
        flag_assume_valid = (flags & 0b1000000000000000) != 0
        # read 1-bit extended flag
        flag_extended = (flags & 0b0100000000000000) != 0
        # extended flag must be zero in version 2
        assert not flag_extended
        # read 2-bit stage
        flag_stage = flags & 0b0011000000000000
