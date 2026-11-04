"""Regressions for problems first observed while playing the real window."""

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from snake.cli import render, run_interactive
from snake.game import GameState


class PlayControlsTests(unittest.TestCase):
    def test_paused_screen_identifies_pause_and_resume_key(self):
        screen = render(GameState(width=8, height=5, seed=7), paused=True)
        self.assertIn("Status: PAUSED", screen)
        self.assertIn("resume", screen)

    def test_ready_screen_explains_how_to_start(self):
        screen = render(GameState(width=8, height=5, seed=7), ready=True)
        self.assertIn("Status: READY", screen)
        self.assertIn("ENTER", screen)
        self.assertIn("SPACE", screen)

    def test_speed_change_is_visible_to_player(self):
        screen = render(GameState(width=8, height=5, seed=7), tick=0.5)
        self.assertIn("Speed: 2.0/s", screen)

    def run_keys(self, state, keys):
        clock = [0.0]
        sequence = iter(keys)

        def read():
            key = next(sequence)
            if key is None:
                clock[0] += 0.2
            return key

        output = io.StringIO()
        with patch("snake.cli.read_key", side_effect=read):
            with patch("snake.cli.time.monotonic", side_effect=lambda: clock[0]):
                with patch("snake.cli.time.sleep"):
                    with redirect_stdout(output):
                        score = run_interactive(state)
        return score, output.getvalue()

    def test_space_pauses_movement_and_escape_quits(self):
        state = GameState(width=8, height=5, seed=7)
        before = state.snake[0]
        score, output = self.run_keys(state, ["\r", None, " ", None, "\x1b"])
        self.assertEqual(state.snake[0], (before[0] + 1, before[1]))
        self.assertEqual(score, 0)
        self.assertIn("Status: PAUSED", output)

    def test_finished_round_can_restart_with_zero_score(self):
        state = GameState(width=4, height=1, seed=7)
        score, output = self.run_keys(state, ["\r", None, "\r", "\x1b"])
        self.assertIn("YOU WIN", output)
        self.assertIn("replay", output)
        self.assertEqual(score, 0)
        self.assertIn("Status: READY", output)


if __name__ == "__main__":
    unittest.main()
