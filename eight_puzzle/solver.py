import argparse
import enum
import logging
from typing import Dict, List, Optional, Tuple

import problem
import search

# 8 Puzzle Problem
# -----------------------------------------------------------------------------

WIDTH = 3
HEIGHT = 3

Position = Tuple[int, int]
Board = Dict[Position, Optional[Position]]


class Action(enum.Enum):
    UP = enum.auto()
    RIGHT = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()

    def opposite(self):
        if self == Action.UP:
            return self.DOWN
        elif self == Action.RIGHT:
            return self.LEFT
        elif self == Action.DOWN:
            return self.UP
        elif self == Action.LEFT:
            return self.RIGHT
        else:
            raise ValueError('self')


class EightPuzzle(problem.Problem[Board, Action]):
    def __init__(self, state: Board):
        super().__init__(state)

    def goal_test(self) -> bool:
        for (i, j), v in self._state.items():
            if v is None:
                if i != WIDTH - 1 or j != HEIGHT - 1:
                    return False
            else:
                x, y = v
                if i != x or j != y:
                    return False
        return True

    @classmethod
    def all_actions(cls) -> List[Action]:
        # noinspection PyTypeChecker
        return list(Action)

    def can_invoke(self, action: Action) -> bool:
        x, y = self._empty_position()
        if action == Action.UP:
            return x > 0
        elif action == Action.RIGHT:
            return y < WIDTH - 1
        elif action == Action.DOWN:
            return x < HEIGHT - 1
        elif action == Action.LEFT:
            return y > 0
        else:
            raise ValueError('action')

    def invoke(self, action: Action) -> 'EightPuzzle':
        state = {**self._state}
        x, y = i, j = self._empty_position()

        if action == Action.UP and x > 0:
            x -= 1
        elif action == Action.RIGHT and y < WIDTH - 1:
            y += 1
        elif action == Action.DOWN and x < HEIGHT - 1:
            x += 1
        elif action == Action.LEFT and y > 0:
            y -= 1

        state[(x, y)], state[(i, j)] = None, state[(x, y)]
        return EightPuzzle(state)

    def _empty_position(self) -> Position:
        for k, v in self._state.items():
            if v is None:
                return k
        raise StopIteration()

    def __str__(self):
        state = self._state
        rv = ""
        for i in range(HEIGHT):
            rv += "\n"
            for j in range(WIDTH):
                it = state[(i, j)]
                if it is None:
                    rv += "-"
                else:
                    x, y = it
                    it = WIDTH * x + y
                    rv += str(it)
                rv += " "
        return rv.strip("\n")

    @classmethod
    def initialize_goal(cls) -> 'EightPuzzle':
        rv = {}
        for i in range(HEIGHT):
            for j in range(WIDTH):
                k = (i, j)
                rv[k] = k
        rv[(HEIGHT - 1, WIDTH - 1)] = None
        return EightPuzzle(rv)


# Heuristics
# -----------------------------------------------------------------------------

def misplaced_tiles(state: Board) -> int:
    rv = 0
    for k, v in state.items():
        if v is None:
            v = (HEIGHT - 1, WIDTH - 1)
        if k != v:
            rv += 1
    return rv


def manhattan_distance(state: Board) -> int:
    rv = 0
    for k, v in state.items():
        if v is None:
            v = (HEIGHT - 1, WIDTH - 1)
        rv += _manhattan_distance(k, v)
    return rv


def _manhattan_distance(a: Position, b: Position) -> int:
    x, y = a
    i, j = b
    return abs(x - i) + abs(y - j)


# Solver
# -----------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="8-puzzle solver.")
    parser.add_argument(
        '-i', '--iterations', type=int, default=15,
        help="Number of iterations to shuffle solution before searching.")
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help="Be verbose.")
    parser.add_argument(
        '-vv', '--debug', action='store_true',
        help="Be more verbose.")

    args = parser.parse_args()
    setup_logging(args)

    problem_ = EightPuzzle.initialize_random(iterations=args.iterations)
    print(problem_)
    print()
    print("Searching for solution ..")

    solution_ = search.a_star(problem_, manhattan_distance)
    print()
    print("Found following solution:")
    print()

    path = flatten_solution(solution_)
    for action, state in path:
        print(state)
        if action:
            print(action)
        print()

    _, state = path[-1]
    assert state.goal_test()


def flatten_solution(solution_: search.Node) -> Tuple[Action, EightPuzzle]:
    rv = []
    it = solution_
    while it.parent:
        rv.insert(0, (it.action, it.state))
        it = it.parent
    # noinspection PyTypeChecker
    return rv


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


if __name__ == '__main__':
    main()
