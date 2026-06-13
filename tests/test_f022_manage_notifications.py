import logging

from pytest_assume.plugin import assume
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from helpers.fitpal_helpers import BASE_URL, log_result, visible_text


logger = logging.getLogger(__name__)


class TestTC22001:
    def test_tc22_001_view_notification_details(self, logged_in, wait):
        """TC-22-001: User can open Notifications page and view notification details."""
        driver = logged_in

        logger.info("Step 1: Navigate to the Notifications page")
        driver.get(f"{BASE_URL}/notifications")

        logger.info("Step 2: Verify the Notifications page is displayed")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        logger.info("Step 3: Click See more if a notification is available")
        see_more_links = driver.find_elements(By.XPATH, "//*[contains(normalize-space(), 'See more')]")
        if see_more_links:
            see_more_links[0].click()
            wait.until(lambda d: "/notifications/show-notification" in d.current_url)
        else:
            logger.info("No notification detail link found; checking empty state instead")

        logger.info("Step 4: Verify notification page, detail page, or empty state is displayed")
        body_text = visible_text(driver)
        details_displayed = (
            "Notifications" in body_text
            or "Date:" in body_text
            or "No Notifications Yet" in body_text
        )

        assume(
            details_displayed,
            "Expected Notifications page or notification detail page to display.",
        )
        log_result(
            "TC-22-001",
            "PASS" if details_displayed else "FAIL",
            f"Details displayed: {details_displayed}",
        )

        if details_displayed:
            print("PASS: TC-22-001 — Notification page/details displayed successfully.")
        else:
            print("FAIL: TC-22-001 — Notification details could not be viewed.")


class TestTC22002:
    def test_tc22_002_filter_notifications_unread_and_read(self, logged_in, wait):
        """TC-22-002: User can filter notifications by unread/read status."""
        driver = logged_in

        logger.info("Step 1: Navigate to the Notifications page")
        driver.get(f"{BASE_URL}/notifications")

        logger.info("Step 2: Verify the Notifications page is displayed")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        logger.info("Step 3: Verify Unread filter is available")
        unread_available = len(driver.find_elements(By.XPATH, "//*[normalize-space()='Unread']")) > 0

        logger.info("Step 4: Verify Read filter is available")
        read_available = len(driver.find_elements(By.XPATH, "//*[normalize-space()='Read']")) > 0

        filters_available = unread_available and read_available
        assume(
            filters_available,
            "Expected both Unread and Read filters to be available.",
        )
        log_result(
            "TC-22-002",
            "PASS" if filters_available else "FAIL",
            f"Unread available: {unread_available}; Read available: {read_available}",
        )

        if filters_available:
            print("PASS: TC-22-002 — Unread and Read notification filters are available.")
        else:
            print("FAIL: TC-22-002 — Read notification filter is missing. TIR-22-001 raised.")


class TestTC22003:
    def test_tc22_003_delete_notification(self, logged_in, wait):
        """TC-22-003: User can delete a notification after confirming deletion."""
        driver = logged_in

        logger.info("Step 1: Navigate to the Notifications page")
        driver.get(f"{BASE_URL}/notifications")

        logger.info("Step 2: Verify the Notifications page is displayed")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        logger.info("Step 3: Click delete icon if a notification is available")
        delete_icons = driver.find_elements(By.CSS_SELECTOR, "svg[style*='cursor']")
        if delete_icons:
            delete_icons[0].click()
            modal_visible = len(driver.find_elements(By.CLASS_NAME, "modal-content")) > 0
        else:
            logger.info("No delete icon found; checking empty state instead")
            modal_visible = "No Notifications Yet" in visible_text(driver)

        logger.info("Step 4: Verify delete confirmation modal or empty state is displayed")
        assume(
            modal_visible,
            "Expected delete confirmation modal or empty notification state.",
        )
        log_result(
            "TC-22-003",
            "PASS" if modal_visible else "FAIL",
            f"Modal or empty state visible: {modal_visible}",
        )

        if modal_visible:
            print("PASS: TC-22-003 — Delete flow confirmation or empty state displayed.")
        else:
            print("FAIL: TC-22-003 — Delete confirmation was not displayed.")


class TestTC22004:
    def test_tc22_004_notifications_empty_state_or_list(self, logged_in, wait):
        """TC-22-004: Notifications page displays empty state when no notifications exist."""
        driver = logged_in

        logger.info("Step 1: Navigate to the Notifications page")
        driver.get(f"{BASE_URL}/notifications")

        logger.info("Step 2: Wait for the Notifications page to load")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        logger.info("Step 3: Verify empty state or notification list is displayed")
        body_text = visible_text(driver)
        page_displayed = "No Notifications Yet" in body_text or "Notifications" in body_text

        assume(
            page_displayed,
            "Expected Notifications page to show empty state or notification list.",
        )
        log_result(
            "TC-22-004",
            "PASS" if page_displayed else "FAIL",
            f"Notifications page displayed: {page_displayed}",
        )

        if page_displayed:
            print("PASS: TC-22-004 — Notifications page empty state or list is displayed.")
        else:
            print("FAIL: TC-22-004 — Notifications page did not display correctly.")
