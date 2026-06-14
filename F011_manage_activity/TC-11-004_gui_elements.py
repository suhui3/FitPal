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
MODAL_TITLE    = (By.CSS_SELECTOR, ".modal-title h1")
EDIT_BUTTON    = (By.XPATH, "//button[normalize-space()='Edit']")
REMOVE_BUTTON  = (By.XPATH, "//button[normalize-space()='Remove']")
DATE_INPUT     = (By.CSS_SELECTOR, "input[type='date']")
TIME_INPUT     = (By.CSS_SELECTOR, "input[type='time']")
DURATION_INPUT = (By.CSS_SELECTOR, "input[type='number']")
SAVE_BUTTON    = (By.CSS_SELECTOR, "button[type='submit']")
ACTIVITIES_CARD = (By.XPATH, "//h5[contains(text(),'Activities Done')]")


class TestTC11004:

    # TP-11-004: Verify Edit Activity page GUI elements are displayed correctly.
    # Precondition: user10@fitpal.com must be logged in with at least one
    # "Running, 10 min/mile" cardio activity logged.
    def test_tc11_004_gui_elements(self, fitness_page, wait):
        """TC-11-004: Activity list shows on Fitness Page and Edit modal displays correctly."""
        driver = fitness_page

        logger.info("Step 1: Verify activity list is displayed on Fitness Page")
        activities_header = wait.until(EC.visibility_of_element_located(ACTIVITIES_CARD))
        list_visible = activities_header.is_displayed()

        logger.info(f"Step 2: Verify '{ACTIVITY_NAME}' is shown in the list")
        activity_items = driver.find_elements(
            By.XPATH,
            f"//div[contains(@class,'fw-semibold') and contains(text(),'{ACTIVITY_NAME}')]"
        )
        activity_listed = len(activity_items) > 0

        logger.info(f"Step 3: Click on activity '{ACTIVITY_NAME}'")
        if not activity_listed:
            log_result("TC-11-004", "FAIL", f"Activity '{ACTIVITY_NAME}' not found in list — log it first")
            print(f"FAIL: Activity '{ACTIVITY_NAME}' not found. Please log it in the app first.")
            assume(False, f"Precondition failed: '{ACTIVITY_NAME}' not in activity list")
            return
        activity_items[0].click()

        logger.info("Step 4: Verify modal title shows activity name")
        modal_title_el = wait.until(EC.visibility_of_element_located(MODAL_TITLE))
        modal_correct = ACTIVITY_NAME in modal_title_el.text

        logger.info("Step 5: Click Edit button and verify edit form fields are shown")
        driver.find_element(*EDIT_BUTTON).click()
        date_shown     = len(driver.find_elements(*DATE_INPUT)) > 0
        time_shown     = len(driver.find_elements(*TIME_INPUT)) > 0
        duration_shown = len(driver.find_elements(*DURATION_INPUT)) > 0
        save_shown     = len(driver.find_elements(*SAVE_BUTTON)) > 0

        passed = all([list_visible, activity_listed, modal_correct,
                      date_shown, time_shown, duration_shown, save_shown])

        assume(passed, "Expected all GUI elements to be visible on Fitness Page and Edit modal")
        log_result("TC-11-004", "PASS" if passed else "FAIL",
                   f"List={list_visible}, Activity={activity_listed}, Modal={modal_correct}, "
                   f"Date={date_shown}, Time={time_shown}, Duration={duration_shown}, Save={save_shown}")

        if passed:
            print("PASS: All GUI elements displayed correctly on Fitness Page and Edit modal")
        else:
            print(f"FAIL: Some GUI elements missing. "
                  f"List={list_visible}, Activity={activity_listed}, Modal={modal_correct}, "
                  f"Date={date_shown}, Time={time_shown}, Duration={duration_shown}, Save={save_shown}")
