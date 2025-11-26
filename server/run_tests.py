import subprocess
import sys
import os
import time

def run_test(test_file):
    """Run a single test file and capture output"""
    print(f"📋 Running {test_file}...")
    print("=" * 50)
    
    try:
        # Run the test and capture output
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Print stdout
        if result.stdout:
            print(result.stdout)
        
        # Print stderr if there was an error
        if result.stderr:
            print("STDERR:", result.stderr)
            
        print("=" * 50)
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print(f"❌ {test_file} timed out")
        print("=" * 50)
        return False
    except Exception as e:
        print(f"❌ Error running {test_file}: {e}")
        print("=" * 50)
        return False

def main():
    print("🚀 Running FitFlow Test Suite")
    print()
    
    # Make sure we're in the correct directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Check if server is running
    print("🔍 Checking if server is running...")
    try:
        import requests
        response = requests.get("http://localhost:5555/", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running!")
        else:
            print("❌ Server returned unexpected status:", response.status_code)
    except:
        print("❌ Server is not running on port 5555")
        print("💡 Please start the server first: python run.py")
        return
    
    print()
    
    # List of test files to run
    test_files = [
        "test_db.py",
        "test_auth.py", 
        "test_jwt.py"
    ]
    
    # Run each test
    results = {}
    for test_file in test_files:
        if os.path.exists(test_file):
            success = run_test(test_file)
            results[test_file] = success
            time.sleep(1)  # Brief pause between tests
        else:
            print(f"❌ Test file {test_file} not found")
            results[test_file] = False
    
    # Print summary
    print("\n🎉 Test Suite Summary")
    print("=" * 50)
    for test_file, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_file}")
    
    # Overall result
    all_passed = all(results.values())
    if all_passed:
        print("\n🎊 All tests passed!")
    else:
        print(f"\n💡 Some tests failed. {sum(results.values())}/{len(results)} passed")

if __name__ == "__main__":
    main()