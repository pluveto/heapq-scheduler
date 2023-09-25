import logging
from typing import Callable, List, Optional, Protocol, TypedDict


class JobDescrition(TypedDict):
    fn: Callable[[], None]
    interval: float  # seconds
    run_immediately: bool
