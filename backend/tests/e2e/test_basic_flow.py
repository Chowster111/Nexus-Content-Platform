import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# URL of the frontend
BASE_URL = "http://localhost:3000"

@pytest.fixture(scope="module")
def driver():
    # Set up Chrome WebDriver in headless mode
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_homepage_loads_and_title(driver):
    driver.get(BASE_URL)
    WebDriverWait(driver, 10).until(EC.title_contains("Blog"))
    assert "Engineering Blog" in driver.title or "Blog" in driver.title

def test_search_bar_present(driver):
    driver.get(BASE_URL)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search-input"))
    )
    search_inputs = driver.find_elements(By.XPATH, "//input[@type='text' or @placeholder]")
    assert any("search" in (el.get_attribute("placeholder") or "").lower() for el in search_inputs) or len(search_inputs) > 0

# --- New Selenium E2E tests for button click and API call flows ---
def test_search_flow(driver):
    driver.get(BASE_URL)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search-input"))
    )
    search_input = driver.find_element(By.ID, "search-input")
    search_input.clear()
    search_input.send_keys("GraphQL")
    search_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Search')]")
    search_button.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".results a, .results .resultItem"))
    )
    results = driver.find_elements(By.CSS_SELECTOR, ".results a, .results .resultItem")
    assert len(results) > 0

def test_recommend_flow(driver):
    driver.get(BASE_URL)
    recommend_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Recommend')]")
    ))
    recommend_tab.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "recommend-input"))
    )
    recommend_input = driver.find_element(By.ID, "recommend-input")
    recommend_input.clear()
    recommend_input.send_keys("machine learning")
    recommend_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Recommend') or contains(text(), 'Search')]")
    recommend_button.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".results a, .results .resultItem"))
    )
    results = driver.find_elements(By.CSS_SELECTOR, ".results a, .results .resultItem")
    assert len(results) > 0

def test_swipe_search_like_dislike(driver):
    driver.get(BASE_URL)
    swipe_toggle = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Swipe Mode')]/following-sibling::div"))
    )
    swipe_toggle.click()
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search-input"))
    )
    search_input.clear()
    search_input.send_keys("GraphQL")
    search_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Search')]")
    search_button.click()
    # Wait for swipe card to appear
    like_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".swipeWrapper .like"))
    )
    like_button.click()
    # Wait for next card or done
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".swipeWrapper"))
    )
    # Try to dislike next card if present
    try:
        dislike_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".swipeWrapper .dislike"))
        )
        dislike_button.click()
    except Exception:
        pass  # No more cards
    # Assert that either another card or the done message is present
    swipe_wrapper = driver.find_element(By.CSS_SELECTOR, ".swipeWrapper")
    assert swipe_wrapper is not None

def test_swipe_recommend_like(driver):
    driver.get(BASE_URL)
    recommend_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Recommend')]")
    ))
    recommend_tab.click()
    swipe_toggle = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Swipe Mode')]/following-sibling::div"))
    )
    swipe_toggle.click()
    recommend_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "recommend-input"))
    )
    recommend_input.clear()
    recommend_input.send_keys("API architecture")
    recommend_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Recommend')]")
    recommend_button.click()
    like_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".swipeWrapper .like"))
    )
    like_button.click()
    # Assert that either another card or the done message is present
    swipe_wrapper = driver.find_element(By.CSS_SELECTOR, ".swipeWrapper")
    assert swipe_wrapper is not None 