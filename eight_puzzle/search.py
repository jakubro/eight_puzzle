import logging
from typing import Callable, List, Optional, TypeVar

import problem

T_State = TypeVar('T_State')
T_Action = TypeVar('T_Action')

_log = logging.getLogger()


class Node:
    def __init__(
            self,
            state: problem.Problem,
            parent: Optional['Node'],
            action: Optional[T_Action],
            cost: int):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = (parent.cost if parent else 0) + cost
        self.depth = parent.depth + 1 if parent else 0


def a_star(
        state: problem.Problem,
        heuristic: Callable[[T_State], int],
) -> Node:
    node = Node(state, None, None, 0)
    frontier: List[Node] = [node]
    explored: List[Node] = []
    i = 0
    while True:
        solution = _a_star_iter(frontier, explored, heuristic)
        if solution:
            return solution

        if i % 100 == 0:
            cost = frontier and frontier[-1].cost
            depth = frontier and frontier[-1].depth
            _log.debug(f"{i} {len(frontier)} {len(explored)} {cost} {depth}")
        i += 1


def _a_star_iter(
        frontier: List[Node],
        explored: List[Node],
        heuristic: Callable[[T_State], int],
) -> Optional[Node]:
    if not frontier:
        raise StopIteration()

    node = frontier.pop()

    if node.state.goal_test():
        return node

    explored.append(node)

    for action in node.state.actions():
        problem_ = node.state.invoke(action)
        state = problem_.state()
        child = Node(problem_, node, action, 1 + heuristic(state))

        found = False
        if not found:
            for i, x in enumerate(frontier):
                if state == x.state.state():
                    if child.cost > x.cost:
                        frontier[i] = child
                        frontier.sort(key=lambda it: it.cost, reverse=True)
                    found = True

        if not found:
            for x in explored:
                if state == x.state.state():
                    found = True
                    break

        if not found:
            frontier.append(child)
            frontier.sort(key=lambda it: it.cost, reverse=True)
