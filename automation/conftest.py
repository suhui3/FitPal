import os

import pytest
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages.cardio_vs_workout_page import CardioVsWorkoutPage
from pages.fitness_page import FitnessPage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage

load_dotenv()


def get_cardio_workout_summary(driver, api_base_url: str, **params) -> list:
    """Fetch cardio vs workout summary via API using the browser session cookies."""
    cookies = {c["name"]: c["value"] for c in driver.get_cookies()}
    response = requests.get(
        f"{api_base_url.rstrip('/')}/api/exercises/cardio-vs-workout-summary",
        cookies=cookies,
        params=params,
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    return data if isinstance(data, list) else []


def get_user_goals(driver, api_base_url: str) -> dict:
    """Fetch daily targets via API using the browser session cookies."""
    cookies = {c["name"]: c["value"] for c in driver.get_cookies()}
    response = requests.get(
        f"{api_base_url.rstrip('/')}/api/users/goals",
        cookies=cookies,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def get_user_exercises(driver, api_base_url: str) -> list:
    """Fetch exercise logs via API using the browser session cookies."""
    cookies = {c["name"]: c["value"] for c in driver.get_cookies()}
    response = requests.get(
        f"{api_base_url.rstrip('/')}/api/exercises",
        cookies=cookies,
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    return data if isinstance(data, list) else []


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("FITPAL_BASE_URL", "http://localhost:5173").rstrip("/")


@pytest.fixture(scope="session")
def api_base_url():
    return os.getenv("FITPAL_API_BASE_URL", "http://localhost:7001").rstrip("/")


@pytest.fixture(scope="session")
def test_credentials():
    return {
        "email": os.getenv("FITPAL_TEST_EMAIL", "user1@fitpal.com"),
        "password": os.getenv("FITPAL_TEST_PASSWORD", "Password123!"),
    }


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--window-size=1400,900")
    if os.getenv("HEADLESS", "").lower() in {"1", "true", "yes"}:
        options.add_argument("--headless=new")

    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)
    browser.implicitly_wait(5)
    yield browser
    browser.quit()


@pytest.fixture
def logged_in_driver(driver, base_url, test_credentials):
    login = LoginPage(driver, base_url)
    login.open()
    login.sign_in(test_credentials["email"], test_credentials["password"])
    return driver


@pytest.fixture
def fitness_page(logged_in_driver, base_url):
    page = FitnessPage(logged_in_driver, base_url)
    page.open()
    return page


@pytest.fixture
def fetch_user_goals(api_base_url):
    def _fetch(driver):
        return get_user_goals(driver, api_base_url)

    return _fetch


@pytest.fixture
def fetch_user_exercises(api_base_url):
    def _fetch(driver):
        return get_user_exercises(driver, api_base_url)

    return _fetch


@pytest.fixture
def fetch_cardio_workout_summary(api_base_url):
    def _fetch(driver, **params):
        return get_cardio_workout_summary(driver, api_base_url, **params)

    return _fetch


@pytest.fixture(scope="session")
def f018_credentials():
    return {
        "email": os.getenv("FITPAL_TEST_EMAIL", "user1@fitpal.com"),
        "password": os.getenv("FITPAL_TEST_PASSWORD", "Password123!"),
    }


@pytest.fixture(scope="session")
def f018_empty_account_credentials():
    return {
        "email": os.getenv("FITPAL_EMPTY_ACCOUNT_EMAIL", "user3@fitpal.com"),
        "password": os.getenv("FITPAL_EMPTY_ACCOUNT_PASSWORD", "Password123!"),
    }


@pytest.fixture
def f018_logged_in_driver(driver, base_url, f018_credentials):
    login = LoginPage(driver, base_url)
    login.open()
    login.sign_in(f018_credentials["email"], f018_credentials["password"])
    return driver


@pytest.fixture
def cardio_vs_workout_page(f018_logged_in_driver, base_url):
    page = CardioVsWorkoutPage(f018_logged_in_driver, base_url)
    page.open()
    return page


@pytest.fixture
def register_page(driver, base_url):
    page = RegisterPage(driver, base_url)
    return page


@pytest.fixture
def empty_account_cardio_page(driver, base_url, f018_empty_account_credentials):
    login = LoginPage(driver, base_url)
    login.open()
    login.sign_in(
        f018_empty_account_credentials["email"],
        f018_empty_account_credentials["password"],
    )
    page = CardioVsWorkoutPage(driver, base_url)
    page.open()
    return page
