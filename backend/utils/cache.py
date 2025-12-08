"""
Redis caching utilities for the BillGenerator backend.
"""
import redis
import json
import os
from functools import wraps
from typing import Any, Callable, Optional

class CacheManager:
    """Manages Redis caching for the application."""
    
    def __init__(self):
        """Initialize Redis connection."""
        redis_host = os.environ.get('REDIS_HOST', 'localhost')
        redis_port = int(os.environ.get('REDIS_PORT', 6379))
        redis_db = int(os.environ.get('REDIS_DB', 0))
        
        try:
            self.redis_client = redis.Redis(
                host=redis_host,
                port=redis_port,
                db=redis_db,
                decode_responses=True
            )
            # Test connection
            self.redis_client.ping()
            self.connected = True
        except Exception as e:
            print(f"Warning: Could not connect to Redis: {e}")
            self.connected = False
            self.redis_client = None
    
    def set(self, key: str, value: Any, expire: int = 300) -> bool:
        """
        Set a value in cache.
        
        Args:
            key: Cache key
            value: Value to cache (will be JSON serialized)
            expire: Expiration time in seconds (default: 5 minutes)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.connected or not self.redis_client:
            return False
            
        try:
            serialized_value = json.dumps(value)
            result = self.redis_client.setex(key, expire, serialized_value)
            return result
        except Exception as e:
            print(f"Cache set error: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/not connected
        """
        if not self.connected or not self.redis_client:
            return None
            
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Cache get error: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """
        Delete a value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.connected or not self.redis_client:
            return False
            
        try:
            result = self.redis_client.delete(key)
            return result > 0
        except Exception as e:
            print(f"Cache delete error: {e}")
            return False
    
    def flush(self) -> bool:
        """
        Flush all cache data.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.connected or not self.redis_client:
            return False
            
        try:
            self.redis_client.flushdb()
            return True
        except Exception as e:
            print(f"Cache flush error: {e}")
            return False

# Global cache manager instance
cache_manager = CacheManager()

def cached(expire: int = 300):
    """
    Decorator to cache function results.
    
    Args:
        expire: Cache expiration time in seconds (default: 5 minutes)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache first
            cached_result = cache_manager.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # If not in cache, call function and cache result
            result = func(*args, **kwargs)
            cache_manager.set(cache_key, result, expire)
            return result
        
        return wrapper
    return decorator