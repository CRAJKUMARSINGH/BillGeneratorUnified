import os
import time
import hashlib
import pickle
import threading
from typing import Any, Dict, Optional, List, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import cachetools
from pathlib import Path
import logging

@dataclass
class CacheEntry:
    data: Any
    timestamp: datetime
    access_count: int
    size_bytes: int
    ttl: Optional[timedelta] = None
    
    @property
    def is_expired(self) -> bool:
        if self.ttl is None:
            return False
        return datetime.now() > self.timestamp + self.ttl
    
    @property
    def age_seconds(self) -> float:
        return (datetime.now() - self.timestamp).total_seconds()

class CacheManager:
    def __init__(self, 
                 memory_cache_size: int = 1000,
                 disk_cache_dir: str = "cache",
                 max_disk_cache_size: int = 100 * 1024 * 1024,  # 100MB
                 default_ttl: Optional[timedelta] = None):
        
        self.memory_cache = cachetools.LRUCache(maxsize=memory_cache_size)
        self.disk_cache_dir = Path(disk_cache_dir)
        self.disk_cache_dir.mkdir(exist_ok=True)
        self.max_disk_cache_size = max_disk_cache_size
        self.default_ttl = default_ttl or timedelta(hours=1)
        
        # Statistics
        self.stats = {
            'memory_hits': 0,
            'memory_misses': 0,
            'disk_hits': 0,
            'disk_misses': 0,
            'evictions': 0,
            'total_requests': 0
        }
        
        self.lock = threading.RLock()
        self.logger = logging.getLogger(__name__)
        
        # Cleanup thread
        self.cleanup_thread = threading.Thread(target=self._cleanup_worker, daemon=True)
        self.cleanup_thread.start()
        
    def _generate_key(self, key: str, namespace: str = "default") -> str:
        """Generate a cache key with namespace"""
        return f"{namespace}:{hashlib.md5(key.encode()).hexdigest()}"
        
    def _get_disk_path(self, key: str) -> Path:
        """Get disk cache file path"""
        return self.disk_cache_dir / f"{key}.cache"
        
    def _serialize_entry(self, entry: CacheEntry) -> bytes:
        """Serialize cache entry"""
        return pickle.dumps(entry)
        
    def _deserialize_entry(self, data: bytes) -> CacheEntry:
        """Deserialize cache entry"""
        return pickle.loads(data)
        
    def get(self, key: str, namespace: str = "default") -> Optional[Any]:
        """Get value from cache"""
        with self.lock:
            self.stats['total_requests'] += 1
            cache_key = self._generate_key(key, namespace)
            
            # Try memory cache first
            if cache_key in self.memory_cache:
                entry = self.memory_cache[cache_key]
                if not entry.is_expired:
                    entry.access_count += 1
                    self.stats['memory_hits'] += 1
                    self.logger.debug(f"Memory cache hit: {key}")
                    return entry.data
                else:
                    # Remove expired entry
                    del self.memory_cache[cache_key]
                    self.stats['evictions'] += 1
                    
            # Try disk cache
            disk_path = self._get_disk_path(cache_key)
            if disk_path.exists():
                try:
                    entry_data = disk_path.read_bytes()
                    entry = self._deserialize_entry(entry_data)
                    
                    if not entry.is_expired:
                        entry.access_count += 1
                        # Promote to memory cache
                        self.memory_cache[cache_key] = entry
                        self.stats['disk_hits'] += 1
                        self.logger.debug(f"Disk cache hit: {key}")
                        return entry.data
                    else:
                        # Remove expired entry
                        disk_path.unlink()
                        self.stats['evictions'] += 1
                        
                except Exception as e:
                    self.logger.error(f"Disk cache read error: {e}")
                    if disk_path.exists():
                        disk_path.unlink()
                        
            self.stats['memory_misses'] += 1
            self.logger.debug(f"Cache miss: {key}")
            return None
            
    def set(self, key: str, value: Any, namespace: str = "default", 
            ttl: Optional[timedelta] = None) -> None:
        """Set value in cache"""
        with self.lock:
            cache_key = self._generate_key(key, namespace)
            ttl = ttl or self.default_ttl
            
            # Create cache entry
            entry = CacheEntry(
                data=value,
                timestamp=datetime.now(),
                access_count=1,
                size_bytes=len(pickle.dumps(value)),
                ttl=ttl
            )
            
            # Store in memory cache
            try:
                self.memory_cache[cache_key] = entry
            except cachetools.CacheSizeError:
                # Memory cache full, evict oldest
                self.stats['evictions'] += 1
                self.memory_cache[cache_key] = entry
                
            # Store in disk cache if value is large
            if entry.size_bytes > 1024:  # Larger than 1KB
                self._store_to_disk(cache_key, entry)
                
            self.logger.debug(f"Cache set: {key} ({entry.size_bytes} bytes)")
            
    def _store_to_disk(self, cache_key: str, entry: CacheEntry):
        """Store entry to disk cache"""
        try:
            disk_path = self._get_disk_path(cache_key)
            entry_data = self._serialize_entry(entry)
            disk_path.write_bytes(entry_data)
        except Exception as e:
            self.logger.error(f"Disk cache write error: {e}")
            
    def delete(self, key: str, namespace: str = "default") -> bool:
        """Delete entry from cache"""
        with self.lock:
            cache_key = self._generate_key(key, namespace)
            deleted = False
            
            # Remove from memory cache
            if cache_key in self.memory_cache:
                del self.memory_cache[cache_key]
                deleted = True
                
            # Remove from disk cache
            disk_path = self._get_disk_path(cache_key)
            if disk_path.exists():
                disk_path.unlink()
                deleted = True
                
            if deleted:
                self.logger.debug(f"Cache delete: {key}")
                
            return deleted
            
    def clear(self, namespace: Optional[str] = None) -> None:
        """Clear cache entries"""
        with self.lock:
            if namespace:
                # Clear specific namespace
                prefix = f"{namespace}:"
                keys_to_remove = [
                    key for key in self.memory_cache.keys()
                    if key.startswith(prefix)
                ]
                
                for key in keys_to_remove:
                    del self.memory_cache[key]
                    
                # Clear disk cache for namespace
                for disk_file in self.disk_cache_dir.glob(f"{namespace}:*.cache"):
                    disk_file.unlink()
                    
                self.logger.info(f"Cleared namespace: {namespace}")
            else:
                # Clear all cache
                self.memory_cache.clear()
                
                for disk_file in self.disk_cache_dir.glob("*.cache"):
                    disk_file.unlink()
                    
                self.logger.info("Cleared all cache")
                
    def _cleanup_worker(self):
        """Background cleanup worker"""
        while True:
            try:
                self._cleanup_expired()
                self._cleanup_disk_size()
                time.sleep(300)  # Run every 5 minutes
            except Exception as e:
                self.logger.error(f"Cleanup worker error: {e}")
                
    def _cleanup_expired(self):
        """Clean up expired entries"""
        with self.lock:
            # Clean memory cache
            expired_keys = []
            for key, entry in self.memory_cache.items():
                if entry.is_expired:
                    expired_keys.append(key)
                    
            for key in expired_keys:
                del self.memory_cache[key]
                self.stats['evictions'] += 1
                
            # Clean disk cache
            for disk_file in self.disk_cache_dir.glob("*.cache"):
                try:
                    entry_data = disk_file.read_bytes()
                    entry = self._deserialize_entry(entry_data)
                    
                    if entry.is_expired:
                        disk_file.unlink()
                        self.stats['evictions'] += 1
                except Exception:
                    disk_file.unlink()
                    
    def _cleanup_disk_size(self):
        """Clean up disk cache to maintain size limit"""
        total_size = sum(
            f.stat().st_size 
            for f in self.disk_cache_dir.glob("*.cache")
        )
        
        if total_size > self.max_disk_cache_size:
            # Get files sorted by access time
            files_with_time = []
            for disk_file in self.disk_cache_dir.glob("*.cache"):
                try:
                    entry_data = disk_file.read_bytes()
                    entry = self._deserialize_entry(entry_data)
                    files_with_time.append((entry.timestamp, disk_file))
                except Exception:
                    files_with_time.append((datetime.min, disk_file))
                    
            # Sort by last access and remove oldest
            files_with_time.sort(key=lambda x: x[0])
            
            for timestamp, disk_file in files_with_time:
                disk_file.unlink()
                self.stats['evictions'] += 1
                total_size -= disk_file.stat().st_size
                
                if total_size <= self.max_disk_cache_size * 0.8:  # 80% of max
                    break
                    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        with self.lock:
            total_requests = self.stats['total_requests']
            hits = self.stats['memory_hits'] + self.stats['disk_hits']
            
            hit_rate = (hits / total_requests * 100) if total_requests > 0 else 0
            
            disk_size = sum(
                f.stat().st_size 
                for f in self.disk_cache_dir.glob("*.cache")
            )
            
            return {
                'memory_cache_size': len(self.memory_cache),
                'memory_cache_maxsize': self.memory_cache.maxsize,
                'disk_cache_size_bytes': disk_size,
                'disk_cache_files': len(list(self.disk_cache_dir.glob("*.cache"))),
                'hit_rate_percent': round(hit_rate, 2),
                'memory_hit_rate_percent': round(
                    (self.stats['memory_hits'] / total_requests * 100) if total_requests > 0 else 0, 2
                ),
                'disk_hit_rate_percent': round(
                    (self.stats['disk_hits'] / total_requests * 100) if total_requests > 0 else 0, 2
                ),
                'evictions': self.stats['evictions'],
                'total_requests': total_requests
            }
            
    def get_memory_info(self) -> Dict:
        """Get memory usage information"""
        with self.lock:
            total_memory_usage = 0
            entry_count = 0
            
            for entry in self.memory_cache.values():
                total_memory_usage += entry.size_bytes
                entry_count += 1
                
            return {
                'entry_count': entry_count,
                'total_memory_bytes': total_memory_usage,
                'average_entry_size': total_memory_usage / entry_count if entry_count > 0 else 0,
                'max_memory_bytes': self.memory_cache.maxsize * 1024  # Estimated
            }

# Global cache manager instance
cache_manager = CacheManager()

def get_cache_manager() -> CacheManager:
    """Get the global cache manager instance"""
    return cache_manager