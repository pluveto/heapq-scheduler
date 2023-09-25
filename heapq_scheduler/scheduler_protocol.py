from typing import Callable, Protocol


class SchedulerProtocol(Protocol):
    def schedule(
        self,
        fn: Callable[[], None],
        interval: float,
        run_immidiately: bool = False,
    ) -> None:
        ...

    def cancel(self, fn: Callable[[], None]) -> None:
        ...

    def start(self) -> None:
        ...

    def stop(self) -> None:
        ...

    def run(self) -> None:
        ...
