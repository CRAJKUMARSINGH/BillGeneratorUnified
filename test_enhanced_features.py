#!/usr/bin/env python3
"""
Test script for the Enhanced ZIP Processor new features
"""

import os
import tempfile
from pathlib import Path
from core.utils.enhanced_zip_processor import EnhancedZipProcessor, ZipConfig


def test_resource_monitoring():
    """Test resource monitoring functionality"""
    print("Testing resource monitoring...")
    
    # Create test files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create test file
        test_file = temp_path / "resource_test.txt"
        test_file.write_text("Resource test content")
        
        # Test resource monitoring
        processor = EnhancedZipProcessor()
        processor.add_file_from_path(test_file, "resource_test.txt")
        
        # Check resources
        has_resources = processor._check_resources()
        print(f"System has adequate resources: {has_resources}")
        
        # Configure resource limits to more reasonable values
        processor.configure_resource_limits(max_memory_percent=99.0, max_cpu_percent=99.0)
        print("Resource limits configured")
        
        # Create ZIP
        zip_buffer, metrics = processor.create_zip(use_cache=False)
        
        assert zip_buffer.getbuffer().nbytes > 0, "ZIP buffer should not be empty"
        
        print("Resource monitoring test passed!")


def test_statistics_collection():
    """Test statistics collection functionality"""
    print("\nTesting statistics collection...")
    
    # Create test files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create test file
        test_file = temp_path / "stats_test.txt"
        test_file.write_text("Statistics test content")
        
        # Test statistics
        processor = EnhancedZipProcessor()
        processor.add_file_from_path(test_file, "stats_test.txt")
        
        # Get initial stats
        initial_stats = processor.get_statistics()
        print(f"Initial stats: {initial_stats}")
        
        # Create ZIP
        zip_buffer, metrics = processor.create_zip(use_cache=False)
        
        # Get final stats
        final_stats = processor.get_statistics()
        print(f"Final stats: {final_stats}")
        
        # Check that stats were updated
        assert final_stats['total_operations'] > initial_stats['total_operations'], "Operations count should increase"
        assert final_stats['successful_operations'] > initial_stats['successful_operations'], "Successful operations should increase"
        
        # Test cache stats
        cache_stats = processor.get_cache_stats()
        print(f"Cache stats: {cache_stats}")
        
        print("Statistics collection test passed!")


def test_retry_logic():
    """Test retry logic functionality"""
    print("\nTesting retry logic...")
    
    # Create test files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create test file
        test_file = temp_path / "retry_test.txt"
        test_file.write_text("Retry test content")
        
        # Test retry logic
        processor = EnhancedZipProcessor()
        processor.add_file_from_path(test_file, "retry_test.txt")
        
        # Create ZIP with retry
        zip_buffer, metrics = processor.create_zip(use_cache=False, max_retries=3)
        
        print(f"Created ZIP with {metrics['total_files']} files")
        assert zip_buffer.getbuffer().nbytes > 0, "ZIP buffer should not be empty"
        
        print("Retry logic test passed!")


def test_convenience_functions():
    """Test convenience functions"""
    print("\nTesting convenience functions...")
    
    # Create test files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create test files
        test_file1 = temp_path / "convenience1.txt"
        test_file1.write_text("Convenience test 1")
        
        test_file2 = temp_path / "convenience2.txt"
        test_file2.write_text("Convenience test 2")
        
        # Test create_zip_from_files
        from core.utils.enhanced_zip_processor import create_zip_from_files
        
        file_paths = [test_file1, test_file2]
        zip_buffer, metrics = create_zip_from_files(file_paths)
        
        print(f"Created ZIP from files with {metrics['total_files']} files")
        assert zip_buffer.getbuffer().nbytes > 0, "ZIP buffer should not be empty"
        assert metrics['total_files'] == 2, "Should have 2 files"
        
        # Test create_zip_from_dict
        from core.utils.enhanced_zip_processor import create_zip_from_dict
        
        data_dict = {
            "data1.txt": "Data content 1",
            "data2.txt": "Data content 2",
            "data3.txt": "Data content 3"
        }
        
        zip_buffer2, metrics2 = create_zip_from_dict(data_dict)
        
        print(f"Created ZIP from dict with {metrics2['total_files']} files")
        assert zip_buffer2.getbuffer().nbytes > 0, "ZIP buffer should not be empty"
        assert metrics2['total_files'] == 3, "Should have 3 files"
        
        print("Convenience functions test passed!")


def main():
    """Run all tests"""
    print("Running Enhanced ZIP Processor New Features Tests")
    print("=" * 60)
    
    try:
        test_resource_monitoring()
        test_statistics_collection()
        test_retry_logic()
        test_convenience_functions()
        
        print("\n" + "=" * 60)
        print("All new features tests passed successfully!")
        
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        raise


if __name__ == "__main__":
    main()