"""Simple in-memory cache with TTL."""

import time
from typing import Optional, Any, Dict


class SimpleCache:
    """Simple in-memory cache with TTL support."""

    def __init__(self, ttl: int = 3600):
        """
        Initialize cache.

        Args:
            ttl: Time-to-live in seconds (default: 3600 = 1 hour)
        """
        self.ttl = ttl
        self._cache: Dict[str, tuple[Any, float]] = {}

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if expired/not found
        """
        if key in self._cache:
            value, timestamp = self._cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            else:
                # Expired, remove from cache
                del self._cache[key]
        return None

    def set(self, key: str, value: Any) -> None:
        """
        Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
        """
        self._cache[key] = (value, time.time())

    def clear(self) -> None:
        """Clear all cached values."""
        self._cache.clear()

    def has(self, key: str) -> bool:
        """
        Check if key exists and is not expired.

        Args:
            key: Cache key

        Returns:
            True if key exists and not expired
        """
        return self.get(key) is not None


# Global cache instance (1-hour TTL like Streamlit's @st.cache_data)
stock_cache = SimpleCache(ttl=3600)
