#!/usr/bin/env python3


import asyncio
from sqroots import sqroots


async def echo(reader, writer):
    while data := await reader.readline():
        try:
            res = sqroots(data) + "\n"
        except:
            res = "\n"
        writer.write(res.encode())

    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(echo, "0.0.0.0", 1337)
    async with server:
        await server.serve_forever()


def serve():
    asyncio.run(main())


if __name__ == "__main __":
    serve()
