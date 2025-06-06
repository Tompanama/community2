#!/usr/bin/env python3
"""
Script to run tests for the Community AI backend
"""

import os
import sys
import pytest

def main():
    """Run the tests"""
    print("Running tests for Community AI backend...")
    
    # Add the current directory to the Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Run the tests
    result = pytest.main(['-v', 'tests/'])
    
    # Return the exit code
    return result

if __name__ == '__main__':
    sys.exit(main())

