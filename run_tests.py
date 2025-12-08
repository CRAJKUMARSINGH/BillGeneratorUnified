#!/usr/bin/env python3
"""
Test runner script for the BillGenerator backend.
"""
import subprocess
import sys
import os

def run_tests():
    """Run all backend tests with pytest."""
    print("Running backend tests...")
    print("=" * 50)
    
    # Change to the project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    # Run pytest with coverage reporting
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/backend", 
            "-v", 
            "--tb=short",
            "--disable-warnings"
        ], check=True)
        
        print("\n" + "=" * 50)
        print("✅ All tests passed!")
        return True
        
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 50)
        print("❌ Some tests failed!")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)