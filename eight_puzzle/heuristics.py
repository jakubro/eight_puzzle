import rules


def misplaced_tiles(problem_: rules.EightPuzzle) -> int:
    """:returns: Count of misplaced tiles."""

    rv = 0
    for k, v in problem_.state.items():
        if v is None:
            v = (problem_.height - 1, problem_.width - 1)
        if k != v:
            rv += 1
    return rv


def manhattan_distance(problem_: rules.EightPuzzle) -> int:
    """:returns: Sum of Manhattan distances for each misplaced tile."""

    rv = 0
    for k, v in problem_.state.items():
        if v is None:
            v = (problem_.height - 1, problem_.width - 1)
        rv += _manhattan_distance(k, v)
    return rv


def _manhattan_distance(a: rules.Position, b: rules.Position) -> int:
    """:returns: Manhattan distance for one misplaced tile, i.e. its distance
    from the current position to the position where it belongs."""

    i, j = a
    x, y = b
    return abs(i - x) + abs(j - y)
