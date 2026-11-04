"""Terminal rendering and keyboard adapters for the Snake game."""

from __future__ import annotations

import os
from contextlib import contextmanager
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


def render(
    state: GameState, *, paused: bool = False, ready: bool = False,
    tick: float = DEFAULT_TICK,
) -> str:
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
    elif ready:
        status = "READY"
    elif paused:
        status = "PAUSED"
    else:
        status = "PLAYING"
    rows.append(
        f"Score: {state.score}  Length: {len(state.snake)}  "
        f"Status: {status}  Speed: {1 / tick:.1f}/s"
    )
    if not state.alive:
        rows.append("ENTER: replay   ESC / Q: quit")
    elif ready:
        rows.append("ENTER / SPACE: start   Arrows / WASD: move   +/-: speed")
    elif paused:
        rows.append("SPACE / P: resume   Arrows / WASD: direction   +/-: speed")
    else:
        rows.append("Arrows / WASD: move   SPACE / P: pause   +/-: speed")
    rows.append("ESC / Q: quit   Letter keys use English input; arrows / SPACE / ESC work with IME.")
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


@contextmanager
def _terminal_screen():
    """Enable ANSI on classic Windows consoles and restore their output mode."""
    restore = None
    if os.name == "nt" and sys.stdout.isatty():
        import ctypes
        import msvcrt

        kernel = ctypes.windll.kernel32
        handle = ctypes.c_void_p(msvcrt.get_osfhandle(sys.stdout.fileno()))
        mode = ctypes.c_ulong()
        if kernel.GetConsoleMode(handle, ctypes.byref(mode)):
            if not kernel.SetConsoleMode(handle, mode.value | 0x0004):
                raise OSError("Could not enable Windows console ANSI rendering")
            restore = (kernel, handle, mode.value)
    print("\x1b[2J\x1b[H\x1b[?25l", end="", flush=True)
    try:
        yield
    finally:
        print("\x1b[?25h", end="\n", flush=True)
        if restore is not None:
            kernel, handle, mode = restore
            kernel.SetConsoleMode(handle, mode)


def run_interactive(state: GameState) -> int:
    """Run keyboard play, including ready, pause, and replay screens."""
    tick = DEFAULT_TICK
    paused = False
    started = False
    next_move = time.monotonic() + tick

    def draw():
        frame = render(state, paused=paused, ready=not started, tick=tick)
        print("\x1b[H" + "\x1b[K\n".join(frame.splitlines()) + "\x1b[K\x1b[J",
              end="", flush=True)

    try:
        with _terminal_screen():
            draw()
            while True:
                key = read_key()
                now = time.monotonic()
                changed = False
                if key in ("q", "Q", "CTRL_C", "\x1b"):
                    return state.score
                if not state.alive:
                    if key in ("\r", "\n", "r", "R"):
                        state = GameState(width=state.width, height=state.height)
                        paused = False
                        started = False
                        next_move = now + tick
                        changed = True
                elif key in ("\r", "\n", " ") and not started:
                    started = True
                    next_move = now + tick
                    changed = True
                elif key in ("p", "P", " "):
                    paused = not paused
                    started = True
                    next_move = now + tick
                    changed = True
                elif key in ("+", "=", "-"):
                    tick = (min(MAX_TICK, tick + 0.02) if key == "-"
                            else max(MIN_TICK, tick - 0.02))
                    next_move = now + tick
                    changed = True
                else:
                    direction = key_to_direction(key or "")
                    if direction is not None and state.alive:
                        state.set_direction(direction)
                        if not started:
                            next_move = now + tick
                        started = True
                        changed = True
                if started and not paused and state.alive and now >= next_move:
                    state.step()
                    next_move = now + tick
                    changed = True
                if changed:
                    draw()
                time.sleep(0.01)
    except KeyboardInterrupt:
        return state.score
