"""
TP-10-006 / TC-10-006 — Success toast appears after saving an activity.

Covered: TCOV-10-006
"""

import logging

import pytest

log = logging.getLogger(__name__)

TEST_DATE = "2026-06-05"
TEST_TIME = "09:00"
EXERCISE = "Bench Press"


@pytest.mark.f010
@pytest.mark.tp_10_006
class TestTp10006SuccessToast:
    """TP-10-006: Verify success toast after logging a workout activity."""

    def test_tc_10_006_exercise_logged_toast_displayed(self, fitness_page):
        case_label = f"log {EXERCISE!r} and verify success toast"
        log.info("[TP-10-006] Running %s", case_label)

        try:
            fitness_page.save_workout_log(
                EXERCISE, TEST_DATE, TEST_TIME, "4", "12"
            )
            fitness_page.wait_for_exercise_logged_toast()
            fitness_page.wait_for_log_modal_closed(EXERCISE)
        except AssertionError as exc:
            log.error("[TP-10-006] FAIL — %s: %s", case_label, exc)
            raise

        log.info("[TP-10-006] PASS — %s", case_label)
