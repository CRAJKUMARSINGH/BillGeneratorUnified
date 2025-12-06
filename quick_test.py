#!/usr/bin/env python3
"""
Quick Test for BillGeneratorUnified
Verifies basic functionality without running all tests.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_quick_test():
    """Run a quick test to verify basic functionality"""
    print("🚀 Running Quick Test for BillGeneratorUnified")
    print("=" * 50)
    
    # Check if required files exist
    root_dir = Path(__file__).parent.absolute()
    required_files = [
        "app.py",
        "test_enhanced_pdf.py",
        "test_chrome_headless.py"
    ]
    
    all_good = True
    for file_name in required_files:
        file_path = root_dir / file_name
        if file_path.exists():
            print(f"✅ Found: {file_name}")
        else:
            print(f"❌ Missing: {file_name}")
            all_good = False
    
    if not all_good:
        print("\n❌ Some required files are missing!")
        return False
    
    # Try importing the main modules
    try:
        # Test importing core modules
        from core.config.config_loader import ConfigLoader
        from core.generators.pdf_generator_enhanced import EnhancedPDFGenerator
        print("✅ Core modules imported successfully")
    except Exception as e:
        print(f"❌ Error importing core modules: {e}")
        return False
    
    # Run a simple PDF test
    print("\n📄 Running simple PDF generation test...")
    try:
        generator = EnhancedPDFGenerator()
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #2c3e50; }
            </style>
        </head>
        <body>
            <h1>Quick Test Successful</h1>
            <p>BillGeneratorUnified is working correctly!</p>
        </body>
        </html>
        """
        
        pdf_bytes = generator.auto_convert(html, zoom=1.0, disable_smart_shrinking=True)
        
        # Save the PDF
        test_output_dir = root_dir / "test_output"
        test_output_dir.mkdir(exist_ok=True)
        output_file = test_output_dir / "quick_test.pdf"
        output_file.write_bytes(pdf_bytes)
        
        print(f"✅ PDF generated successfully: {len(pdf_bytes)} bytes")
        print(f"📁 Saved to: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        return False

if __name__ == "__main__":
    print("⚡ BillGeneratorUnified Quick Test")
    print()
    
    success = run_quick_test()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Quick test PASSED! BillGeneratorUnified is ready to use.")
        print("\nNext steps:")
        print("  1. Run RUN_ALL_TESTS.bat for comprehensive testing")
        print("  2. Or run individual test scripts:")
        print("     - python test_enhanced_pdf.py")
        print("     - python test_chrome_headless.py")
        print("     - python batch_run_demo.py")
    else:
        print("❌ Quick test FAILED!")
        print("\nPlease check the error messages above.")
        print("Run RUN_ALL_TESTS.bat for detailed diagnostics.")
    
    sys.exit(0 if success else 1)