import logging
import os
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


logger = logging.getLogger(__name__)
BASE_URL = os.getenv("FITPAL_BASE_URL", "http://localhost:5173")

EMAIL_FIELD = (By.ID, "formBasicEmail")
PASSWORD_FIELD = (By.ID, "formBasicPassword")
SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
CONFIRM_PASSWORD_FIELDS = (By.CSS_SELECTOR, "input[name='comfirmPassword']")
TOAST = (By.CSS_SELECTOR, ".Toastify__toast")
BELL_BUTTON = (By.CSS_SELECTOR, "button")


def log_result(case_id, status, details=""):
    Path("test-results").mkdir(exist_ok=True)
    with Path("test-results/niu-bingkun-results.log").open("a", encoding="utf-8") as f:
        f.write(f"{case_id},{status},{details}\n")


def open_page(driver, path):
    driver.get(f"{BASE_URL}{path}")


def sign_in(driver, wait, email, password):
    open_page(driver, "/sign-in")
    wait.until(EC.presence_of_element_located(EMAIL_FIELD)).clear()
    driver.find_element(*EMAIL_FIELD).send_keys(email)
    driver.find_element(*PASSWORD_FIELD).clear()
    driver.find_element(*PASSWORD_FIELD).send_keys(password)
    driver.find_element(*SUBMIT_BUTTON).click()
    wait.until(lambda d: "/home" in d.current_url or "/calorie-calculator" in d.current_url)


def visible_text(driver):
    return driver.find_element(By.TAG_NAME, "body").text


def click_by_text(driver, wait, text):
    locator = (By.XPATH, f"//*[normalize-space()='{text}']")
    wait.until(EC.element_to_be_clickable(locator)).click()


def click_contains_text(driver, wait, text):
    locator = (By.XPATH, f"//*[contains(normalize-space(), '{text}')]")
    wait.until(EC.element_to_be_clickable(locator)).click()


def find_buttons_containing(driver, text):
    return driver.find_elements(By.XPATH, f"//*[contains(normalize-space(), '{text}')]")
