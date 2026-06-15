"""
TP-01-003 / TC-01-003 — Blank email shows error feedback.

Covered: TCOV-01-010
"""

import logging

import pytest

log = logging.getLogger(__name__)


@pytest.mark.f001
@pytest.mark.tp_01_003
class TestTp01003BlankEmail:
    """TP-01-003: Verify blank email is rejected with an error message."""

    def test_tc_01_003_blank_email_rejected(self, register_page):
        case_label = "email=<blank>, password=FitPal@123"
        log.info("[TP-01-003] Running %s", case_label)

        try:
            register_page.open()
            register_page.register("", "FitPal@123")
            register_page.assert_registration_rejected()
        except AssertionError as exc:
            log.error("[TP-01-003] FAIL — %s: %s", case_label, exc)
            raise

        log.info("[TP-01-003] PASS — %s", case_label)
