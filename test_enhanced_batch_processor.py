#!/usr/bin/env python3
"""
Test script for enhanced batch processor
"""

import time
from core.processors.batch_processor_enhanced import EnhancedBatchProcessor, BatchConfig


def test_basic_batch_processing():
    """Test basic batch processing functionality"""
    print("Testing basic batch processing...")
    
    # Create processor
    processor = EnhancedBatchProcessor()
    
    # Simple test function
    def square_number(x):
        time.sleep(0.1)  # Simulate some work
        return x * x
    
    # Test data
    test_data = list(range(1, 11))  # 1 to 10
    
    # Process batch
    job_id = processor.submit_batch(
        items=test_data,
        processor=square_number,
        config=BatchConfig(max_workers=2, batch_size=3)
    )
    
    print(f"Submitted job: {job_id}")
    
    # Wait for completion
    while True:
        status = processor.get_job_status(job_id)
        if status and status['status'] in ['completed', 'failed']:
            break
        time.sleep(0.1)
    
    # Check results
    status = processor.get_job_status(job_id)
    if status and status['status'] == 'completed':
        results = status.get('results', [])
        expected = [x * x for x in test_data]
        actual = sorted(results) if results else []
        
        if actual == expected:
            print("✅ Basic batch processing test passed!")
            return True
        else:
            print(f"❌ Results mismatch. Expected: {expected}, Got: {actual}")
            return False
    else:
        print(f"❌ Job failed with status: {status}")
        return False


def test_parallel_processing():
    """Test parallel processing capabilities"""
    print("\nTesting parallel processing...")
    
    # Create processor
    processor = EnhancedBatchProcessor()
    
    # Test function that takes different amounts of time
    def process_with_delay(item):
        delay, value = item
        time.sleep(delay)
        return value * 2
    
    # Test data with different processing times
    test_data = [(0.1, 1), (0.2, 2), (0.1, 3), (0.3, 4), (0.1, 5)]
    
    start_time = time.time()
    
    # Process with multiple workers
    job_id = processor.submit_batch(
        items=test_data,
        processor=process_with_delay,
        config=BatchConfig(max_workers=3, batch_size=2)
    )
    
    # Wait for completion
    while True:
        status = processor.get_job_status(job_id)
        if status and status['status'] in ['completed', 'failed']:
            break
        time.sleep(0.1)
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    # Check if parallel processing was effective
    # Sequential processing would take ~0.8 seconds (0.1+0.2+0.1+0.3+0.1)
    # Parallel processing should be faster
    if processing_time < 0.6:  # Allow some overhead
        print(f"✅ Parallel processing test passed! (Time: {processing_time:.2f}s)")
        return True
    else:
        print(f"❌ Parallel processing may not be working effectively. (Time: {processing_time:.2f}s)")
        return False


def test_error_handling():
    """Test error handling capabilities"""
    print("\nTesting error handling...")
    
    # Create processor
    processor = EnhancedBatchProcessor()
    
    # Test function that raises exceptions for some inputs
    def sometimes_fail(x):
        if x == 5:
            raise ValueError("Intentional error for testing")
        return x * x
    
    # Test data including one that will fail
    test_data = [1, 2, 3, 4, 5, 6, 7]
    
    # Process batch
    job_id = processor.submit_batch(
        items=test_data,
        processor=sometimes_fail,
        config=BatchConfig(max_workers=2, retry_attempts=0)
    )
    
    # Wait for completion
    while True:
        status = processor.get_job_status(job_id)
        if status and status['status'] in ['completed_with_errors', 'failed']:
            break
        time.sleep(0.1)
    
    # Check results
    status = processor.get_job_status(job_id)
    if status and status['status'] == 'completed_with_errors':
        results = status.get('results', [])
        errors = status.get('errors_count', 0)
        
        # Should have 6 successful results and 1 error
        if len(results) == 6 and errors == 1:
            print("✅ Error handling test passed!")
            return True
        else:
            print(f"❌ Unexpected results. Results: {len(results)}, Errors: {errors}")
            return False
    else:
        print(f"❌ Unexpected job status: {status}")
        return False


def test_statistics():
    """Test statistics collection"""
    print("\nTesting statistics collection...")
    
    # Create processor
    processor = EnhancedBatchProcessor()
    
    # Simple test function
    def identity(x):
        return x
    
    # Process a small batch
    job_id = processor.submit_batch(
        items=[1, 2, 3],
        processor=identity
    )
    
    # Wait for completion
    while True:
        status = processor.get_job_status(job_id)
        if status and status['status'] in ['completed', 'failed']:
            break
        time.sleep(0.1)
    
    # Get statistics
    stats = processor.get_statistics()
    
    # Check that statistics are reasonable
    if (stats['total_jobs'] >= 1 and 
        stats['completed_jobs'] >= 1 and 
        stats['total_items_processed'] >= 3):
        print("✅ Statistics collection test passed!")
        print(f"   Stats: {stats}")
        return True
    else:
        print(f"❌ Statistics seem incorrect: {stats}")
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("ENHANCED BATCH PROCESSOR TEST SUITE")
    print("=" * 50)
    
    tests = [
        test_basic_batch_processing,
        test_parallel_processing,
        test_error_handling,
        test_statistics
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Enhanced batch processor is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    run_all_tests()