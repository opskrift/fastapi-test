import numpy as np
import pickle
import time
import os


xs = {k: list(range(k + 1)) for k in range(1000)}


pid = os.fork()

print(os.getpid())

if pid == 0:
    print("Child", hex(id(xs)), len(xs))
    time.sleep(10)
    print("Child does COW")
    time.sleep(5)
    xs[0] = [v + 1 for v in xs[0]]
    print("Child", hex(id(xs)), len(xs))

else:
    print("Parent", hex(id(xs)), len(xs))
    time.sleep(60)
    os.waitpid(pid, 0)
