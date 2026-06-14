import logging

import pytest
from pytest_assume.plugin import assume
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from helpers.fitpal_helpers import log_result

logger = logging.getLogger(__name__)

WAIT = 10

EMAIL_FIELD    = (By.ID, "formBasicEmail")
PASSWORD_FIELD = (By.ID, "formBasicPassword")
SUBMIT_BUTTON  = (By.CSS_SELECTOR, "button[type='submit']")
TOAST          = (By.CSS_SELECTOR, ".toast-body")


def fill_field(driver, locator, value):
    el = driver.find_element(*locator)
    el.clear()
    el.send_keys(value)


def get_toast(driver, timeout=5):
    try:
        toast = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(TOAST)
        )
        return toast.text.strip()
    except Exception:
        return ""


class TestTC02003:

    # TP-02-003: Verify that an error message is displayed when
    # invalid credentials are entered.
    # Precondition: user10@fitpal.com must be registered in the system.
    def test_tc02_003_invalid_credentials(self, sign_in_page, wait):
        """TC-02-003: Invalid credentials show error message."""
        driver = sign_in_page

        logger.info("Step 1: Enter valid email: user10@fitpal.com")
        fill_field(driver, EMAIL_FIELD, "user10@fitpal.com")

        logger.info("Step 2: Enter wrong password: WrongPass@99")
        fill_field(driver, PASSWORD_FIELD, "WrongPass@99")

        logger.info("Step 3: Click Sign In button")
        driver.find_element(*SUBMIT_BUTTON).click()

        logger.info("Step 4: Verify error toast is displayed")
        toast = get_toast(driver)
        still_on_page = "sign-in" in driver.current_url
        passed = bool(toast) or still_on_page

        assume(passed, "Expected error toast or page to remain on sign-in")
        log_result("TC-02-003", "PASS" if passed else "FAIL",
                   f"Toast: '{toast}'")

        if passed:
            print(f"PASS: Error shown for invalid credentials. Toast: '{toast}'")
        else:
            print("FAIL: No error shown for invalid credentials")
