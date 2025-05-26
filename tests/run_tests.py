import unittest
import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import test modules
from tests.test_lexer import TestLexer
from tests.test_parser import TestParser
from tests.test_interpreter import TestInterpreter

def run_tests():
    """Run all tests for the language implementation"""
    # Create a test suite combining all test cases
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestLexer))
    test_suite.addTest(unittest.makeSuite(TestParser))
    test_suite.addTest(unittest.makeSuite(TestInterpreter))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result

if __name__ == "__main__":
    result = run_tests()
    # Exit with non-zero code if there were failures
    sys.exit(not result.wasSuccessful())