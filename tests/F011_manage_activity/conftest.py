import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL     = "http://localhost:5173"
SIGN_IN_URL  = f"{BASE_URL}/sign-in"
FITNESS_URL  = f"{BASE_URL}/fitness"

EMAIL    = "user10@fitpal.com"
PASSWORD = "Password@123"


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
def fitness_page(driver):
    # Log in
    driver.get(SIGN_IN_URL)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "formBasicEmail"))
    )
    driver.find_element(By.ID, "formBasicEmail").send_keys(EMAIL)
    driver.find_element(By.ID, "formBasicPassword").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Wait for redirect then navigate to fitness page
    WebDriverWait(driver, 10).until(EC.url_contains("/home"))
    driver.get(FITNESS_URL)

    # Switch date filter to "All" so all logged activities are visible
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='date-radio-4']"))
    )
    driver.find_element(By.CSS_SELECTOR, "label[for='date-radio-4']").click()

    return driver
