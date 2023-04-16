import hashlib
import zlib
import os


def hash_object(data, object_type, write=True):
    header = '{} {}'.format(object_type, len(data)).encode()
    object_data = header + b'\x00' + data
    object_hash = hashlib.sha1(object_data, usedforsecurity=False).hexdigest()
    subdir = object_hash[:2]
    object_file = object_hash[2:]
    if write:
        object_path = os.path.join('.git', 'objects', subdir, object_file)
        with open(object_path, 'wb') as f:
            f.write(zlib.compress(object_data))
    return object_hash

def read_object(object_hash):
    subdir = object_hash[:2]
    object_file = object_hash[2:]
    object_path = os.path.join('.git', 'objects', subdir, object_file)
    object_data = bytes()
    with open(object_path, 'rb') as f:
        object_data = f.read()
    header, data = object_data.split(b'\x00')
    object_type, data_length = header.split(b' ')
    return object_type, data
