"""
TP-01-001 / TC-01-001 — Valid registration with standard and boundary passwords.

Covered: TCOV-01-001, TCOV-01-003, TCOV-01-004, TCOV-01-006, TCOV-01-007,
         TCOV-01-008, TCOV-01-014, TCOV-01-015
"""

import logging

import pytest

log = logging.getLogger(__name__)

VALID_REGISTRATION_CASES = [
    pytest.param("newuser@test.com", "FitPal@123", id="standard_valid"),
    pytest.param("testPw1@fitpal.com", "P@ss12", id="password_min_boundary"),
    pytest.param(
        "testPw2@fitpal.com",
        "P@ss1234P@ss1234P@ss1234P@ss1234",
        id="password_max_boundary",
    ),
]


@pytest.mark.f001
@pytest.mark.tp_01_001
class TestTp01001ValidRegistration:
    """TP-01-001: Verify successful registration through onboarding to Home."""

    @pytest.mark.parametrize("email,password", VALID_REGISTRATION_CASES)
    def test_tc_01_001_valid_registration_flow(self, register_page, email, password, request):
        unique_email = register_page.unique_email(email)
        case_label = f"{request.node.callspec.id} (email={unique_email!r})"
        log.info("[TP-01-001] Running %s", case_label)

        try:
            register_page.open()
            register_page.assert_register_form_visible()
            register_page.complete_onboarding(unique_email, password)

            assert "/home" in register_page.driver.current_url, (
                "Expected user to reach Home Page after onboarding"
            )
        except AssertionError as exc:
            log.error("[TP-01-001] FAIL — %s: %s", case_label, exc)
            raise

        log.info("[TP-01-001] PASS — %s", case_label)
