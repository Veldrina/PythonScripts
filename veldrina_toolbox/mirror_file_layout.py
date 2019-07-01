"""Mirror File Layout
This tool will analyze a directory tree and record its structure, which can then be used to rearrange the contents
of another directory tree so that identical files have the same relative paths.

Usage:
    mirror_file_layout.py [-n | --dry-run] [-v | --verbose] (record | replay) DIRECTORY FILE
    mirror_file_layout.py (-h | --help)

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

# Global script settings
verbose_output: bool = False
dry_run: bool = False

def PrintVerboseOutput(message: str):
    if (verbose_output):
        print(message)

def CollectHashesFromDirectory(directory: str):
    """
    Calculates hashes for all files (recursively) in the specified directory.
    """ 
    hashmap = {}
    for root, dirs, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(root, name)
            PrintVerboseOutput("Processing {0}".format(file_path)) 

            hash = CalculateFileHash(file_path)
            path = os.path.relpath(file_path, directory)
            
            if (hash not in hashmap):
                hashmap[hash] = SplitPathIntoComponents(path)
            else:
                raise DuplicateFileHashException(hashmap[hash], path)
            PrintVerboseOutput("Digest is: {0}".format(hash))
    return hashmap


def CalculateFileHash(file_path: str):
    """ 
    The hash is generated from 8 KiB centered around the midpoint of the file, or the
    entire file, whichever is smaller.
    """
    BUFFER_SIZE = 8 * 1024 * 1024
    hasher = hashlib.sha256()
    file_size = os.path.getsize(file_path)
    with open(file_path, "rb") as f:
        if (file_size >= BUFFER_SIZE):
            seek_point = (file_size // 2) - (BUFFER_SIZE // 2)
            f.seek(seek_point)
            
        hasher.update(f.read(BUFFER_SIZE))
    return hasher.hexdigest()    

def SplitPathIntoComponents(path: str):
    components = []
    while True:
        path, folder = os.path.split(path)

        if folder != "":
            components.append(folder)
        else:
            if path != "":
                components.append(path)
            break

    components.reverse()
    return components

def RecordFileLayout(target_directory_path: str, hash_file_path: str):
    raise NotImplementedError

def ReplayFileLayout(target_directory_path: str, hash_file_path: str):
    raise NotImplementedError

if __name__ == "__main__":
    arguments = docopt(__doc__)

    # Set script options based on arguments
    verbose_output = arguments["--verbose"]
    dry_run = arguments["--dry-run"]

    print(arguments)

    # Perform invoked command
    if (arguments["record"]):
        RecordFileLayout(arguments["DIRECTORY"], arguments["FILE"])
    elif (arguments["replay"]):
        ReplayFileLayout(arguments["DIRECTORY"], arguments["FILE"])
    else:
        raise NotImplementedError("Unknown command")

    