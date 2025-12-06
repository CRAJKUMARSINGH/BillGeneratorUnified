#!/usr/bin/env python3
"""
Comprehensive Test Runner for BillGeneratorUnified
Runs all tests in sequence and provides a summary of results.
"""

import subprocess
import os
import sys
import time
from datetime import datetime

def run_command(cmd, desc, cwd=None):
    """Run a command and return the result"""
    print(f"\n{'='*60}")
    print(f"🚀 RUNNING: {desc}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd, 
            check=True, 
            capture_output=True, 
            text=True,
            cwd=cwd
        )
        print("✅ SUCCESS")
        if result.stdout:
            # Show first 50 lines of output to keep console readable
            lines = result.stdout.split('\n')
            for i, line in enumerate(lines[:50]):
                print(f"  {line}")
            if len(lines) > 50:
                print(f"  ... ({len(lines) - 50} more lines)")
        return True
    except subprocess.CalledProcessError as e:
        print("❌ FAILED")
        print(f"Error: {e}")
        if e.stdout:
            print(f"STDOUT:\n{e.stdout}")
        if e.stderr:
            print(f"STDERR:\n{e.stderr}")
        return False
    except FileNotFoundError:
        print("❌ FAILED - Command not found")
        return False

def check_file_exists(filepath, description):
    """Check if a file exists and report"""
    if os.path.exists(filepath):
        print(f"✅ Found {description}: {filepath}")
        return True
    else:
        print(f"❌ Missing {description}: {filepath}")
        return False

def main():
    print(f"{'='*80}")
    print("🧪 BILL GENERATOR UNIFIED - COMPREHENSIVE TEST RUNNER")
    print(f"{'='*80}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Set the root path to the parent directory where the Python files are located
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(root_dir, "OUTPUT_FILES")
    input_dir = os.path.join(root_dir, "INPUT_FILES")
    
    print(f"📂 Root directory: {root_dir}")
    print(f"📂 Output directory: {output_dir}")
    print(f"📂 Input directory: {input_dir}")
    
    # Check directories
    if not os.path.exists(root_dir):
        print(f"❌ Root directory does not exist: {root_dir}")
        return
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"✅ Created output directory: {output_dir}")
    
    # Track test results
    test_results = []
    
    # Test 1: Check for required files/directories
    print(f"\n{'='*60}")
    print("🔍 CHECKING REQUIRED FILES AND DIRECTORIES")
    print(f"{'='*60}")
    
    checks = [
        (os.path.join(root_dir, "app.py"), "Main application"),
        (os.path.join(root_dir, "batch_run_demo.py"), "Batch demo script"),
        (os.path.join(root_dir, "test_chrome_headless.py"), "Chrome headless test"),
        (os.path.join(root_dir, "test_enhanced_pdf.py"), "Enhanced PDF test"),
    ]
    
    for filepath, description in checks:
        exists = check_file_exists(filepath, description)
        test_results.append((f"File check: {description}", exists))
    
    # Test 2: Run main app (single bill generation)
    test_results.append((
        "Main app (single bill generation)",
        run_command([sys.executable, "app.py"], "Main App Test", cwd=root_dir)
    ))
    time.sleep(2)  # Brief pause between tests
    
    # Test 3: Run batch demo
    test_results.append((
        "Batch run demo",
        run_command([sys.executable, "batch_run_demo.py"], "Batch Demo Test", cwd=root_dir)
    ))
    time.sleep(2)
    
    # Test 4: Run headless Chrome test
    test_results.append((
        "Headless Chrome test",
        run_command([sys.executable, "test_chrome_headless.py"], "Chrome Headless Test", cwd=root_dir)
    ))
    time.sleep(2)
    
    # Test 5: Run enhanced PDF test
    test_results.append((
        "Enhanced PDF test",
        run_command([sys.executable, "test_enhanced_pdf.py"], "Enhanced PDF Test", cwd=root_dir)
    ))
    time.sleep(2)
    
    # Test 6: Run launcher scripts
    launchers_dir = os.path.join(root_dir, "launchers")
    if os.path.exists(launchers_dir):
        print(f"\n{'='*60}")
        print("🎮 RUNNING LAUNCHER SCRIPTS")
        print(f"{'='*60}")
        
        for launcher in os.listdir(launchers_dir):
            if launcher.endswith(".py"):
                launcher_path = os.path.join("launchers", launcher)
                test_results.append((
                    f"Launcher: {launcher}",
                    run_command([sys.executable, launcher_path], f"Launcher Test: {launcher}", cwd=root_dir)
                ))
                time.sleep(2)
    
    # Summary
    print(f"\n{'='*80}")
    print("📊 TEST RESULTS SUMMARY")
    print(f"{'='*80}")
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    passed = 0
    failed = 0
    
    for test_name, success in test_results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if success:
            passed += 1
        else:
            failed += 1
    
    print(f"\n📈 Final Score: {passed}/{passed + failed} tests passed")
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED! The Bill Generator is working correctly.")
    else:
        print(f"⚠️  {failed} test(s) failed. Please check the output above for details.")
    
    # Instructions for checking output
    print(f"\n📋 NEXT STEPS:")
    print(f"   - Check generated PDFs in: {output_dir}")
    if os.path.exists(os.path.join(root_dir, "BATCH_RUN_SUMMARY.txt")):
        print(f"   - Review batch run summary: {os.path.join(root_dir, 'BATCH_RUN_SUMMARY.txt')}")
    print(f"   - Check test_output/ directory for additional generated files")

if __name__ == "__main__":
    main()