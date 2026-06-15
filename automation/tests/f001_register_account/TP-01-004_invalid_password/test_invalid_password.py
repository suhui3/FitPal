"""
TP-01-004 / TC-01-004 — Invalid password shows error feedback.

Covered: TCOV-01-011, TCOV-01-012, TCOV-01-013

Note: Current app enforces minimum length (6) only. Passwords missing uppercase
or special characters may be accepted server-side; tests assert TCS-expected
rejection (inline error, HTML5 validation, error toast, or blocked navigation).
"""

import logging

import pytest
from _pytest.outcomes import Failed
from selenium.common.exceptions import TimeoutException

log = logging.getLogger(__name__)

INVALID_PASSWORD_CASES = [
    pytest.param("fitpal@123", id="missing_uppercase"),
    pytest.param("FitPal123", id="missing_special_character"),
    pytest.param("P@ss1", id="below_minimum_length"),
]


def _assert_password_rejected(register_page):
    try:
        register_page.wait_for_create_profile_page()
        pytest.fail(
            "Registration succeeded but invalid password was expected to be rejected"
        )
    except TimeoutException:
        pass

    register_page.assert_registration_rejected()


@pytest.mark.f001
@pytest.mark.tp_01_004
class TestTp01004InvalidPassword:
    """TP-01-004: Verify invalid passwords are rejected with error feedback."""

    @pytest.mark.parametrize("password", INVALID_PASSWORD_CASES)
    def test_tc_01_004_invalid_password_rejected(self, register_page, password, request):
        email = register_page.unique_email("user2@test.com")
        case_label = f"{request.node.callspec.id} (email={email!r}, password={password!r})"
        log.info("[TP-01-004] Running %s", case_label)

        try:
            register_page.open()
            register_page.register(email, password)
            _assert_password_rejected(register_page)
        except (AssertionError, Failed) as exc:
            log.error("[TP-01-004] FAIL — %s: %s", case_label, exc)
            raise

        log.info("[TP-01-004] PASS — %s", case_label)
