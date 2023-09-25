from abc import abstractmethod
from typing import Callable, Optional, Protocol


_TaskFn = Callable[[], None]
_TaskCallback = Callable[[_TaskFn], None]


class SchedulerProtocol(Protocol):
    @abstractmethod
    def schedule(
        self,
        fn: _TaskFn,
        period: float,
        immidiately: bool = False,
        life: int = -1,
    ) -> None:
        ...

    @abstractmethod
    def cancel(self, fn: _TaskFn, on_cancelled: Optional[_TaskCallback] = None) -> None:
        ...

    @abstractmethod
    def start(self) -> None:
        ...

    @abstractmethod
    def join(self) -> None:
        ...

    @abstractmethod
    def stop(self, callback: Optional[_TaskFn] = None) -> None:
        ...

    @abstractmethod
    def run(self) -> None:
        ...
