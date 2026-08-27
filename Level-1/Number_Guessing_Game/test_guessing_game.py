import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from guessing_game import play_game

# Test suite for validating the number guessing game.
class Test_No_Guessing_Game(unittest.TestCase):

    # Verify that the player wins when the guessed number is correct.
    @patch("guessing_game.random.randint", return_value = 50)
    @patch("builtins.input", return_value="50")

    def test_correct_guess(self, mock_input, mock_random):
        output = io.StringIO()

        with redirect_stdout(output):
            play_game()

        self.assertIn("Congratulations!", output.getvalue())

    # verify that a guess lower than the secrete number shows the correct line.
    @patch("guessing_game.random.randint", return_value = 50)
    @patch("builtins.input", side_effect = ["25", "50"])

    def test_too_low_guess(self, mock_input, mock_random):
        output = io.StringIO()

        with redirect_stdout(output):
            play_game()

        self.assertIn("Too Low! Try a higher number.", output.getvalue())
        self.assertIn("Congratulations!", output.getvalue())

    # Verify that a guess higher than the secret number shows the correct hint.
    @patch("guessing_game.random.randint", return_value = 50)
    @patch("builtins.input", side_effect = ["75", "50"])

    def test_too_high_guess(self, mock_input, mock_random):
        output = io.StringIO()

        with redirect_stdout(output):
            play_game()

        self.assertIn("Too High! Try a lower number.", output.getvalue())
        self.assertIn("Congratulations!", output.getvalue())

    # Verify that invalid input does not consume a valid attempt.
    @patch("guessing_game.random.randint", return_value = 50)
    @patch("builtins.input", side_effect = ["hello", "50"])

    def test_invalid_input_no_attempt_penalty(self, mock_input, mock_random):
        output = io.StringIO()

        with redirect_stdout(output):
            play_game()

        result = output.getvalue()

        self.assertIn("Please Enter the Valid Number.", result)
        self.assertEqual(mock_input.call_count, 2)

        first_prompt = mock_input.call_args_list[0].args[0]
        second_prompt = mock_input.call_args_list[1].args[0]

        self.assertIn("[5 attempts left]", first_prompt)
        self.assertIn("[5 attempts left]", second_prompt)

    # Verify that the game ends after all five valid attempts are used.
    @patch("guessing_game.random.randint", return_value = 50)
    @patch("builtins.input", side_effect = ["10","20","30","40","60"])

    def test_game_over_after_max_attempts(self, mock_input, mock_random):
        output = io.StringIO()

        with redirect_stdout(output):
            play_game()

        result = output.getvalue()

        self.assertIn("Game Over!", result)
        self.assertIn("The number was 50", result)

# Run the test suite when this file is executed directly.
if __name__=="__main__":
    unittest.main()