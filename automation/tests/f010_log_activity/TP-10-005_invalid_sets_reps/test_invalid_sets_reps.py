"""
TP-10-005 / TC-10-005 — Invalid non-numeric activity details show validation feedback.

Covered: TCOV-10-005
"""

import logging

import pytest
from _pytest.outcomes import Failed
from selenium.common.exceptions import TimeoutException

log = logging.getLogger(__name__)

TEST_DATE = "2026-06-05"
TEST_TIME = "09:00"
EXERCISE = "Walking, 2mph"


def _assert_invalid_log_rejected(fitness_page, exercise_name: str):
    """Expect error toast, or modal still open with no success toast."""
    try:
        fitness_page.wait_for_log_error_toast(timeout=3)
        return
    except TimeoutException:
        pass

    if fitness_page.is_log_modal_visible(exercise_name):
        fitness_page.assert_no_exercise_logged_toast()
        if fitness_page.has_log_modal_html5_validation_error():
            return
        pytest.fail(
            "Modal stayed open but no error toast or HTML5 validation shown"
        )

    pytest.fail(
        "Expected error feedback for invalid log input; "
        "modal closed without rejection (app may have accepted invalid values)"
    )


@pytest.mark.f010
@pytest.mark.tp_10_005
class TestTp10005InvalidNonNumericInput:
    """TP-10-005: Verify non-numeric duration input is rejected."""

    def test_tc_10_005_duration_abc_rejected(self, fitness_page):
        case_label = f"{EXERCISE}, duration=abc"
        log.info("[TP-10-005] Running %s", case_label)

        try:
            fitness_page.open_exercise_log_modal(EXERCISE)
            fitness_page.fill_cardio_log(TEST_DATE, TEST_TIME, "")
            fitness_page.set_log_field_value_js("Duration (minutes)", "abc")
            fitness_page.click_save_log()
            _assert_invalid_log_rejected(fitness_page, EXERCISE)
        except (AssertionError, Failed) as exc:
            log.error("[TP-10-005] FAIL — %s: %s", case_label, exc)
            raise

        log.info("[TP-10-005] PASS — %s", case_label)
