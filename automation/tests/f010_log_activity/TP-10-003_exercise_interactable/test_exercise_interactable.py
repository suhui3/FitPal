"""
TP-10-003 / TC-10-003 — Exercise items are interactable on the Fitness Page.

Covered: TCOV-10-003
"""

import logging

import pytest

log = logging.getLogger(__name__)

EXERCISE = "Bench Press"


@pytest.mark.f010
@pytest.mark.tp_10_003
class TestTp10003ExerciseInteractable:
    """TP-10-003: Verify exercise items open the log activity modal."""

    def test_tc_10_003_exercise_item_opens_log_modal(self, fitness_page):
        case_label = f"click {EXERCISE!r} on Fitness Page"
        log.info("[TP-10-003] Running %s", case_label)

        try:
            fitness_page.search_exercise(EXERCISE)
            fitness_page.click_exercise(EXERCISE)
            fitness_page.assert_log_modal_visible(EXERCISE)
        except AssertionError as exc:
            log.error("[TP-10-003] FAIL — %s: %s", case_label, exc)
            raise

        log.info("[TP-10-003] PASS — %s", case_label)
