import os
import sys

if getattr(sys, "frozen", False):
    ROOT_DIR = os.path.dirname(sys.executable)
else:
    ROOT_DIR = os.path.dirname(os.path.realpath(__file__))


RESOURCE_DIR = os.path.join(ROOT_DIR, "resources")
INPUT_DIR = os.path.join(RESOURCE_DIR, "input")
OUTPUT_DIR = os.path.join(RESOURCE_DIR, "output")
