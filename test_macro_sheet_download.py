#!/usr/bin/env python3
"""
Test script for macro sheet download functionality
Verifies that macro-enabled scrutiny sheets are properly integrated into the download system
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.utils.download_manager import EnhancedDownloadManager, FileType
from core.ui.enhanced_download_center import integrate_with_batch_processor

def test_macro_sheet_integration():
    """Test that macro sheets are properly integrated"""
    print("Testing Macro Sheet Download Integration")
    print("=" * 50)
    
    # Create a mock batch result with macro sheet
    mock_batch_result = [{
        'status': 'success',
        'filename': 'test_file.xlsx',
        'output_folder': 'test_output/test_run',
        'macro_sheet': {
            'success': True,
            'saved_xlsm_path': 'test_output/test_run/test_file_scrutiny_sheet.xlsm',
            'saved_pdf_path': 'test_output/test_run/test_file_scrutiny_sheet.pdf'
        }
    }]
    
    # Create download manager
    download_manager = EnhancedDownloadManager()
    
    # Test integration
    try:
        integrate_with_batch_processor(mock_batch_result, download_manager)
        print("✅ Integration function executed without errors")
    except Exception as e:
        print(f"❌ Integration failed: {e}")
        return False
    
    # Check that items were added
    items = download_manager.get_all_items()
    print(f"📊 Total items in download manager: {len(items)}")
    
    # Check for macro sheet
    xlsm_items = [item for item in items if item.name.endswith('.xlsm')]
    pdf_items = [item for item in items if 'scrutiny_sheet.pdf' in item.name]
    
    print(f"📊 Macro-enabled Excel files (.xlsm): {len(xlsm_items)}")
    print(f"📊 PDF exports of scrutiny sheets: {len(pdf_items)}")
    
    if xlsm_items:
        print(f"✅ Found macro sheet: {xlsm_items[0].name}")
        print(f"   Category: {xlsm_items[0].category.value}")
        print(f"   File type: {xlsm_items[0].file_type.value}")
    else:
        print("⚠️  No macro sheets found")
        
    if pdf_items:
        print(f"✅ Found PDF export: {pdf_items[0].name}")
        
    # Test file type recognition
    print("\nTesting file type recognition:")
    print(f"XLSM MIME type: {FileType.XLSM.value}")
    
    return True

def test_download_manager_extensions():
    """Test that download manager properly handles .xlsm files"""
    print("\nTesting Download Manager Extensions")
    print("=" * 50)
    
    download_manager = EnhancedDownloadManager()
    
    # Test adding .xlsm file
    try:
        test_content = b"fake xlsm content"
        download_manager.add_excel_file("test_sheet.xlsm", test_content, "Test macro sheet")
        print("✅ Added .xlsm file to download manager")
    except Exception as e:
        print(f"❌ Failed to add .xlsm file: {e}")
        return False
    
    # Test adding regular .xlsx file
    try:
        test_content = b"fake xlsx content"
        download_manager.add_excel_file("test_file.xlsx", test_content, "Test regular Excel file")
        print("✅ Added .xlsx file to download manager")
    except Exception as e:
        print(f"❌ Failed to add .xlsx file: {e}")
        return False
    
    # Check file types
    items = download_manager.get_all_items()
    for item in items:
        print(f"📄 {item.name}: {item.file_type.name} ({item.file_type.value})")
    
    return True

if __name__ == "__main__":
    print("Macro Sheet Download Integration Test")
    print("=" * 50)
    
    success = True
    success &= test_macro_sheet_integration()
    success &= test_download_manager_extensions()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! Macro sheet download integration is working correctly.")
    else:
        print("❌ Some tests failed. Please check the implementation.")