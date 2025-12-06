import subprocess
import os

def run_command(cmd, desc):
    print(f"\n=== Running: {desc} ===")
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ {desc} completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ {desc} failed with error: {e}")

# Set the root path to the parent directory where the Python files are located
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define tests to run
tests = [
    (["python", os.path.join(root, "app.py")], "Main app (single bill generation)"),
    (["python", os.path.join(root, "batch_run_demo.py")], "Batch run demo"),
    (["python", os.path.join(root, "test_chrome_headless.py")], "Headless Chrome test"),
    (["python", os.path.join(root, "test_enhanced_pdf.py")], "Enhanced PDF test"),
]

# Add launcher tests dynamically based on what exists
launchers_dir = os.path.join(root, "launchers")
if os.path.exists(launchers_dir):
    for launcher in os.listdir(launchers_dir):
        if launcher.endswith(".py"):
            launcher_path = os.path.join(launchers_dir, launcher)
            tests.append((["python", launcher_path], f"Launcher: {launcher}"))

if __name__ == "__main__":
    for cmd, desc in tests:
        run_command(cmd, desc)

    print("\n🎉 All tests attempted. Check OUTPUT_FILES/ and BATCH_RUN_SUMMARY.txt for results.")