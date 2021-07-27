import logging
import os
import uuid

import hug
import structlog

"""
Using a thread-local storage for request-wide context.
"""


IS_FIRST = True


@hug.get("/hello")
def _(foo: hug.types.text, bar: hug.types.text):
    global IS_FIRST, logger
    if IS_FIRST:
        logger = configure_logger()
        IS_FIRST = False

    # You would put this into some kind of middleware or processor so it's set
    # automatically for all requests in all views.
    structlog.threadlocal.clear_threadlocal()
    structlog.threadlocal.bind_threadlocal(
        worker=os.getpid(),
        request_id=uuid.uuid4().hex[:4],
        foo=foo,
        bar=bar,
    )
    # End of belongs-to-middleware.

    log = logger.bind()

    out = result(foo, bar)
    log.info(f"Worker {os.getpid()} doing work...", out=out)

    return f"DONE {os.getpid()}"


def result(x, y):
    """
    This uses the thread-local binding information defined in the main handler.
    Notice that there's no need to pass the logger object or a log prefix.
    """
    log = structlog.get_logger()
    log.info(f"working {x} + {y}")
    return x + y


def configure_logger():
    logging.basicConfig(
        format="%(message)s",
        filename=f"log_{os.getpid()}.txt",
        filemode="a",
        level=logging.DEBUG,
        force=True,
    )
    # TODO: dump one JSON per line
    structlog.configure(
        processors=[
            structlog.threadlocal.merge_threadlocal,  # <--!!!
            structlog.processors.JSONRenderer(indent=2, sort_keys=False),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
    )

    return structlog.get_logger()


def post_fork(*args, **kwargs):
    print("POSTFORKING")


if __name__.startswith("uwsgi_file"):
    logger = configure_logger()

    print(f"\nHello from {os.getpid()}\n")
