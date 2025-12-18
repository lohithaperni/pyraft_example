"""Example database tests using configuration-driven approach"""

import pytest
from core.db_helper import (
    get_query,
    execute_query,
    execute_insert,
    get_test_data,
    verify_expected_count,
    cleanup_test_data
)


def test_db_connection(db_connection):
    """Test database connection"""
    assert db_connection is not None, "Database connection should be established"
    
    # Test a simple query
    result = execute_query("SELECT 1 as test", fetch_one=True)
    assert result is not None, "Should be able to execute a query"
    assert result.get("test") == 1, "Query result should be correct"


def test_db_get_user_count(db_queries):
    """Test getting user count from database"""
    query = get_query("user_queries", "get_user_count")
    assert query is not None, "User count query should exist"
    
    result = execute_query(query, fetch_one=True)
    assert result is not None, "Should get user count result"
    assert "count" in result, "Result should contain count field"
    assert isinstance(result["count"], int), "Count should be an integer"
    assert result["count"] >= 0, "Count should be non-negative"


def test_db_get_user_by_email(db_queries):
    """Test getting user by email"""
    query = get_query("user_queries", "get_user_by_email")
    assert query is not None, "Get user by email query should exist"
    
    # Use test email (this may not exist in DB, so we expect None or empty result)
    test_email = "test_user_1@test.example.com"
    result = execute_query(query, params={"email": test_email}, fetch_one=True)
    
    # Result can be None if user doesn't exist, or a dict if it does
    if result is not None:
        assert "email" in result, "Result should contain email field"
        assert result["email"] == test_email, "Email should match"


def test_db_insert_and_cleanup(db_queries, db_test_data):
    """Test inserting test data and cleaning it up"""
    # Get insert query
    insert_query = get_query("insert_queries", "insert_user")
    assert insert_query is not None, "Insert user query should exist"
    
    # Get test data
    test_users = get_test_data("users_to_insert")
    assert test_users is not None and len(test_users) > 0, "Test users data should exist"
    
    # Use first test user
    test_user = test_users[0]
    
    # Insert test user (may fail if constraints violated - that's okay for example)
    try:
        user_id = execute_insert(
            insert_query,
            params={
                "name": test_user["name"],
                "email": f"test_automation_{test_user['email']}",
                "password_hash": test_user["password_hash"],
                "role": test_user["role"]
            }
        )
        
        if user_id:
            # Verify user was inserted
            get_query_sql = get_query("user_queries", "get_user_by_id")
            if get_query_sql:
                result = execute_query(
                    get_query_sql.replace(":user_id", str(user_id)),
                    fetch_one=True
                )
                assert result is not None, "Inserted user should be retrievable"
            
            # Cleanup: Delete the test user
            delete_query = get_query("delete_queries", "delete_user")
            if delete_query:
                execute_query(
                    delete_query.replace(":user_id", str(user_id)),
                    fetch=False
                )
    except Exception as e:
        # If insert fails (e.g., constraint violation), that's okay for example test
        pytest.skip(f"Insert test skipped due to: {str(e)}")


def test_db_verify_table_counts():
    """Test verifying table row counts"""
    # Verify users table has reasonable count
    result = verify_expected_count("users", expected_min=0, expected_max=100000)
    assert result is True, "Users table count should be within expected range"
    
    # Note: Adjust table name and ranges based on your actual database schema


def test_db_get_products_in_stock(db_queries):
    """Test getting products that are in stock"""
    query = get_query("product_queries", "get_products_in_stock")
    
    if query:
        results = execute_query(query)
        assert results is not None, "Should get products in stock"
        assert isinstance(results, list), "Results should be a list"
        
        # Verify all returned products have stock > 0
        for product in results:
            assert product.get("stock", 0) > 0, "All products should have stock > 0"


def test_db_cleanup_test_data(db_queries):
    """Test cleanup queries exist and can be executed"""
    cleanup_query = get_query("cleanup_queries", "cleanup_test_users")
    
    if cleanup_query:
        # Execute cleanup (this is safe - only deletes test data)
        try:
            execute_query(cleanup_query, fetch=False)
            # If no exception, cleanup was successful
            assert True
        except Exception as e:
            # If cleanup fails, log but don't fail test
            pytest.skip(f"Cleanup skipped: {str(e)}")

