"""
Performance tuning configuration for Python applications.
This module provides configurations similar to JVM tuning parameters described in the documentation.
"""

import os
import gc
import sys
import psutil
from typing import Dict, Any


class PerformanceTuner:
    """Performance tuning configuration similar to JVM tuning parameters."""
    
    def __init__(self):
        """Initialize performance tuner with default values."""
        self.config = {
            # Memory settings (similar to -Xms, -Xmx)
            'initial_heap_size_mb': 512,
            'maximum_heap_size_mb': 2048,
            
            # Garbage collection settings (similar to G1GC settings)
            'gc_threshold_0': 700,  # Threshold for collecting generation 0
            'gc_threshold_1': 10,   # Threshold for collecting generation 1
            'gc_threshold_2': 10,   # Threshold for collecting generation 2
            
            # Threading settings (similar to thread pool settings)
            'max_worker_threads': psutil.cpu_count(),
            'min_worker_threads': max(1, psutil.cpu_count() // 2),
            
            # String optimization (similar to string deduplication)
            'enable_string_deduplication': True,
            
            # Connection pooling settings
            'database_max_pool_size': 20,
            'database_min_idle_connections': 5,
            'database_connection_timeout_ms': 30000,
            
            # File I/O settings
            'file_buffer_size_kb': 8,
            'enable_file_caching': True,
            
            # Caching settings
            'cache_max_size': 1000,
            'cache_expire_after_write_seconds': 3600,
        }
    
    def apply_memory_settings(self) -> None:
        """Apply memory-related settings."""
        # Set garbage collection thresholds
        gc.set_threshold(
            self.config['gc_threshold_0'],
            self.config['gc_threshold_1'],
            self.config['gc_threshold_2']
        )
        
        # Force garbage collection to apply settings
        gc.collect()
        
        print(f"Applied memory settings: GC thresholds set to "
              f"({self.config['gc_threshold_0']}, "
              f"{self.config['gc_threshold_1']}, "
              f"{self.config['gc_threshold_2']})")
    
    def get_recommended_threading(self) -> Dict[str, int]:
        """
        Get recommended threading settings based on system resources.
        
        Returns:
            Dictionary with recommended thread settings
        """
        cpu_count = psutil.cpu_count()
        memory_gb = psutil.virtual_memory().total / (1024**3)
        
        # Calculate recommended workers based on CPU and memory
        recommended_workers = min(
            self.config['max_worker_threads'],
            max(self.config['min_worker_threads'], cpu_count)
        )
        
        return {
            'recommended_workers': recommended_workers,
            'cpu_cores': cpu_count,
            'total_memory_gb': round(memory_gb, 1)
        }
    
    def optimize_string_handling(self) -> None:
        """Optimize string handling similar to JVM string deduplication."""
        if self.config['enable_string_deduplication']:
            # In Python, we can't directly deduplicate strings like JVM,
            # but we can recommend using sys.intern() for frequently used strings
            print("String optimization enabled: Consider using sys.intern() for "
                  "frequently used strings to reduce memory usage")
    
    def get_database_config(self) -> Dict[str, Any]:
        """
        Get database configuration similar to HikariCP settings.
        
        Returns:
            Dictionary with database configuration
        """
        return {
            'max_pool_size': self.config['database_max_pool_size'],
            'min_idle_connections': self.config['database_min_idle_connections'],
            'connection_timeout_ms': self.config['database_connection_timeout_ms']
        }
    
    def get_system_stats(self) -> Dict[str, Any]:
        """
        Get current system statistics.
        
        Returns:
            Dictionary with system statistics
        """
        memory = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent(interval=1)
        
        return {
            'cpu_percent': cpu_percent,
            'memory_total_gb': round(memory.total / (1024**3), 1),
            'memory_available_gb': round(memory.available / (1024**3), 1),
            'memory_percent_used': memory.percent,
            'cpu_count': psutil.cpu_count()
        }
    
    def apply_all_optimizations(self) -> None:
        """Apply all performance optimizations."""
        print("Applying all performance optimizations...")
        
        # Apply memory settings
        self.apply_memory_settings()
        
        # Optimize string handling
        self.optimize_string_handling()
        
        # Show recommended threading
        threading_info = self.get_recommended_threading()
        print(f"Threading recommendations: {threading_info}")
        
        # Show system stats
        system_stats = self.get_system_stats()
        print(f"System stats: {system_stats}")
        
        print("All performance optimizations applied successfully!")


# Global performance tuner instance
performance_tuner = PerformanceTuner()


def get_performance_config() -> Dict[str, Any]:
    """
    Get the current performance configuration.
    
    Returns:
        Dictionary with performance configuration
    """
    return performance_tuner.config


def apply_performance_tuning() -> None:
    """Apply all performance tuning configurations."""
    performance_tuner.apply_all_optimizations()


# Environment-based configuration
def load_from_environment() -> None:
    """Load configuration from environment variables."""
    env_mappings = {
        'INITIAL_HEAP_SIZE_MB': 'initial_heap_size_mb',
        'MAXIMUM_HEAP_SIZE_MB': 'maximum_heap_size_mb',
        'MAX_WORKER_THREADS': 'max_worker_threads',
        'MIN_WORKER_THREADS': 'min_worker_threads',
        'DATABASE_MAX_POOL_SIZE': 'database_max_pool_size',
        'CACHE_MAX_SIZE': 'cache_max_size'
    }
    
    for env_var, config_key in env_mappings.items():
        env_value = os.environ.get(env_var)
        if env_value:
            try:
                performance_tuner.config[config_key] = int(env_value)
            except ValueError:
                print(f"Warning: Invalid value for {env_var}: {env_value}")


# Example usage
if __name__ == "__main__":
    # Load from environment
    load_from_environment()
    
    # Apply optimizations
    apply_performance_tuning()
    
    # Show configuration
    config = get_performance_config()
    print(f"\nCurrent performance configuration: {config}")