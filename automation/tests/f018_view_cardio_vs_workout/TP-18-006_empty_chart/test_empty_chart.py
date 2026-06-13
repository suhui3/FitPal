"""
TP-18-006 / TC-18-006 — Empty chart for account with zero activities.

Covered: TCOV-18-012

Input: New account with zero activities.
Precondition: User logged in with no activity logged.
"""

import logging

import pytest

log = logging.getLogger(__name__)


@pytest.mark.f018
@pytest.mark.tp_18_006
class TestTp18006EmptyChart:
    """TP-18-006: Verify empty chart for account with zero activities."""

    def test_tc_18_006_empty_chart_zero_activities(
        self, empty_account_cardio_page, fetch_cardio_workout_summary
    ):
        case_label = "zero-activity account → empty chart displayed"
        log.info("[TP-18-006] Running %s", case_label)

        try:
            empty_account_cardio_page.assert_daily_view()
            empty_account_cardio_page.assert_cardio_line_chart()

            summary = fetch_cardio_workout_summary(
                empty_account_cardio_page.driver,
                mode="daily",
                startDate="2000-01-01",
                endDate="2100-12-31",
            )
            assert summary == [], (
                "API should return no activity data for account with zero activities; "
                f"got: {summary!r}"
            )
        except AssertionError as exc:
            log.error("[TP-18-006] FAIL — %s: %s", case_label, exc)
            raise

        log.info("[TP-18-006] PASS — %s", case_label)
