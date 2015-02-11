"""
Usage: 

"""

import os
import subprocess
from docopt import docopt



sshControlMasterCommand = r"ssh -nNf -o ControlMaster=yes -o ControlPath=\"$HOME/.ssh/ctl/%L-%r@%h:%p\""
sshTerminateControlMasterCommand = r"ssh -O exit -o ControlPath=\"$HOME/.ssh/ctl/%L-%r@%h:%p\""
sshControlPathCommand = r"ssh -o \'ControlPath=$HOME/.ssh/ctl/%L-%r@%h:%p\'"

def EstablishSshControlMaster(self):
    # Set up the SSH ControlMaster
    os.makedirs("~/.ssh/ctl", mode = 0o700)

if __name__ == '__main__':
    """
    The main function and entry point
    """
    arguments = docopt(__doc__, version='Naval Fate 2.0')
    print(arguments)