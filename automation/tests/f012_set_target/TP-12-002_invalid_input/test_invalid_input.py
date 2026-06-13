"""
TP-12-002 / TC-12-002 — Invalid input shows error feedback.

Covered: TCOV-12-002, TCOV-12-006, TCOV-12-009, TCOV-12-013

Note: Current app may block some cases via HTML5 validation or accept 0/negative
values server-side. Tests assert TCS-expected rejection (error toast or blocked save).
"""

import logging

import pytest
from _pytest.outcomes import Failed
from selenium.common.exceptions import TimeoutException

log = logging.getLogger(__name__)

INVALID_TARGET_CASES = [
    pytest.param("0", "60", id="steps_zero"),
    pytest.param("", "60", id="steps_blank"),
    pytest.param("10000", "-5", id="minutes_negative"),
    pytest.param("10000", "0", id="minutes_zero"),
    pytest.param("10000", "abc", id="minutes_non_numeric"),
]


def _assert_invalid_input_rejected(fitness_page):
    """Expect error toast, or HTML5 validation / modal still open with no success."""
    try:
        fitness_page.wait_for_error_toast(timeout=3)
        return
    except TimeoutException:
        pass

    if fitness_page.is_modal_visible():
        fitness_page.assert_no_success_toast()
        if fitness_page.has_html5_validation_error():
            return
        pytest.fail("Modal stayed open but no error toast or HTML5 validation shown")

    pytest.fail(
        "Expected error toast or blocked save for invalid input; "
        "modal closed without error feedback (app may have accepted invalid values)"
    )


@pytest.mark.f012
@pytest.mark.tp_12_002
class TestTp12002InvalidInput:
    """TP-12-002: Verify error message for invalid input."""

    @pytest.mark.parametrize("steps,workout_minutes", INVALID_TARGET_CASES)
    def test_tc_12_002_invalid_input_rejected(
        self, fitness_page, steps, workout_minutes, request
    ):
        case_label = (
            f"{request.node.callspec.id} "
            f"(steps={steps!r}, workout_minutes={workout_minutes!r})"
        )
        log.info("[TP-12-002] Running %s", case_label)

        try:
            fitness_page.open_set_target_modal()
            fitness_page.assert_set_target_modal_visible()

            if workout_minutes == "abc":
                fitness_page.fill_targets(steps, "")
                fitness_page.set_minutes_value_js("abc")
            else:
                fitness_page.fill_targets(steps, workout_minutes)

            fitness_page.click_save_target()
            _assert_invalid_input_rejected(fitness_page)
        except (AssertionError, Failed) as exc:
            log.error("[TP-12-002] FAIL — %s: %s", case_label, exc)
            raise

        log.info("[TP-12-002] PASS — %s", case_label)
