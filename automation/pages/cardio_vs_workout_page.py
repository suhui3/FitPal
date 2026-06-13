from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def _js_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    driver.execute_script("arguments[0].click();", element)


_CHART_INSTANCE_SCRIPT = """
const canvas = document.querySelector('canvas');
if (!canvas) return null;

const fiberKey = Object.keys(canvas).find((key) =>
    key.startsWith('__reactFiber$') || key.startsWith('__reactInternalInstance$')
);
if (!fiberKey) return null;

let fiber = canvas[fiberKey];
while (fiber) {
    let hook = fiber.memoizedState;
    while (hook) {
        const state = hook.memoizedState;
        if (state && typeof state === 'object' && state.current && state.current.config) {
            const chart = state.current;
            return {
                type: chart.config.type,
                yAxisTitle: chart.options?.scales?.y?.title?.text ?? null,
                data: chart.data?.datasets?.[0]?.data ?? [],
            };
        }
        hook = hook.next;
    }
    fiber = fiber.return;
}
return null;
"""


class CardioVsWorkoutPage:
    PAGE_PATH = "/cardio-vs-workout"

    def __init__(self, driver, base_url: str):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 15)

    def open(self):
        self.driver.get(f"{self.base_url}{self.PAGE_PATH}")
        self.wait_for_chart_loaded()

    def open_without_login(self):
        self.driver.get(f"{self.base_url}{self.PAGE_PATH}")
        self.wait.until(lambda d: not self.is_page_loaded())

    def _get_chart_instance(self):
        return self.driver.execute_script(_CHART_INSTANCE_SCRIPT)

    def wait_for_chart_loaded(self):
        self.wait.until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//p[normalize-space()='Loading chart...']")
            )
        )
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "canvas")))
        WebDriverWait(self.driver, 10).until(lambda _: self._get_chart_instance() is not None)

    def is_page_loaded(self) -> bool:
        canvases = self.driver.find_elements(By.CSS_SELECTOR, "canvas")
        if not any(c.is_displayed() for c in canvases):
            return False
        headings = self.driver.find_elements(
            By.XPATH,
            "//h4[contains(text(), 'Daily Activity') or contains(text(), 'Weekly Activity')]",
        )
        return any(h.is_displayed() for h in headings)

    def is_access_denied(self) -> bool:
        if self.is_page_loaded():
            return False
        path = self.driver.current_url.rstrip("/").replace(self.base_url, "") or "/"
        return path in {"/", "/sign-in"}

    def _toggle(self, label: str):
        toggle = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//span[normalize-space()='{label}']"))
        )
        _js_click(self.driver, toggle)

    def select_type(self, chart_type: str):
        self._toggle(chart_type.capitalize())

    def select_mode(self, mode: str):
        self._toggle(mode.capitalize())

    def is_type_selected(self, chart_type: str) -> bool:
        el = self.driver.find_element(
            By.XPATH, f"//span[normalize-space()='{chart_type.capitalize()}']"
        )
        style = el.get_attribute("style") or ""
        return "font-weight: bold" in style or "font-weight:bold" in style

    def is_mode_selected(self, mode: str) -> bool:
        el = self.driver.find_element(
            By.XPATH, f"//span[normalize-space()='{mode.capitalize()}']"
        )
        style = el.get_attribute("style") or ""
        return "font-weight: bold" in style or "font-weight:bold" in style

    def get_activity_heading(self) -> str:
        heading = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//h4[contains(text(), 'Daily Activity') or contains(text(), 'Weekly Activity')]",
                )
            )
        )
        return heading.text.strip()

    def get_period_label(self) -> str:
        label = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class,'align-items-center')]//strong")
            )
        )
        return label.text.strip()

    def click_previous_period(self):
        prev = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.bi-chevron-left"))
        )
        self.driver.execute_script(
            "arguments[0].dispatchEvent("
            "new MouseEvent('click', { bubbles: true, cancelable: true }));",
            prev,
        )
        self.wait_for_chart_loaded()

    def get_chart_type(self):
        chart = self._get_chart_instance()
        return chart["type"] if chart else None

    def get_y_axis_title(self):
        chart = self._get_chart_instance()
        return chart["yAxisTitle"] if chart else None

    def assert_cardio_line_chart(self):
        assert self.get_chart_type() == "line", (
            f"Expected Cardio line chart, got chart type: {self.get_chart_type()!r}"
        )
        assert self.get_y_axis_title() == "Total Minutes", (
            f"Expected y-axis 'Total Minutes', got: {self.get_y_axis_title()!r}"
        )
        assert self.is_type_selected("cardio"), "Cardio type toggle should be selected"

    def assert_workout_bar_chart(self):
        assert self.get_chart_type() == "bar", (
            f"Expected Workout bar chart, got chart type: {self.get_chart_type()!r}"
        )
        assert self.get_y_axis_title() == "Total Reps", (
            f"Expected y-axis 'Total Reps', got: {self.get_y_axis_title()!r}"
        )
        assert self.is_type_selected("workout"), "Workout type toggle should be selected"

    def assert_daily_view(self):
        assert self.is_mode_selected("daily"), "Daily mode toggle should be selected"
        assert self.get_activity_heading() == "Daily Activity", (
            f"Expected 'Daily Activity' heading, got: {self.get_activity_heading()!r}"
        )

    def assert_weekly_view(self):
        assert self.is_mode_selected("weekly"), "Weekly mode toggle should be selected"
        assert self.get_activity_heading() == "Weekly Activity", (
            f"Expected 'Weekly Activity' heading, got: {self.get_activity_heading()!r}"
        )
