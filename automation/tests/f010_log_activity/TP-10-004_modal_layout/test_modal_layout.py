"""
TP-10-004 / TC-10-004 — Logging modal shows correct input fields and Save button.

Covered: TCOV-10-004
"""

import logging

import pytest

log = logging.getLogger(__name__)

MODAL_LAYOUT_CASES = [
    pytest.param("Squats", id="squats_workout_modal"),
    pytest.param("Bench Press", id="bench_press_workout_modal"),
]


@pytest.mark.f010
@pytest.mark.tp_10_004
class TestTp10004ModalLayout:
    """TP-10-004: Verify logging modal layout for workout activities."""

    @pytest.mark.parametrize("exercise", MODAL_LAYOUT_CASES)
    def test_tc_10_004_workout_modal_fields_visible(self, fitness_page, exercise, request):
        case_label = f"{request.node.callspec.id} (exercise={exercise!r})"
        log.info("[TP-10-004] Running %s", case_label)

        try:
            fitness_page.open_exercise_log_modal(exercise)
            fitness_page.assert_workout_log_modal_fields(exercise)
        except AssertionError as exc:
            log.error("[TP-10-004] FAIL — %s: %s", case_label, exc)
            raise

        log.info("[TP-10-004] PASS — %s", case_label)
