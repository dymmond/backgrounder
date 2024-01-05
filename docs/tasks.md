# Tasks

Like Starlette and any other Starlette based frameworks, in Esmerald you can define background
tasks to run **after** the returning response.

You can use the [Task](#task) and [Task](#tasks) with any ASGI framework as if it was native.

This can be useful for those operations that need to happen after the request without blocking the
client (the client doesn't have to wait to complete) from receiving that same response.

Also you can simply run them as non-blocking operations without relying on any ASGI framework,
simple Python background tasks.

::: backgrounder.Task

::: backgrounder.Tasks
    options:
        members:
            - add_task
