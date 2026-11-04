import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from snake.cli import key_to_direction, render, run_demo
from snake.game import Direction, GameState
import snake.main as main_module


class CliTests(unittest.TestCase):
    def test_render_shows_score_and_controls(self):
        output = render(GameState(width=8, height=5, seed=7))

        self.assertIn("Score: 0", output)
        self.assertIn("WASD", output)
        self.assertIn("Q", output)

    def test_key_to_direction_accepts_lower_and_uppercase(self):
        self.assertEqual(key_to_direction("w"), Direction.UP)
        self.assertEqual(key_to_direction("D"), Direction.RIGHT)
        self.assertIsNone(key_to_direction("x"))

    def test_demo_is_noninteractive_and_reports_result(self):
        output = run_demo(seed=7)

        self.assertIn("DEMO", output)
        self.assertIn("score=", output)
        self.assertIn("length=", output)
        self.assertIn("status=", output)

    def test_interactive_entry_does_not_print_a_duplicate_initial_frame(self):
        captured = io.StringIO()
        with patch.object(main_module, "run_interactive", return_value=0) as runner:
            with redirect_stdout(captured):
                exit_code = main_module.main(["--width", "8", "--height", "5"])

        self.assertEqual(exit_code, 0)
        self.assertEqual(captured.getvalue(), "")
        runner.assert_called_once()

    def test_interactive_entry_returns_zero_after_a_scored_quit(self):
        with patch.object(main_module, "run_interactive", return_value=1):
            self.assertEqual(main_module.main([]), 0)


if __name__ == "__main__":
    unittest.main()
