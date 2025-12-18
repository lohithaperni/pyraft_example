# RAFT-Style Selenium + pytest Framework (Python)

This project is a configuration-driven Selenium framework in Python, inspired by RAFT-style separation of concerns: config, core, pages, and tests.

## What is Configuration-Driven Testing?

Configuration-driven testing separates test configuration from test code, allowing you to:
- **Switch environments** (dev, stage, prod) without changing code
- **Change browser settings** (headless, wait times) via config files
- **Manage test data** separately from test logic
- **Run the same tests** across different configurations easily

## Folder Structure

- `config/`
  - `env/`: environment configs (base URLs, etc.).
  - `run/`: run configs (browser, headless, waits).
  - `data/`: test data.
- `core/`: config loader and WebDriver factory.
- `pages/`: Page Object Model classes.
- `tests/`: pytest test files.
- `conftest.py`: pytest fixtures and CLI options.
- `requirements.txt`: dependencies.

## Setup

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## How to Use Configuration-Driven Testing

### 1. Running Tests with Different Environments

The `--env` flag selects which environment configuration to use:

```bash
# Run tests against development environment
pytest --env=dev --run=chrome_local -v

# Run tests against staging environment
pytest --env=stage --run=chrome_local -v

# Run tests against production environment
pytest --env=prod --run=chrome_local -v
```

**Available environments:**
- `dev` → Uses `config/env/dev.yaml` (https://platform-dev.revalu.world/)
- `stage` → Uses `config/env/stage.yaml` (https://platform-dev.revalu.world/)
- `prod` → Uses `config/env/prod.yaml` (https://platform.revalu.io/)

### 2. Running Tests with Different Browser Configurations

The `--run` flag selects which browser/run configuration to use:

```bash
# Run with Chrome (non-headless)
pytest --env=dev --run=chrome_local -v

# Run with Chrome (headless) - if you create chrome_headless.yaml
pytest --env=dev --run=chrome_headless -v
```

**Current run configs:**
- `chrome_local` → Chrome browser, visible window, 5s implicit wait

### 3. Creating New Configurations

#### Adding a New Environment

Create a new YAML file in `config/env/`:

```yaml
# config/env/uat.yaml
base_url: "https://uat.yourapp.com"
```

Then run: `pytest --env=uat --run=chrome_local -v`

#### Adding a New Run Configuration

Create a new YAML file in `config/run/`:

```yaml
# config/run/chrome_headless.yaml
browser: "chrome"
headless: true
implicit_wait: 10
```

Then run: `pytest --env=dev --run=chrome_headless -v`

#### Adding Test Data

Create or modify YAML files in `config/data/`:

```yaml
# config/data/login_users.yaml
valid_user:
  username: "standard_user"
  password: "secret_sauce"

admin_user:
  username: "admin"
  password: "admin123"
```

Access in tests via the `login_users` fixture (or create custom fixtures).

### 4. Using Fixtures in Your Tests

The framework provides these pytest fixtures automatically:

```python
def test_example(driver, base_url, login_users):
    # driver: WebDriver instance (automatically created/closed)
    # base_url: Base URL from selected environment config
    # login_users: Test data from config/data/login_users.yaml
    
    page = LoginPage(driver, base_url)
    page.open_login()
    page.login(login_users["valid_user"]["username"], 
                login_users["valid_user"]["password"])
```

**Available Fixtures:**
- `driver`: WebDriver instance (created before test, closed after)
- `base_url`: Base URL string from environment config
- `env_config`: Full environment config dictionary
- `run_config`: Full run config dictionary
- `login_users`: Login test data dictionary

### 5. Example Usage Scenarios

#### Scenario 1: Run same tests on multiple environments
```bash
# Test on dev
pytest --env=dev --run=chrome_local tests/test_login.py

# Test on stage
pytest --env=stage --run=chrome_local tests/test_login.py

# Test on prod
pytest --env=prod --run=chrome_local tests/test_login.py
```

#### Scenario 2: Run tests in headless mode for CI/CD
```bash
# Create config/run/chrome_headless.yaml first, then:
pytest --env=dev --run=chrome_headless tests/
```

#### Scenario 3: Run specific test with custom config
```bash
pytest --env=dev --run=chrome_local tests/test_login.py::test_valid_login -v
```

### 6. Default Values

If you don't specify flags, defaults are used:
- `--env` defaults to `dev`
- `--run` defaults to `chrome_local`

So this works: `pytest -v` (uses dev + chrome_local)

## Benefits of Configuration-Driven Approach

1. **No Code Changes**: Switch environments/configs without touching test code
2. **Easy Maintenance**: Update URLs/configs in one place (YAML files)
3. **Flexibility**: Mix and match environments with browser configs
4. **CI/CD Friendly**: Easy to parameterize in pipelines
5. **Team Collaboration**: Non-developers can update configs without code knowledge

## Extending the Framework

- **Add more pages**: Create new classes in `pages/` inheriting from `BasePage`
- **Add more tests**: Create new test files in `tests/`
- **Add more data**: Create new YAML files in `config/data/` and load them in `conftest.py`
- **Add browser support**: Extend `core/driver_factory.py` to support Firefox, Edge, etc.

