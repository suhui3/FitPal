import logging

import pytest
from pytest_assume.plugin import assume
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from helpers.fitpal_helpers import log_result

logger = logging.getLogger(__name__)

WAIT = 10

ACTIVITY_NAME  = "Running, 10 min/mile"
TOAST          = (By.CSS_SELECTOR, ".toast-body")
MODAL_TITLE    = (By.CSS_SELECTOR, ".modal-title h1")
EDIT_BUTTON    = (By.XPATH, "//button[normalize-space()='Edit']")
SAVE_BUTTON    = (By.CSS_SELECTOR, "button[type='submit']")
DURATION_INPUT = (By.CSS_SELECTOR, "input[type='number']")


def get_toast(driver, timeout=5):
    try:
        el = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(TOAST)
        )
        return el.text.strip()
    except Exception:
        return ""


def fill_field(driver, locator, value):
    el = driver.find_element(*locator)
    el.clear()
    el.send_keys(value)


def js_click(driver, locator):
    el = driver.find_element(*locator)
    driver.execute_script("arguments[0].click();", el)


class TestTC11003:

    # TP-11-003: Verify error message is displayed when invalid details are entered.
    # Precondition: user10@fitpal.com must be logged in with at least one
    # "Running, 10 min/mile" cardio activity logged.
    def test_tc11_003_invalid_duration(self, fitness_page, wait):
        """TC-11-003: Error message shown when Duration is invalid (negative value)."""
        driver = fitness_page

        logger.info(f"Step 1: Click on activity '{ACTIVITY_NAME}'")
        activity = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//div[contains(@class,'fw-semibold') and contains(text(),'{ACTIVITY_NAME}')]")
        ))
        activity.click()

        logger.info("Step 2: Verify activity details modal is displayed")
        wait.until(EC.visibility_of_element_located(MODAL_TITLE))

        logger.info("Step 3: Click Edit button")
        driver.find_element(*EDIT_BUTTON).click()

        logger.info("Step 4: Enter invalid Duration = -10")
        fill_field(driver, DURATION_INPUT, "-10")

        logger.info("Step 5: Click Save button")
        js_click(driver, SAVE_BUTTON)

        logger.info("Step 6: Verify error is shown (toast or form validation prevents save)")
        toast = get_toast(driver)
        modal_still_open = len(driver.find_elements(*MODAL_TITLE)) > 0
        passed = bool(toast) or modal_still_open

        assume(passed, "Expected error toast or modal to remain open for invalid duration")
        log_result("TC-11-003", "PASS" if passed else "FAIL",
                   f"Toast: '{toast}' | Modal still open: {modal_still_open}")

        if passed:
            print(f"PASS: Error displayed for invalid duration. Toast: '{toast}'")
        else:
            print("FAIL: No error shown for invalid duration")
