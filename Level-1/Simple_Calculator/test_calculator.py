import unittest
from calculator import addition,subtraction,multiplication,division

    # Test Suite for validating calculator operations.
class TestCalculator(unittest.TestCase):

    # Verify addition returns the correct result or not.
    def test_addition(self):
        self.assertEqual(addition(2, 3), 5)

    # Verify subtraction returns the correct result or not.
    def test_subtraction(self):
        self.assertEqual(subtraction(2, 3), -1)

    # Verify multiplication returns the correct result or not.
    def test_multiplication(self):
        self.assertEqual(multiplication(2, 3), 6)

    # Verify division returns the correct result or not.
    def test_division(self):
        self.assertEqual(division(4, 2), 2)

    # # Verify division by zero returns the expected error message or not
    def test_division_by_zero(self):
        self.assertEqual(
            division(10, 0),
            "Error: Division by zero is not allowed."
        )
        
 # Run the test suite when this file is executed directly.
if __name__=="__main__":
    unittest.main()