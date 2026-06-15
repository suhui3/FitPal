"""
TP-01-002 / TC-01-002 — Invalid registration input shows error feedback.

Covered: TCOV-01-002, TCOV-01-005, TCOV-01-009
"""

import logging

import pytest

log = logging.getLogger(__name__)


@pytest.mark.f001
@pytest.mark.tp_01_002
class TestTp01002InvalidInput:
    """TP-01-002: Verify account is not created for invalid email and password."""

    def test_tc_01_002_invalid_registration_rejected(self, register_page):
        case_label = "email=missing_at_domain.com, password=123"
        log.info("[TP-01-002] Running %s", case_label)

        try:
            register_page.open()
            register_page.register("missing_at_domain.com", "123")
            register_page.assert_registration_rejected()
            assert register_page.is_on_register_page(), (
                "Account should not be created; user should remain on Register page"
            )
        except AssertionError as exc:
            log.error("[TP-01-002] FAIL — %s: %s", case_label, exc)
            raise

        log.info("[TP-01-002] PASS — %s", case_label)
