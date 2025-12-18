import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def load_yaml(path: Path) -> dict:
    with path.open() as f:
        return yaml.safe_load(f)


def load_env_config(env: str) -> dict:
    path = BASE_DIR / "config" / "env" / f"{env}.yaml"
    return load_yaml(path)


def load_run_config(run: str) -> dict:
    path = BASE_DIR / "config" / "run" / f"{run}.yaml"
    return load_yaml(path)


def load_data_config(name: str) -> dict:
    path = BASE_DIR / "config" / "data" / f"{name}.yaml"
    return load_yaml(path)


def load_api_config(config_name: str) -> dict:
    """Load API configuration from config/data/api/"""
    path = BASE_DIR / "config" / "data" / "api" / f"{config_name}.yaml"
    return load_yaml(path)


def load_db_config(config_name: str) -> dict:
    """Load database configuration from config/data/db/"""
    path = BASE_DIR / "config" / "data" / "db" / f"{config_name}.yaml"
    return load_yaml(path)

