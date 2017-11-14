import sys
import traceback
import shutil
import os
import time
import subprocess

from AutoGrader.devices import HardwareBase

class BBB2b(HardwareBase):
    """
    For generating events
    """

    def __init__(self, name, config, hardware_engine, file_folder):
        
        # parameters
        self.binary_path = None
        self.input_path = None
        self.stdout_path = None
        self.stderr_path = None

        # device info
        self.name = None
        self.config = None

        # parse config
        if "binary_file" not in config:
            raise Exception('"binary_file" field is required')
        self.binary_path = os.path.join(file_folder, config['binary_file'])
        
        if "input_file" not in config:
            raise Exception('"input_file" field is required')
        self.input_path = os.path.join(file_folder, config['input_file'])

        if "stdout_file" not in config:
            raise Exception('"stdout_file" field is required')
        self.stdout_path = os.path.join(file_folder, config['stdout_file'])

        if "stderr_file" not in config:
            raise Exception('"stderr_file" field is required')
        self.stderr_path = os.path.join(file_folder, config['stderr_file'])

        self.name = name
        self.config = config

    def on_before_execution(self):
        subprocess.call(['ssh', 'root@192.168.7.2', 'testenv/prepare.sh'])
        subprocess.call(['scp', self.binary_path, 'root@192.168.7.2:~/testenv/files/student_bin'])
        subprocess.call(['scp', self.input_path, 'root@192.168.7.2:~/testenv/files/student_input.txt'])

    def on_execute(self):
        subprocess.call(['ssh', 'root@192.168.7.2', 'testenv/run.py', 'student_input.txt'])

    def on_terminate(self):
        subprocess.call(['scp', 'root@192.168.7.2:~/testenv/files/stdout.txt', self.stdout_path])
        subprocess.call(['scp', 'root@192.168.7.2:~/testenv/files/stderr.txt', self.stderr_path])
    
    def on_reset_after_execution(self):
        pass
