"""
Test foo module.
"""
from heapq_scheduler.foo import greet


def test_greet():
    assert greet() == "Hello, World"

    assert greet("Python dev") == "Hello, Python dev"
