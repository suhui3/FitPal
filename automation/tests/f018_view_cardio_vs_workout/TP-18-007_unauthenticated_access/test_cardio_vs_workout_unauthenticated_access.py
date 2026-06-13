"""
TP-18-007 / TC-18-007 — Unauthenticated users cannot view Cardio vs Workout.

Covered: TCOV-18-013

Input: Open Cardio vs Workout URL with no session.
"""

import logging

import pytest

from pages.cardio_vs_workout_page import CardioVsWorkoutPage

log = logging.getLogger(__name__)


@pytest.mark.f018
@pytest.mark.tp_18_007
class TestTp18007UnauthenticatedAccess:
    """TP-18-007: Verify unauthenticated users cannot view Cardio vs Workout."""

    def test_tc_18_007_unauthenticated_cannot_access_cardio_vs_workout(
        self, driver, base_url
    ):
        case_label = "unauthenticated direct /cardio-vs-workout access"
        log.info("[TP-18-007] Running %s", case_label)

        try:
            driver.delete_all_cookies()

            page = CardioVsWorkoutPage(driver, base_url)
            page.open_without_login()

            assert not page.is_page_loaded(), (
                "Cardio vs Workout page should not be viewable without an active session"
            )
            assert page.is_access_denied(), (
                "User should be redirected to landing or sign-in when unauthenticated"
            )
        except AssertionError as exc:
            log.error("[TP-18-007] FAIL — %s: %s", case_label, exc)
            raise

        log.info("[TP-18-007] PASS — %s", case_label)
