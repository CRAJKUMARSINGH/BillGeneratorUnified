import os
import time
import threading
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, Future, as_completed
import logging
from queue import Queue, Empty
import psutil

@dataclass
class BatchConfig:
    max_workers: int = 4
    batch_size: int = 100
    timeout_seconds: float = 300.0
    retry_attempts: int = 3
    retry_delay: float = 1.0
    progress_callback: Optional[Callable[[int, int], None]] = None

@dataclass
class BatchJob:
    job_id: str
    items: List[Any]
    processor: Callable[[Any], Any]
    config: BatchConfig
    status: str = "pending"
    results: List[Any] = None
    errors: List[Exception] = None
    start_time: float = None
    end_time: float = None
    processed_count: int = 0

class ParallelBatchProcessor:
    def __init__(self, config: BatchConfig = None):
        self.config = config or BatchConfig()
        self.active_jobs: Dict[str, BatchJob] = {}
        self.job_queue: Queue = Queue()
        self.executor: Optional[ThreadPoolExecutor] = None
        self.futures: Dict[str, Future] = {}
        self.lock = threading.RLock()
        self.logger = logging.getLogger(__name__)
        
        # Resource monitoring
        self.max_memory_percent = 80.0
        self.max_cpu_percent = 90.0
        
        # Statistics
        self.stats = {
            'total_jobs': 0,
            'completed_jobs': 0,
            'failed_jobs': 0,
            'total_items_processed': 0,
            'average_processing_time': 0.0
        }
        
        # Start worker thread
        self.worker_thread = threading.Thread(target=self._job_processor, daemon=True)
        self.worker_thread.start()
        
    def submit_batch(self, items: List[Any], processor: Callable[[Any], Any],
                    job_id: str = None, config: BatchConfig = None) -> str:
        """Submit batch job for processing"""
        if job_id is None:
            job_id = f"batch_{int(time.time() * 1000)}"
            
        job_config = config or self.config
        
        job = BatchJob(
            job_id=job_id,
            items=items,
            processor=processor,
            config=job_config,
            status="queued",
            results=[],
            errors=[],
            start_time=time.time()
        )
        
        with self.lock:
            self.active_jobs[job_id] = job
            self.job_queue.put(job)
            self.stats['total_jobs'] += 1
            
        self.logger.info(f"Batch job submitted: {job_id} ({len(items)} items)")
        return job_id
        
    def _job_processor(self):
        """Background thread for processing jobs"""
        while True:
            try:
                # Get job from queue
                job = self.job_queue.get(timeout=1.0)
                
                # Check system resources
                if not self._check_resources():
                    self.logger.warning("Insufficient resources, waiting...")
                    time.sleep(5.0)
                    self.job_queue.put(job)  # Re-queue job
                    continue
                    
                # Process job
                self._process_job(job)
                
            except Empty:
                continue
            except Exception as e:
                self.logger.error(f"Job processor error: {e}")
                
    def _process_job(self, job: BatchJob):
        """Process individual batch job"""
        try:
            job.status = "processing"
            self.logger.info(f"Processing job: {job.job_id}")
            
            # Create thread pool for this job
            with ThreadPoolExecutor(max_workers=job.config.max_workers) as executor:
                # Submit items in batches
                batch_futures = {}
                
                for i in range(0, len(job.items), job.config.batch_size):
                    batch = job.items[i:i + job.config.batch_size]
                    future = executor.submit(self._process_batch, batch, job)
                    batch_futures[future] = i
                    
                # Collect results
                for future in as_completed(batch_futures, timeout=job.config.timeout_seconds):
                    try:
                        batch_results = future.result()
                        job.results.extend(batch_results)
                        job.processed_count += len(batch_results)
                        
                        # Update progress
                        if job.config.progress_callback:
                            job.config.progress_callback(job.processed_count, len(job.items))
                            
                    except Exception as e:
                        job.errors.append(e)
                        self.logger.error(f"Batch processing error: {e}")
                        
            job.status = "completed" if not job.errors else "completed_with_errors"
            job.end_time = time.time()
            
            # Update statistics
            with self.lock:
                self.stats['completed_jobs'] += 1
                self.stats['total_items_processed'] += job.processed_count
                
                # Update average processing time
                processing_time = job.end_time - job.start_time
                total_completed = self.stats['completed_jobs']
                current_avg = self.stats['average_processing_time']
                self.stats['average_processing_time'] = (
                    (current_avg * (total_completed - 1) + processing_time) / total_completed
                )
                
            self.logger.info(f"Job completed: {job.job_id} - "
                           f"{job.processed_count}/{len(job.items)} items processed")
                           
        except Exception as e:
            job.status = "failed"
            job.end_time = time.time()
            job.errors.append(e)
            
            with self.lock:
                self.stats['failed_jobs'] += 1
                
            self.logger.error(f"Job failed: {job.job_id} - {e}")
            
    def _process_batch(self, batch: List[Any], job: BatchJob) -> List[Any]:
        """Process a batch of items with retry logic"""
        results = []
        
        for item in batch:
            success = False
            last_error = None
            
            for attempt in range(job.config.retry_attempts):
                try:
                    result = job.processor(item)
                    results.append(result)
                    success = True
                    break
                    
                except Exception as e:
                    last_error = e
                    if attempt < job.config.retry_attempts - 1:
                        time.sleep(job.config.retry_delay * (2 ** attempt))  # Exponential backoff
                        
            if not success:
                job.errors.append(last_error or Exception("Unknown error"))
                
        return results
        
    def _check_resources(self) -> bool:
        """Check if system resources are available"""
        try:
            # Check memory
            memory = psutil.virtual_memory()
            if memory.percent > self.max_memory_percent:
                return False
                
            # Check CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent > self.max_cpu_percent:
                return False
                
            return True
            
        except Exception:
            return True  # Assume resources are available if check fails
            
    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific job"""
        with self.lock:
            job = self.active_jobs.get(job_id)
            if not job:
                return None
                
            return {
                'job_id': job.job_id,
                'status': job.status,
                'total_items': len(job.items),
                'processed_count': job.processed_count,
                'progress_percent': (job.processed_count / len(job.items)) * 100 if job.items else 0,
                'errors_count': len(job.errors),
                'start_time': job.start_time,
                'end_time': job.end_time,
                'duration': (job.end_time or time.time()) - job.start_time
            }
            
    def get_all_jobs(self) -> List[Dict[str, Any]]:
        """Get status of all jobs"""
        with self.lock:
            return [self.get_job_status(job_id) for job_id in self.active_jobs.keys()]
            
    def get_active_jobs(self) -> List[Dict[str, Any]]:
        """Get status of active jobs"""
        with self.lock:
            return [
                self.get_job_status(job_id) 
                for job_id, job in self.active_jobs.items()
                if job.status in ['queued', 'processing']
            ]
            
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a job"""
        with self.lock:
            job = self.active_jobs.get(job_id)
            if not job or job.status in ['completed', 'failed']:
                return False
                
            job.status = "cancelled"
            job.end_time = time.time()
            
            # Cancel associated futures if any
            if job_id in self.futures:
                self.futures[job_id].cancel()
                del self.futures[job_id]
                
            self.logger.info(f"Job cancelled: {job_id}")
            return True
            
    def cleanup_completed_jobs(self, max_age_hours: int = 24):
        """Clean up completed jobs older than specified hours"""
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        with self.lock:
            jobs_to_remove = []
            
            for job_id, job in self.active_jobs.items():
                if (job.status in ['completed', 'failed', 'cancelled'] and 
                    job.end_time and 
                    current_time - job.end_time > max_age_seconds):
                    jobs_to_remove.append(job_id)
                    
            for job_id in jobs_to_remove:
                del self.active_jobs[job_id]
                if job_id in self.futures:
                    del self.futures[job_id]
                    
            if jobs_to_remove:
                self.logger.info(f"Cleaned up {len(jobs_to_remove)} old jobs")
                
    def get_statistics(self) -> Dict[str, Any]:
        """Get processing statistics"""
        with self.lock:
            active_count = sum(
                1 for job in self.active_jobs.values()
                if job.status in ['queued', 'processing']
            )
            
            return {
                'total_jobs': self.stats['total_jobs'],
                'completed_jobs': self.stats['completed_jobs'],
                'failed_jobs': self.stats['failed_jobs'],
                'active_jobs': active_count,
                'total_items_processed': self.stats['total_items_processed'],
                'average_processing_time': self.stats['average_processing_time'],
                'success_rate': (
                    (self.stats['completed_jobs'] - len([j for j in self.active_jobs.values() if 'error' in j.status])) /
                    max(1, self.stats['completed_jobs'])
                ) * 100
            }
            
    def configure_resource_limits(self, max_memory_percent: float = 80.0, 
                                 max_cpu_percent: float = 90.0):
        """Configure resource limits"""
        self.max_memory_percent = max_memory_percent
        self.max_cpu_percent = max_cpu_percent
        
        self.logger.info(f"Resource limits updated: Memory={max_memory_percent}%, CPU={max_cpu_percent}%")
        
    def shutdown(self):
        """Shutdown the processor"""
        self.logger.info("Shutting down parallel batch processor")
        
        # Cancel all active jobs
        with self.lock:
            for job_id in list(self.active_jobs.keys()):
                self.cancel_job(job_id)
                
        # Shutdown executor if running
        if self.executor:
            self.executor.shutdown(wait=True)

# Global batch processor instance
batch_processor = ParallelBatchProcessor()

def get_batch_processor() -> ParallelBatchProcessor:
    """Get the global batch processor instance"""
    return batch_processor