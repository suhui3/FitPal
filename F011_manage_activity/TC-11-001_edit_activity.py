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
DATE_INPUT     = (By.CSS_SELECTOR, "input[type='date']")
TIME_INPUT     = (By.CSS_SELECTOR, "input[type='time']")
DURATION_INPUT = (By.CSS_SELECTOR, "input[type='number']")


def get_toast(driver, timeout=5):
    try:
        el = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(TOAST)
        )
        return el.text.strip()
    except Exception:
        return ""


def react_fill(driver, locator, value):
    """Set value on a React controlled input and trigger onChange."""
    el = driver.find_element(*locator)
    driver.execute_script("""
        var el = arguments[0], val = arguments[1];
        var nativeInputValueSetter = Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype, 'value').set;
        nativeInputValueSetter.call(el, val);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    """, el, value)


def js_click(driver, locator):
    el = driver.find_element(*locator)
    driver.execute_script("arguments[0].click();", el)


class TestTC11001:

    # TP-11-001: Verify activity is edited and saved successfully with valid details.
    # Precondition: user10@fitpal.com must be logged in with at least one
    # "Running, 10 min/mile" cardio activity logged.
    def test_tc11_001_edit_activity(self, fitness_page, wait):
        """TC-11-001: Activity is updated and saved successfully with valid inputs."""
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

        logger.info("Step 4: Enter Date = 2025-06-16")
        react_fill(driver, DATE_INPUT, "2025-06-16")

        logger.info("Step 5: Enter Start Time = 20:58")
        react_fill(driver, TIME_INPUT, "20:58")

        logger.info("Step 6: Enter Duration = 20")
        react_fill(driver, DURATION_INPUT, "20")

        logger.info("Step 7: Click Save button")
        js_click(driver, SAVE_BUTTON)

        logger.info("Step 8: Verify modal closes and/or success toast is displayed")
        toast = get_toast(driver)
        modal_closed = wait.until(EC.invisibility_of_element_located(MODAL_TITLE))
        passed = bool(toast) or modal_closed

        assume(passed, "Expected modal to close or success toast after saving activity")
        log_result("TC-11-001", "PASS" if passed else "FAIL",
                   f"Toast: '{toast}' | Modal closed: {modal_closed}")

        if passed:
            print(f"PASS: Activity saved. Toast: '{toast}' | Modal closed: {modal_closed}")
        else:
            print(f"FAIL: Save did not complete. Toast: '{toast}'")
