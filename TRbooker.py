import importlib
import sys
import subprocess

required_modules = [
    "requests",
    "selenium",
    "ddddocr",
    "prettytable",
    "pyfiglet",
    "rgbprint",
]


def install_requirement():
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        rgbprint("\nRequirements are successfully installed!!!\n", color="green")
    except subprocess.CalledProcessError:
        print("\nError installing requirements. Please make sure 'pip' is installed.\n")


def check_module(module_name):
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False


if all(check_module(module) for module in required_modules):
    print("\nAll modules we need are installed\n")
else:
    install_requirement()

import requests
import selenium
import ddddocr
import prettytable
import pyfiglet
from rgbprint import Color, rgbprint
