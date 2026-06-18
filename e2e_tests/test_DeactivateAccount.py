import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    # Set up Chrome options (headless for testing environment, comment out `--headless` for visual debugging)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture
def logged_in_driver(driver):
    # FitPal frontend default local URL
    frontend_url = "http://localhost:5173"
    
    # Sign in first (pre-requisite)
    driver.get(f"{frontend_url}/sign-in")
    wait = WebDriverWait(driver, 10)
    
    email_input = wait.until(EC.visibility_of_element_located((By.ID, "formBasicEmail")))
    password_input = driver.find_element(By.ID, "formBasicPassword")
    
    # Enter seed user credentials (from SETUP.md)
    email_input.send_keys("user1@fitpal.com")
    password_input.send_keys("Password123!")
    
    submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    # Click via JavaScript to avoid click interception from overlapping container layouts in headless mode
    driver.execute_script("arguments[0].click();", submit_button)
    
    # Wait until redirect to dashboard home
    wait.until(EC.url_contains("/home"))
    return driver

def test_deactivate_password_validation_fitpal(logged_in_driver):
    driver = logged_in_driver
    wait = WebDriverWait(driver, 10)
    
    # 1. Navigate to the deactivate account page directly
    driver.get("http://localhost:5173/deactivate-account")
    
    # 2. Locate input field and button
    # The input matches the controlId "formConfirmPassword" in DeactivateAccountPage.jsx
    password_input = wait.until(EC.visibility_of_element_located((By.ID, "formConfirmPassword")))
    deactivate_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Deactivate Account')]")
    
    # 3. Enter password: FitPal@123
    password_input.clear()
    password_input.send_keys("FitPal@123")
    
    # 4. Click Deactivate
    driver.execute_script("arguments[0].click();", deactivate_btn)
    
    # 5. Verify response (Toast message or HTML5 validation message)
    has_response = False
    try:
        # Check for toast notification indicating password validation response (e.g. incorrect password toast)
        toast_body = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "toast-body"))
        )
        print(f"Test FitPal@123 Toast Response: {toast_body.text}")
        has_response = True
    except Exception:
        # Fallback: check HTML5 validation tooltip
        tooltip = driver.execute_script("return arguments[0].validationMessage;", password_input)
        print(f"Test FitPal@123 Tooltip: {tooltip}")
        if tooltip:
            has_response = True
            
    assert has_response, "Expected system response (Toast alert or browser-native validation tooltip), but got neither."

def test_deactivate_password_validation_wrong(logged_in_driver):
    driver = logged_in_driver
    wait = WebDriverWait(driver, 10)
    
    # 1. Navigate to the deactivate account page directly
    driver.get("http://localhost:5173/deactivate-account")
    
    # 2. Locate input field and button
    # The input matches the controlId "formConfirmPassword" in DeactivateAccountPage.jsx
    password_input = wait.until(EC.visibility_of_element_located((By.ID, "formConfirmPassword")))
    deactivate_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Deactivate Account')]")
    
    # 3. Enter password: wrongPassword
    password_input.clear()
    password_input.send_keys("wrongPassword")
    
    # 4. Click Deactivate
    driver.execute_script("arguments[0].click();", deactivate_btn)
    
    # 5. Verify response (Toast message or HTML5 validation message)
    has_response = False
    try:
        # Check for toast notification indicating password validation response
        toast_body = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "toast-body"))
        )
        print(f"Test wrongPassword Toast Response: {toast_body.text}")
        has_response = True
    except Exception:
        # Fallback: check HTML5 validation tooltip
        tooltip = driver.execute_script("return arguments[0].validationMessage;", password_input)
        print(f"Test wrongPassword Tooltip: {tooltip}")
        if tooltip:
            has_response = True
            
    assert has_response, "Expected system response (Toast alert or browser-native validation tooltip), but got neither."
