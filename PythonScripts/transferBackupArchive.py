"""
Usage: transferBackupArchive.py [--verbose]

"""

import os
import subprocess
import sys
from docopt import docopt


sshControlPathCommand = r"ssh -o \'ControlPath=$HOME/.ssh/ctl/%L-%r@%h:%p\'"

def EstablishSSHControlMaster(user, host):
    sshControlMasterCommand =  "{0} {1}@{2}".format(
        r"ssh -nNf -o ControlMaster=yes -o ControlPath=\"$HOME/.ssh/ctl/%L-%r@%h:%p\"",
        user,
        host)
    os.makedirs("~/.ssh/ctl", mode = 0o700)
    process = subprocess.Popen(
        sshControlMasterCommand, 
        stdin = sys.stdin, 
        stdout = sys.stdout, 
        stderr = sys.stderr, 
        shell = True)
    process.wait()

def TerminateSSHControlMaster(user, host):
    sshTerminateControlMasterCommand = "{0} {1}@{2}".format(
        r"ssh -O exit -o ControlPath=\"$HOME/.ssh/ctl/%L-%r@%h:%p\"",
        user,
        host)
    process = subprocess.Popen(
        sshTerminateControlMasterCommand, 
        stdin = sys.stdin, 
        stdout = sys.stdout, 
        stderr = sys.stderr, 
        shell = True)
    process.wait()

def ListSourceContents(user, host, dir):
    remoteListingCommand = "{0} {1}@{2} ls {3}".format(
        sshControlPathCommand,
        user,
        host,
        dir)
    process = subprocess.Popen(
        remoteListingCommand,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE)
    out, err = process.communicate()

if __name__ == '__main__':
    """
    The main function and entry point
    """
    arguments = docopt(__doc__)
    print(arguments)

    EstablishSSHControlMaster(self.SourceUser, self.SourceHost)