import pytest
from core.config_loader import load_env_config, load_run_config, load_data_config, load_api_config, load_db_config
from core.driver_factory import create_driver
from core.api_helper import (
    load_api_endpoints,
    load_api_payloads,
    load_api_headers,
    load_api_test_data,
    get_api_base_url,
    get_headers
)
from core.db_helper import (
    load_db_connections,
    load_db_queries,
    load_db_test_data,
    get_db_config,
    create_connection,
    return_connection,
    close_all_pools
)
from core.data_helper import (
    load_users,
    load_forms,
    load_test_scenarios
)


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Environment name: dev, stage, prod, etc.",
    )
    parser.addoption(
        "--run",
        action="store",
        default="chrome_local",
        help="Run config name: chrome_local, etc.",
    )


@pytest.fixture(scope="session")
def env_config(pytestconfig):
    env = pytestconfig.getoption("--env")
    return load_env_config(env)


@pytest.fixture(scope="session")
def run_config(pytestconfig):
    run = pytestconfig.getoption("--run")
    return load_run_config(run)


@pytest.fixture(scope="session")
def base_url(env_config):
    return env_config["base_url"]


@pytest.fixture(scope="session")
def login_users():
    return load_data_config("login_users")


@pytest.fixture
def driver(run_config):
    driver = create_driver(run_config)
    yield driver
    driver.quit()


# API Testing Fixtures
@pytest.fixture(scope="session")
def api_base_url(env_config):
    """Get API base URL from environment config"""
    return env_config.get("api_base_url", "")


@pytest.fixture(scope="session")
def api_endpoints():
    """Load API endpoints configuration"""
    return load_api_endpoints()


@pytest.fixture(scope="session")
def api_payloads():
    """Load API payloads configuration"""
    return load_api_payloads()


@pytest.fixture(scope="session")
def api_headers(pytestconfig):
    """Load API headers for the current environment"""
    env = pytestconfig.getoption("--env", default="dev")
    return get_headers(env=env)


@pytest.fixture(scope="session")
def api_test_data():
    """Load API test data"""
    return load_api_test_data()


@pytest.fixture(scope="session")
def expected_responses():
    """Load expected API responses"""
    from core.api_helper import load_expected_responses
    return load_expected_responses()


# Database Testing Fixtures
@pytest.fixture(scope="session")
def db_config(pytestconfig):
    """Get database configuration for the current environment"""
    env = pytestconfig.getoption("--env", default="dev")
    return get_db_config(env)


@pytest.fixture(scope="session")
def db_queries():
    """Load database queries configuration"""
    return load_db_queries()


@pytest.fixture(scope="session")
def db_test_data():
    """Load database test data"""
    return load_db_test_data()


@pytest.fixture(scope="function")
def db_connection(pytestconfig):
    """Create a database connection for the test"""
    env = pytestconfig.getoption("--env", default="dev")
    conn = create_connection(env=env)
    yield conn
    return_connection(conn, env=env)


@pytest.fixture(scope="session", autouse=True)
def cleanup_db_pools():
    """Cleanup database connection pools after all tests"""
    yield
    close_all_pools()


# UI Testing Fixtures
@pytest.fixture(scope="session")
def users():
    """Load users test data"""
    return load_users()


@pytest.fixture(scope="session")
def forms():
    """Load forms test data"""
    return load_forms()


@pytest.fixture(scope="session")
def test_scenarios():
    """Load test scenarios"""
    return load_test_scenarios()

