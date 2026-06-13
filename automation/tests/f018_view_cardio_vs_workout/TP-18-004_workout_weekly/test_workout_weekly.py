"""
TP-18-004 / TC-18-004 — Workout bar chart in Weekly view.

Covered: TCOV-18-011

Input: Email user@test.com, Password FitPal@123
       Select 'Workout' & Select 'Weekly'
Precondition: User logged in with at least one activity logged.
"""

import logging

import pytest

log = logging.getLogger(__name__)


@pytest.mark.f018
@pytest.mark.tp_18_004
class TestTp18004WorkoutWeekly:
    """TP-18-004: Verify users can view total workout activity weekly."""

    def test_tc_18_004_workout_bar_chart_weekly(self, cardio_vs_workout_page):
        case_label = "Workout + Weekly → bar chart in Weekly view"
        log.info("[TP-18-004] Running %s", case_label)

        try:
            cardio_vs_workout_page.select_type("workout")
            cardio_vs_workout_page.select_mode("weekly")
            cardio_vs_workout_page.wait_for_chart_loaded()

            cardio_vs_workout_page.assert_weekly_view()
            cardio_vs_workout_page.assert_workout_bar_chart()
        except AssertionError as exc:
            log.error("[TP-18-004] FAIL — %s: %s", case_label, exc)
            raise

        log.info("[TP-18-004] PASS — %s", case_label)
