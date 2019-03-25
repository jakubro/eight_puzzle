import argparse
import logging
from typing import Tuple

import heuristics
import rules
import search


def main() -> None:
    parser = argparse.ArgumentParser(description="8 puzzle.")
    parser.add_argument(
        'action', choices=['solve', 'play'])
    parser.add_argument(
        '-i', '--iterations', type=int, default=15,
        help="Number of iterations to shuffle solution before searching.")
    parser.add_argument(
        '-ww', '--width', type=int, default=3,
        help="Width of the board.")
    parser.add_argument(
        '-hh', '--height', type=int, default=3,
        help="Height of the board.")
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help="Be verbose.")
    parser.add_argument(
        '-vv', '--debug', action='store_true',
        help="Be even more verbose.")

    args = parser.parse_args()
    setup_logging(args)

    if args.action == 'solve':
        solve(args)
    else:
        assert args.action == 'play'
        play(args)


def solve(args: argparse.Namespace) -> None:
    problem_ = rules.EightPuzzle.initialize_random(
        iterations=args.iterations,
        width=args.width,
        height=args.height)
    print(problem_)

    print("\nSearching for solution ..")
    solution_ = search.a_star(problem_, heuristics.manhattan_distance)

    print("\nFound following solution:")
    path = flatten_solution(solution_)
    for action, state in path:
        print(state)
        if action:
            print(action)
        print()

    _, state = path[-1]
    assert state.goal_test()


def play(args: argparse.Namespace) -> None:
    problem_ = rules.EightPuzzle.initialize_random(
        iterations=args.iterations,
        width=args.width,
        height=args.height)

    while True:
        print(f"\n{problem_}")
        print("\nType W for UP, A for RIGHT, S for DOWN and L for LEFT:  ",
              end='')

        s = input().lower()
        if s == 'w':
            action = rules.Action.UP
        elif s == 's':
            action = rules.Action.DOWN
        elif s == 'a':
            action = rules.Action.LEFT
        elif s == 'd':
            action = rules.Action.RIGHT
        else:
            continue

        problem_ = problem_.invoke(action)


def setup_logging(args: argparse.Namespace) -> None:
    log = logging.getLogger()
    if args.debug:
        log.setLevel(logging.DEBUG)
    elif args.verbose:
        log.setLevel(logging.INFO)
    else:
        log.setLevel(logging.WARNING)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)


def flatten_solution(
        solution_: search.Node,
) -> Tuple[rules.Action, rules.EightPuzzle]:
    """Flattens path (node.parent -> node.parent -> ... -> node)."""

    rv = []
    it = solution_
    while it.parent:
        rv.insert(0, (it.action, it.state))
        it = it.parent
    # noinspection PyTypeChecker
    return rv


if __name__ == '__main__':
    main()
