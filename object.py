import hashlib
import zlib
import os


def hash_object(data, object_type, write=True):
    header = "{} {}".format(object_type, len(data)).encode()
    object_data = header + b"\x00" + data
    # get SHA-1 hash of object data
    object_hash = hashlib.sha1(object_data, usedforsecurity=False).hexdigest()
    subdir = object_hash[:2]
    object_file = object_hash[2:]
    if write:
        object_path = os.path.join(".git", "objects", subdir, object_file)
        if not os.path.exists(object_path):
            # create directories and subdirectories for object path
            os.makedirs(os.path.dirname(object_path), exist_ok=True)
            with open(object_path, "wb") as f:
                # compress object data using zlib
                f.write(zlib.compress(object_data))
    return object_hash


def read_object(object_hash):
    subdir = object_hash[:2]
    object_file = object_hash[2:]
    object_path = os.path.join(".git", "objects", subdir, object_file)
    if not os.path.exists(object_path):
        raise Exception("Object does not exist")
    object_data = bytes()
    with open(object_path, "rb") as f:
        object_data = f.read()
    # decompress zlib-compressed data
    object_data = zlib.decompress(object_data)
    nul_index = object_data.index(b"\x00")
    header, data = object_data[:nul_index], object_data[nul_index + 1 :]
    object_type, data_length = header.split(b" ")
    assert data_length == len(data)
    return object_type, data
