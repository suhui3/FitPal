from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    def __init__(self, driver, base_url: str):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 15)

    def open(self):
        self.driver.get(f"{self.base_url}/sign-in")

    def sign_in(self, email: str, password: str):
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
        self.driver.find_element(By.CSS_SELECTOR, "input[type='email']").clear()
        self.driver.find_element(By.CSS_SELECTOR, "input[type='email']").send_keys(email)
        self.driver.find_element(By.CSS_SELECTOR, "input[type='password']").clear()
        self.driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        self.wait.until(EC.url_contains("/home"))
