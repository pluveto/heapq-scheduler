"""
Test scheduler module.
"""
import time
import unittest
from typing import Callable
from unittest import mock

from heapq_scheduler.heapq_scheduler import Scheduler


class Test(unittest.TestCase):
    def setUp(self):
        self.scheduler = Scheduler()

    def tearDown(self):
        ...

    def test_schedule(self):
        counter1 = 0
        counter2 = 0

        def fn1():
            nonlocal counter1
            counter1 += 1

        def fn2():
            nonlocal counter2
            counter2 += 1

        self.scheduler.schedule(fn1, 1, True)
        self.scheduler.schedule(fn2, 2, True)
        self.scheduler.start()
        time_start = time.time()
        time_end = 0

        time.sleep(4.8)

        def on_stop():
            nonlocal time_end
            time_end = time.time()

        self.scheduler.stop(on_stop)
        self.scheduler.join()

        # time     counter1 counter2
        # 0        1        1
        # 1        2        1
        # 2        3        2
        # 3        4        2
        # 4        5        3

        self.assertTrue(time_end - time_start > 4.8)
        self.assertTrue(time_end - time_start < 5.2)
        self.assertEqual(counter1, 5)
        self.assertEqual(counter2, 3)

    def test_cancel(self):
        counter1 = 0

        def fn1():
            nonlocal counter1
            counter1 += 1

        self.scheduler.schedule(fn1, 1, True)
        self.scheduler.start()

        time.sleep(0.5)
        # now counter1 == 1
        self.scheduler.cancel(fn1)
        self.scheduler.stop()
        self.scheduler.join()

        self.assertEqual(counter1, 1)

    def test_reschedule(self):
        # we have two state
        # state1: freq = 10, run for 1 second
        # state2: freq = 1, run for 3 second
        # they transition from one to another for 2 round

        round = 0
        state = 1
        counter1 = 0
        counter2 = 0

        print("\nround", "state", "counter1", "counter2", sep="\t")

        def fn():
            nonlocal round, state
            nonlocal counter1, counter2

            print(
                round,
                state,
                counter1,
                counter2,
                sep="\t",
            )
            if round == 2:
                self.scheduler.stop()
                return

            def schedule_next(task: Callable):
                nonlocal state
                if state == 1:
                    freq = 10
                else:
                    freq = 1
                print("next freq = ", freq)
                self.scheduler.schedule(task, 1.0 / freq, True)

            if state == 1:
                counter1 += 1
                if counter1 == 10:
                    counter1 = 0
                    state = 2
                    self.scheduler.cancel(fn, on_cancelled=schedule_next)
                    return

            if state == 2:
                counter2 += 1
                if counter2 == 3:
                    counter2 = 0
                    state = 1
                    round += 1
                    self.scheduler.cancel(fn, on_cancelled=schedule_next)
                    return

        self.scheduler.schedule(fn, 1 / 10, True)
        self.scheduler.start()
        self.scheduler.join()

        self.assertEqual(round, 2)
        self.assertEqual(state, 1)
        self.assertEqual(counter1, 0)
        self.assertEqual(counter2, 0)

    def test_restart(self):
        fn1 = mock.MagicMock()
        fn2 = mock.MagicMock()

        self.scheduler.schedule(fn1, 1, False)
        self.scheduler.schedule(fn2, 2, True)

        self.scheduler.start()
        time.sleep(0.5)
        self.scheduler.cancel(fn1)
        time.sleep(0.5)
        self.scheduler.stop()
        self.scheduler.join()

        fn1.assert_not_called()

        fn2.assert_called_once()

        fn1.reset_mock()
        fn2.reset_mock()

        self.scheduler.start()
        time.sleep(0.5)  # fn2 called
        self.scheduler.cancel(fn2)
        time.sleep(0.5)
        self.scheduler.stop()

        fn1.assert_not_called()

        fn2.assert_called_once()


if __name__ == "__main__":
    import pytest

    pytest.main()
