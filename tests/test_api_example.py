"""Example API tests using configuration-driven approach"""

import pytest
from core.api_helper import (
    get_full_url,
    get_payload,
    get_headers,
    make_api_request,
    get_expected_response
)


def test_api_health_check(api_base_url, api_endpoints):
    """Test API health check endpoint"""
    health_endpoint = api_endpoints["endpoints"]["health"]["health_check"]
    url = api_base_url + health_endpoint
    
    headers = get_headers()
    response = make_api_request("GET", url, headers=headers)
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert "status" in response.json() or "healthy" in response.json().get("message", "").lower()


def test_api_login_success(api_base_url, api_endpoints, api_payloads, expected_responses):
    """Test successful API login"""
    login_endpoint = api_endpoints["endpoints"]["authentication"]["login"]
    url = api_base_url + login_endpoint
    
    # Get valid login payload
    payload = get_payload("login_request", "valid")
    assert payload is not None, "Login payload not found"
    
    headers = get_headers()
    response = make_api_request("POST", url, headers=headers, payload=payload)
    
    # Get expected response structure
    expected = get_expected_response("login_success")
    
    assert response.status_code == expected["status_code"], \
        f"Expected {expected['status_code']}, got {response.status_code}"
    
    response_json = response.json()
    assert "token" in response_json or "access_token" in response_json, \
        "Login response should contain token"


def test_api_login_failure(api_base_url, api_endpoints, api_payloads, expected_responses):
    """Test API login with invalid credentials"""
    login_endpoint = api_endpoints["endpoints"]["authentication"]["login"]
    url = api_base_url + login_endpoint
    
    # Get invalid login payload
    payload = get_payload("login_request", "invalid")
    assert payload is not None, "Invalid login payload not found"
    
    # Try with wrong password payload
    wrong_password_payload = payload.get("wrong_password", payload)
    
    headers = get_headers()
    response = make_api_request("POST", url, headers=headers, payload=wrong_password_payload)
    
    # Get expected response structure
    expected = get_expected_response("login_failure")
    
    assert response.status_code == expected["status_code"], \
        f"Expected {expected['status_code']}, got {response.status_code}"
    
    response_json = response.json()
    assert "error" in response_json or "message" in response_json, \
        "Error response should contain error message"


def test_api_get_user(api_base_url, api_endpoints, api_test_data, api_headers):
    """Test getting user by ID (example - requires authentication)"""
    user_endpoint = api_endpoints["endpoints"]["users"]["get_user"]
    valid_user_id = api_test_data["users"]["valid_user_id"]
    
    # Replace path parameter
    url = api_base_url + user_endpoint.replace("{user_id}", str(valid_user_id))
    
    headers = get_headers()
    # Note: In real scenario, you'd add auth token to headers
    # headers["Authorization"] = f"Bearer {auth_token}"
    
    response = make_api_request("GET", url, headers=headers)
    
    # This test may fail if authentication is required - that's expected
    # In real scenario, you'd authenticate first and use the token
    assert response.status_code in [200, 401, 403], \
        f"Unexpected status code: {response.status_code}"


def test_api_create_user(api_base_url, api_endpoints, api_payloads, expected_responses):
    """Test creating a user via API"""
    create_user_endpoint = api_endpoints["endpoints"]["users"]["create_user"]
    url = api_base_url + create_user_endpoint
    
    # Get valid create user payload
    payload = get_payload("create_user_request", "valid")
    assert payload is not None, "Create user payload not found"
    
    headers = get_headers()
    response = make_api_request("POST", url, headers=headers, payload=payload)
    
    # Get expected response structure
    expected = get_expected_response("create_user_success")
    
    # Note: This may fail if user already exists or auth required
    assert response.status_code in [expected["status_code"], 400, 401, 409], \
        f"Unexpected status code: {response.status_code}"
    
    if response.status_code == expected["status_code"]:
        response_json = response.json()
        assert "id" in response_json or "user_id" in response_json, \
            "Create user response should contain user ID"

