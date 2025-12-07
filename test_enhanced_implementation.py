#!/usr/bin/env python3
"""
Test the enhanced implementation of the scrutiny sheet generator
"""

import os
from pathlib import Path

def test_enhanced_implementation():
    """Test the enhanced scrutiny sheet implementation"""
    
    print("Testing Enhanced Scrutiny Sheet Implementation")
    print("=" * 50)
    
    # Create test output directory
    test_output = Path("test_output")
    test_output.mkdir(exist_ok=True)
    
    # Run the enhanced module directly
    print("Running enhanced macro scrutiny sheet module...")
    
    try:
        import subprocess
        result = subprocess.run([
            "python", "add_macro_scrutiny_sheet.py"
        ], capture_output=True, text=True, timeout=60)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
            
        print(f"Return code: {result.returncode}")
        
        if result.returncode == 0:
            print("✅ Enhanced implementation test completed successfully!")
            return True
        else:
            print("❌ Enhanced implementation test failed!")
            return False
            
    except Exception as e:
        print(f"💥 Test execution failed: {e}")
        return False

if __name__ == "__main__":
    success = test_enhanced_implementation()
    if success:
        print("\n🎉 All tests passed!")
    else:
        print("\n💥 Some tests failed!")