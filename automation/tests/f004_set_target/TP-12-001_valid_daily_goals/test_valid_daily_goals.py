"""
TP-12-001 / TC-12-001 — Valid daily goals for steps and activity minutes.

Covered: TCOV-12-001, TCOV-12-003, TCOV-12-004, TCOV-12-005,
         TCOV-12-007, TCOV-12-008, TCOV-12-010, TCOV-12-011, TCOV-12-012
"""

import logging

import pytest

log = logging.getLogger(__name__)

VALID_TARGET_CASES = [
    (10000, 60),
    (5000, 45),
    (1, 1),
    (100000, 100000),
]


@pytest.mark.f012
@pytest.mark.tp_12_001
class TestTp12001ValidTargets:
    """TP-12-001: Verify systems can set valid daily goals."""

    def test_tc_12_001_valid_daily_targets(self, fitness_page, fetch_user_goals):
        for index, (steps, workout_minutes) in enumerate(VALID_TARGET_CASES, start=1):
            case_label = (
                f"Case {index}/{len(VALID_TARGET_CASES)}: "
                f"steps={steps}, workout_minutes={workout_minutes}"
            )
            log.info("[TP-12-001] Running %s", case_label)

            try:
                fitness_page.open_set_target_modal()
                fitness_page.assert_set_target_modal_visible()
                fitness_page.save_targets(str(steps), str(workout_minutes))

                fitness_page.wait_for_success_toast()
                fitness_page.wait_for_modal_closed()

                goals = fetch_user_goals(fitness_page.driver)
                assert goals["steps"] == steps, (
                    f"Expected dailyTargetSteps={steps}, got {goals['steps']}"
                )
                assert goals["activity"] == workout_minutes, (
                    f"Expected dailyTargetActivity={workout_minutes}, "
                    f"got {goals['activity']}"
                )

                goal_text = fitness_page.get_goal_text_for_tab("steps")
                assert f"/ {steps} steps" in goal_text, (
                    f"Expected progress to show '/ {steps} steps', got: {goal_text!r}"
                )
            except AssertionError as exc:
                log.error("[TP-12-001] FAIL — %s: %s", case_label, exc)
                raise

            log.info("[TP-12-001] PASS — %s", case_label)
