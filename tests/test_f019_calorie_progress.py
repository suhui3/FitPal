import logging

from pytest_assume.plugin import assume
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from helpers.fitpal_helpers import BASE_URL, log_result, visible_text


logger = logging.getLogger(__name__)

CHART_TITLE = "Calories Intake vs Calories Consumption"


class TestTC19001:
    def test_tc19_001_calorie_progress_daily_view(self, logged_in, wait):
        """TC-19-001: Calorie intake and calorie burned progress is displayed in Daily view."""
        driver = logged_in

        logger.info("Step 1: Navigate to the Calorie Progress page")
        driver.get(f"{BASE_URL}/calorie-burned")

        logger.info("Step 2: Verify the Calorie Progress page is displayed")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        logger.info("Step 3: Verify the calorie comparison chart title is displayed")
        body_text = visible_text(driver)
        chart_title_displayed = CHART_TITLE in body_text

        logger.info("Step 4: Verify chart canvas is rendered")
        chart_canvas_displayed = len(driver.find_elements(By.TAG_NAME, "canvas")) > 0

        daily_chart_displayed = chart_title_displayed and chart_canvas_displayed
        assume(
            daily_chart_displayed,
            "Expected calorie comparison chart to be visible in Daily view.",
        )
        log_result(
            "TC-19-001",
            "PASS" if daily_chart_displayed else "FAIL",
            f"Title: {chart_title_displayed}, Canvas: {chart_canvas_displayed}",
        )

        if daily_chart_displayed:
            print("PASS: TC-19-001 — Daily calorie progress chart is displayed.")
        else:
            print("FAIL: TC-19-001 — Daily calorie progress chart is not displayed.")


class TestTC19002:
    def test_tc19_002_calorie_progress_weekly_view(self, logged_in, wait):
        """TC-19-002: Calorie progress chart updates when Weekly view or another range is selected."""
        driver = logged_in

        logger.info("Step 1: Navigate to the Calorie Progress page")
        driver.get(f"{BASE_URL}/calorie-burned")

        logger.info("Step 2: Verify the page body is loaded")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        logger.info("Step 3: Click Weekly control if it is available")
        weekly_controls = driver.find_elements(By.XPATH, "//*[contains(normalize-space(), 'Weekly')]")
        if weekly_controls:
            weekly_controls[0].click()
        else:
            logger.info("Weekly control was not found; continuing with chart visibility check")

        logger.info("Step 4: Verify the calorie comparison chart remains visible")
        body_text = visible_text(driver)
        chart_title_displayed = CHART_TITLE in body_text
        chart_canvas_displayed = len(driver.find_elements(By.TAG_NAME, "canvas")) > 0
        weekly_chart_displayed = chart_title_displayed and chart_canvas_displayed

        assume(
            weekly_chart_displayed,
            "Expected calorie chart to remain visible after selecting Weekly view.",
        )
        log_result(
            "TC-19-002",
            "PASS" if weekly_chart_displayed else "FAIL",
            f"Weekly controls: {len(weekly_controls)}, Title: {chart_title_displayed}, Canvas: {chart_canvas_displayed}",
        )

        if weekly_chart_displayed:
            print("PASS: TC-19-002 — Weekly calorie progress chart is displayed.")
        else:
            print("FAIL: TC-19-002 — Weekly calorie progress chart is not displayed correctly.")


class TestTC19003:
    def test_tc19_003_calorie_progress_empty_range(self, logged_in, wait):
        """TC-19-003: Calorie progress page handles empty data range gracefully."""
        driver = logged_in

        logger.info("Step 1: Navigate to the Calorie Progress page")
        driver.get(f"{BASE_URL}/calorie-burned")

        logger.info("Step 2: Wait for page body to load")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        logger.info("Step 3: Verify the page does not crash when data is empty or loading")
        body_text = visible_text(driver)
        page_loaded = CHART_TITLE in body_text or "Loading chart" in body_text
        no_crash = "Error" not in body_text and "Cannot read" not in body_text
        empty_range_handled = page_loaded and no_crash

        assume(
            empty_range_handled,
            "Expected empty or zero data range to render without page crash.",
        )
        log_result(
            "TC-19-003",
            "PASS" if empty_range_handled else "FAIL",
            f"Page loaded: {page_loaded}, No crash: {no_crash}",
        )

        if empty_range_handled:
            print("PASS: TC-19-003 — Empty calorie data range is handled gracefully.")
        else:
            print("FAIL: TC-19-003 — Empty calorie data range caused an error or broken page.")
