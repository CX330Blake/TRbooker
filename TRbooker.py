# check the modules

import importlib
import sys
import subprocess

required_modules = [
    "requests",
    "selenium",
    "Pillow",
    "prettytable",
    "pyfiglet",
    "rgbprint",
    "pytesseract",
]


def install_requirement():
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        print("\nRequirements are successfully installed!!!\n")
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

#

import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from PIL import Image
import pytesseract
import prettytable
import pyfiglet
from rgbprint import Color, rgbprint


def recaptcha():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

    # 定位 reCAPTCHA 元素
    recaptcha_frame = driver.find_element(
        By.XPATH, "//iframe[@title='recaptcha challenge']"
    )
    driver.switch_to.frame(recaptcha_frame)

    # 定位方形框元素
    checkbox = driver.find_element(
        By.XPATH, "//div[@class='recaptcha-checkbox-checkmark']"
    )
    checkbox.click()


with open("Timetable.json", "r", encoding="uft-8") as file:
    timetable = json.load(file)

def find_station():
    for station in timetable:
        if station 