import abc
import random
from typing import Generic, List, Optional, TypeVar

T_State = TypeVar('T_State')
T_Action = TypeVar('T_Action')


class Problem(Generic[T_State, T_Action]):
    def __init__(self, state: T_State):
        """
        :param state: Initial state.
        """

        self._state = state

    @abc.abstractmethod
    def goal_test(self) -> bool:
        """:returns: True if current state is the goal, otherwise False."""

        pass

    @property
    def state(self) -> T_State:
        """:returns: Current state."""

        return self._state

    @classmethod
    @abc.abstractmethod
    def all_actions(cls) -> List[T_Action]:
        """:returns: List of all actions."""

        pass

    def actions(self) -> List[T_Action]:
        """:returns: List of actions applicable in the current state."""

        rv = []
        for action in self.all_actions():
            if self.can_invoke(action):
                rv.append(action)
        return rv

    @abc.abstractmethod
    def can_invoke(self, action: T_Action) -> bool:
        """Tests whether the action is applicable in the current state.

        :param action: Action to test.
        :returns: True if action is applicable in the current state,
        otherwise False.
        """

        pass

    @abc.abstractmethod
    def invoke(self, action: T_Action) -> 'Problem':
        """Invokes action.

        :param action: Action to invoke.
        :returns: Problem, which is transitioned to the new state.

        **Remarks:**

        This method does not alter the `self`. Instead, it returns modified
        problem.
        """

        pass

    @classmethod
    @abc.abstractmethod
    def initialize_goal(cls, **kwargs) -> 'Problem':
        """:returns: New problem, which is in the goal state."""

        pass

    @classmethod
    def initialize_random(cls, iterations: int = 100, **kwargs) -> 'Problem':
        """Initializes random problem.

        :param iterations: Number of iterations used to shuffle problem.
        :returns: New problem, which is not in the goal state.

        **Remarks:**

        This method at first initializes problem, which is in the goal state,
        and then it "shuffles" the problem for a specified number of
        iterations.
        """

        rv = cls.initialize_goal(**kwargs)
        action: T_Action = None
        while rv.goal_test():
            for _ in range(iterations):
                actions = rv.actions()
                action = cls._random_action(actions, action)
                rv = rv.invoke(action)
        return rv

    @classmethod
    def _random_action(
            cls,
            actions: List[T_Action],
            previous: Optional[T_Action],
    ) -> T_Action:
        # avoid cancelling previous action
        previous = previous and previous.opposite()
        while True:
            i = random.randint(0, len(actions) - 1)
            current = actions[i]
            if current != previous:
                return current
