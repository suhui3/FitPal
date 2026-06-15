# FitPal — Automated UI Tests

Browser-based end-to-end tests for FitPal using **pytest** and **Selenium** (Chrome). Tests drive the React frontend and, where needed, verify results through the backend API using the browser session cookies.

## Prerequisites

| Requirement | Notes |
|-------------|--------|
| **Python** 3.10+ | Check with `python3 --version` |
| **Google Chrome** | Installed locally; ChromeDriver is managed automatically via `webdriver-manager` |
| **Running FitPal app** | Backend on port `7001`, frontend on port `5173` |
| **Demo seed data** | Required for most tests (see below) |

For app setup (MongoDB, `.env`, starting servers), see the root [SETUP.md](../SETUP.md).

### Seed data before running tests

Most tests sign in as seeded users. From the project root:

```bash
cd backend
npm run seed:demo
```

Default test accounts (see [SETUP.md](../SETUP.md#seeded-test-accounts)):

| Account | Used for |
|---------|----------|
| `user1@fitpal.com` / `Password123!` | Logged-in flows (fitness, goals, cardio vs workout) |
| `user3@fitpal.com` / `Password123!` | Empty-chart / partial-profile scenarios (`FITPAL_EMPTY_ACCOUNT_*`) |

Registration tests (`f001`) create new users and do not depend on seed data.

## One-time setup

From the `automation/` directory:

```bash
cd automation

# Create and activate a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

Edit `.env` if your URLs or credentials differ from the defaults.

## Environment variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `FITPAL_BASE_URL` | `http://localhost:5173` | Frontend URL |
| `FITPAL_API_BASE_URL` | `http://localhost:7001` | Backend API URL |
| `FITPAL_TEST_EMAIL` | `user1@fitpal.com` | Primary test user |
| `FITPAL_TEST_PASSWORD` | `Password123!` | Primary test user password |
| `FITPAL_EMPTY_ACCOUNT_EMAIL` | `user3@fitpal.com` | Empty-data test user |
| `FITPAL_EMPTY_ACCOUNT_PASSWORD` | `Password123!` | Empty-data test user password |
| `HEADLESS` | _(unset)_ | Set to `1`, `true`, or `yes` to run Chrome without a visible window |

Use `localhost` consistently (not `127.0.0.1` on one side and `localhost` on the other) to avoid cookie issues.

## Running tests

**Start the app first** in two terminals:

```bash
# Terminal 1 — backend
cd backend && npm run dev

# Terminal 2 — frontend
cd frontend && npm run dev
```

Then run pytest from the `automation/` directory:

```bash
cd automation
source .venv/bin/activate   # if using a venv
pytest
```

You can also run from the **repository root** (uses the root `pytest.ini`):

```bash
pytest
```

### Run a subset of tests

Filter by feature (`f###`) or test plan (`tp_##_###`) markers:

```bash
# All registration tests
pytest -m f001

# Single test plan
pytest -m tp_10_005

# One test file
pytest tests/f010_log_activity/TP-10-005_invalid_sets_reps/

# One test class or method (keyword expression)
pytest -k "invalid_sets_reps"
pytest -k "test_tc_10_005"
```

List registered markers:

```bash
pytest --markers
```

### Useful pytest options

```bash
# Stop on first failure
pytest -x

# Show print/log output without capturing
pytest -s

# Run headless (no browser window)
HEADLESS=1 pytest

# Combine filters
HEADLESS=1 pytest -m f010 -v
```

## Test suite layout

Tests are grouped by feature ID and test plan ID:

```text
automation/
├── conftest.py          # Shared fixtures (driver, login, API helpers)
├── pages/               # Page objects (Login, Register, Fitness, etc.)
├── fixtures/            # Static assets used in tests
├── tests/
│   ├── f001_register_account/       # UC-01 Register Account
│   ├── f010_log_activity/           # UC-10 Log Activity
│   ├── f012_set_target/             # UC-12 Set Target
│   └── f018_view_cardio_vs_workout/ # UC-18 Cardio vs Workout charts
├── pytest.ini
├── requirements.txt
└── .env.example
```

### Feature coverage

| Marker | Feature | Test plans |
|--------|---------|------------|
| `f001` | Register Account | `tp_01_001` – `tp_01_004` |
| `f010` | Log Activity | `tp_10_001` – `tp_10_006` |
| `f012` | Set Target | `tp_12_001` – `tp_12_003` |
| `f018` | View Cardio vs Workout | `tp_18_001` – `tp_18_007` |

Each test file docstring maps to a test case ID (e.g. `TP-10-005` / `TC-10-005`).

## How tests work

1. **Browser fixture** — `conftest.py` launches Chrome (headless or visible) and tears it down after each test.
2. **Page objects** — Interactions live in `pages/` (e.g. `FitnessPage`, `LoginPage`) to keep tests readable.
3. **Logged-in fixtures** — `logged_in_driver`, `fitness_page`, and similar fixtures sign in before the test runs.
4. **API verification** — Some tests call backend endpoints with the browser cookies to confirm data was saved (e.g. exercise logs, goals).

## Troubleshooting

### `Connection refused` or tests time out on page load

- Confirm backend (`http://localhost:7001`) and frontend (`http://localhost:5173`) are running.
- Check `FITPAL_BASE_URL` and `FITPAL_API_BASE_URL` in `automation/.env`.

### Login fails / wrong user state

- Re-run `npm run seed:demo` in `backend/`.
- Ensure credentials in `.env` match seeded accounts.
- Log out manually in the browser is not needed — each test gets a fresh driver.

### Chrome / ChromeDriver errors

- Update Google Chrome to the latest version.
- Delete the local WebDriver cache and retry: `rm -rf .wdm` (from `automation/`).
- On first run, `webdriver-manager` downloads a matching ChromeDriver; network access is required.

### `ModuleNotFoundError: No module named 'pages'`

Run pytest from the `automation/` directory, or from the repo root (root `pytest.ini` sets `pythonpath = automation`).

### Marker warnings (`PytestUnknownMarkWarning`)

Run from `automation/` so the local `pytest.ini` (with all markers) is picked up, or ensure you use the root `pytest.ini` which registers feature markers.

### Tests pass locally but fail in CI

Set `HEADLESS=1` and confirm the CI image has Chrome installed. This project currently targets local Chrome via Selenium; CI setup may require additional configuration.

## Adding new tests

1. Add a folder under `tests/f###_<feature_name>/TP-##-###_<description>/`.
2. Create `test_<name>.py` with `@pytest.mark.f###` and `@pytest.mark.tp_##_###` markers.
3. Register new markers in `automation/pytest.ini` (and root `pytest.ini` if tests are run from the repo root).
4. Reuse or extend page objects in `pages/` rather than putting selectors directly in tests.
