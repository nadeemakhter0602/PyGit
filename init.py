import os


def init(repo_name=None):
    git_path = str()
    if repo_name is None:
        git_path = '.git'
        os.mkdir(git_path)
    else:
        os.mkdir(repo_name)
        git_path = os.path.join(repo_name, '.git')
        os.mkdir(git_path)
    # create required sub directories
    sub_directories = ['objects', 'refs']
    sub_directories.append(os.path.join('refs', 'heads'))
    for directory in sub_directories:
        os.mkdir(os.path.join(git_path, directory))
    # write to HEAD file
    master_bytes = b'ref: refs/heads/master'
    with open(os.path.join(git_path, 'HEAD'), 'wb') as f:
        f.write(master_bytes)
    print("initialized empty repository: %s" % git_path)
