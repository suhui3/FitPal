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
MODAL_TITLE    = (By.CSS_SELECTOR, ".modal-title")
MODAL_BODY     = (By.CSS_SELECTOR, ".modal-body")


def fill_field(driver, locator, value):
    el = driver.find_element(*locator)
    el.clear()
    el.send_keys(value)


def get_modal_title(driver, timeout=5):
    try:
        el = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(MODAL_TITLE)
        )
        return el.text.strip()
    except Exception:
        return ""


class TestTC02002:

    # TP-02-002: Verify that a deactivated account is prompted for
    # reactivation during login.
    # Precondition: user10@fitpal.com must be deactivated in the database.
    def test_tc02_002_deactivated_account(self, sign_in_page, wait):
        """TC-02-002: Deactivated account shows reactivation modal."""
        driver = sign_in_page

        logger.info("Step 1: Enter email of deactivated account: user10@fitpal.com")
        fill_field(driver, EMAIL_FIELD, "user10@fitpal.com")

        logger.info("Step 2: Enter correct password: Password@123")
        fill_field(driver, PASSWORD_FIELD, "Password@123")

        logger.info("Step 3: Click Sign In button")
        driver.find_element(*SUBMIT_BUTTON).click()

        logger.info("Step 4: Verify reactivation modal is displayed")
        modal_title = get_modal_title(driver)
        title_correct = "Reactivate Account" in modal_title

        logger.info("Step 5: Verify modal body mentions deactivated account")
        modal_body_text = driver.find_element(*MODAL_BODY).text if title_correct else ""
        body_correct = "deactivated" in modal_body_text.lower()

        passed = title_correct and body_correct

        assume(passed, "Expected reactivation modal to appear for deactivated account")
        log_result("TC-02-002", "PASS" if passed else "FAIL",
                   f"Modal title: '{modal_title}' | Modal body: '{modal_body_text}'")

        if passed:
            print(f"PASS: Reactivation modal displayed. Title: '{modal_title}'")
        else:
            print(f"FAIL: Modal not shown or missing content. Title: '{modal_title}'")
