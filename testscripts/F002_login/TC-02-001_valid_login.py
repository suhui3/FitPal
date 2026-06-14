import logging

import pytest
from pytest_assume.plugin import assume
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from helpers.fitpal_helpers import log_result

logger = logging.getLogger(__name__)

WAIT = 10

EMAIL_FIELD   = (By.ID, "formBasicEmail")
PASSWORD_FIELD = (By.ID, "formBasicPassword")
SUBMIT_BUTTON  = (By.CSS_SELECTOR, "button[type='submit']")


def fill_field(driver, locator, value):
    el = driver.find_element(*locator)
    el.clear()
    el.send_keys(value)


class TestTC02001:

    # TP-02-001: Verify the user is successfully authenticated
    # and redirected to the Home Page with valid credentials.
    # Precondition: user10@fitpal.com must be active and registered.
    def test_tc02_001_valid_login(self, sign_in_page, wait):
        """TC-02-001: Valid credentials redirect to Home Page."""
        driver = sign_in_page

        logger.info("Step 1: Enter valid email: user10@fitpal.com")
        fill_field(driver, EMAIL_FIELD, "user10@fitpal.com")

        logger.info("Step 2: Enter valid password: Password@123")
        fill_field(driver, PASSWORD_FIELD, "Password@123")

        logger.info("Step 3: Click Sign In button")
        driver.find_element(*SUBMIT_BUTTON).click()

        logger.info("Step 4: Verify redirect to Home Page")
        wait.until(EC.url_contains("/home"))
        passed = "/home" in driver.current_url

        assume(passed, "Expected redirect to /home after valid login")
        log_result("TC-02-001", "PASS" if passed else "FAIL",
                   f"Current URL: '{driver.current_url}'")

        if passed:
            print(f"PASS: User redirected to Home Page. URL: '{driver.current_url}'")
        else:
            print(f"FAIL: Expected '/home' in URL, got: '{driver.current_url}'")
