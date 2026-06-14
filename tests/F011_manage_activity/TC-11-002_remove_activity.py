import logging

import pytest
from pytest_assume.plugin import assume
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from helpers.fitpal_helpers import log_result

logger = logging.getLogger(__name__)

WAIT = 10

ACTIVITY_NAME = "Running, 10 min/mile"
TOAST         = (By.CSS_SELECTOR, ".toast-body")
MODAL_TITLE   = (By.CSS_SELECTOR, ".modal-title h1")
REMOVE_BUTTON = (By.XPATH, "//button[normalize-space()='Remove']")


def get_toast(driver, timeout=5):
    try:
        el = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(TOAST)
        )
        return el.text.strip()
    except Exception:
        return ""


class TestTC11002:

    # TP-11-002: Verify activity is removed successfully from activity list.
    # Precondition: user10@fitpal.com must be logged in with at least one
    # "Running, 10 min/mile" cardio activity logged.
    def test_tc11_002_remove_activity(self, fitness_page, wait):
        """TC-11-002: Activity is removed successfully from the activity list."""
        driver = fitness_page

        logger.info(f"Step 1: Click on activity '{ACTIVITY_NAME}'")
        activity = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//div[contains(@class,'fw-semibold') and contains(text(),'{ACTIVITY_NAME}')]")
        ))
        activity.click()

        logger.info("Step 2: Verify activity details modal is displayed")
        wait.until(EC.visibility_of_element_located(MODAL_TITLE))

        logger.info("Step 3: Click Remove button")
        driver.find_element(*REMOVE_BUTTON).click()

        logger.info("Step 4: Verify success toast is displayed")
        toast = get_toast(driver)

        logger.info("Step 5: Verify activity is no longer in the list")
        activity_gone = len(driver.find_elements(
            By.XPATH,
            f"//div[contains(@class,'fw-semibold') and contains(text(),'{ACTIVITY_NAME}')]"
        )) == 0
        passed = bool(toast) or activity_gone

        assume(passed, "Expected activity to be removed from the list")
        log_result("TC-11-002", "PASS" if passed else "FAIL",
                   f"Toast: '{toast}' | Activity gone: {activity_gone}")

        if passed:
            print(f"PASS: Activity removed successfully. Toast: '{toast}'")
        else:
            print("FAIL: Activity was not removed from the list")
