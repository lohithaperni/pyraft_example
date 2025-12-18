"""API helper functions for loading API configs and making API calls"""

import requests
from typing import Dict, Any, Optional
from core.config_loader import load_data_config, load_env_config, BASE_DIR
from pathlib import Path


def load_api_endpoints() -> Dict[str, Any]:
    """Load API endpoints configuration"""
    return load_data_config("api/endpoints")


def load_api_payloads() -> Dict[str, Any]:
    """Load API request payloads"""
    return load_data_config("api/payloads")


def load_api_headers() -> Dict[str, Any]:
    """Load API headers configuration"""
    return load_data_config("api/headers")


def load_api_test_data() -> Dict[str, Any]:
    """Load API test data"""
    return load_data_config("api/test_data")


def load_expected_responses() -> Dict[str, Any]:
    """Load expected API responses"""
    return load_data_config("api/expected_responses")


def get_api_base_url(env: str = "dev") -> str:
    """Get API base URL for the specified environment"""
    env_config = load_env_config(env)
    return env_config.get("api_base_url", "")


def get_endpoint(endpoint_group: str, endpoint_name: str) -> Optional[str]:
    """Get a specific endpoint URL"""
    endpoints = load_api_endpoints()
    endpoint_group_data = endpoints.get("endpoints", {}).get(endpoint_group, {})
    return endpoint_group_data.get(endpoint_name)


def get_full_url(env: str, endpoint_group: str, endpoint_name: str, **path_params) -> str:
    """Construct full API URL with base URL and endpoint, replacing path parameters"""
    base_url = get_api_base_url(env)
    endpoint = get_endpoint(endpoint_group, endpoint_name)
    
    if not endpoint:
        raise ValueError(f"Endpoint {endpoint_group}.{endpoint_name} not found")
    
    # Replace path parameters in endpoint
    full_url = base_url + endpoint
    for key, value in path_params.items():
        full_url = full_url.replace(f"{{{key}}}", str(value))
    
    return full_url


def get_payload(payload_name: str, payload_type: str = "valid") -> Optional[Dict[str, Any]]:
    """Get a specific payload by name and type (valid/invalid)"""
    payloads = load_api_payloads()
    payload_data = payloads.get(payload_name, {})
    return payload_data.get(payload_type)


def get_headers(env: str = "dev", header_type: str = "default_headers") -> Dict[str, str]:
    """Get headers for API requests"""
    headers_config = load_api_headers()
    
    if header_type == "authenticated_headers":
        headers = headers_config.get("authenticated_headers", {}).get(env, {})
    elif header_type == "default_headers":
        headers = headers_config.get("default_headers", {})
    else:
        headers = headers_config.get(header_type, {})
    
    return headers.copy()


def get_auth_token(env: str = "dev", token_type: str = "bearer_token") -> Optional[str]:
    """Get authentication token for the specified environment"""
    headers_config = load_api_headers()
    auth_tokens = headers_config.get("auth_tokens", {}).get(env, {})
    return auth_tokens.get(token_type)


def merge_headers(base_headers: Dict[str, str], additional_headers: Dict[str, str]) -> Dict[str, str]:
    """Merge headers with additional headers taking precedence"""
    merged = base_headers.copy()
    merged.update(additional_headers)
    return merged


def get_expected_response(response_name: str) -> Optional[Dict[str, Any]]:
    """Get expected response structure"""
    expected_responses = load_expected_responses()
    return expected_responses.get(response_name)


def make_api_request(
    method: str,
    url: str,
    headers: Optional[Dict[str, str]] = None,
    payload: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    timeout: int = 30
) -> requests.Response:
    """Make an API request using requests library"""
    if headers is None:
        headers = get_headers()
    
    if method.upper() == "GET":
        response = requests.get(url, headers=headers, params=params, timeout=timeout)
    elif method.upper() == "POST":
        response = requests.post(url, headers=headers, json=payload, params=params, timeout=timeout)
    elif method.upper() == "PUT":
        response = requests.put(url, headers=headers, json=payload, params=params, timeout=timeout)
    elif method.upper() == "DELETE":
        response = requests.delete(url, headers=headers, params=params, timeout=timeout)
    elif method.upper() == "PATCH":
        response = requests.patch(url, headers=headers, json=payload, params=params, timeout=timeout)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")
    
    return response

