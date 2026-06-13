"""
TP-18-002 / TC-18-002 — Cardio line chart in Weekly view.

Covered: TCOV-18-002, TCOV-18-009

Input: Email user@test.com, Password FitPal@123
       Select 'Cardio' & Select 'Weekly'
Precondition: User logged in with at least one activity logged.
"""

import logging

import pytest

log = logging.getLogger(__name__)


@pytest.mark.f018
@pytest.mark.tp_18_002
class TestTp18002CardioWeekly:
    """TP-18-002: Verify users can view total cardio activity weekly."""

    def test_tc_18_002_cardio_line_chart_weekly(self, cardio_vs_workout_page):
        case_label = "Cardio + Weekly → line chart in Weekly view"
        log.info("[TP-18-002] Running %s", case_label)

        try:
            cardio_vs_workout_page.select_type("cardio")
            cardio_vs_workout_page.select_mode("weekly")
            cardio_vs_workout_page.wait_for_chart_loaded()

            cardio_vs_workout_page.assert_weekly_view()
            cardio_vs_workout_page.assert_cardio_line_chart()
        except AssertionError as exc:
            log.error("[TP-18-002] FAIL — %s: %s", case_label, exc)
            raise

        log.info("[TP-18-002] PASS — %s", case_label)
