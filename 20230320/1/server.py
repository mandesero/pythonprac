#!/usr/bin/env python3

import cowsay as cs
import shlex
import asyncio
from collections import defaultdict

from defaults import WEAPONS


class Client:
    client_list = {}

    def __init__(self, name, addr):
        self.name = name
        self.addr = addr
        self.hero = None
        self.writer = None
        Client.client_list.update({name: self})

    @staticmethod
    def connect(name, addr):
        if name in Client.client_list:
            return False

        _ = Client(name, addr)
        return True

    @staticmethod
    def meta(name):
        if name in Client.client_list:
            return Client.client_list[name]

    @staticmethod
    def disconnect(name):
        if Client.meta(name):
            Client.client_list.pop(name)

    def __str__(self):
        return f"""
        Name: {self.name}
        Addr: {self.addr}
        Pos : {self.hero.pos}
        """

    def broadcast(self, msg):
        for _, obj in filter(lambda u: u[0] != self.name, Client.client_list.items()):
            obj.writer.write(msg)


list_cows = cs.list_cows() + ["jgsbat"]


class Hero:
    WEAPONS = WEAPONS

    def __init__(self):
        self.pos = [0, 0]


class Monster:
    def __init__(self, name, hello_string, hp, coords):
        self.name = name
        self.msg = hello_string
        self.hp = hp
        self.coords = coords


class Game:
    ways = {
        "up": (0, 1),
        "down": (0, -1),
        "right": (1, 0),
        "left": (-1, 0),
    }

    field = [[None] * 10 for _ in range(10)]

    def __init__(self, player):
        self.player = player

    def add_monster(self, monster):
        i, j = monster.coords
        msg = f"Added monster {monster.name} to {monster.coords} saying {monster.msg}."
        if self.field[i][j]:
            msg += "\nReplaced the old monster"

        self.field[i][j] = monster

        return msg

    def encounter(self, x, y):
        return self.field[x][y].msg, self.field[x][y].name

    def change_hero_pos(self, way):
        x, y = Game.ways[way]

        i = self.player.hero.pos[0] = (x + self.player.hero.pos[0]) % 10
        j = self.player.hero.pos[1] = (y + self.player.hero.pos[1]) % 10

        msg = f"Moved to ({i}, {j})"
        if self.field[i][j]:
            text, name = self.encounter(i, j)
            msg += cs.cowsay(message=text, cow=name)

        return msg

    def attack(self, pos, name, dmg):
        msg = "No monster here"
        i, j = pos
        flag = False
        if monster := self.field[i][j]:
            if monster.name == name:
                dmg = dmg if monster.hp > dmg else monster.hp
                monster.hp -= dmg

                msg = f"Attacked {monster.name}, damage {dmg} hp"

                if monster.hp == 0:
                    msg += f"\n{monster.name} died"
                    self.field[i][j] = None
                else:
                    msg += f"\n{monster.name} now has {monster.hp} hp"
                flag = True
            else:
                msg = f"No {name} here"

        return msg, flag


async def echo(reader, writer):
    host, port = writer.get_extra_info("peername")
    print(f"New connection from {host}:{port}")
    usr = await reader.readline()
    usr = usr.decode().strip()

    if not Client.connect(usr, f"{host}:{port}"):
        writer.write(f"User with login {usr} already exists.\n".encode())
        print(f"Disconnect {host}:{port}")
        writer.close()
        await writer.wait_closed()

    else:
        clt = Client.meta(usr)
        clt.hero = Hero()
        clt.writer = writer
        writer.write(str(Client.meta(usr)).encode())
        clt.broadcast(("\n New user:\n" + str(Client.meta(usr))).encode())

        dungeon = Game(clt)
        while not reader.at_eof():
            data = await reader.readline()
            msg = shlex.split(data.decode().strip())
            ans = ""
            print(msg)
            match msg:
                case way if len(way) == 1 and way[0] in Game.ways:
                    ans = dungeon.change_hero_pos(way[0])
                    writer.write(ans.encode())
                    await writer.drain()

                case ["addmon", *args]:
                    print("Addmon")
                    if len(args) == 8:
                        if args[0] in list_cows:
                            ans = dungeon.add_monster(
                                Monster(
                                    args[0],
                                    args[args.index("hello") + 1],
                                    int(args[args.index("hp") + 1]),
                                    (
                                        int(args[args.index("coords") + 1]),
                                        int(args[args.index("coords") + 2]),
                                    ),
                                )
                            )
                            print(ans)
                            clt.broadcast((clt.name + ": " + ans).encode())

                case ["attack", *args]:
                    print("Attack")
                    ans = dungeon.attack(clt.hero.pos, args[0], int(args[1]))
                    print(ans)
                    if ans[1]:
                        clt.broadcast((clt.name + ": " + ans[0]).encode())
                    else:
                        writer.write(ans[0].encode())
                        await writer.drain()

                case ["quit"]:
                    break

                case _:
                    ans = "Error"

        clt.broadcast(("Dissconnect:\n" + str(clt)).encode())
        writer.write("Goodbye".encode())
        Client.disconnect(usr)
        writer.close()
        await writer.wait_closed()


async def main():
    server = await asyncio.start_server(echo, "0.0.0.0", 1338)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
