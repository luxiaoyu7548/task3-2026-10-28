"""Command-line entry point for the Snake game."""

from __future__ import annotations

import argparse

try:  # Supports both package and direct-script execution.
    from .cli import run_demo, run_interactive
    from .game import GameState
except ImportError:  # pragma: no cover - exercised by direct script launch.
    from cli import run_demo, run_interactive
    from game import GameState


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="A dependency-free terminal Snake game")
    parser.add_argument("--demo", action="store_true", help="run a deterministic non-interactive demo")
    parser.add_argument("--seed", type=int, default=7, help="random seed for reproducible food placement")
    parser.add_argument("--width", type=int, default=24, help="board width in cells")
    parser.add_argument("--height", type=int, default=14, help="board height in cells")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.demo:
        print(run_demo(seed=args.seed))
        return 0

    state = GameState(width=args.width, height=args.height, seed=args.seed)
    run_interactive(state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
