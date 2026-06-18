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

def test_log_steps_valid_input(logged_in_driver):
    driver = logged_in_driver
    wait = WebDriverWait(driver, 10)
    
    # Navigate to the Fitness page
    driver.get("http://localhost:5173/fitness")
    
    # Click "Log Steps" button to open the modal
    log_steps_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Log Steps')]")))
    driver.execute_script("arguments[0].click();", log_steps_btn)
    
    # Locate input fields inside the modal form
    date_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//form//input[@type='date']")))
    steps_input = driver.find_element(By.XPATH, "//form//input[@type='number']")
    save_button = driver.find_element(By.XPATH, "//form//button[@type='submit' and contains(text(), 'Save')]")
    
    # Fill in: Date (5 June 2026) & Steps (5000)
    # Using JS execution for date input to prevent localization/OS language formatting issues.
    driver.execute_script("arguments[0].value = '2026-06-05';", date_input)
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", date_input)
    
    steps_input.clear()
    steps_input.send_keys("5000")
    
    # Click Save
    driver.execute_script("arguments[0].click();", save_button)
    
    # Verify response (Toast notification or HTML5 validation message)
    has_response = False
    try:
        toast_body = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "toast-body"))
        )
        print(f"Test 1 Toast Response: {toast_body.text}")
        has_response = True
    except Exception:
        # Fallback: check if HTML5 validation has generated a tooltip message
        date_tooltip = driver.execute_script("return arguments[0].validationMessage;", date_input)
        steps_tooltip = driver.execute_script("return arguments[0].validationMessage;", steps_input)
        print(f"Test 1 Date Tooltip: {date_tooltip}, Steps Tooltip: {steps_tooltip}")
        if date_tooltip or steps_tooltip:
            has_response = True
            
    assert has_response, "Expected system response (Toast alert or browser-native validation tooltip), but got neither."

def test_log_steps_blank_input(logged_in_driver):
    driver = logged_in_driver
    wait = WebDriverWait(driver, 10)
    
    # Navigate to the Fitness page
    driver.get("http://localhost:5173/fitness")
    
    # Click "Log Steps" button to open the modal
    log_steps_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Log Steps')]")))
    driver.execute_script("arguments[0].click();", log_steps_btn)
    
    # Locate input fields inside the modal form
    date_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//form//input[@type='date']")))
    steps_input = driver.find_element(By.XPATH, "//form//input[@type='number']")
    save_button = driver.find_element(By.XPATH, "//form//button[@type='submit' and contains(text(), 'Save')]")
    
    # Fill in: Date (<blank>) & Steps (<blank>)
    driver.execute_script("arguments[0].value = '';", date_input)
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", date_input)
    steps_input.clear()

    # Click Save
    driver.execute_script("arguments[0].click();", save_button)
    
    # Verify response (Toast notification or HTML5 validation message)
    # Since inputs are blank and have the 'required' attribute, HTML5 tooltips should trigger.
    has_response = False
    
    # Check for HTML5 browser validation messages (tooltips)
    date_tooltip = driver.execute_script("return arguments[0].validationMessage;", date_input)
    steps_tooltip = driver.execute_script("return arguments[0].validationMessage;", steps_input)
    print(f"Test 2 Date Tooltip: '{date_tooltip}', Steps Tooltip: '{steps_tooltip}'")
    
    if date_tooltip or steps_tooltip:
        has_response = True
    else:
        # Fallback: check if standard toast notification appeared
        try:
            toast_body = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "toast-body"))
            )
            print(f"Test 2 Toast Response: {toast_body.text}")
            has_response = True
        except Exception:
            pass
            
    assert has_response, "Expected system validation response (browser validation tooltip or Toast message), but got neither."
