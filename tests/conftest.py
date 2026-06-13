import os

import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


BASE_URL = os.getenv("FITPAL_BASE_URL", "http://localhost:5173")
DEFAULT_EMAIL = os.getenv("FITPAL_TEST_EMAIL", "user10@fitpal.com")
DEFAULT_PASSWORD = os.getenv("FITPAL_TEST_PASSWORD", "Password@123")


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1366,768")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 10)


@pytest.fixture
def logged_in(driver, wait):
    from helpers.fitpal_helpers import sign_in

    sign_in(driver, wait, DEFAULT_EMAIL, DEFAULT_PASSWORD)
    return driver
