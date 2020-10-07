import socket
import sys
import os
import time
import signal

class JobSeekerNode:

    def __init__(self, name):
        self.name = name