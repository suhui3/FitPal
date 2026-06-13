"""
TP-18-001 / TC-18-001 — Default Cardio line chart in Daily view.

Covered: TCOV-18-001, TCOV-18-004, TCOV-18-005, TCOV-18-008

Input: Email user@test.com, Password FitPal@123
Precondition: User logged in with at least one activity logged.
"""

import logging

import pytest

log = logging.getLogger(__name__)


@pytest.mark.f018
@pytest.mark.tp_18_001
class TestTp18001CardioDailyDefault:
    """TP-18-001: Verify users can view total cardio activity daily."""

    def test_tc_18_001_cardio_line_chart_daily_default(self, cardio_vs_workout_page):
        case_label = "default Cardio line chart in Daily view"
        log.info("[TP-18-001] Running %s", case_label)

        try:
            cardio_vs_workout_page.assert_daily_view()
            cardio_vs_workout_page.assert_cardio_line_chart()
        except AssertionError as exc:
            log.error("[TP-18-001] FAIL — %s: %s", case_label, exc)
            raise

        log.info("[TP-18-001] PASS — %s", case_label)
