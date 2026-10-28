"""Deterministic, terminal-independent rules for the Snake game."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
import random
from typing import Deque, Optional

Point = tuple[int, int]


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @property
    def delta(self) -> tuple[int, int]:
        return self.value


@dataclass(frozen=True)
class StepResult:
    moved: bool
    ate_food: bool = False
    collision: bool = False
    finished: bool = False


class GameState:
    """Mutable game state with deterministic transitions and no I/O."""

    def __init__(self, width: int = 24, height: int = 14, seed: Optional[int] = None):
        if width < 3 or height < 1:
            raise ValueError("width must be at least 3 and height must be positive")

        self.width = width
        self.height = height
        self._random = random.Random(seed)
        self.direction = Direction.RIGHT
        self.score = 0
        self.alive = True
        self.won = False

        start_x = min(max(2, width // 2), width - 1)
        center_y = height // 2
        self.snake: Deque[Point] = deque(
            (start_x - offset, center_y) for offset in range(3)
        )
        self.food: Optional[Point] = None
        self._place_food()
        if self.food is None:
            self.won = True
            self.alive = False

    @property
    def status(self) -> str:
        if self.won:
            return "won"
        if not self.alive:
            return "collision"
        return "playing"

    def set_direction(self, direction: Direction) -> None:
        """Set a non-reversing direction; invalid values are ignored by callers."""
        if not self.alive or self._is_opposite(direction, self.direction):
            return
        self.direction = direction

    def step(self) -> StepResult:
        """Advance one frame and return the observable outcome."""
        if not self.alive:
            return StepResult(moved=False, finished=True)

        dx, dy = self.direction.delta
        head_x, head_y = self.snake[0]
        next_head = (head_x + dx, head_y + dy)

        if not self._inside(next_head):
            self.alive = False
            return StepResult(moved=False, collision=True, finished=True)

        ate_food = next_head == self.food
        occupied = set(self.snake)
        if not ate_food:
            occupied.discard(self.snake[-1])
        if next_head in occupied:
            self.alive = False
            return StepResult(moved=False, collision=True, finished=True)

        self.snake.appendleft(next_head)
        if ate_food:
            self.score += 1
            self._place_food()
            if self.food is None:
                self.won = True
                self.alive = False
            return StepResult(
                moved=True,
                ate_food=True,
                finished=not self.alive,
            )

        self.snake.pop()
        return StepResult(moved=True)

    def _inside(self, point: Point) -> bool:
        x, y = point
        return 0 <= x < self.width and 0 <= y < self.height

    def _place_food(self) -> None:
        occupied = set(self.snake)
        free = [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if (x, y) not in occupied
        ]
        self.food = self._random.choice(free) if free else None

    @staticmethod
    def _is_opposite(first: Direction, second: Direction) -> bool:
        return first.delta == (-second.delta[0], -second.delta[1])
