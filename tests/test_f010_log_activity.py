import logging

from pytest_assume.plugin import assume
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from helpers.fitpal_helpers import BASE_URL, TOAST, log_result, visible_text


logger = logging.getLogger(__name__)

FITNESS_PAGE_TITLE = "Fitness Tracker"
LOG_EXERCISE_TITLE = "Log Exercise"
WORKOUT_NAME = "Bench Press"
CARDIO_NAME = "Walking, 2mph"
WORKOUT_DATE = "2026-06-05"
WORKOUT_TIME = "09:00"
WORKOUT_SETS = "4"
WORKOUT_REPS = "12"


def _open_fitness_page(driver, wait):
    driver.get(f"{BASE_URL}/fitness")
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))


def _click_exercise(driver, wait, exercise_name):
    exercise = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//*[normalize-space()='{exercise_name}']")
        )
    )
    exercise.click()


def _modal_visible(driver):
    return len(driver.find_elements(By.CLASS_NAME, "modal-content")) > 0


def _workout_inputs(driver):
    return {
        "date": driver.find_element(By.CSS_SELECTOR, ".modal-content input[type='date']"),
        "time": driver.find_element(By.CSS_SELECTOR, ".modal-content input[type='time']"),
        "sets": driver.find_elements(By.CSS_SELECTOR, ".modal-content input[type='number']")[0],
        "reps": driver.find_elements(By.CSS_SELECTOR, ".modal-content input[type='number']")[1],
    }


def _cardio_inputs(driver):
    return {
        "date": driver.find_element(By.CSS_SELECTOR, ".modal-content input[type='date']"),
        "time": driver.find_element(By.CSS_SELECTOR, ".modal-content input[type='time']"),
        "duration": driver.find_element(By.CSS_SELECTOR, ".modal-content input[type='number']"),
    }


class TestTC10001:
    def test_tc10_001_log_activity_main_flow(self, logged_in, wait):
        """TC-10-001: User can log a workout activity with valid details."""
        driver = logged_in

        logger.info("Step 1: Navigate to the Fitness page")
        _open_fitness_page(driver, wait)

        logger.info("Step 2: Click Bench Press exercise")
        _click_exercise(driver, wait, WORKOUT_NAME)

        logger.info("Step 3: Verify logging modal is displayed")
        wait.until(lambda d: _modal_visible(d))

        logger.info(
            "Step 4: Fill in activity details - Date: %s, Start Time: %s, Sets: %s, Reps: %s",
            WORKOUT_DATE,
            WORKOUT_TIME,
            WORKOUT_SETS,
            WORKOUT_REPS,
        )
        inputs = _workout_inputs(driver)
        inputs["date"].send_keys(WORKOUT_DATE)
        inputs["time"].send_keys(WORKOUT_TIME)
        inputs["sets"].send_keys(WORKOUT_SETS)
        inputs["reps"].send_keys(WORKOUT_REPS)

        logger.info("Step 5: Click Save button")
        driver.find_element(By.XPATH, "//button[normalize-space()='Save']").click()

        logger.info("Step 6: Verify activity is saved successfully")
        saved = wait.until(
            lambda d: not _modal_visible(d)
            or len(d.find_elements(*TOAST)) > 0
            or WORKOUT_NAME in visible_text(d)
        )

        assume(saved, "Expected workout activity to be saved successfully.")
        log_result("TC-10-001", "PASS" if saved else "FAIL", f"Saved: {saved}")

        if saved:
            print("PASS: TC-10-001 - Workout activity logged successfully.")
        else:
            print("FAIL: TC-10-001 - Workout activity was not logged successfully.")


class TestTC10002:
    def test_tc10_002_invalid_activity_details_show_error(self, logged_in, wait):
        """TC-10-002: Invalid activity details are rejected by the logging form."""
        driver = logged_in

        logger.info("Step 1: Navigate to the Fitness page")
        _open_fitness_page(driver, wait)

        logger.info("Step 2: Click Walking, 2mph cardio exercise item")
        _click_exercise(driver, wait, CARDIO_NAME)

        logger.info("Step 3: Verify logging modal is displayed")
        wait.until(lambda d: _modal_visible(d))

        logger.info("Step 4: Fill invalid activity details - Duration: -10")
        inputs = _cardio_inputs(driver)
        inputs["date"].send_keys(WORKOUT_DATE)
        inputs["time"].send_keys(WORKOUT_TIME)
        inputs["duration"].send_keys("-10")

        logger.info("Step 5: Click Save button")
        driver.find_element(By.XPATH, "//button[normalize-space()='Save']").click()

        logger.info("Step 6: Verify invalid details are not accepted")
        invalid_rejected = _modal_visible(driver)

        assume(
            invalid_rejected,
            "Expected invalid activity duration to be rejected and modal to remain open.",
        )
        log_result(
            "TC-10-002",
            "PASS" if invalid_rejected else "FAIL",
            f"Invalid rejected: {invalid_rejected}",
        )

        if invalid_rejected:
            print("PASS: TC-10-002 - Invalid activity details were rejected.")
        else:
            print("FAIL: TC-10-002 - Invalid activity details were accepted. TIR-10-001 raised.")


class TestTC10003:
    def test_tc10_003_exercise_items_are_interactable(self, logged_in, wait):
        """TC-10-003: Exercise items are interactable on the Fitness page."""
        driver = logged_in

        logger.info("Step 1: Navigate to the Fitness page")
        _open_fitness_page(driver, wait)

        logger.info("Step 2: Verify the Fitness page and Log Exercise section are displayed")
        body_text = visible_text(driver)
        page_displayed = FITNESS_PAGE_TITLE in body_text and LOG_EXERCISE_TITLE in body_text

        logger.info("Step 3: Click Bench Press exercise item")
        _click_exercise(driver, wait, WORKOUT_NAME)

        logger.info("Step 4: Verify the exercise item opens the logging modal")
        wait.until(lambda d: _modal_visible(d))
        exercise_interactable = page_displayed and _modal_visible(driver)

        assume(
            exercise_interactable,
            "Expected exercise item to be clickable and open the log activity modal.",
        )
        log_result(
            "TC-10-003",
            "PASS" if exercise_interactable else "FAIL",
            f"Page displayed: {page_displayed}, Modal visible: {_modal_visible(driver)}",
        )

        if exercise_interactable:
            print("PASS: TC-10-003 - Exercise item is interactable.")
        else:
            print("FAIL: TC-10-003 - Exercise item did not open the logging modal.")


class TestTC10004:
    def test_tc10_004_logging_modal_fields_visible(self, logged_in, wait):
        """TC-10-004: Logging modal displays required input fields and Save button."""
        driver = logged_in

        logger.info("Step 1: Navigate to the Fitness page")
        _open_fitness_page(driver, wait)

        logger.info("Step 2: Click Bench Press exercise item")
        _click_exercise(driver, wait, WORKOUT_NAME)

        logger.info("Step 3: Verify logging modal is displayed")
        wait.until(lambda d: _modal_visible(d))

        logger.info("Step 4: Verify Date, Start Time, Sets, Reps fields and Save button are visible")
        inputs = _workout_inputs(driver)
        save_visible = driver.find_element(By.XPATH, "//button[normalize-space()='Save']").is_displayed()
        fields_visible = (
            inputs["date"].is_displayed()
            and inputs["time"].is_displayed()
            and inputs["sets"].is_displayed()
            and inputs["reps"].is_displayed()
            and save_visible
        )

        assume(
            fields_visible,
            "Expected logging modal to show Date, Start Time, Sets, Reps fields and Save button.",
        )
        log_result(
            "TC-10-004",
            "PASS" if fields_visible else "FAIL",
            f"Fields visible: {fields_visible}",
        )

        if fields_visible:
            print("PASS: TC-10-004 - Logging modal fields and Save button are visible.")
        else:
            print("FAIL: TC-10-004 - Logging modal is missing required fields.")


class TestTC10005:
    def test_tc10_005_invalid_activity_details_show_error(self, logged_in, wait):
        """TC-10-005: Invalid activity details are rejected by the logging form."""
        driver = logged_in

        logger.info("Step 1: Navigate to the Fitness page")
        _open_fitness_page(driver, wait)

        logger.info("Step 2: Click Bench Press exercise item")
        _click_exercise(driver, wait, WORKOUT_NAME)

        logger.info("Step 3: Verify logging modal is displayed")
        wait.until(lambda d: _modal_visible(d))

        logger.info("Step 4: Fill invalid activity details")
        inputs = _workout_inputs(driver)
        inputs["date"].send_keys(WORKOUT_DATE)
        inputs["time"].send_keys(WORKOUT_TIME)
        inputs["sets"].send_keys("-1")
        inputs["reps"].send_keys("-1")

        logger.info("Step 5: Click Save button")
        driver.find_element(By.XPATH, "//button[normalize-space()='Save']").click()

        logger.info("Step 6: Verify invalid details are not accepted")
        still_on_modal = _modal_visible(driver)
        invalid_rejected = still_on_modal

        assume(
            invalid_rejected,
            "Expected invalid activity details to be rejected and modal to remain open.",
        )
        log_result(
            "TC-10-005",
            "PASS" if invalid_rejected else "FAIL",
            f"Invalid rejected: {invalid_rejected}",
        )

        if invalid_rejected:
            print("PASS: TC-10-005 - Invalid activity details were rejected.")
        else:
            print("FAIL: TC-10-005 - Invalid activity details were accepted. TIR-10-001 raised.")


class TestTC10006:
    def test_tc10_006_success_toast_after_save(self, logged_in, wait):
        """TC-10-006: Success toast message appears after saving a valid activity."""
        driver = logged_in

        logger.info("Step 1: Navigate to the Fitness page")
        _open_fitness_page(driver, wait)

        logger.info("Step 2: Click Bench Press exercise item")
        _click_exercise(driver, wait, WORKOUT_NAME)

        logger.info("Step 3: Fill in valid activity details")
        wait.until(lambda d: _modal_visible(d))
        inputs = _workout_inputs(driver)
        inputs["date"].send_keys(WORKOUT_DATE)
        inputs["time"].send_keys(WORKOUT_TIME)
        inputs["sets"].send_keys(WORKOUT_SETS)
        inputs["reps"].send_keys(WORKOUT_REPS)

        logger.info("Step 4: Click Save button")
        driver.find_element(By.XPATH, "//button[normalize-space()='Save']").click()

        logger.info("Step 5: Verify success toast message appears")
        toast_visible = wait.until(
            lambda d: "Exercise logged!" in visible_text(d) or len(d.find_elements(*TOAST)) > 0
        )

        assume(toast_visible, "Expected success toast message after saving activity.")
        log_result(
            "TC-10-006",
            "PASS" if toast_visible else "FAIL",
            f"Toast visible: {toast_visible}",
        )

        if toast_visible:
            print("PASS: TC-10-006 - Success toast appears after saving activity.")
        else:
            print("FAIL: TC-10-006 - Success toast did not appear after saving activity.")
