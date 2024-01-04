import sys

if sys.version_info >= (3, 10):  # pragma: no cover
    from typing import ParamSpec
else:  # pragma: no cover
    from typing_extensions import ParamSpec

from typing import Any, Callable, Sequence, Union

import anyio
from typing_extensions import Annotated, Doc

from backgrounder._internal import Repr
from backgrounder.concurrency import enforce_async_callable

P = ParamSpec("P")


class Task(Repr):
    """
    `Task` as a single instance can be easily achieved.

    **Example**

    ```python
    from backgrounder import Task

    async def send_email_notification(message: str):
        '''
        Sends an email notification
        '''
        send_notification(message)

    task = Task(send_email_notification, "message to someone")
    ```
    """

    __slots__ = ("func", "args", "kwargs")

    def __init__(
        self,
        func: Annotated[
            Callable[P, Any],
            Doc(
                """
                Any callable to be executed by in the background.
                This can be `async def` of normal blocking `def`.

                **Example**

                ```python
                from backgrounder import Task

                # For blocking callables
                def send_notification(message: str) -> None:
                    ...

                task = Task(send_notification, "A notification")
                await task()

                # For async callables
                async def send_notification(message: str) -> None:
                    ...

                task = Task(send_notification, "A notification")
                await task()
                ```
                """
            ),
        ],
        *args: Annotated[
            Any,
            Doc(
                """
                Any arguments of the callable.

                **Example**

                ```python
                from backgrounder import Task

                # For blocking callables
                def send_notification(message: str, email: str) -> None:
                    ...

                task = Task(send_notification, "A notification", "user@example.com")

                # For async callables
                async def send_notification(message: str, email: str) -> None:
                    ...

                task = Task(send_notification, "A notification", "user@example.com")
                ```
                """
            ),
        ],
        **kwargs: Annotated[
            Any,
            Doc(
                """
                Any kwyword arguments of the callable.

                **Example**

                ```python
                from typing import Any

                from backgrounder import Task

                data = {"message": "A notification", "email": "user@example.com"}

                # For blocking callables
                def send_notification(**kwargs: Any) -> None:
                    message = kwargs.pop("message", None)
                    email = kwargs.pop("email", None)

                task = Task(send_notification, **data)

                # For async callables
                async def send_notification(**kwargs: Any) -> None:
                    message = kwargs.pop("message", None)
                    email = kwargs.pop("email", None)

                task = Task(send_notification, **data)
                ```
                """
            ),
        ],
    ) -> None:
        self.func = enforce_async_callable(func)
        self.args = args
        self.kwargs = kwargs

    async def __call__(self) -> None:
        await self.func(*self.args, **self.kwargs)


class Tasks(Task):
    """
    Alternatively, the `Tasks` can also be used to be passed
    in.

    **Example**

    ```python
    from datetime import datetime

    from backgrounder import Task, Tasks

    async def send_email_notification(message: str):
        '''
        Sends an email notification
        '''
        send_notification(message)


    def write_in_file():
        with open("log.txt", mode="w") as log:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content = f"Notification sent @ {now}"
            log.write(content)

    tasks = Tasks([
        Task(send_email_notification, message="Account created"),
        Task(write_in_file),
    ])

    await tasks()
    ```

    When `as_group` is set to True, it will run all the tasks concurrently (as a group)

    **Example**

    ```python
    from datetime import datetime

    from backgrounder import Task, Tasks

    async def send_email_notification(message: str):
        '''
        Sends an email notification
        '''
        send_notification(message)


    def write_in_file():
        with open("log.txt", mode="w") as log:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content = f"Notification sent @ {now}"
            log.write(content)

    tasks = Tasks([
        Task(send_email_notification, message="Account created"),
        Task(write_in_file),
    ], as_group=True)

    await tasks()
    ```
    """

    __slots__ = ("tasks", "as_group")

    def __init__(
        self,
        tasks: Annotated[
            Union[Sequence[Task], None],
            Doc(
                """
                A `list` of [tasks](#tasks) to run execute.

                **Example**

                ```python
                from datetime import datetime

                from backgrounder import Task, Tasks

                async def send_email_notification(message: str):
                    '''
                    Sends an email notification
                    '''
                    send_notification(message)


                def write_in_file():
                    with open("log.txt", mode="w") as log:
                        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        content = f"Notification sent @ {now}"
                        log.write(content)

                tasks = Tasks([
                    Task(send_email_notification, message="Account created"),
                    Task(write_in_file),
                ])

                await tasks()
                ```
                """
            ),
        ] = None,
        as_group: Annotated[
            bool,
            Doc(
                """
                Boolean flag indicating if the tasks should be run concurrently, in other
                words, as a group.

                **Example**

                ```python
                from datetime import datetime

                from backgrounder import Task, Tasks

                async def send_email_notification(message: str):
                    '''
                    Sends an email notification
                    '''
                    send_notification(message)


                def write_in_file():
                    with open("log.txt", mode="w") as log:
                        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        content = f"Notification sent @ {now}"
                        log.write(content)

                tasks = Tasks([
                    Task(send_email_notification, message="Account created"),
                    Task(write_in_file),
                ], as_group=True)

                await tasks()
                ```
                """
            ),
        ] = False,
    ):
        self.tasks = list(tasks) if tasks else []
        self.as_group = as_group

    def add_task(self, func: Callable[P, Any], *args: P.args, **kwargs: P.kwargs) -> None:
        """
        Another way of adding tasks to the `Tasks` object.

        **Example**

        ```python
        from datetime import datetime

        from backgrounder import Task, Tasks

        async def send_email_notification(message: str):
            '''
            Sends an email notification
            '''
            send_notification(message)


        def write_in_file():
            with open("log.txt", mode="w") as log:
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                content = f"Notification sent @ {now}"
                log.write(content)

        tasks = Tasks()
        tasks.add_task(send_email_notification, message="Account created")
        tasks.add_task(write_in_file)

        await tasks()
        ```

        Or if you want to run them concurrently.

        **Example**

        ```python
        from datetime import datetime

        from backgrounder import Task, Tasks

        async def send_email_notification(message: str):
            '''
            Sends an email notification
            '''
            send_notification(message)


        def write_in_file():
            with open("log.txt", mode="w") as log:
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                content = f"Notification sent @ {now}"
                log.write(content)

        tasks = Tasks(as_group=True)
        tasks.add_task(send_email_notification, message="Account created")
        tasks.add_task(write_in_file)

        await tasks()
        ```
        """
        task = Task(func, *args, **kwargs)
        self.tasks.append(task)

    async def run_single(self) -> None:
        for task in self.tasks:
            await task()

    async def run_as_group(self) -> None:
        async with anyio.create_task_group() as group:
            for task in self.tasks:
                group.start_soon(task)

    async def __call__(self) -> None:
        if not self.as_group:
            await self.run_single()
        else:
            await self.run_as_group()
