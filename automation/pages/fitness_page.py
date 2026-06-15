import platform

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def _js_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    driver.execute_script("arguments[0].click();", element)


class FitnessPage:
    MODAL_TITLE = "Set Daily Target"
    SUCCESS_TOAST = "Daily target saved!"
    LOG_SUCCESS_TOAST = "Exercise logged!"

    def __init__(self, driver, base_url: str):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 15)

    def open(self):
        self.driver.get(f"{self.base_url}/fitness")
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//h5[contains(text(), \"Today's Progress Overview\")]")
            )
        )

    def open_set_target_modal(self):
        steps_tab = self.wait.until(EC.element_to_be_clickable((By.ID, "tab-steps")))
        _js_click(self.driver, steps_tab)
        set_target_btn = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[normalize-space()='Set Target']")
            )
        )
        _js_click(self.driver, set_target_btn)
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//h1[contains(text(), '{self.MODAL_TITLE}')]")
            )
        )

    def _step_input(self):
        return self.driver.find_element(
            By.XPATH,
            "//label[contains(text(), 'Daily Step Target')]/following::input[@type='number'][1]",
        )

    def _minutes_input(self):
        return self.driver.find_element(
            By.XPATH,
            "//label[contains(text(), 'Daily Workout Minutes Target')]/following::input[@type='number'][1]",
        )

    def _clear_and_type(self, element, value: str):
        modifier = Keys.COMMAND if platform.system() == "Darwin" else Keys.CONTROL
        element.click()
        element.send_keys(modifier, "a")
        element.send_keys(Keys.BACKSPACE)
        if value != "":
            element.send_keys(value)

    def fill_targets(self, steps: str, workout_minutes: str):
        self._clear_and_type(self._step_input(), steps)
        self._clear_and_type(self._minutes_input(), workout_minutes)

    def click_save_target(self):
        save_btn = self.driver.find_element(
            By.XPATH, "//button[normalize-space()='Save Target']"
        )
        _js_click(self.driver, save_btn)

    def save_targets(self, steps: str, workout_minutes: str):
        self.fill_targets(steps, workout_minutes)
        self.click_save_target()

    def is_modal_visible(self) -> bool:
        modals = self.driver.find_elements(
            By.XPATH, f"//h1[contains(text(), '{self.MODAL_TITLE}')]"
        )
        return any(modal.is_displayed() for modal in modals)

    def wait_for_success_toast(self):
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//div[contains(@class,'toast-body') and contains(., '{self.SUCCESS_TOAST}')]")
            )
        )

    def wait_for_modal_closed(self):
        self.wait.until(
            EC.invisibility_of_element_located(
                (By.XPATH, f"//h1[contains(text(), '{self.MODAL_TITLE}')]")
            )
        )

    def get_steps_goal_text(self) -> str:
        return self.get_goal_text_for_tab("steps")

    def assert_set_target_modal_visible(self):
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//h1[contains(text(), '{self.MODAL_TITLE}')]")
            )
        )
        assert self._step_input().is_displayed()
        assert self._minutes_input().is_displayed()
        save_btn = self.driver.find_element(
            By.XPATH, "//button[normalize-space()='Save Target']"
        )
        assert save_btn.is_displayed()

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

    def assert_no_success_toast(self):
        toasts = self.driver.find_elements(
            By.XPATH,
            f"//div[contains(@class,'toast-body') and contains(., '{self.SUCCESS_TOAST}')]",
        )
        assert not any(t.is_displayed() for t in toasts), (
            "Success toast should not appear for invalid input"
        )

    def get_goal_text_for_tab(self, tab: str) -> str:
        tab_id = f"tab-{tab}"
        tab_el = self.wait.until(EC.element_to_be_clickable((By.ID, tab_id)))
        if tab_el.get_attribute("checked") is None:
            _js_click(self.driver, tab_el)
        label = "steps" if tab == "steps" else "min"
        self.wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "small.text-muted"), label
            )
        )
        return self.driver.find_element(By.CSS_SELECTOR, "small.text-muted").text

    def open_fitness_without_login(self):
        self.driver.get(f"{self.base_url}/fitness")
        self.wait.until(lambda d: not self.is_fitness_page_loaded())

    def is_fitness_page_loaded(self) -> bool:
        headings = self.driver.find_elements(
            By.XPATH,
            "//h5[contains(text(), \"Today's Progress Overview\")]",
        )
        return any(h.is_displayed() for h in headings)

    def is_access_denied(self) -> bool:
        if self.is_fitness_page_loaded():
            return False
        path = self.driver.current_url.rstrip("/").replace(self.base_url, "") or "/"
        return path in {"/", "/sign-in"}

    def has_html5_validation_error(self) -> bool:
        if not self.is_modal_visible():
            return False
        for element in (self._step_input(), self._minutes_input()):
            message = self.driver.execute_script(
                "return arguments[0].validationMessage;", element
            )
            if message:
                return True
        return False

    def set_minutes_value_js(self, value: str):
        minutes_input = self._minutes_input()
        self.driver.execute_script(
            "arguments[0].value = arguments[1];"
            "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
            minutes_input,
            value,
        )

    def _search_input(self):
        return self.driver.find_element(
            By.CSS_SELECTOR, "input[placeholder='Search']"
        )

    def search_exercise(self, name: str):
        search = self._search_input()
        modifier = Keys.COMMAND if platform.system() == "Darwin" else Keys.CONTROL
        search.click()
        search.send_keys(modifier, "a")
        search.send_keys(Keys.BACKSPACE)
        search.send_keys(name)
        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    f"//li[contains(@class,'list-group-item') and normalize-space()='{name}']",
                )
            )
        )

    def click_exercise(self, name: str):
        exercise = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//li[contains(@class,'list-group-item') and normalize-space()='{name}']",
                )
            )
        )
        _js_click(self.driver, exercise)

    def open_exercise_log_modal(self, name: str):
        self.search_exercise(name)
        self.click_exercise(name)
        self.assert_log_modal_visible(name)

    def _log_modal_title(self, exercise_name: str):
        return self.driver.find_element(
            By.XPATH,
            f"//div[contains(@class,'modal')]//h1[contains(text(), '{exercise_name}')]",
        )

    def is_log_modal_visible(self, exercise_name: str) -> bool:
        modals = self.driver.find_elements(
            By.XPATH,
            f"//div[contains(@class,'modal')]//h1[contains(text(), '{exercise_name}')]",
        )
        return any(modal.is_displayed() for modal in modals)

    def assert_log_modal_visible(self, exercise_name: str):
        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    f"//div[contains(@class,'modal')]//h1[contains(text(), '{exercise_name}')]",
                )
            )
        )

    def wait_for_log_modal_closed(self, exercise_name: str):
        self.wait.until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    f"//div[contains(@class,'modal')]//h1[contains(text(), '{exercise_name}')]",
                )
            )
        )

    def _log_modal_input(self, label_text: str):
        return self.driver.find_element(
            By.XPATH,
            f"//div[contains(@class,'modal')]//label[contains(text(), '{label_text}')]"
            f"/following::input[1]",
        )

    def _log_modal_save_button(self):
        return self.driver.find_element(
            By.XPATH,
            "//div[contains(@class,'modal')]//button[@type='submit' and normalize-space()='Save']",
        )

    def assert_workout_log_modal_fields(self, exercise_name: str):
        self.assert_log_modal_visible(exercise_name)
        assert self._log_modal_input("Date").is_displayed()
        assert self._log_modal_input("Start Time").is_displayed()
        assert self._log_modal_input("Number of Sets").is_displayed()
        assert self._log_modal_input("Number of Reps").is_displayed()
        assert self._log_modal_save_button().is_displayed()

    def assert_cardio_log_modal_fields(self, exercise_name: str):
        self.assert_log_modal_visible(exercise_name)
        assert self._log_modal_input("Date").is_displayed()
        assert self._log_modal_input("Start Time").is_displayed()
        assert self._log_modal_input("Duration (minutes)").is_displayed()
        assert self._log_modal_save_button().is_displayed()

    def _set_log_input_value(self, label_text: str, value: str):
        field = self._log_modal_input(label_text)
        self.driver.execute_script(
            """
            const input = arguments[0];
            const nextValue = arguments[1];
            const setter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype,
                'value'
            ).set;
            setter.call(input, nextValue);
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            """,
            field,
            value,
        )

    def _set_log_date(self, date: str):
        """Set modal date field. Expects YYYY-MM-DD."""
        self._set_log_input_value("Date", date)

    def _set_log_time(self, time: str):
        """Set modal start time field. Expects HH:MM."""
        self._set_log_input_value("Start Time", time)

    def fill_workout_log(self, date: str, time: str, sets: str, reps: str):
        self._set_log_date(date)
        self._set_log_time(time)
        self._set_log_input_value("Number of Sets", sets)
        self._set_log_input_value("Number of Reps", reps)

    def fill_cardio_log(self, date: str, time: str, duration: str):
        self._set_log_date(date)
        self._set_log_time(time)
        self._set_log_input_value("Duration (minutes)", duration)

    def set_log_field_value_js(self, label_text: str, value: str):
        self._set_log_input_value(label_text, value)

    def click_save_log(self):
        _js_click(self.driver, self._log_modal_save_button())

    def save_workout_log(
        self, exercise_name: str, date: str, time: str, sets: str, reps: str
    ):
        self.open_exercise_log_modal(exercise_name)
        self.fill_workout_log(date, time, sets, reps)
        self.click_save_log()

    def save_cardio_log(
        self, exercise_name: str, date: str, time: str, duration: str
    ):
        self.open_exercise_log_modal(exercise_name)
        self.fill_cardio_log(date, time, duration)
        self.click_save_log()

    def wait_for_exercise_logged_toast(self):
        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    f"//div[contains(@class,'toast-body') and contains(., '{self.LOG_SUCCESS_TOAST}')]",
                )
            )
        )

    def assert_no_exercise_logged_toast(self):
        toasts = self.driver.find_elements(
            By.XPATH,
            f"//div[contains(@class,'toast-body') and contains(., '{self.LOG_SUCCESS_TOAST}')]",
        )
        assert not any(t.is_displayed() for t in toasts), (
            "Success toast should not appear for invalid log input"
        )

    def wait_for_log_error_toast(self, timeout: int = 5):
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class,'toast') and contains(@class,'bg-danger')]"
                    "//div[contains(@class,'toast-body')]",
                )
            )
        )

    def has_log_modal_html5_validation_error(self) -> bool:
        if not self.driver.find_elements(
            By.XPATH, "//div[contains(@class,'modal') and contains(@class,'show')]"
        ):
            return False
        labels = ("Date", "Start Time", "Number of Sets", "Number of Reps", "Duration (minutes)")
        for label in labels:
            fields = self.driver.find_elements(
                By.XPATH,
                f"//div[contains(@class,'modal')]//label[contains(text(), '{label}')]"
                f"/following::input[1]",
            )
            for element in fields:
                if not element.is_displayed():
                    continue
                message = self.driver.execute_script(
                    "return arguments[0].validationMessage;", element
                )
                if message:
                    return True
        return False

    def assert_activity_visible_in_list(self, activity_name: str):
        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    f"//div[contains(@class,'card-body')]//div[contains(@class,'fw-semibold') "
                    f"and normalize-space()='{activity_name}']",
                )
            )
        )
