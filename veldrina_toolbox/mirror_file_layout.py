"""Mirror File Layout
This tool will analyze a directory tree and record its structure, which can then be used to rearrange the contents
of another directory  tree so that identical files have the same relative paths.

Usage:
    mirror_file_layout.py record DIRECTORY FILE
    mirror_file_layout.py replay DIRECTORY FILE

Arguments:
    DIRECTORY   The directory to analyze (if recording) or rearrange (if replaying)
    FILE        The file to write the analysis to (if recording) or use to determine how to perform the rearrangement (if replaying)

Options:
    -n, --dry-run  Do not make modifications to filesystem
    -v, --verbose  More output
    -h, --help  Display this help text
"""

import os
import subprocess
import hashlib
from docopt import docopt

class DuplicateFileHashException(Exception):
    def __init__(self, original_path: str, new_path: str):
        self.message = "Hash collision between '{0}' and '{1}'".format(original_path, new_path)

def CalculateFileHashes(directory: str):
    hashmap = {}
    for root, dirs, files in os.walk(directory):
        for name in files:
            hasher = hashlib.sha256()
            print("Processing {0}".format(os.path.join(root, name)))
            with open(os.path.join(root, name), "rb") as f:
                for chunk in iter(lambda: f.read(2 * 1024 * 1024), b''): 
                    hasher.update(chunk)

            path = os.path.relpath(os.path.join(root, name), directory)
            hash = hasher.hexdigest()
            if (hash not in hashmap):
                hashmap[hash] = SplitPathIntoComponents(path)
            else:
                raise DuplicateFileHashException(hashmap[hash], path)
            print("Digest is: {0}".format(hash))
    return hashmap

def SplitPathIntoComponents(path: str):
    folders = []
    while True:
        path, folder = os.path.split(path)

        if folder != "":
            folders.append(folder)
        else:
            if path != "":
                folders.append(path)
            break

    folders.reverse()
    return folders

def RecordFileLayout(path: str):
    raise NotImplementedError

def ReplayFileLayout(path: str):
    raise NotImplementedError

if __name__ == "__main__":
    arguments = docopt(__doc__)


    print(arguments)