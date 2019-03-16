import abc
import random
from typing import Generic, List, Optional, TypeVar

T_State = TypeVar('T_State')
T_Action = TypeVar('T_Action')


class Problem(Generic[T_State, T_Action]):
    def __init__(self, state: T_State):
        self._state = state

    @abc.abstractmethod
    def goal_test(self) -> bool:
        pass

    def state(self) -> T_State:
        return self._state

    @classmethod
    @abc.abstractmethod
    def all_actions(cls) -> List[T_Action]:
        pass

    def actions(self) -> List[T_Action]:
        rv = []
        for action in self.all_actions():
            if self.can_invoke(action):
                rv.append(action)
        return rv

    @abc.abstractmethod
    def can_invoke(self, action: T_Action) -> bool:
        pass

    @abc.abstractmethod
    def invoke(self, action: T_Action) -> 'Problem':
        pass

    @classmethod
    @abc.abstractmethod
    def initialize_goal(cls) -> 'Problem':
        pass

    @classmethod
    def initialize_random(cls, iterations: int = 100) -> 'Problem':
        rv = cls.initialize_goal()
        action: T_Action = None
        for _ in range(iterations):
            actions = rv.actions()
            action = cls._next_random_action(actions, action)
            rv = rv.invoke(action)
        return rv

    @classmethod
    def _next_random_action(
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
