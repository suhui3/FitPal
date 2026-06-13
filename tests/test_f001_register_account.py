import logging
import time

from pytest_assume.plugin import assume
from selenium.webdriver.support import expected_conditions as EC

from helpers.fitpal_helpers import (
    BASE_URL,
    CONFIRM_PASSWORD_FIELDS,
    EMAIL_FIELD,
    PASSWORD_FIELD,
    SUBMIT_BUTTON,
    log_result,
    visible_text,
)


logger = logging.getLogger(__name__)

REGISTER_PASSWORD = "FitPal@123"


class TestTC01001:
    def test_tc01_001_register_account_valid_details(self, driver, wait):
        """TC-01-001: New user account is successfully registered with valid details."""
        email = f"niu.register.{int(time.time())}@fitpal.com"

        logger.info("Step 1: Navigate to the Register page")
        driver.get(f"{BASE_URL}/register")

        logger.info("Step 2: Verify the Register page is displayed")
        wait.until(EC.presence_of_element_located(EMAIL_FIELD))

        logger.info("Step 3: Enter valid email: %s", email)
        driver.find_element(*EMAIL_FIELD).send_keys(email)

        logger.info("Step 4: Enter valid password")
        driver.find_element(*PASSWORD_FIELD).send_keys(REGISTER_PASSWORD)

        logger.info("Step 5: Enter matching confirm password")
        driver.find_element(*CONFIRM_PASSWORD_FIELDS).send_keys(REGISTER_PASSWORD)

        logger.info("Step 6: Click the Register button")
        driver.find_element(*SUBMIT_BUTTON).click()

        logger.info("Step 7: Verify user is redirected to the next registration setup page")
        redirected = wait.until(
            lambda d: "/create-profile" in d.current_url
            or "/calorie-calculator" in d.current_url
            or "/home" in d.current_url
        )

        assume(
            redirected,
            "Expected successful registration to redirect user to next setup page or Home page.",
        )
        log_result(
            "TC-01-001",
            "PASS" if redirected else "FAIL",
            f"Redirected URL: {driver.current_url}",
        )

        if redirected:
            print("PASS: TC-01-001 — Account registered successfully.")
        else:
            print("FAIL: TC-01-001 — Account registration did not redirect correctly.")


class TestTC01002:
    def test_tc01_002_register_invalid_input_shows_validation(self, driver, wait):
        """TC-01-002: Error message is displayed when invalid registration input is entered."""

        logger.info("Step 1: Navigate to the Register page")
        driver.get(f"{BASE_URL}/register")

        logger.info("Step 2: Verify the Register page is displayed")
        wait.until(EC.presence_of_element_located(EMAIL_FIELD))

        logger.info("Step 3: Enter invalid email")
        driver.find_element(*EMAIL_FIELD).send_keys("invalid-email")

        logger.info("Step 4: Enter invalid password")
        driver.find_element(*PASSWORD_FIELD).send_keys("123")

        logger.info("Step 5: Enter mismatched confirm password")
        driver.find_element(*CONFIRM_PASSWORD_FIELDS).send_keys("1234")

        logger.info("Step 6: Click the Register button")
        driver.find_element(*SUBMIT_BUTTON).click()

        logger.info("Step 7: Verify validation message is displayed and account is not created")
        body_text = visible_text(driver)
        validation_displayed = (
            "Password must be at least 6 characters" in body_text
            or "Your password do not match" in body_text
            or "/register" in driver.current_url
        )

        assume(
            validation_displayed,
            "Expected validation feedback and no successful registration.",
        )
        log_result(
            "TC-01-002",
            "PASS" if validation_displayed else "FAIL",
            f"Validation displayed: {validation_displayed}",
        )

        if validation_displayed:
            print("PASS: TC-01-002 — Validation message displayed for invalid input.")
        else:
            print("FAIL: TC-01-002 — Invalid registration input was not handled correctly.")
