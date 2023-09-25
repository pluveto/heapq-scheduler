import heapq
import logging
import threading
import time
from typing import Callable, Dict, Optional, Tuple, cast

from heapq_scheduler.scheduler_protocol import SchedulerProtocol


_TaskFn = Callable[[], None]
_TaskCallback = Callable[[_TaskFn], None]
_QueueItemTuple = Tuple[float, int, _TaskFn, float, int]

_off_next_run = 0
_off_fn = 2
_off_period = 3
_off_life = 4


class _QueueItem:
    next_run: float
    fn_id: int
    fn: _TaskFn
    period: float
    life: int

    def __init__(self, next_run: float, fn: _TaskFn, period: float, life: int) -> None:
        self.next_run = next_run
        self.fn_id = id(fn)
        self.fn = fn
        self.period = period
        self.life = life

    def to_tuple(self) -> _QueueItemTuple:
        return (self.next_run, self.fn_id, self.fn, self.period, self.life)

    @classmethod
    def from_tuple(cls, tup: _QueueItemTuple) -> "_QueueItem":
        item = cls(
            tup[_off_next_run], tup[_off_fn], tup[_off_period], tup[_off_life]  # type: ignore
        )

        return item

    def __str__(self) -> str:
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.next_run))
        return f"_QueueItem(next_run='{time_str}', period={self.period}, fn_id={self.fn_id})"


class Scheduler(SchedulerProtocol):
    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        auto_stop: bool = False,
    ) -> None:
        # self._pending: List[Tuple[_Task, float]] = []
        self._heapq = []
        self._cancel_mark: Dict[_TaskFn, Optional[_TaskCallback]] = {}
        self._stop: Optional[Callable[[], None]] = None
        self._thread: Optional[threading.Thread] = None
        self._auto_stop = auto_stop

    def schedule(
        self,
        fn: Callable[[], None],
        period: float,
        immidiately: bool = False,
        life: int = -1,
    ) -> None:
        ts = time.time()
        next_run = ts if immidiately else ts + period
        item = _QueueItem(next_run, fn, period, life)
        self._schedule(item)

    def _schedule(self, item: _QueueItem) -> None:
        """Schedule for next run."""
        # task = item.fn
        # if task in self._cancel_mark:
        #     callback = self._cancel_mark[cast(_Task, task)]
        #     if callback is not None:
        #         callback(task)
        #     del self._cancel_mark[task]
        #     return
        heapq.heappush(self._heapq, item.to_tuple())

    def cancel(
        self, fn: Callable[[], None], on_cancelled: Optional[_TaskCallback] = None
    ) -> None:
        def default_callback(task: _TaskFn) -> None:
            pass

        self._logger.debug(f"set cancel {fn}")
        self._cancel_mark[fn] = on_cancelled or default_callback

    def start(self) -> None:
        if self._thread is not None:
            return
        thread = threading.Thread(target=self.run, daemon=True)
        self._thread = thread
        thread.start()

    def join(self) -> None:
        if self._thread is not None:
            cast(threading.Thread, self._thread).join()

    def stop(self, callback: Optional[Callable[[], None]] = None) -> None:
        if self._stop is not None:
            return

        def default_callback() -> None:
            pass

        self._logger.debug("set stop")
        self._stop = callback or default_callback

    def _next(self) -> _QueueItemTuple:
        assert self._heapq
        return heapq.heappop(self._heapq)

    def _before_iteration(self, exit_mark: Dict[str, bool]) -> bool:
        if self._stop is not None:
            cast(Callable, self._stop)()
            self._stop = None
            exit_mark["stop"] = True
            return False

        if not self._heapq and not self._auto_stop:
            time.sleep(0.1)
            return False

        return True

    def _before_call(self, item: _QueueItem) -> bool:
        if item.fn in self._cancel_mark:
            callback = self._cancel_mark[cast(_TaskFn, item.fn)]
            if callback is not None:
                callback(item.fn)
            del self._cancel_mark[item.fn]
            return False

        self._logger.debug(f"to call {item}")
        dt = item.next_run - time.time()
        if dt > 0:
            self._schedule(item)
            time.sleep(dt)
            return False

        return True

    def _before_schedule(self, item: _QueueItem) -> bool:
        if item.life > 0:
            item.life -= 1
            if item.life == 0:
                return False

        item.next_run += item.period
        return True

    def run(self) -> None:
        while self._heapq or not self._auto_stop:
            exit_mark = {
                "stop": False,
            }
            proceed = self._before_iteration(exit_mark)
            if not proceed:
                if exit_mark["stop"]:
                    break
                continue

            item = _QueueItem.from_tuple(self._next())

            if not self._before_call(item):
                continue

            item.fn()

            if not self._before_schedule(item):
                continue

            self._schedule(item)

            self._after_schedule()

    def _after_schedule(self) -> None:
        self._logger.debug("heapq:")
        for item in self._heapq:
            self._logger.debug(f"    {_QueueItem.from_tuple(item)}")
        self._logger.debug(f"cancel_mark: {self._cancel_mark}")
        self._logger.debug(f"stop: {self._stop}")
