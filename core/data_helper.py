"""Enhanced data loading utilities for test data management"""

from typing import Dict, Any, List, Optional
from pathlib import Path
from core.config_loader import load_data_config, BASE_DIR


def load_users() -> Dict[str, Any]:
    """Load user test data"""
    return load_data_config("users")


def load_forms() -> Dict[str, Any]:
    """Load form test data"""
    return load_data_config("forms")


def load_test_scenarios() -> Dict[str, Any]:
    """Load test scenario data"""
    return load_data_config("test_scenarios")


def get_user_by_role(role: str) -> Optional[Dict[str, Any]]:
    """Get a user by role from users config"""
    users = load_users()
    for key, user_data in users.items():
        if isinstance(user_data, dict) and user_data.get("role") == role:
            return user_data
    return None


def get_form_data(form_name: str, data_type: str = "valid_data") -> Optional[Dict[str, Any]]:
    """Get form data by form name and data type (valid_data or invalid_data)"""
    forms = load_forms()
    form_data = forms.get(form_name, {})
    return form_data.get(data_type)


def get_scenario_step(scenario_name: str, step_name: str) -> Optional[Dict[str, Any]]:
    """Get a specific step from a test scenario"""
    scenarios = load_test_scenarios()
    scenario = scenarios.get(scenario_name, {})
    return scenario.get(step_name)


def merge_data(base_data: Dict[str, Any], override_data: Dict[str, Any]) -> Dict[str, Any]:
    """Merge two data dictionaries, with override_data taking precedence"""
    merged = base_data.copy()
    merged.update(override_data)
    return merged


def replace_placeholders(data: Any, replacements: Dict[str, str]) -> Any:
    """Replace placeholders in data with actual values"""
    if isinstance(data, dict):
        return {k: replace_placeholders(v, replacements) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_placeholders(item, replacements) for item in data]
    elif isinstance(data, str):
        result = data
        for key, value in replacements.items():
            result = result.replace(f"{{{key}}}", str(value))
        return result
    else:
        return data


def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> bool:
    """Validate that all required fields are present in data"""
    return all(field in data for field in required_fields)


def get_nested_value(data: Dict[str, Any], path: str, default: Any = None) -> Any:
    """Get a nested value from a dictionary using dot notation path"""
    keys = path.split(".")
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current

