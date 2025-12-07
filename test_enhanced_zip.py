#!/usr/bin/env python3
"""
Test script for enhanced ZIP functionality
"""

import io
import os
from core.utils.enhanced_zip_processor import EnhancedZipProcessor, ZipConfig, create_zip_from_dict
from core.utils.download_manager import EnhancedDownloadManager, DownloadCategory, FileType
from core.ui.enhanced_download_ui import EnhancedDownloadUI, create_download_manager, create_enhanced_download_ui


def test_basic_zip_functionality():
    """Test basic ZIP creation functionality"""
    print("Testing basic ZIP functionality...")
    
    # Create sample data
    sample_data = {
        "document1.html": "<html><body><h1>Test Document 1</h1></body></html>",
        "document2.html": "<html><body><h1>Test Document 2</h1></body></html>",
        "report.pdf": b"%PDF-1.4\n%Test PDF content",
        "data.xlsx": b"PK\x03\x04\x14\x00\x00\x00\x08\x00"  # Simple XLSX header
    }
    
    # Test with default config
    config = ZipConfig()
    
    try:
        zip_buffer, metrics = create_zip_from_dict(sample_data, config)
        
        print(f"✅ ZIP created successfully!")
        print(f"   Total files: {metrics['total_files']}")
        print(f"   Total size: {metrics['total_size_bytes']} bytes")
        print(f"   Processing time: {metrics['processing_time']}")
        
        # Verify ZIP content
        import zipfile
        with zipfile.ZipFile(io.BytesIO(zip_buffer.getvalue()), 'r') as zip_file:
            file_list = zip_file.namelist()
            print(f"   Files in ZIP: {file_list}")
            
        return True
    except Exception as e:
        print(f"❌ Error in basic ZIP test: {e}")
        return False


def test_download_manager():
    """Test download manager functionality"""
    print("\nTesting download manager...")
    
    try:
        # Create download manager
        dm = create_download_manager()
        
        # Add sample items
        dm.add_html_document("test1.html", "<h1>Test 1</h1>", "First test document")
        dm.add_pdf_document("report.pdf", b"%PDF-1.4\n%Test", "Sample PDF report")
        dm.add_doc_document("document.doc", b"Microsoft Word Document", "Sample DOC file")
        dm.add_excel_file("data.xlsx", b"Excel data", "Sample Excel file")
        
        # Test categorization
        categorized = dm.get_items_by_category()
        print(f"✅ Download manager created with {len(dm.get_all_items())} items")
        print(f"   Categories: {list(categorized.keys())}")
        
        # Test statistics
        stats = dm.get_statistics()
        print(f"   Total items: {stats['total_items']}")
        print(f"   Total size: {stats['total_size_mb']} MB")
        
        return True
    except Exception as e:
        print(f"❌ Error in download manager test: {e}")
        return False


def test_memory_efficient_processing():
    """Test memory-efficient processing with large files"""
    print("\nTesting memory-efficient processing...")
    
    try:
        # Create config with memory limits
        config = ZipConfig(
            compression_level=1,  # Low compression for speed
            memory_limit_mb=256,  # Set memory limit
            max_file_size_mb=50,
            max_total_size_mb=100
        )
        
        # Create processor
        with EnhancedZipProcessor(config) as processor:
            # Add small files
            processor.add_file_from_memory("small_file.txt", "Small content")
            
            # Add larger content
            large_content = "A" * 10000  # 10KB of data
            processor.add_file_from_memory("large_file.txt", large_content)
            
            # Create ZIP
            zip_buffer, metrics = processor.create_zip()
            
            print(f"✅ Memory-efficient processing successful!")
            print(f"   Files processed: {metrics['total_files']}")
            print(f"   Total size: {metrics['total_size_bytes']} bytes")
            
        return True
    except Exception as e:
        print(f"❌ Error in memory-efficient processing test: {e}")
        return False


def test_progress_tracking():
    """Test progress tracking functionality"""
    print("\nTesting progress tracking...")
    
    try:
        # Track progress
        progress_updates = []
        
        def progress_callback(progress, message):
            progress_updates.append((progress, message))
            print(f"   Progress: {progress:.1f}% - {message}")
        
        # Create processor with progress tracking
        config = ZipConfig(enable_progress_tracking=True)
        
        with EnhancedZipProcessor(config) as processor:
            processor.set_progress_callback(progress_callback)
            
            # Add files
            for i in range(5):
                processor.add_file_from_memory(f"file_{i}.txt", f"Content of file {i}")
            
            # Create ZIP
            zip_buffer, metrics = processor.create_zip()
            
        print(f"✅ Progress tracking test completed with {len(progress_updates)} updates")
        
        # Verify we got progress updates
        if len(progress_updates) > 0 and progress_updates[-1][0] == 100:
            print("   Progress tracking working correctly")
            return True
        else:
            print("   Progress tracking may have issues")
            return False
            
    except Exception as e:
        print(f"❌ Error in progress tracking test: {e}")
        return False


def test_security_features():
    """Test security features like file size limits"""
    print("\nTesting security features...")
    
    try:
        # Create config with small limits
        config = ZipConfig(
            max_file_size_mb=1,  # Very small limit
            max_total_size_mb=2
        )
        
        # Try to add a file that exceeds limits
        with EnhancedZipProcessor(config) as processor:
            # This should work (small file)
            processor.add_file_from_memory("small.txt", "Small content")
            
            # This should fail (large file)
            try:
                large_content = "A" * (2 * 1024 * 1024)  # 2MB content
                processor.add_file_from_memory(large_content, "large.txt")
                print("   ❌ Security check failed - large file was accepted")
                return False
            except ValueError as e:
                print(f"   ✅ Security check passed - large file rejected: {str(e)}")
                
        return True
    except Exception as e:
        print(f"❌ Error in security features test: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("ENHANCED ZIP FUNCTIONALITY TEST SUITE")
    print("=" * 50)
    
    tests = [
        test_basic_zip_functionality,
        test_download_manager,
        test_memory_efficient_processing,
        test_progress_tracking,
        test_security_features
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
        print("🎉 All tests passed! Enhanced ZIP functionality is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    run_all_tests()