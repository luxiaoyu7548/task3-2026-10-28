"""Terminal rendering and keyboard adapters for the Snake game."""

from __future__ import annotations

import os
import select
import sys
import time
from typing import Optional

try:  # Supports both ``python -m snake.main`` and ``python snake/main.py``.
    from .game import Direction, GameState
except ImportError:  # pragma: no cover - exercised by direct script launch.
    from game import Direction, GameState

DEFAULT_TICK = 0.16
MIN_TICK = 0.05
MAX_TICK = 0.50


def key_to_direction(key: str) -> Optional[Direction]:
    mapping = {
        "w": Direction.UP,
        "W": Direction.UP,
        "UP": Direction.UP,
        "\x00H": Direction.UP,
        "\xe0H": Direction.UP,
        "s": Direction.DOWN,
        "S": Direction.DOWN,
        "DOWN": Direction.DOWN,
        "\x00P": Direction.DOWN,
        "\xe0P": Direction.DOWN,
        "a": Direction.LEFT,
        "A": Direction.LEFT,
        "LEFT": Direction.LEFT,
        "\x00K": Direction.LEFT,
        "\xe0K": Direction.LEFT,
        "d": Direction.RIGHT,
        "D": Direction.RIGHT,
        "RIGHT": Direction.RIGHT,
        "\x00M": Direction.RIGHT,
        "\xe0M": Direction.RIGHT,
    }
    return mapping.get(key)


def render(state: GameState) -> str:
    snake = set(state.snake)
    head = state.snake[0]
    rows = ["+" + "-" * state.width + "+"]
    for y in range(state.height):
        cells = []
        for x in range(state.width):
            point = (x, y)
            if point == head:
                cells.append("@")
            elif point in snake:
                cells.append("o")
            elif point == state.food:
                cells.append("*")
            else:
                cells.append(" ")
        rows.append("|" + "".join(cells) + "|")
    rows.append("+" + "-" * state.width + "+")
    if state.won:
        status = "YOU WIN"
    elif not state.alive:
        status = "GAME OVER"
    else:
        status = "PLAYING"
    rows.append(f"Score: {state.score}  Length: {len(state.snake)}  Status: {status}")
    rows.append("WASD / arrows: move   P: pause   +/-: speed   Q: quit")
    return "\n".join(rows)


def read_key() -> Optional[str]:
    """Read one key without blocking; return ``None`` when no key is ready."""
    if os.name == "nt":
        import msvcrt

        if not msvcrt.kbhit():
            return None
        first = msvcrt.getwch()
        if first in ("\x00", "\xe0"):
            return first + msvcrt.getwch()
        if first == "\x03":
            return "CTRL_C"
        return first

    ready, _, _ = select.select([sys.stdin], [], [], 0)
    if not ready:
        return None
    first = sys.stdin.read(1)
    if first == "\x03":
        return "CTRL_C"
    if first == "\x1b":
        sequence = sys.stdin.read(2)
        return {"[A": "UP", "[B": "DOWN", "[C": "RIGHT", "[D": "LEFT"}.get(
            sequence, first + sequence
        )
    return first


def run_demo(seed: int = 7) -> str:
    """Run a deterministic, non-blocking smoke demonstration."""
    state = GameState(width=12, height=8, seed=seed)
    steps = 0
    state.food = (state.snake[0][0] + 1, state.snake[0][1])
    state.step()  # guaranteed first-frame eat, exercising growth and scoring.
    steps += 1
    for direction in (Direction.DOWN, Direction.LEFT, Direction.UP):
        state.set_direction(direction)
        state.step()
        steps += 1
    return (
        f"DEMO seed={seed} steps={steps} score={state.score} "
        f"length={len(state.snake)} status={state.status}"
    )


def run_interactive(state: GameState) -> int:
    """Run the real keyboard-driven game and return the final score."""
    tick = DEFAULT_TICK
    paused = False
    print("\x1b[?25l", end="", flush=True)
    try:
        while state.alive:
            print("\x1b[2J\x1b[H" + render(state), end="\n", flush=True)
            key = read_key()
            if key in ("q", "Q", "CTRL_C"):
                return state.score
            if key in ("p", "P"):
                paused = not paused
            elif key in ("+", "="):
                tick = max(MIN_TICK, tick - 0.02)
            elif key == "-":
                tick = min(MAX_TICK, tick + 0.02)
            else:
                direction = key_to_direction(key or "")
                if direction is not None:
                    state.set_direction(direction)
            if not paused:
                state.step()
            time.sleep(tick)
        print(render(state), flush=True)
        return state.score
    except KeyboardInterrupt:
        return state.score
    finally:
        print("\x1b[?25h", flush=True)
