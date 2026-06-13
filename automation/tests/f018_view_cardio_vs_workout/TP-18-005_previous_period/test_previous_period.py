"""
TP-18-005 / TC-18-005 — Previous-period navigation shows earlier timeframe.

Covered: TCOV-18-007

Input: Email user@test.com, Password FitPal@123
       Click previous arrow; verify earlier period
Precondition: User logged in with at least one activity logged.
"""

import logging

import pytest

log = logging.getLogger(__name__)


@pytest.mark.f018
@pytest.mark.tp_18_005
class TestTp18005PreviousPeriod:
    """TP-18-005: Verify activity in the previous timeframe is displayed."""

    def test_tc_18_005_previous_period_navigation(self, cardio_vs_workout_page):
        case_label = "click previous arrow → earlier period displayed"
        log.info("[TP-18-005] Running %s", case_label)

        try:
            current_label = cardio_vs_workout_page.get_period_label()
            cardio_vs_workout_page.click_previous_period()
            cardio_vs_workout_page.wait_for_chart_loaded()

            previous_label = cardio_vs_workout_page.get_period_label()
            assert previous_label != current_label, (
                f"Period label should change after previous arrow; "
                f"still showing: {previous_label!r}"
            )
            assert cardio_vs_workout_page.is_page_loaded(), (
                "Chart should remain visible for the previous timeframe"
            )
        except AssertionError as exc:
            log.error("[TP-18-005] FAIL — %s: %s", case_label, exc)
            raise

        log.info("[TP-18-005] PASS — %s", case_label)
