#!/usr/bin/env python3
"""
Comprehensive Test Runner for BillGeneratorUnified
Runs all tests in sequence and provides a detailed summary of results.
"""

import subprocess
import os
import sys
import time
import shutil
from datetime import datetime
from pathlib import Path

def run_command(cmd, desc, cwd=None, timeout=60):
    """Run a command and return the result"""
    print(f"\n{'='*70}")
    print(f"🚀 RUNNING: {desc}")
    print(f"{'='*70}")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd, 
            check=True, 
            capture_output=True, 
            text=True,
            cwd=cwd,
            timeout=timeout
        )
        print("✅ SUCCESS")
        if result.stdout:
            # Show first 100 lines of output to keep console readable
            lines = result.stdout.split('\n')
            for i, line in enumerate(lines[:100]):
                print(f"  {line}")
            if len(lines) > 100:
                print(f"  ... ({len(lines) - 100} more lines)")
        return True, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        print("❌ FAILED")
        print(f"Return code: {e.returncode}")
        if e.stdout:
            print(f"STDOUT:\n{e.stdout}")
        if e.stderr:
            print(f"STDERR:\n{e.stderr}")
        return False, e.stdout, e.stderr
    except subprocess.TimeoutExpired:
        print("❌ FAILED - Command timed out")
        return False, "", "Timeout"
    except FileNotFoundError:
        print("❌ FAILED - Command not found")
        return False, "", "Command not found"

def check_file_exists(filepath, description):
    """Check if a file exists and report"""
    if os.path.exists(filepath):
        print(f"✅ Found {description}: {filepath}")
        return True
    else:
        print(f"❌ Missing {description}: {filepath}")
        return False

def setup_test_environment():
    """Set up the test environment by copying test files to input directory"""
    print(f"\n{'='*70}")
    print("🔧 SETTING UP TEST ENVIRONMENT")
    print(f"{'='*70}")
    
    root_dir = Path(__file__).parent.absolute()
    input_dir = root_dir / "input"
    test_input_dir = root_dir / "TEST_INPUT_FILES"
    
    # Create input directory if it doesn't exist
    input_dir.mkdir(exist_ok=True)
    print(f"✅ Created/verified input directory: {input_dir}")
    
    # Copy test files from TEST_INPUT_FILES to input directory
    if test_input_dir.exists():
        copied_files = 0
        for file_path in test_input_dir.iterdir():
            if file_path.is_file() and file_path.suffix in ['.xlsx', '.xls']:
                dest_path = input_dir / file_path.name
                shutil.copy2(file_path, dest_path)
                print(f"  📄 Copied: {file_path.name}")
                copied_files += 1
        
        if copied_files > 0:
            print(f"✅ Copied {copied_files} test files to input directory")
            return True
        else:
            print("⚠️  No Excel files found in TEST_INPUT_FILES")
            return False
    else:
        print("⚠️  TEST_INPUT_FILES directory not found")
        return False

def main():
    print(f"{'='*80}")
    print("🧪 BILL GENERATOR UNIFIED - COMPREHENSIVE TEST SUITE")
    print(f"{'='*80}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Set the root path
    root_dir = Path(__file__).parent.absolute()
    output_dir = root_dir / "OUTPUT_FILES"
    test_output_dir = root_dir / "test_output"
    
    print(f"📂 Root directory: {root_dir}")
    print(f"📂 Output directory: {output_dir}")
    
    # Create necessary directories
    output_dir.mkdir(exist_ok=True)
    test_output_dir.mkdir(exist_ok=True)
    print(f"✅ Created output directories")
    
    # Setup test environment
    setup_test_environment()
    
    # Track test results
    test_results = []
    
    # Test 1: Check for required files/directories
    print(f"\n{'='*70}")
    print("🔍 CHECKING REQUIRED FILES AND DIRECTORIES")
    print(f"{'='*70}")
    
    checks = [
        (root_dir / "app.py", "Main application"),
        (root_dir / "batch_run_demo.py", "Batch demo script"),
        (root_dir / "test_chrome_headless.py", "Chrome headless test"),
        (root_dir / "test_enhanced_pdf.py", "Enhanced PDF test"),
        (root_dir / "requirements.txt", "Requirements file"),
    ]
    
    for filepath, description in checks:
        exists = check_file_exists(filepath, description)
        test_results.append((f"File check: {description}", exists))
    
    # Test 2: Check Python dependencies
    print(f"\n{'='*70}")
    print("🔍 CHECKING PYTHON DEPENDENCIES")
    print(f"{'='*70}")
    
    success, stdout, stderr = run_command(
        [sys.executable, "-m", "pip", "list"], 
        "List installed packages"
    )
    if success:
        # Check for key dependencies
        required_packages = ['streamlit', 'pandas', 'weasyprint']
        found_packages = []
        for line in stdout.split('\n'):
            for package in required_packages:
                if package.lower() in line.lower():
                    found_packages.append(package)
                    print(f"✅ Found package: {package}")
        
        missing_packages = set(required_packages) - set(found_packages)
        for package in missing_packages:
            print(f"❌ Missing package: {package}")
        
        test_results.append(("Python dependencies check", len(missing_packages) == 0))
    
    # Test 3: Run enhanced PDF test
    print(f"\n{'='*70}")
    print("📄 RUNNING ENHANCED PDF TEST")
    print(f"{'='*70}")
    
    test_results.append((
        "Enhanced PDF test",
        run_command([sys.executable, "test_enhanced_pdf.py"], "Enhanced PDF Test", cwd=root_dir)[0]
    ))
    time.sleep(2)
    
    # Test 4: Run headless Chrome test
    print(f"\n{'='*70}")
    print("🌐 RUNNING CHROME HEADLESS TEST")
    print(f"{'='*70}")
    
    test_results.append((
        "Headless Chrome test",
        run_command([sys.executable, "test_chrome_headless.py"], "Chrome Headless Test", cwd=root_dir)[0]
    ))
    time.sleep(2)
    
    # Test 5: Run batch demo
    print(f"\n{'='*70}")
    print("📦 RUNNING BATCH PROCESSING TEST")
    print(f"{'='*70}")
    
    test_results.append((
        "Batch run demo",
        run_command([sys.executable, "batch_run_demo.py"], "Batch Demo Test", cwd=root_dir)[0]
    ))
    time.sleep(2)
    
    # Test 6: Run main app test (non-interactive)
    print(f"\n{'='*70}")
    print("🖥️  RUNNING MAIN APP TEST")
    print(f"{'='*70}")
    
    # We'll test if the app can be imported without errors
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("app", root_dir / "app.py")
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            # Add to sys.modules before executing to avoid ImportError
            sys.modules["app"] = module
            spec.loader.exec_module(module)
            print("✅ Main app imported successfully")
            test_results.append(("Main app import test", True))
        else:
            print("❌ Failed to load main app module")
            test_results.append(("Main app import test", False))
    except Exception as e:
        print(f"❌ Error importing main app: {e}")
        test_results.append(("Main app import test", False))
    
    # Test 7: Run launcher scripts
    launchers_dir = root_dir / "launchers"
    if launchers_dir.exists():
        print(f"\n{'='*70}")
        print("🎮 RUNNING LAUNCHER SCRIPTS")
        print(f"{'='*70}")
        
        for launcher in launchers_dir.iterdir():
            if launcher.is_file() and launcher.suffix == '.py':
                launcher_path = launcher.relative_to(root_dir)
                test_results.append((
                    f"Launcher: {launcher.name}",
                    run_command([sys.executable, str(launcher_path)], f"Launcher Test: {launcher.name}", cwd=root_dir)[0]
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
    print(f"   - Check test_output/ directory for additional generated files")
    print(f"   - Review any batch processing output in the timestamped folders")
    
    # Return exit code based on test results
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)