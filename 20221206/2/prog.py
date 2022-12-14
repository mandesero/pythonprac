import asyncio
import sys
from copy import copy
import random


async def merge(A, B, start, middle, finnish, event_in1, event_in2, event_out):
    await event_in1.wait()
    await event_in2.wait()

    tmp = copy(A)
    t1, t2 = start, middle

    for i in range(start, finnish):

        if t1 == middle:
            B[i:finnish] = tmp[t2:finnish]
            break

        if t2 == finnish:
            B[i:finnish] = tmp[t1:middle]
            break

        if tmp[t1] < tmp[t2]:
            B[i] = tmp[t1]
            t1 += 1
        else:
            B[i] = tmp[t2]
            t2 += 1

    event_out.set()


async def mtasks(A):
    result = copy(A)
    def foo(i, j, event, tasks=[]):
        if -1 <= i - j <= 1:
            event.set()
            return

        event_in1, event_in2 = asyncio.Event(), asyncio.Event()
        task = asyncio.create_task(
            merge(
                result, result,
                i, (i + j) // 2, j,
                event_in1, event_in2, event
            )
        )
        tasks.append(task)

        foo(i, (i + j) // 2, event_in1)
        foo((i + j) // 2, j, event_in2)
        return tasks

    return foo(0, len(result), asyncio.Event()), result


if __name__ == '__main__':
    exec(sys.stdin.read())
