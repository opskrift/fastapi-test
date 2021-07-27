def work_fn(xs, model):
    # logger bound with current request's details
    logger = get_logger()

    # do work
    out = model(xs)
    logger.info(...)  # log extra info

    return out


g_is_worker_initialized = False


@get("/path")
def _(foo: int, xs: List[int]) -> Tuple[str, List[int]]:

    # TODO: this extra init is what we want to avoid
    # handle before-first-request
    global g_is_worker_initialized, logger
    if not g_is_worker_initialized:
        resource_manager.model.load_state()
        logger = (
            setup_logging()
        )  # NOTE: can log to the same file from multiple processes

        g_is_worker_initialized = True
    # done before-first-request

    uid = uuid()

    logger = get_logger()
    logger.bind(**request_details)
    # NOTE for structlog: use {clear,bind}_threadlocal to bind request-specific data

    # `work_fn` will use the bound logger
    recs = work_fn(xs, resource_manager.model)

    return (uid, recs)

def setup_logging():
    logger = ...  # log to file

    return logger

# Ideally, we'd have something like
@on_startup(...)
def init(...):
    setup_logging()
    ...


# if running as a service (i.e. not imported by other means)
# NOTE for uWSGI: __name__.startswith("uwsgi_file")
if __name__ == "<something special>":

    # This is only loaded in the parent process.
    # After fork, worker processes will inherit it -- globally available.
    resource_manager = ResourceManager()
    resource_manager.install("rec_dict", pickle_load("/path/to/rec_dict.pkl"))
    resource_manager.install("model", load_model(...))

    # at this point, N fork()s happen -- spawning each worker.
