"""
TP-12-003 / TC-12-003 — Unauthenticated users cannot access Set Target.

Covered: TCOV-12-014
"""

import logging

import pytest

from pages.fitness_page import FitnessPage

log = logging.getLogger(__name__)


@pytest.mark.f012
@pytest.mark.tp_12_003
class TestTp12003UnauthenticatedAccess:
    """TP-12-003: Verify unauthenticated users cannot access the fitness page."""

    def test_tc_12_003_unauthenticated_cannot_access_fitness(self, driver, base_url):
        case_label = "unauthenticated direct /fitness access"
        log.info("[TP-12-003] Running %s", case_label)

        try:
            driver.delete_all_cookies()

            page = FitnessPage(driver, base_url)
            page.open_fitness_without_login()

            assert not page.is_fitness_page_loaded(), (
                "Fitness page should not be viewable without an active session"
            )
            assert page.is_access_denied(), (
                "User should be redirected to landing or sign-in when unauthenticated"
            )
        except AssertionError as exc:
            log.error("[TP-12-003] FAIL — %s: %s", case_label, exc)
            raise

        log.info("[TP-12-003] PASS — %s", case_label)
