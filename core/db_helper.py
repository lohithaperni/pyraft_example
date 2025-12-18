"""Database helper functions for loading DB configs and executing queries"""

from typing import Dict, Any, Optional, List
import psycopg2
from psycopg2 import pool, sql
from psycopg2.extras import RealDictCursor
from core.config_loader import load_data_config, load_env_config, BASE_DIR


# Connection pool (can be initialized per environment)
_connection_pools: Dict[str, pool.ThreadedConnectionPool] = {}


def load_db_connections() -> Dict[str, Any]:
    """Load database connection configurations"""
    return load_data_config("db/connections")


def load_db_queries() -> Dict[str, Any]:
    """Load SQL queries configuration"""
    return load_data_config("db/queries")


def load_db_test_data() -> Dict[str, Any]:
    """Load database test data"""
    return load_data_config("db/test_data")


def load_db_assertions() -> Dict[str, Any]:
    """Load database assertion configurations"""
    return load_data_config("db/assertions")


def get_db_config(env: str = "dev") -> Dict[str, Any]:
    """Get database configuration for the specified environment"""
    connections = load_db_connections()
    return connections.get(env, {})


def create_connection(env: str = "dev", use_pool: bool = True) -> Any:
    """Create a database connection for the specified environment"""
    db_config = get_db_config(env)
    
    if not db_config:
        raise ValueError(f"Database configuration for environment '{env}' not found")
    
    if use_pool:
        pool_key = f"{env}_pool"
        if pool_key not in _connection_pools:
            _connection_pools[pool_key] = pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=db_config.get("pool_size", 5),
                host=db_config["host"],
                port=db_config["port"],
                database=db_config["database"],
                user=db_config["username"],
                password=db_config["password"]
            )
        return _connection_pools[pool_key].getconn()
    else:
        return psycopg2.connect(
            host=db_config["host"],
            port=db_config["port"],
            database=db_config["database"],
            user=db_config["username"],
            password=db_config["password"]
        )


def return_connection(conn: Any, env: str = "dev"):
    """Return a connection to the pool"""
    pool_key = f"{env}_pool"
    if pool_key in _connection_pools:
        _connection_pools[pool_key].putconn(conn)


def get_query(query_group: str, query_name: str) -> Optional[str]:
    """Get a specific SQL query"""
    queries = load_db_queries()
    query_group_data = queries.get(query_group, {})
    return query_group_data.get(query_name)


def execute_query(
    query: str,
    params: Optional[Dict[str, Any]] = None,
    env: str = "dev",
    fetch: bool = True,
    fetch_one: bool = False
) -> Optional[List[Dict[str, Any]]]:
    """Execute a SQL query and return results"""
    conn = None
    try:
        conn = create_connection(env)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute(query, params)
        
        if fetch:
            if fetch_one:
                result = cursor.fetchone()
                return dict(result) if result else None
            else:
                results = cursor.fetchall()
                return [dict(row) for row in results]
        else:
            conn.commit()
            return None
            
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            return_connection(conn, env)


def execute_insert(query: str, params: Optional[Dict[str, Any]] = None, env: str = "dev") -> Optional[Any]:
    """Execute an INSERT query and return the inserted ID"""
    conn = None
    try:
        conn = create_connection(env)
        cursor = conn.cursor()
        
        cursor.execute(query, params)
        conn.commit()
        
        # Try to get the returned ID (for RETURNING clause)
        try:
            return cursor.fetchone()[0]
        except:
            return None
            
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            return_connection(conn, env)


def cleanup_test_data(table: str, condition: str, params: Optional[Dict[str, Any]] = None, env: str = "dev"):
    """Clean up test data from a table"""
    query = f"DELETE FROM {table} WHERE {condition}"
    execute_query(query, params=params, env=env, fetch=False)


def get_test_data(data_type: str) -> Optional[List[Dict[str, Any]]]:
    """Get test data sets for database operations"""
    test_data = load_db_test_data()
    return test_data.get(data_type)


def verify_expected_count(table: str, expected_min: Optional[int] = None, 
                         expected_max: Optional[int] = None, env: str = "dev") -> bool:
    """Verify that table row count is within expected range"""
    query = f"SELECT COUNT(*) as count FROM {table}"
    result = execute_query(query, env=env, fetch_one=True)
    
    if result is None:
        return False
    
    count = result.get("count", 0)
    
    if expected_min is not None and count < expected_min:
        return False
    if expected_max is not None and count > expected_max:
        return False
    
    return True


def close_all_pools():
    """Close all connection pools (useful for cleanup)"""
    for pool_key, connection_pool in _connection_pools.items():
        connection_pool.closeall()
    _connection_pools.clear()

