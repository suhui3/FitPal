"""
TP-18-003 / TC-18-003 — Workout bar chart in Daily view.

Covered: TCOV-18-003, TCOV-18-006, TCOV-18-010

Input: Email user@test.com, Password FitPal@123
       Select 'Workout' & Select 'Daily'
Precondition: User logged in with at least one activity logged.
"""

import logging

import pytest

log = logging.getLogger(__name__)


@pytest.mark.f018
@pytest.mark.tp_18_003
class TestTp18003WorkoutDaily:
    """TP-18-003: Verify users can view total workout activity daily."""

    def test_tc_18_003_workout_bar_chart_daily(self, cardio_vs_workout_page):
        case_label = "Workout + Daily → bar chart in Daily view"
        log.info("[TP-18-003] Running %s", case_label)

        try:
            cardio_vs_workout_page.select_type("workout")
            cardio_vs_workout_page.select_mode("daily")
            cardio_vs_workout_page.wait_for_chart_loaded()

            cardio_vs_workout_page.assert_daily_view()
            cardio_vs_workout_page.assert_workout_bar_chart()
        except AssertionError as exc:
            log.error("[TP-18-003] FAIL — %s: %s", case_label, exc)
            raise

        log.info("[TP-18-003] PASS — %s", case_label)
