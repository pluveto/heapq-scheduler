# Scheduler

> A Python library for scheduling tasks at specific intervals.

[![Python CI](https://github.com/MichaelCurrin/py-project-template/actions/workflows/main.yml/badge.svg)](https://github.com/MichaelCurrin/py-project-template/actions/workflows/main.yml)
[![GitHub tag](https://img.shields.io/github/tag/MichaelCurrin/py-project-template?include_prereleases=&sort=semver)](https://github.com/MichaelCurrin/py-project-template/releases/)
[![License](https://img.shields.io/badge/License-MIT-blue)](#license)

[![Made with Python](https://img.shields.io/badge/Python->=3.6-blue?logo=python&logoColor=white)](https://python.org "Go to Python website")

## Purpose

In many situations the number of threads that can be used to run tasks is limited. For example, on embbded devices or in a web server. So if we can use only one thread, how can we schedule tasks to run at specific intervals?

The purpose of this library is to provide a lightweight and convenient way to schedule tasks to run at specific intervals. It can be used in various scenarios where you need to automate repetitive tasks or perform actions periodically. And all tasks are run in a single thread.

## Features

- Schedule tasks to run at specific intervals.
- Option to run a task immediately upon scheduling.
- Specify the number of times a task should run before stopping.
- Ability to cancel scheduled tasks.
- Lightweight and easy to use.
- Use new thread to run tasks, or run in the current thread.

## Example usage

```python
from heapq_scheduler.heapq_scheduler import Scheduler

def task():
    print("Running task...")

scheduler = Scheduler()
scheduler.schedule(task, period=5, immediately=True, life=10)
scheduler.start()
scheduler.join()
```

## Documentation

> How to install and run this project

[![view - Documentation](https://img.shields.io/badge/view-Documentation-blue?style=for-the-badge)](https://michaelcurrin.github.io/py-project-template/)

## Installation

To install the Scheduler library, run the following command:

```shell
pip install heapq_scheduler
```

### Requirements

The Scheduler library requires Python 3.6 or higher.

## Usage

To use the Scheduler library in your project, follow these steps:

1. Import the `Scheduler` class from the `scheduler` module.
2. Create an instance of the `Scheduler` class.
3. Define a function that represents the task you want to schedule.
4. Use the `schedule` method of the `Scheduler` instance to schedule the task.
5. Optionally, start the scheduler using the `start` method.
6. Optionally, join the scheduler using the `join` method to wait for it to finish.

Here is an example:

```python
from scheduler import Scheduler

def task():
    print("Running task...")

scheduler = Scheduler()
scheduler.schedule(task, period=5, immediately=True, life=10)
scheduler.start()
scheduler.join()
```

## Development

To contribute to the development of the Scheduler library, follow these steps:

1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Submit a pull request.

## License

Released under the [MIT](/LICENSE) license by [Your Name](https://github.com/your-username)
