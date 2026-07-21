import unittest
import sys

def run_suite():
    """Discover and run all automated unit tests in the tests/ directory."""
    print("=" * 60)
    print(" 🧪 Softwarica Lost & Found - Running Automated Test Suite")
    print("=" * 60)
    
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='tests', pattern='test_*.py')

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("=" * 60)
    if result.wasSuccessful():
        print(" SUCCESS: All automated tests passed clean!")
        sys.exit(0)
    else:
        print(" FAILURE: Some tests failed. Check output above.")
        sys.exit(1)

if __name__ == '__main__':
    run_suite()