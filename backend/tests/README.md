# Testing Guide for Engineering Blog Recommender

This directory contains all tests for the Engineering Blog Recommender system, including unit, integration, and end-to-end (E2E) browser tests.

---

## Test Types & Structure

- **Unit Tests** (`unit/`):
  - Test individual functions and modules in isolation.
  - Fast, do not require external services.
  - Example: utility functions, recommender logic.

- **Integration Tests** (`integration/`):
  - Test API endpoints and service interactions.
  - Require the backend (and sometimes frontend) to be running.
  - Example: `/analytics/top-liked-articles`, `/analytics/top-liked-categories`, likes, search, recommend, scraper, and auth endpoints.

- **End-to-End (E2E) Tests** (`e2e/`):
  - Use Selenium to simulate real user flows in the browser.
  - Require the frontend and backend to be running with test data.
  - Example: loading the homepage, searching, recommending, enabling swipe mode, swiping/liking/disliking articles.

---

## Directory Layout

```
backend/tests/
  unit/           # Unit tests (pytest)
  integration/    # Integration/API tests (pytest, httpx)
  e2e/            # End-to-end browser tests (pytest, selenium)
  README.md       # This guide
```

---

## How to Run Tests

### 1. Unit & Integration Tests

- **Install dependencies:**
  ```bash
  pip install -r ../requirements.txt
  pip install pytest httpx
  ```
- **Run all tests:**
  ```bash
  pytest
  ```
- **Run only integration tests:**
  ```bash
  pytest integration/
  ```
- **Run a specific test file:**
  ```bash
  pytest integration/test_analytics.py
  ```

### 2. End-to-End (Selenium) Tests

- **Install dependencies:**
  ```bash
  pip install selenium pytest
  # Download ChromeDriver (or another driver) matching your browser version and add it to your PATH
  ```
- **Start the frontend and backend:**
  - Frontend: `http://localhost:3000`
  - Backend: `http://localhost:8000`
  - Make sure there is some test data in the database.
- **Run E2E tests:**
  ```bash
  pytest e2e/test_basic_flow.py
  ```

---

## What Each Test Covers

### Integration Tests
- **test_analytics.py:**
  - `/analytics/top-liked-articles`: Returns the top 3 most liked articles.
  - `/analytics/top-liked-categories`: Returns the top 3 most liked categories.
- **Other integration tests:**
  - Likes, recommend, search, scraper, and auth endpoints.

### E2E Selenium Tests (`e2e/test_basic_flow.py`)
- Home page loads and title is correct.
- Search bar is present.
- Search flow: enter query, click search, results appear.
- Recommend flow: switch tab, enter query, click recommend, results appear.
- Swipe mode (search): enable swipe, perform search, swipe right (like) and left (dislike) through results.
- Swipe mode (recommend): enable swipe, perform recommend, swipe right (like) through results.
- All E2E tests use robust WebDriverWaits for reliability.

---

## Tips & Troubleshooting

- **Selenium/ChromeDriver:** Ensure ChromeDriver matches your installed Chrome version and is in your PATH.
- **Test Data:** E2E and integration tests expect some articles and likes in the database. Add test data if needed.
- **Port Conflicts:** Make sure nothing else is running on ports 3000 (frontend) or 8000 (backend).
- **Flaky Tests:** If tests fail intermittently, check for slow network/database, or increase WebDriverWait timeouts.
- **Extending Tests:**
  - Add new E2E flows (e.g., login, like persistence) in `e2e/`.
  - Add new API/integration tests in `integration/`.
  - Add new unit tests in `unit/`.

---

## Contributing

- Follow the existing structure for new tests.
- Use descriptive test names and comments.
- Prefer WebDriverWait over time.sleep in Selenium tests.
- Keep tests isolated and idempotent where possible.

---

Happy testing! 