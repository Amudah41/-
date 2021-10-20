import pytest
from selenium import webdriver

import os

cwd = os.getcwd()
link = f"file:{cwd}/qa-test.html"

valid_email = "test@protei.ru"
valid_password = "test"
