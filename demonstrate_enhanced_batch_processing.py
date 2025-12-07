#!/usr/bin/env python3
"""
Demonstration of enhanced batch processing capabilities
"""

import time
from core.processors.batch_processor_enhanced import EnhancedBatchProcessor, BatchConfig


def demonstrate_basic_usage():
    """Demonstrate basic usage of the enhanced batch processor"""
    print("=== Basic Usage Demonstration ===")
    
    # Create processor
    processor = EnhancedBatchProcessor()
    
    # Simple processing function
    def process_item(item):
        # Simulate some work
        time.sleep(0.1)
        return item ** 2
    
    # Submit batch job
    items = [1, 2, 3, 4, 5]
    job_id = processor.submit_batch(
        items=items,
        processor=process_item,
        config=BatchConfig(max_workers=3)
    )
    
    print(f"Submitted job: {job_id}")
    
    # Wait for completion and show progress
    while True:
        status = processor.get_job_status(job_id)
        if status:
            print(f"Progress: {status['progress_percent']:.1f}% ({status['processed_count']}/{status['total_items']})")
        
        if status and status['status'] in ['completed', 'failed']:
            break
        time.sleep(0.2)
    
    # Show results
    status = processor.get_job_status(job_id)
    if status and 'results' in status:
        print(f"Results: {status['results']}")
    
    print("✅ Basic usage demonstration completed!\n")


def demonstrate_parallel_processing():
    """Demonstrate parallel processing capabilities"""
    print("=== Parallel Processing Demonstration ===")
    
    # Create processor
    processor = EnhancedBatchProcessor()
    
    # Processing function with varying durations
    def process_with_varying_time(item):
        delay = item * 0.1  # Different delays for different items
        time.sleep(delay)
        return f"Processed item {item} (delay: {delay}s)"
    
    # Submit batch with multiple workers
    items = [1, 2, 3, 4, 5, 6, 7, 8]
    start_time = time.time()
    
    job_id = processor.submit_batch(
        items=items,
        processor=process_with_varying_time,
        config=BatchConfig(max_workers=4, batch_size=3)
    )
    
    print(f"Processing {len(items)} items with 4 workers...")
    
    # Wait for completion
    while True:
        status = processor.get_job_status(job_id)
        if status and status['status'] in ['completed', 'failed']:
            break
        time.sleep(0.1)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"Completed in {total_time:.2f} seconds")
    
    # Show that parallel processing was effective
    # Sequential would take: 0.1+0.2+0.3+0.4+0.5+0.6+0.7+0.8 = 3.6 seconds
    # Parallel with 4 workers should be much faster
    if total_time < 2.0:  # Allow some overhead
        print("✅ Parallel processing working effectively!")
    else:
        print("⚠️ Parallel processing may not be optimal")
    
    print("✅ Parallel processing demonstration completed!\n")


def demonstrate_error_handling():
    """Demonstrate error handling capabilities"""
    print("=== Error Handling Demonstration ===")
    
    # Create processor
    processor = EnhancedBatchProcessor()
    
    # Processing function that sometimes fails
    def sometimes_fail(item):
        if item == 3 or item == 7:  # These will fail
            raise ValueError(f"Intentional error for item {item}")
        time.sleep(0.1)
        return item * 10
    
    # Submit batch job
    items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    job_id = processor.submit_batch(
        items=items,
        processor=sometimes_fail,
        config=BatchConfig(max_workers=2, retry_attempts=0)  # No retries for clearer demo
    )
    
    print(f"Processing {len(items)} items (2 will fail)...")
    
    # Wait for completion
    while True:
        status = processor.get_job_status(job_id)
        if status and status['status'] in ['completed_with_errors', 'failed']:
            break
        time.sleep(0.1)
    
    # Show results
    status = processor.get_job_status(job_id)
    if status:
        print(f"Status: {status['status']}")
        print(f"Successful results: {len(status['results'])}")
        print(f"Errors: {status['errors_count']}")
        
        if status['results']:
            print(f"Some successful results: {status['results'][:3]}...")
    
    print("✅ Error handling demonstration completed!\n")


def demonstrate_configuration_options():
    """Demonstrate various configuration options"""
    print("=== Configuration Options Demonstration ===")
    
    # Show different configuration options
    configs = [
        BatchConfig(max_workers=1, batch_size=1, timeout_seconds=60),
        BatchConfig(max_workers=4, batch_size=5, timeout_seconds=30, retry_attempts=2),
        BatchConfig(max_workers=8, batch_size=10, timeout_seconds=15, retry_attempts=1)
    ]
    
    for i, config in enumerate(configs, 1):
        print(f"Config {i}:")
        print(f"  Workers: {config.max_workers}")
        print(f"  Batch Size: {config.batch_size}")
        print(f"  Timeout: {config.timeout_seconds}s")
        print(f"  Retries: {config.retry_attempts}")
        print()
    
    print("✅ Configuration options demonstration completed!\n")


def demonstrate_statistics():
    """Demonstrate statistics collection"""
    print("=== Statistics Collection Demonstration ===")
    
    # Create processor
    processor = EnhancedBatchProcessor()
    
    # Simple processing function
    def process_simple(item):
        time.sleep(0.05)
        return item
    
    # Process several small batches
    for i in range(3):
        job_id = processor.submit_batch(
            items=list(range(1, 6)),
            processor=process_simple,
            config=BatchConfig(max_workers=2)
        )
        
        # Wait for completion
        while True:
            status = processor.get_job_status(job_id)
            if status and status['status'] in ['completed', 'failed']:
                break
            time.sleep(0.1)
    
    # Show statistics
    stats = processor.get_statistics()
    print("Processor Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("✅ Statistics collection demonstration completed!\n")


def main():
    """Main demonstration function"""
    print("🚀 Enhanced Batch Processor Demonstration")
    print("=" * 50)
    
    # Run demonstrations
    demonstrate_basic_usage()
    demonstrate_parallel_processing()
    demonstrate_error_handling()
    demonstrate_configuration_options()
    demonstrate_statistics()
    
    print("=" * 50)
    print("🎉 All demonstrations completed!")
    print("\nKey Benefits Shown:")
    print("✅ Parallel processing for faster execution")
    print("✅ Error handling with graceful degradation")
    print("✅ Configurable processing options")
    print("✅ Real-time progress tracking")
    print("✅ Comprehensive statistics collection")


if __name__ == "__main__":
    main()