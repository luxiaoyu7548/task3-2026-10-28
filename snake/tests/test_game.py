import unittest
from collections import deque

from snake.game import Direction, GameState


class GameStateTests(unittest.TestCase):
    def test_initial_state_has_three_segment_snake_and_food(self):
        state = GameState(width=10, height=6, seed=7)

        self.assertEqual(len(state.snake), 3)
        self.assertEqual(state.score, 0)
        self.assertTrue(state.alive)
        self.assertFalse(state.won)
        self.assertNotIn(state.food, state.snake)

    def test_step_moves_snake_in_current_direction(self):
        state = GameState(width=10, height=6, seed=7)
        before = list(state.snake)

        result = state.step()

        self.assertTrue(result.moved)
        self.assertEqual(state.snake[0], (before[0][0] + 1, before[0][1]))
        self.assertEqual(len(state.snake), 3)

    def test_reverse_direction_is_ignored(self):
        state = GameState(width=10, height=6, seed=7)

        state.set_direction(Direction.LEFT)
        state.step()

        self.assertEqual(state.direction, Direction.RIGHT)
        self.assertTrue(state.alive)

    def test_eating_food_grows_and_scores(self):
        state = GameState(width=10, height=6, seed=7)
        state.food = (state.snake[0][0] + 1, state.snake[0][1])

        result = state.step()

        self.assertTrue(result.ate_food)
        self.assertEqual(state.score, 1)
        self.assertEqual(len(state.snake), 4)
        self.assertNotIn(state.food, state.snake)

    def test_wall_collision_ends_game(self):
        state = GameState(width=3, height=3, seed=7)

        result = state.step()

        self.assertTrue(result.collision)
        self.assertTrue(result.finished)
        self.assertFalse(state.alive)
        self.assertFalse(state.won)

    def test_self_collision_ends_game(self):
        state = GameState(width=5, height=5, seed=7)
        state.snake = deque([(2, 1), (2, 2), (1, 2), (1, 1), (0, 1)])
        state.set_direction(Direction.DOWN)
        state.set_direction(Direction.LEFT)

        result = state.step()

        self.assertTrue(result.collision)
        self.assertFalse(state.alive)

    def test_full_board_finishes_game(self):
        state = GameState(width=4, height=1, seed=7)
        state.food = (3, 0)

        result = state.step()

        self.assertTrue(result.ate_food)
        self.assertTrue(result.finished)
        self.assertTrue(state.won)
        self.assertFalse(state.alive)
        self.assertEqual(len(state.snake), 4)

    def test_initial_full_board_is_already_won(self):
        state = GameState(width=3, height=1, seed=7)

        self.assertIsNone(state.food)
        self.assertTrue(state.won)
        self.assertFalse(state.alive)
        self.assertEqual(state.status, "won")


if __name__ == "__main__":
    unittest.main()
