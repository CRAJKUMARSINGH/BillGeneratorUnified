import os
import shutil
import tempfile
import threading
from typing import Dict, List, Optional, Callable, Any, BinaryIO, Union
from dataclasses import dataclass
from pathlib import Path
import logging
import time

@dataclass
class StreamingConfig:
    chunk_size: int = 8192
    temp_dir: Optional[str] = None
    max_file_size: Optional[int] = None
    progress_callback: Optional[Callable[[int, int], None]] = None

class StreamingProcessor:
    def __init__(self, config: StreamingConfig = None):
        self.config = config or StreamingConfig()
        self.active_streams: Dict[str, Dict] = {}
        self.lock = threading.RLock()
        self.logger = logging.getLogger(__name__)
        
        # Create temp directory if specified
        if self.config.temp_dir:
            Path(self.config.temp_dir).mkdir(parents=True, exist_ok=True)
            
    def stream_file(self, 
                   source: Union[str, BinaryIO], 
                   destination: Union[str, BinaryIO],
                   stream_id: Optional[str] = None) -> Dict[str, Any]:
        """Stream file from source to destination"""
        if stream_id is None:
            stream_id = f"stream_{int(time.time() * 1000)}"
            
        with self.lock:
            self.active_streams[stream_id] = {
                'start_time': time.time(),
                'bytes_processed': 0,
                'status': 'active',
                'source': str(source),
                'destination': str(destination)
            }
            
        try:
            # Handle different source types
            if isinstance(source, str):
                source_file = open(source, 'rb')
                source_size = os.path.getsize(source)
                should_close_source = True
            else:
                source_file = source
                source_file.seek(0, 2)  # Seek to end
                source_size = source_file.tell()
                source_file.seek(0)  # Reset to beginning
                should_close_source = False
                
            # Handle different destination types
            if isinstance(destination, str):
                dest_file = open(destination, 'wb')
                should_close_dest = True
            else:
                dest_file = destination
                should_close_dest = False
                
            bytes_processed = 0
            last_progress_time = time.time()
            
            while True:
                chunk = source_file.read(self.config.chunk_size)
                if not chunk:
                    break
                    
                dest_file.write(chunk)
                bytes_processed += len(chunk)
                
                # Update progress
                with self.lock:
                    self.active_streams[stream_id]['bytes_processed'] = bytes_processed
                    
                # Call progress callback
                if (self.config.progress_callback and 
                    time.time() - last_progress_time > 0.1):  # Update every 100ms
                    self.config.progress_callback(bytes_processed, source_size)
                    last_progress_time = time.time()
                    
                # Check max file size
                if (self.config.max_file_size and 
                    bytes_processed > self.config.max_file_size):
                    raise ValueError(f"File size exceeds maximum allowed: {self.config.max_file_size}")
                    
            # Close files if we opened them
            if should_close_source:
                source_file.close()
            if should_close_dest:
                dest_file.close()
                
            # Update stream status
            with self.lock:
                self.active_streams[stream_id]['status'] = 'completed'
                self.active_streams[stream_id]['end_time'] = time.time()
                
            result = {
                'stream_id': stream_id,
                'bytes_processed': bytes_processed,
                'source_size': source_size,
                'duration': time.time() - self.active_streams[stream_id]['start_time'],
                'status': 'completed'
            }
            
            self.logger.info(f"Streaming completed: {stream_id} ({bytes_processed} bytes)")
            return result
            
        except Exception as e:
            with self.lock:
                self.active_streams[stream_id]['status'] = 'error'
                self.active_streams[stream_id]['error'] = str(e)
                
            self.logger.error(f"Streaming error: {stream_id} - {e}")
            raise
            
    def stream_with_progress(self, 
                           source: Union[str, BinaryIO], 
                           destination: Union[str, BinaryIO],
                           progress_callback: Callable[[int, int], None]) -> Dict[str, Any]:
        """Stream file with progress callback"""
        self.config.progress_callback = progress_callback
        return self.stream_file(source, destination)
        
    def create_temp_stream(self, data: bytes, filename: str = None) -> str:
        """Create temporary file for streaming"""
        if filename is None:
            filename = f"temp_stream_{int(time.time() * 1000)}.tmp"
            
        if self.config.temp_dir:
            temp_path = Path(self.config.temp_dir) / filename
        else:
            fd, temp_path = tempfile.mkstemp(suffix=filename)
            os.close(fd)
            
        with open(temp_path, 'wb') as f:
            f.write(data)
            
        self.logger.debug(f"Created temp stream: {temp_path}")
        return str(temp_path)
        
    def get_stream_info(self, stream_id: str) -> Optional[Dict]:
        """Get information about active stream"""
        with self.lock:
            return self.active_streams.get(stream_id)
            
    def get_active_streams(self) -> List[Dict]:
        """Get list of active streams"""
        with self.lock:
            return [
                {**info, 'stream_id': stream_id}
                for stream_id, info in self.active_streams.items()
                if info['status'] == 'active'
            ]
            
    def cleanup_stream(self, stream_id: str):
        """Clean up stream resources"""
        with self.lock:
            if stream_id in self.active_streams:
                del self.active_streams[stream_id]
                
    def cleanup_temp_files(self, max_age_hours: int = 24):
        """Clean up temporary files older than specified hours"""
        if not self.config.temp_dir:
            return
            
        temp_dir = Path(self.config.temp_dir)
        current_time = time.time()
        
        for temp_file in temp_dir.glob("temp_stream_*.tmp"):
            file_age = current_time - temp_file.stat().st_mtime
            if file_age > max_age_hours * 3600:
                try:
                    temp_file.unlink()
                    self.logger.debug(f"Cleaned up temp file: {temp_file}")
                except Exception as e:
                    self.logger.error(f"Error cleaning up temp file {temp_file}: {e}")
                    
    def batch_stream(self, file_pairs: List[tuple]) -> List[Dict[str, Any]]:
        """Stream multiple files in batch"""
        results = []
        
        for source, destination in file_pairs:
            try:
                result = self.stream_file(source, destination)
                results.append(result)
            except Exception as e:
                results.append({
                    'source': str(source),
                    'destination': str(destination),
                    'error': str(e),
                    'status': 'error'
                })
                
        return results
        
    def estimate_transfer_time(self, file_size: int) -> float:
        """Estimate transfer time based on file size"""
        # Simple estimation based on average transfer speed
        avg_speed_bytes_per_sec = 10 * 1024 * 1024  # 10 MB/s
        return file_size / avg_speed_bytes_per_sec
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Clean up active streams
        with self.lock:
            self.active_streams.clear()
            
        # Clean up temp files
        self.cleanup_temp_files()

# Global streaming processor instance
streaming_processor = StreamingProcessor()

def get_streaming_processor() -> StreamingProcessor:
    """Get the global streaming processor instance"""
    return streaming_processor