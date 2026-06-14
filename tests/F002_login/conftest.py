import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "http://localhost:5173"
SIGN_IN_URL = f"{BASE_URL}/sign-in"


@pytest.fixture
def driver():
    options = Options()
    d = webdriver.Chrome(options=options)
    d.implicitly_wait(10)
    yield d
    d.quit()


@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 10)


@pytest.fixture
def sign_in_page(driver):
    driver.get(SIGN_IN_URL)
    return driver
