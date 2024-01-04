# Backgrounder

<p align="center">
  <a href="https://backgrounder.dymmond.com"><img src="https://res.cloudinary.com/dymmond/image/upload/v1704377775/backgrounder/logo-ext_iwwiw1.png" alt='Backgrounder'></a>
</p>

<p align="center">
    <em>🚀 Run background tasks in async mode in any application. 🚀</em>
</p>

<p align="center">
<a href="https://github.com/dymmond/backgrounder/actions/workflows/test-suite.yml/badge.svg?event=push&branch=main" target="_blank">
    <img src="https://github.com/dymmond/backgrounder/actions/workflows/test-suite.yml/badge.svg?event=push&branch=main" alt="Test Suite">
</a>

<a href="https://pypi.org/project/backgrounder" target="_blank">
    <img src="https://img.shields.io/pypi/v/backgrounder?color=%2334D058&label=pypi%20package" alt="Package version">
</a>

<a href="https://pypi.org/project/backgrounder" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/backgrounder.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Documentation**: [https://backgrounder.dymmond.com](https://www.backgrounder.dymmond.com) 📚

**Source Code**: [https://github.com/dymmond/backgrounder](https://github.com/dymmond/backgrounder)

**The official supported version is always the latest released**.

---

## Motivation

Running background tasks nowadays is a must and not a nice to have and some of the the greatest
frameworks out there implement this functionality as part of the ASGI reference.

[Esmerald][esmerald], [FastAPI][fastapi] and [Starlette][starlette] by design implement the background
tasks for you and those are great functionailties to have but what if you want to use background
tasks without any of these frameworks? What if you simply want to have something that simply
runs background tasks regardless of the framework you are using *if you are using one at all**?

Well, this is where **backgrounder** comes to play and help you.

## Compatibility

This package is 100% compatible with any ASGI framework that implements or wants to implement
background tasks, which means you can even use it with [Esmerald][esmerald], [FastAPI][fastapi] or [Starlette][starlette]
without using the native version of each framework but **also allows** to run this inside anything else
like **Django** for example.

## How to use it

This package is actually very simple to use it, really, there is no rocket science since the
library handles a lot of the magic for you.

For the purposes of these examples, we will be using [Esmerald][esmerald] since it belongs to the
same ecosystem but feel free to use with anything you want.

### Using the backgrounder instead of default from the framework

As mentioned before, usually the ASGI frameworks like **Esmerald** come with a default background
task option but let us assume you want to use **backgrounder** instead how it would look like.

```python
from esmerald.responses import Response, get

from backgrounder.tasks import Task, Tasks


def set_values(values_to_add) -> None:
    for value in values_to_add:
        values.add(value)


tasks = Tasks(
    [
        Task(set_values, ["a", "b", "c", "h"]),
        Task(set_values, values_to_add=["d", "e", "f", "g"]),
    ],
    as_group=True,
)


@get(background=tasks)
async def home() -> Response:
    return Response("Task started", media_type="text/plain")
```

Simple, right? Internally Esmerald or any other framework will handle the process of the background
tasks for you and instead of using the native library, we simply pass the `Tasks` object from
the **backgrounder** and it should be it.

### Using as independent async object in any application

Well, here it is where the things become interesting. What if you want to run the tasks outside
of the response of a framework? Or if you want to run without a framework at all?

Well you can use the [Task](./tasks.md#task) directly. Something like this

```python
from backgrounder import Task

async def send_notification(email: str):
    """
    Sends an email notification to a given email
    """
    ...


task = Task(send_notification, "user@example.com")
await task()
```

This will make sure your task will always run in `async` mode and therefore, not blocking and
taking advantage of the asynchronous functionality from Python.

You can also define `blocking` functions. **Backgrounder** will make sure it will always run them
in `async` for you.

```python
from backgrounder import Task

def send_notification(email: str):
    """
    Sends an email notification to a given email
    """
    ...


task = Task(send_notification, "user@example.com")
await task()
```

This can be particularly useful if you want to implement some asynchronous functionality in your
applications without using a whole ASGI framework for it, for example, using **Django**, although
now also supporting `async` natively, you might want to run some background tasks there that basically
do not exist natively (by the time of the writting).

### The decorator

**Backgrounder** also offers a decorator for you to use which can be extremely useful if you don't
want to use the [Task](./tasks.md#task) object directly, providing a cleaner version out of the box.


```python
from backgrounder import background

@background
def send_notification(email: str):
    """
    Sends an email notification to a given email
    """
    ...


send_notification("user@example.com")
```

As simple as this, this will automatically execute the task in the background for you with all
the `async` magic being provided.

[starlette]: https://www.starlette.io
[esmerald]: https://esmerald.dev
[fastapi]: https://fastapi.tiangolo.com
