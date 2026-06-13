import uuid
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


def _js_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    driver.execute_script("arguments[0].click();", element)


class RegisterPage:
    SUCCESS_TOAST = "Registration successful"
    CALORIE_MODAL_TITLE = "Daily Calorie Target"
    TEST_PROFILE_IMAGE = (
        Path(__file__).resolve().parent.parent / "fixtures" / "test_profile.png"
    )

    def __init__(self, driver, base_url: str):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 15)

    @staticmethod
    def unique_email(base_email: str) -> str:
        local, domain = base_email.split("@", 1)
        return f"{local}+{uuid.uuid4().hex[:8]}@{domain}"

    def open(self):
        self.driver.get(f"{self.base_url}/register")
        self.assert_register_form_visible()

    def _email_input(self):
        return self.driver.find_element(By.CSS_SELECTOR, "input[type='email']")

    def _password_input(self):
        return self.driver.find_element(
            By.XPATH,
            "//label[normalize-space()='Password']/following::input[@type='password' or @type='text'][1]",
        )

    def _confirm_password_input(self):
        return self.driver.find_element(
            By.XPATH,
            "//label[contains(normalize-space(),'Comfirm Password')]/following::input[@type='password' or @type='text'][1]",
        )

    def fill_registration(self, email: str, password: str, confirm_password: str | None = None):
        confirm = confirm_password if confirm_password is not None else password
        self._email_input().clear()
        self._email_input().send_keys(email)
        self._password_input().clear()
        self._password_input().send_keys(password)
        self._confirm_password_input().clear()
        self._confirm_password_input().send_keys(confirm)

    def click_register(self):
        register_btn = self.driver.find_element(
            By.XPATH, "//button[@type='submit' and normalize-space()='Register']"
        )
        _js_click(self.driver, register_btn)

    def register(self, email: str, password: str, confirm_password: str | None = None):
        self.fill_registration(email, password, confirm_password)
        self.click_register()

    def assert_register_form_visible(self):
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
        assert self._password_input().is_displayed()
        assert self._confirm_password_input().is_displayed()
        register_btn = self.driver.find_element(
            By.XPATH, "//button[@type='submit' and normalize-space()='Register']"
        )
        assert register_btn.is_displayed()

    def wait_for_create_profile_page(self):
        self.wait.until(EC.url_contains("/create-profile"))
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//h1[normalize-space()='Create your profile']")
            )
        )

    def fill_profile(
        self,
        first_name: str = "Test",
        last_name: str = "User",
        gender: str = "Male",
        dob: str = "2000-01-01",
        image_path: str | Path | None = None,
    ):
        image = Path(image_path) if image_path else self.TEST_PROFILE_IMAGE
        file_input = self.driver.find_element(By.ID, "fileUpload")
        file_input.send_keys(str(image.resolve()))

        self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='First Name']").clear()
        self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='First Name']").send_keys(
            first_name
        )
        self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Last Name']").clear()
        self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Last Name']").send_keys(
            last_name
        )
        Select(self.driver.find_element(By.CSS_SELECTOR, "select")).select_by_visible_text(gender)
        dob_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='date']")
        self.driver.execute_script("arguments[0].value = '';", dob_input)
        month, day, year = dob.split("-")
        dob_input.send_keys(f"{month}/{day}/{year}")

    def submit_profile(self):
        create_btn = self.driver.find_element(
            By.XPATH, "//button[@type='submit' and normalize-space()='Create']"
        )
        _js_click(self.driver, create_btn)
        self.wait.until(
            lambda d: "/calorie-calculator" in d.current_url
            or d.find_elements(
                By.XPATH,
                "//div[contains(@class,'toast') and contains(@class,'bg-danger')]",
            )
        )

    def wait_for_calorie_calculator_page(self):
        self.wait.until(EC.url_contains("/calorie-calculator"))
        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//h1[contains(normalize-space(), 'Help us calculate your target calorie intake')]",
                )
            )
        )

    def fill_physical_info(
        self,
        weight: str = "70",
        height: str = "175",
        activity_level_label: str = "Moderately Active (3-5 days/week)",
        weight_goal_label: str = "Maintain Weight",
    ):
        weight_input = self.driver.find_element(By.ID, "weight")
        weight_input.clear()
        weight_input.send_keys(weight)

        height_input = self.driver.find_element(By.ID, "height")
        height_input.clear()
        height_input.send_keys(height)

        Select(self.driver.find_element(By.ID, "activity-level")).select_by_visible_text(
            activity_level_label
        )
        Select(self.driver.find_element(By.ID, "weight-goal")).select_by_visible_text(
            weight_goal_label
        )

    def submit_physical_info(self):
        submit_btn = self.driver.find_element(
            By.XPATH, "//button[@type='submit' and normalize-space()='Submit']"
        )
        _js_click(self.driver, submit_btn)

    def assert_calorie_target_modal_visible(self):
        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    f"//div[contains(@class,'modal')]//h5[contains(normalize-space(), '{self.CALORIE_MODAL_TITLE}')]"
                    f" | //div[contains(@class,'modal')]//*[contains(normalize-space(), '{self.CALORIE_MODAL_TITLE}')]",
                )
            )
        )
        kcal_heading = self.driver.find_elements(
            By.XPATH, "//div[contains(@class,'modal')]//h1[contains(., 'kcal')]"
        )
        assert any(el.is_displayed() for el in kcal_heading), (
            "Expected daily calorie value in modal"
        )

    def go_to_home_from_calorie_modal(self):
        lets_go_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class,'modal')]//button[normalize-space()=\"Let's Go!\"]")
            )
        )
        _js_click(self.driver, lets_go_btn)

    def wait_for_home_page(self):
        self.wait.until(EC.url_contains("/home"))

    def complete_onboarding(
        self,
        email: str,
        password: str,
        confirm_password: str | None = None,
    ):
        self.register(email, password, confirm_password)
        self.wait_for_create_profile_page()
        self.fill_profile()
        self.submit_profile()
        self.wait_for_calorie_calculator_page()
        self.fill_physical_info()
        self.submit_physical_info()
        self.assert_calorie_target_modal_visible()
        self.go_to_home_from_calorie_modal()
        self.wait_for_home_page()

    def is_on_register_page(self) -> bool:
        return "/register" in self.driver.current_url

    def has_inline_error(self) -> bool:
        errors = self.driver.find_elements(By.CSS_SELECTOR, "span.text-danger")
        return any(error.is_displayed() and error.text.strip() for error in errors)

    def get_inline_error_texts(self) -> list[str]:
        return [
            error.text.strip()
            for error in self.driver.find_elements(By.CSS_SELECTOR, "span.text-danger")
            if error.is_displayed() and error.text.strip()
        ]

    def wait_for_error_toast(self, timeout: int = 5):
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class,'toast') and contains(@class,'bg-danger')]"
                    "//div[contains(@class,'toast-body')]",
                )
            )
        )

    def wait_for_success_toast(self):
        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    f"//div[contains(@class,'toast-body') and contains(., '{self.SUCCESS_TOAST}')]",
                )
            )
        )

    def has_html5_validation_error(self) -> bool:
        for element in (self._email_input(), self._password_input(), self._confirm_password_input()):
            message = self.driver.execute_script(
                "return arguments[0].validationMessage;", element
            )
            if message:
                return True
        return False

    def assert_registration_rejected(self):
        """Expect inline error, error toast, HTML5 validation, or remain on register page."""
        if self.has_inline_error():
            return
        try:
            self.wait_for_error_toast(timeout=3)
            return
        except Exception:
            pass
        if self.has_html5_validation_error():
            return
        if self.is_on_register_page():
            return
        raise AssertionError(
            "Expected registration to be rejected with visible error feedback "
            "or to remain on the Register page"
        )
