#!/usr/bin/env python3
"""
Test script for the Enhanced ZIP Processor
"""

import os
import tempfile
from pathlib import Path
from core.utils.enhanced_zip_processor import EnhancedZipProcessor, ZipConfig


def test_basic_functionality():
    """Test basic ZIP creation functionality"""
    print("Testing basic functionality...")
    
    # Create test files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create test files
        test_file1 = temp_path / "test1.txt"
        test_file1.write_text("This is test file 1")
        
        test_file2 = temp_path / "test2.txt"
        test_file2.write_text("This is test file 2 with more content to make it larger")
        
        # Test basic ZIP creation
        config = ZipConfig(compression_level=6, streaming_threshold_mb=1)  # Low threshold for testing
        processor = EnhancedZipProcessor(config)
        
        processor.add_file_from_path(test_file1, "file1.txt")
        processor.add_file_from_path(test_file2, "file2.txt")
        processor.add_file_from_memory("Direct content", "direct.txt")
        
        # Create ZIP
        zip_buffer, metrics = processor.create_zip(use_cache=False)
        
        print(f"Created ZIP with {metrics['total_files']} files")
        print(f"Total size: {metrics['total_size_bytes']} bytes")
        print(f"Processing time: {metrics.get('creation_duration_seconds', 'N/A')} seconds")
        print(f"Memory usage: {metrics['memory_usage_mb']:.2f} MB")
        
        # Verify ZIP content
        assert zip_buffer.getbuffer().nbytes > 0, "ZIP buffer should not be empty"
        assert metrics['total_files'] == 3, "Should have 3 files"
        
        print("Basic functionality test passed!")


def test_streaming_functionality():
    """Test streaming functionality for large files"""
    print("\nTesting streaming functionality...")
    
    # Create test files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create a larger test file to trigger streaming
        large_file = temp_path / "large_file.txt"
        with open(large_file, 'w') as f:
            for i in range(10000):  # Create a file large enough to trigger streaming
                f.write(f"Line {i}: This is test content for streaming functionality.\n")
        
        # Test streaming ZIP creation
        config = ZipConfig(
            compression_level=1,  # Low compression for speed
            streaming_threshold_mb=0.1,  # Very low threshold to force streaming
            chunk_size=1024
        )
        processor = EnhancedZipProcessor(config)
        
        processor.add_file_from_path(large_file, "large_file.txt")
        
        # Create ZIP with streaming
        zip_buffer, metrics = processor.create_zip(use_cache=False)
        
        print(f"Created streaming ZIP with {metrics['total_files']} files")
        print(f"Total size: {metrics['total_size_bytes']} bytes")
        
        # Verify ZIP content
        assert zip_buffer.getbuffer().nbytes > 0, "ZIP buffer should not be empty"
        assert metrics['total_files'] == 1, "Should have 1 file"
        
        print("Streaming functionality test passed!")


def test_caching_functionality():
    """Test caching functionality"""
    print("\nTesting caching functionality...")
    
    # Create test files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create test files
        test_file = temp_path / "cache_test.txt"
        test_file.write_text("Content for cache testing")
        
        # Test caching
        config = ZipConfig(compression_level=1)  # Low compression for speed
        processor = EnhancedZipProcessor(config)
        
        processor.add_file_from_path(test_file, "cached_file.txt")
        
        # Create ZIP with caching enabled
        zip_buffer1, metrics1 = processor.create_zip(use_cache=True)
        
        print(f"First creation: {metrics1['total_files']} files, {metrics1['total_size_bytes']} bytes")
        
        # Create ZIP again - should use cache
        zip_buffer2, metrics2 = processor.create_zip(use_cache=True)
        
        print(f"Second creation (cached): {metrics2['total_files']} files, {metrics2['total_size_bytes']} bytes")
        
        # Verify both results are the same
        assert zip_buffer1.getbuffer().nbytes == zip_buffer2.getbuffer().nbytes, "Cached and fresh results should be identical"
        
        # Check cache stats
        cache_stats = processor.get_cache_stats()
        print(f"Cache stats: {cache_stats['cache_entries']} entries, {cache_stats['total_cache_size_bytes']} bytes total")
        
        print("Caching functionality test passed!")


def test_progress_tracking():
    """Test progress tracking functionality"""
    print("\nTesting progress tracking...")
    
    progress_updates = []
    
    def progress_callback(progress, message):
        progress_updates.append((progress, message))
        if len(progress_updates) <= 5:  # Only print first few updates
            print(f"Progress: {progress:.1f}% - {message}")
    
    # Create test files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create multiple test files
        for i in range(5):
            test_file = temp_path / f"test_{i}.txt"
            test_file.write_text(f"This is test file {i}")
        
        # Test progress tracking
        config = ZipConfig(compression_level=1)  # Low compression for speed
        processor = EnhancedZipProcessor(config)
        processor.set_progress_callback(progress_callback)
        
        # Add multiple files
        for i in range(5):
            test_file = temp_path / f"test_{i}.txt"
            processor.add_file_from_path(test_file, f"file_{i}.txt")
        
        # Create ZIP
        zip_buffer, metrics = processor.create_zip(use_cache=False)
        
        # Verify progress tracking worked
        assert len(progress_updates) > 0, "Should have received progress updates"
        assert any(progress == 100.0 for progress, _ in progress_updates), "Should have completed progress"
        
        print(f"Received {len(progress_updates)} progress updates")
        print("Progress tracking test passed!")


def test_memory_monitoring():
    """Test memory monitoring functionality"""
    print("\nTesting memory monitoring...")
    
    # Create test files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create test file
        test_file = temp_path / "memory_test.txt"
        test_file.write_text("Memory test content")
        
        # Test memory monitoring
        config = ZipConfig(memory_limit_mb=1024)  # High limit for testing
        processor = EnhancedZipProcessor(config)
        
        processor.add_file_from_path(test_file, "memory_test.txt")
        
        # Get memory stats
        memory_stats = processor._get_memory_stats()
        print(f"Memory stats: {memory_stats['process_memory_mb']:.2f} MB process usage")
        
        # Create ZIP
        zip_buffer, metrics = processor.create_zip(use_cache=False)
        
        print(f"Final memory usage: {metrics['memory_usage_mb']:.2f} MB")
        
        # Verify memory stats are reasonable
        assert metrics['memory_usage_mb'] > 0, "Memory usage should be positive"
        
        print("Memory monitoring test passed!")


def main():
    """Run all tests"""
    print("Running Enhanced ZIP Processor Tests")
    print("=" * 50)
    
    try:
        test_basic_functionality()
        test_streaming_functionality()
        test_caching_functionality()
        test_progress_tracking()
        test_memory_monitoring()
        
        print("\n" + "=" * 50)
        print("All tests passed successfully!")
        
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        raise


if __name__ == "__main__":
    main()