"""
TP-10-002 / TC-10-002 — Invalid activity details are rejected.

Covered: TCOV-10-002, TCOV-10-007, TCOV-10-010
"""

import logging

import pytest
from _pytest.outcomes import Failed
from selenium.common.exceptions import TimeoutException

log = logging.getLogger(__name__)

TEST_DATE = "2026-06-05"
TEST_TIME = "09:00"

INVALID_INPUT_CASES = [
    pytest.param(
        "Walking, 2mph",
        "0",
        None,
        None,
        id="cardio_duration_zero",
    ),
    pytest.param(
        "Walking, 2mph",
        "-10",
        None,
        None,
        id="cardio_duration_negative",
    ),
    pytest.param(
        "Bench Press",
        None,
        "0",
        "0",
        id="workout_sets_reps_zero",
    ),
]


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
@pytest.mark.tp_10_002
class TestTp10002InvalidActivityDetails:
    """TP-10-002: Verify invalid cardio duration and workout sets/reps are rejected."""

    @pytest.mark.parametrize(
        "exercise,duration,sets,reps", INVALID_INPUT_CASES
    )
    def test_tc_10_002_invalid_activity_details_rejected(
        self, fitness_page, exercise, duration, sets, reps, request
    ):
        case_label = f"{request.node.callspec.id} (exercise={exercise!r})"
        log.info("[TP-10-002] Running %s", case_label)

        try:
            fitness_page.open_exercise_log_modal(exercise)

            if duration is not None:
                fitness_page.fill_cardio_log(TEST_DATE, TEST_TIME, duration)
            else:
                fitness_page.fill_workout_log(TEST_DATE, TEST_TIME, sets, reps)

            fitness_page.click_save_log()
            _assert_invalid_log_rejected(fitness_page, exercise)
        except (AssertionError, Failed) as exc:
            log.error("[TP-10-002] FAIL — %s: %s", case_label, exc)
            raise

        log.info("[TP-10-002] PASS — %s", case_label)
