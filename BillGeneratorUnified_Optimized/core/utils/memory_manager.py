import gc
import threading
import time
import psutil
import os
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import weakref
import logging

@dataclass
class MemoryStats:
    total_memory: int
    available_memory: int
    used_memory: int
    memory_percent: float
    process_memory: int
    process_percent: float
    timestamp: datetime

class MemoryManager:
    def __init__(self, max_memory_percent: float = 80.0, cleanup_interval: int = 30):
        self.max_memory_percent = max_memory_percent
        self.cleanup_interval = cleanup_interval
        self.process = psutil.Process()
        self.memory_history: List[MemoryStats] = []
        self.cleanup_callbacks: List[Callable] = []
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.logger = logging.getLogger(__name__)
        
        # Weak references for tracking objects
        self.tracked_objects: Dict[str, weakref.WeakSet] = {}
        
    def start_monitoring(self):
        """Start background memory monitoring"""
        if self.monitoring:
            return
            
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_memory, daemon=True)
        self.monitor_thread.start()
        self.logger.info("Memory monitoring started")
        
    def stop_monitoring(self):
        """Stop background memory monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        self.logger.info("Memory monitoring stopped")
        
    def _monitor_memory(self):
        """Background monitoring thread"""
        while self.monitoring:
            try:
                stats = self.get_memory_stats()
                self.memory_history.append(stats)
                
                # Keep only last 100 records
                if len(self.memory_history) > 100:
                    self.memory_history.pop(0)
                    
                # Check if cleanup is needed
                if stats.memory_percent > self.max_memory_percent:
                    self.logger.warning(f"Memory usage high: {stats.memory_percent:.1f}%")
                    self.perform_cleanup()
                    
            except Exception as e:
                self.logger.error(f"Memory monitoring error: {e}")
                
            time.sleep(self.cleanup_interval)
            
    def get_memory_stats(self) -> MemoryStats:
        """Get current memory statistics"""
        memory_info = psutil.virtual_memory()
        process_memory = self.process.memory_info()
        
        return MemoryStats(
            total_memory=memory_info.total,
            available_memory=memory_info.available,
            used_memory=memory_info.used,
            memory_percent=memory_info.percent,
            process_memory=process_memory.rss,
            process_percent=self.process.memory_percent(),
            timestamp=datetime.now()
        )
        
    def perform_cleanup(self):
        """Perform memory cleanup"""
        self.logger.info("Performing memory cleanup...")
        
        # Run cleanup callbacks
        for callback in self.cleanup_callbacks:
            try:
                callback()
            except Exception as e:
                self.logger.error(f"Cleanup callback error: {e}")
                
        # Force garbage collection
        collected = gc.collect()
        self.logger.info(f"Garbage collection collected {collected} objects")
        
        # Clear caches if needed
        if hasattr(self, '_clear_caches'):
            self._clear_caches()
            
    def register_cleanup_callback(self, callback: Callable):
        """Register a cleanup callback"""
        self.cleanup_callbacks.append(callback)
        
    def track_object(self, obj: object, category: str = "default"):
        """Track an object for memory monitoring"""
        if category not in self.tracked_objects:
            self.tracked_objects[category] = weakref.WeakSet()
        self.tracked_objects[category].add(obj)
        
    def get_tracked_objects_count(self, category: str = "default") -> int:
        """Get count of tracked objects in category"""
        if category in self.tracked_objects:
            return len(self.tracked_objects[category])
        return 0
        
    def get_memory_report(self) -> Dict:
        """Get comprehensive memory report"""
        stats = self.get_memory_stats()
        
        report = {
            "current_stats": stats,
            "history_count": len(self.memory_history),
            "tracked_objects": {
                category: len(objects) 
                for category, objects in self.tracked_objects.items()
            },
            "cleanup_callbacks": len(self.cleanup_callbacks),
            "monitoring_active": self.monitoring
        }
        
        # Add trend analysis if we have history
        if len(self.memory_history) > 1:
            recent = self.memory_history[-10:]
            avg_memory = sum(s.memory_percent for s in recent) / len(recent)
            report["trend"] = {
                "average_memory_percent": avg_memory,
                "peak_memory_percent": max(s.memory_percent for s in recent),
                "memory_increasing": recent[-1].memory_percent > recent[0].memory_percent
            }
            
        return report
        
    def _clear_caches(self):
        """Clear various caches"""
        # Clear functools.lru_cache
        import functools
        for func in gc.get_objects():
            if isinstance(func, functools._lru_cache_wrapper):
                func.cache_clear()
                
        # Clear module caches
        import sys
        for module in list(sys.modules.values()):
            if hasattr(module, '__dict__'):
                module.__dict__.clear()
                
    def optimize_memory_usage(self):
        """Actively optimize memory usage"""
        self.logger.info("Optimizing memory usage...")
        
        # Compact memory
        if hasattr(gc, 'collect'):
            for generation in range(3):
                collected = gc.collect(generation)
                self.logger.debug(f"Generation {generation}: collected {collected} objects")
                
        # Clear object pools
        self.tracked_objects.clear()
        
        # Trigger cleanup callbacks
        self.perform_cleanup()
        
    def __enter__(self):
        self.start_monitoring()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_monitoring()

# Global memory manager instance
memory_manager = MemoryManager()

def get_memory_manager() -> MemoryManager:
    """Get the global memory manager instance"""
    return memory_manager