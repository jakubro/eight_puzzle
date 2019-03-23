import enum
from typing import Dict, List, Optional, Tuple

import problem

#: Tuple of vertical and horizontal offset from the origin (top, left).
Position = Tuple[int, int]

#: Key is position of this tile on the board.
#: Value is position where this tile belongs. None if the tile is empty.
Board = Dict[Position, Optional[Position]]


class Action(enum.Enum):
    """Direction in which to move the empty tile."""

    UP = enum.auto()
    RIGHT = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()

    def opposite(self):
        """:returns: Opposite direction."""

        if self == Action.UP:
            return self.DOWN
        elif self == Action.RIGHT:
            return self.LEFT
        elif self == Action.DOWN:
            return self.UP
        else:
            assert self == Action.LEFT
            return self.RIGHT


class EightPuzzle(problem.Problem[Board, Action]):
    """8 puzzle.

    See https://en.wikipedia.org/wiki/15_puzzle
    """

    def __init__(self, state: Board, width: int, height: int):
        """
        :param state: Initial state.
        :param width: Width of the board.
        :param height: Height of the board.
        :param height: Height of the board.
        """

        super().__init__(state)
        self.width = width
        self.height = height

    def goal_test(self) -> bool:
        for (i, j), v in self.state.items():
            if v is None:
                if i != self.height - 1 or j != self.width - 1:
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
        i, j = self._empty_position()
        if action == Action.UP:
            return i > 0
        elif action == Action.RIGHT:
            return j < self.width - 1
        elif action == Action.DOWN:
            return i < self.height - 1
        else:
            assert action == Action.LEFT
            return j > 0

    def invoke(self, action: Action) -> 'EightPuzzle':
        state = {**self.state}
        i, j = x, y = self._empty_position()

        if action == Action.UP and i > 0:
            i -= 1
        elif action == Action.RIGHT and j < self.width - 1:
            j += 1
        elif action == Action.DOWN and i < self.height - 1:
            i += 1
        elif action == Action.LEFT and j > 0:
            j -= 1

        state[(i, j)], state[(x, y)] = None, state[(i, j)]
        return EightPuzzle(state, self.width, self.height)

    def _empty_position(self) -> Position:
        """:returns: Position of the empty tile."""

        for k, v in self.state.items():
            if v is None:
                return k
        raise StopIteration()

    def __str__(self):
        state = self.state
        rv = ""
        for i in range(self.height):
            rv += "\n"
            for j in range(self.width):
                it = state[(i, j)]
                if it is None:
                    rv += "-"
                else:
                    x, y = it
                    it = self.width * x + y
                    rv += str(it)
                rv += " "
        return rv.strip("\n")

    @classmethod
    def initialize_goal(cls, **kwargs) -> 'EightPuzzle':
        width = kwargs.get('width')
        height = kwargs.get('height')
        rv = {}
        for i in range(height):
            for j in range(width):
                k = (i, j)
                rv[k] = k
        rv[(height - 1, width - 1)] = None
        return EightPuzzle(rv, **kwargs)
