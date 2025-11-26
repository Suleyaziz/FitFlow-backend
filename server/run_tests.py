import subprocess
import sys

def run_tests():
    print("🚀 Running FitFlow Test Suite\n")
    
    test_files = [
        "test_db.py",
        "test_jwt.py", 
        "test_auth.py"
    ]
    
    for test_file in test_files:
        print(f"📋 Running {test_file}...")
        print("=" * 50)
        
        try:
            # Run the test file
            result = subprocess.run([sys.executable, test_file], 
                                  capture_output=True, text=True)
            
            # Print output
            print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            
            print("=" * 50)
            
        except Exception as e:
            print(f"❌ Failed to run {test_file}: {e}")
            print("=" * 50)
    
    print("🎉 All tests completed!")

if __name__ == '__main__':
    run_tests()