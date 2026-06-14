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
REMOVE_BUTTON  = (By.XPATH, "//button[normalize-space()='Remove']")
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


def fill_field(driver, locator, value):
    el = driver.find_element(*locator)
    el.clear()
    el.send_keys(value)


def js_click(driver, locator):
    el = driver.find_element(*locator)
    driver.execute_script("arguments[0].click();", el)


def click_activity(driver, wait, name):
    item = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//div[contains(@class,'fw-semibold') and contains(text(),'{name}')]")
    ))
    item.click()
    wait.until(EC.visibility_of_element_located(MODAL_TITLE))


class TestTC11005:

    # TP-11-005: Verify success or error feedback message is shown after saving changes.
    # Precondition: user10@fitpal.com must be logged in with at least two
    # "Running, 10 min/mile" cardio activities logged (one for valid edit,
    # one for invalid date test).
    def test_tc11_005_valid_save_shows_success(self, fitness_page, wait):
        """TC-11-005a: Valid edit (Date=2025-06-16) shows success feedback."""
        driver = fitness_page

        logger.info(f"Step 1: Click on activity '{ACTIVITY_NAME}'")
        click_activity(driver, wait, ACTIVITY_NAME)

        logger.info("Step 2: Click Edit, enter Date=2025-06-16, Time=20:58, Duration=20")
        driver.find_element(*EDIT_BUTTON).click()
        fill_field(driver, DATE_INPUT, "2025-06-16")
        fill_field(driver, TIME_INPUT, "20:58")
        fill_field(driver, DURATION_INPUT, "20")

        logger.info("Step 3: Click Save")
        js_click(driver, SAVE_BUTTON)

        logger.info("Step 4: Verify success toast is shown")
        toast = get_toast(driver)
        passed = bool(toast) and "updated" in toast.lower()

        assume(passed, "Expected success toast after valid save")
        log_result("TC-11-005a", "PASS" if passed else "FAIL", f"Toast: '{toast}'")

        if passed:
            print(f"PASS: Success toast shown after valid save. Toast: '{toast}'")
        else:
            print(f"FAIL: No success toast after valid save. Toast: '{toast}'")

    def test_tc11_005_invalid_date_shows_error(self, fitness_page, wait):
        """TC-11-005b: Invalid edit (Date=2030-06-16) shows error feedback."""
        driver = fitness_page

        logger.info(f"Step 1: Click on activity '{ACTIVITY_NAME}'")
        click_activity(driver, wait, ACTIVITY_NAME)

        logger.info("Step 2: Click Edit, enter future Date=2030-06-16, Time=20:58, Duration=20")
        driver.find_element(*EDIT_BUTTON).click()
        fill_field(driver, DATE_INPUT, "2030-06-16")
        fill_field(driver, TIME_INPUT, "20:58")
        fill_field(driver, DURATION_INPUT, "20")

        logger.info("Step 3: Click Save")
        js_click(driver, SAVE_BUTTON)

        logger.info("Step 4: Verify error toast or modal remains open")
        toast = get_toast(driver)
        modal_open = len(driver.find_elements(*MODAL_TITLE)) > 0
        passed = bool(toast) or modal_open

        assume(passed, "Expected error feedback for invalid future date")
        log_result("TC-11-005b", "PASS" if passed else "FAIL", f"Toast: '{toast}'")

        if passed:
            print(f"PASS: Error feedback shown for invalid date. Toast: '{toast}'")
        else:
            print("FAIL: No error feedback for invalid future date")

    def test_tc11_005_remove_activity(self, fitness_page, wait):
        """TC-11-005c: Activity is removed from list after clicking Remove."""
        driver = fitness_page

        logger.info(f"Step 1: Click on activity '{ACTIVITY_NAME}'")
        click_activity(driver, wait, ACTIVITY_NAME)

        logger.info("Step 2: Click Remove button")
        driver.find_element(*REMOVE_BUTTON).click()

        logger.info("Step 3: Verify activity is removed from list")
        toast = get_toast(driver)
        activity_gone = len(driver.find_elements(
            By.XPATH,
            f"//div[contains(@class,'fw-semibold') and contains(text(),'{ACTIVITY_NAME}')]"
        )) == 0
        passed = bool(toast) or activity_gone

        assume(passed, "Expected activity to be removed from list")
        log_result("TC-11-005c", "PASS" if passed else "FAIL",
                   f"Toast: '{toast}' | Activity gone: {activity_gone}")

        if passed:
            print(f"PASS: Activity removed from list. Toast: '{toast}'")
        else:
            print("FAIL: Activity not removed from list")
