import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

BASE_URL = "http://localhost:5173"
SIGN_IN_URL = f"{BASE_URL}/sign-in"

# Credentials from test spec
VALID_EMAIL = "user10@fitpal.com"
VALID_PASSWORD = "Password@123"
WRONG_PASSWORD = "WrongPass@99"


class TestF002Login(unittest.TestCase):

    def setUp(self):
        options = Options()
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def _open_sign_in(self):
        self.driver.get(SIGN_IN_URL)
        self.wait.until(EC.presence_of_element_located((By.ID, "formBasicEmail")))

    def _fill_and_submit(self, email, password):
        self.driver.find_element(By.ID, "formBasicEmail").send_keys(email)
        self.driver.find_element(By.ID, "formBasicPassword").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # TC-02-001: Valid credentials — user is redirected to Home Page
    # Precondition: account user@fitpal.com must be active and registered
    def test_TC_02_001_valid_login_redirects_to_home(self):
        self._open_sign_in()
        self._fill_and_submit(VALID_EMAIL, VALID_PASSWORD)

        self.wait.until(EC.url_contains("/home"))
        self.assertIn("/home", self.driver.current_url,
                      "Expected redirect to /home after successful login")

    # TC-02-002: Deactivated account — reactivation modal is shown
    # Precondition: account user@fitpal.com must be deactivated in the database
    def test_TC_02_002_deactivated_account_shows_modal(self):
        self._open_sign_in()
        self._fill_and_submit(VALID_EMAIL, VALID_PASSWORD)

        modal_title = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal-title"))
        )
        self.assertIn("Reactivate Account", modal_title.text,
                      "Expected reactivation modal to appear for deactivated account")

        modal_body = self.driver.find_element(By.CSS_SELECTOR, ".modal-body")
        self.assertIn("deactivated", modal_body.text.lower(),
                      "Expected modal body to mention deactivated account")

    # TC-02-003: Invalid credentials — error toast is displayed
    # Precondition: account user@fitpal.com must be registered in the system
    def test_TC_02_003_invalid_credentials_shows_error(self):
        self._open_sign_in()
        self._fill_and_submit(VALID_EMAIL, WRONG_PASSWORD)

        toast = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".toast-body p"))
        )
        self.assertTrue(toast.is_displayed(),
                        "Expected error toast to be visible")
        self.assertIn("Invalid Credentials", toast.text,
                      "Expected toast to show 'Invalid Credentials' message")


if __name__ == "__main__":
    unittest.main(verbosity=2)
