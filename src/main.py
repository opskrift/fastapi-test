import os
from fastapi import FastAPI
import pickle
import time

from resource_manager import ResourceManager

app = FastAPI()

resource_manager = ResourceManager()


@app.on_event("startup")
async def startup_event():
    # TODO: can this be called only once, by the master process,
    #   so that the workers make use of CoW after fork()?

    # TODO: expose loaded resources

    print(f"I am worker {os.getpid()} starting up...")

    with open("data/in.npy", "rb") as fp:
        xs = pickle.load(fp)
        print(f"Worker {os.getpid()} loaded {hex(id(xs))} on {__name__}.")

    resource_manager.install("xs", xs)


@app.get("/hello")
async def root():
    return {
        "message": "Hello World",
        "name": __name__,
        "pid": os.getpid(),
        "id(xs)": hex(id(resource_manager.xs)),
    }


"""
- when running with uvicorn, __name__ == <filename>(.py) (not the default __main__)
"""
