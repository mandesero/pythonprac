#!/usr/bin/env python3
import asyncio
import cowsay as cs
import shlex as sx

conn_users = {}
clients = {}

list_cows = cs.list_cows()


def is_login_allow(login):
    return login in list_cows


async def cow_chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info("peername"))
    print(me)
    conn_users[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(conn_users[me].get())

    while not reader.at_eof():
        done, pending = await asyncio.wait(
            [send, receive], return_when=asyncio.FIRST_COMPLETED
        )
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())

                text = q.result().decode().strip()
                command = sx.split(text)
                match command:
                    case ["login", login]:
                        if me not in clients:
                            if is_login_allow(login):
                                if login in [clients[usr][0] for usr in clients]:
                                    await conn_users[me].put(
                                        f"::: Login {login} is already use."
                                    )
                                    break

                                clients[me] = login, me
                                await conn_users[me].put(
                                    f"::: Succsess login with {login}."
                                )
                            else:
                                await conn_users[me].put(
                                    f"::: Invalid username {login}."
                                )
                        else:
                            await conn_users[me].put(
                                f"::: You are already logged in with the username: {clients[me][0]}."
                            )

                    case args:
                        if me not in clients and args != ["cows"]:
                            await conn_users[me].put(
                                "::: You are an unauthorized user (login <name> to log in)."
                            )
                            break

                        match args:
                            case ["who"]:
                                await conn_users[me].put(
                                    "Auth users: "
                                    + ", ".join([clients[usr][0] for usr in clients])
                                )
                            case ["cows"]:
                                await conn_users[me].put(
                                    "Free logins: "
                                    + ", ".join(
                                        set(cs.list_cows())
                                        - set([clients[usr][0] for usr in clients])
                                    )
                                )

                            case ["say", login, *text]:
                                if login not in [clients[usr][0] for usr in clients]:
                                    await conn_users[me].put(
                                        f"User with this name {login} does not exist."
                                    )
                                else:
                                    message = cs.cowsay(
                                        message=" ".join(text), cow=clients[me][0]
                                    )
                                    for out in clients.values():
                                        if out[0] == login:
                                            await conn_users[out[1]].put(
                                                f"Private message from {clients[me][0]}:\n{message}"
                                            )
                                            break

                            case ["yield", *text]:
                                message = cs.cowsay(
                                    message=" ".join(text), cow=clients[me][0]
                                )
                                for out in clients.values():
                                    if conn_users[out[1]] is not conn_users[me]:
                                        await conn_users[out[1]].put(
                                            f"{clients[me][0]}:\n{message}"
                                        )

                            case ["quit"]:
                                send.cancel()
                                receive.cancel()
                                print(me, "DONE")
                                del clients[me]
                                del conn_users[me]
                                writer.close()
                                await writer.wait_closed()
                                return

            elif q is receive:
                receive = asyncio.create_task(conn_users[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()

    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del conn_users[me]
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(cow_chat, "0.0.0.0", 1337)
    async with server:
        await server.serve_forever()


asyncio.run(main())
