"""
TP-10-001 / TC-10-001 — Valid workout and cardio activity logging with BVA.

Covered: TCOV-10-001, TCOV-10-008, TCOV-10-009, TCOV-10-011, TCOV-10-012
"""

import logging

import pytest

log = logging.getLogger(__name__)

TEST_DATE = "2026-06-05"
TEST_TIME = "09:00"

WORKOUT_LOG_CASES = [
    pytest.param("Bench Press", "4", "12", id="main_flow"),
    pytest.param("Bench Press", "1", "1", id="sets_reps_min_boundary"),
    pytest.param("Bench Press", "99", "99", id="sets_reps_max_boundary"),
]

CARDIO_DURATION_CASES = [
    pytest.param("1", id="duration_min_boundary"),
    pytest.param("999", id="duration_max_boundary"),
]


def _find_workout(logs, date, name, sets, reps):
    for entry in logs:
        if entry.get("date") != date:
            continue
        for workout in entry.get("workout", []):
            if (
                workout.get("name") == name
                and workout.get("sets") == sets
                and workout.get("reps") == reps
            ):
                return workout
    return None


def _find_cardio(logs, date, name, duration):
    for entry in logs:
        if entry.get("date") != date:
            continue
        for cardio in entry.get("cardio", []):
            if cardio.get("name") == name and cardio.get("duration") == duration:
                return cardio
    return None


@pytest.mark.f010
@pytest.mark.tp_10_001
class TestTp10001ValidLogActivity:
    """TP-10-001: Verify valid activity logging and boundary values are accepted."""

    @pytest.mark.parametrize("exercise,sets,reps", WORKOUT_LOG_CASES)
    def test_tc_10_001_valid_workout_log(
        self, fitness_page, fetch_user_exercises, exercise, sets, reps, request
    ):
        case_label = (
            f"{request.node.callspec.id} "
            f"(exercise={exercise!r}, sets={sets}, reps={reps})"
        )
        log.info("[TP-10-001] Running %s", case_label)

        try:
            fitness_page.save_workout_log(
                exercise, TEST_DATE, TEST_TIME, sets, reps
            )
            fitness_page.wait_for_exercise_logged_toast()
            fitness_page.wait_for_log_modal_closed(exercise)
            fitness_page.assert_activity_visible_in_list(exercise)

            logs = fetch_user_exercises(fitness_page.driver)
            saved = _find_workout(
                logs, TEST_DATE, exercise, int(sets), int(reps)
            )
            assert saved is not None, (
                f"Expected workout log for {exercise} with sets={sets}, reps={reps}"
            )
        except AssertionError as exc:
            log.error("[TP-10-001] FAIL — %s: %s", case_label, exc)
            raise

        log.info("[TP-10-001] PASS — %s", case_label)

    @pytest.mark.parametrize("duration", CARDIO_DURATION_CASES)
    def test_tc_10_001_valid_cardio_duration_boundaries(
        self, fitness_page, fetch_user_exercises, duration, request
    ):
        exercise = "Walking, 2mph"
        case_label = f"{request.node.callspec.id} (duration={duration})"
        log.info("[TP-10-001] Running %s", case_label)

        try:
            fitness_page.save_cardio_log(
                exercise, TEST_DATE, TEST_TIME, duration
            )
            fitness_page.wait_for_exercise_logged_toast()
            fitness_page.wait_for_log_modal_closed(exercise)
            fitness_page.assert_activity_visible_in_list(exercise)

            logs = fetch_user_exercises(fitness_page.driver)
            saved = _find_cardio(logs, TEST_DATE, exercise, int(duration))
            assert saved is not None, (
                f"Expected cardio log for {exercise} with duration={duration}"
            )
        except AssertionError as exc:
            log.error("[TP-10-001] FAIL — %s: %s", case_label, exc)
            raise

        log.info("[TP-10-001] PASS — %s", case_label)
