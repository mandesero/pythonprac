#!/usr/bin/env python3

import cowsay as cs
import shlex
import asyncio
import threading
import locale
import gettext
import os
from typing import Optional, Tuple, TypeAlias, List
from time import sleep
from random import choice


# ===== Types =====
Name: TypeAlias = str
Address: TypeAlias = str
Coordinates: TypeAlias = List[int]
HP: TypeAlias = int
Hello: TypeAlias = str
MonsterMeta: TypeAlias = Tuple[Name, Hello, Coordinates]
ClientMeta: TypeAlias = Tuple[Name, Address, Coordinates]
Way: TypeAlias = str
# =================

popath = os.path.join(os.path.dirname(__file__), "po")
ENG = gettext.translation("server", popath, languages=["en"], fallback=True)
RU = gettext.translation("server", popath, languages=["ru"], fallback=True)

list_cows = cs.list_cows() + ["jgsbat"]
WEAPONS = {
    "sword": 10,
    "spear": 15,
    "axe": 20,
}


class Client:

    """
    A client object, representing a player in a multiplayer game. Each client has a name, address, hero object, and writer
    object for sending messages to other clients.

    Attributes:
        client_list: (dict) A class-level dictionary mapping client names to client objects.
    """

    client_list = {}

    def __init__(self, name: Name, addr: Address) -> None:
        """
        Initializes a new client with the given name, address, and hero object. Adds the client to the client list.

            :param name: (str) The name of the client.
            :param addr: (str) The address of the client.
        """
        self.name = name
        self.addr = addr
        self.pos = [0, 0]
        self.writer = None
        self.locale = ENG
        Client.client_list.update({name: self})

    @staticmethod
    def connect(name: Name, addr: Address) -> bool:
        """
        Static method that creates a new client and adds it to the client list with the given name and address.

            :param name: (str) The name of the client to be added.
            :param addr: (str) The address of the client to be added.
            :return: (bool) True if the client was successfully added to the client list, False otherwise.
        """

        if name in Client.client_list:
            return False

        Client(name, addr)
        return True

    @staticmethod
    def meta(name: Name) -> ClientMeta:
        """
        Static method that retrieves the client with the given name from the client list.

            :param name: (str) The name of the client to be retrieved.
            :return: (Client or None) The client object with the given name if it exists in the client list, or None otherwise.
        """

        if name in Client.client_list:
            tmp = Client.client_list[name]
            return tmp.name, tmp.addr, tmp.pos

        return tuple()

    @staticmethod
    def disconnect(name: Name) -> Tuple[bool, Name]:
        """
        Static method that removes the client with the given name from the client list.

            :param name: (str) The name of the client to be removed.
            :return: None
        """

        if name in Client.client_list:
            Client.client_list.pop(name)
            return True, name
        return False, name

    def __str__(self) -> str:
        """
        Returns a string representation of the client object.

            :return: (str) A string representation of the client object.
        """

        name = f"Name     : {self.name}"
        addr = f"Address  : {self.addr}"
        pos = f"Position : {self.pos}"

        return "\n".join((name, addr, pos)) + "\n"


class Monster:
    """
    A monster object, representing an enemy character in a multiplayer game.

    Attributes:
        monsters: (dict) - A class-level dictionary mapping monsters names to monsters objects.
    """

    monsters = {}

    def __init__(self, name: Name, msg: Hello, hp: HP, coords: Coordinates) -> None:
        """
        Initializes a new monster with the given name, greeting message, hitpoints, and coordinates.

        :param name: (str) The name of the monster.
        :param msg: (str) The greeting string that the monster outputs.
        :param hp: (int) The hitpoints of the monster.
        :param coords: (tuple) The coordinates of the monster on the field in the format (x, y).
        """
        self.name = name
        self.msg = msg
        self.hp = hp
        self.coords = coords
        Monster.monsters.update({name: self})

    @staticmethod
    def pop(name: Name) -> None:
        """
        Delete monster from monsters list

        :param name: (Name) - name of the monster
        :return: None
        """
        if name in Monster.monsters:
            Monster.monsters.pop(name)

    def meta(self) -> MonsterMeta:
        """
        Get meta of the monster

        :return: (MonsterMeta) - meta of the monster
        """
        return self.name, self.msg, self.coords


class Game:
    """
    Game class for MOOD.

    Attributes:
        ways (dict): dictionary of possible directions
        field (list): game field

    """

    field = [[None] * 10 for _ in range(10)]

    ways = {
        "up": (0, 1),
        "down": (0, -1),
        "right": (1, 0),
        "left": (-1, 0),
    }

    @staticmethod
    def add_monster(monster: Optional[Monster]) -> Tuple[MonsterMeta, bool]:
        """
        Adds monster to the game field

        :param monster: (Monster) monster instance
        :return: (Tuple[MonsterMeta, bool]) monster name, message and coordinates and replacing flag
        """

        i, j = monster.coords
        replace = False

        if Game.field[i][j]:
            replace = True

        Game.field[i][j] = monster

        return monster.meta(), replace

    @staticmethod
    def encounter(coords: Coordinates) -> MonsterMeta:
        """
        Checks if there is a monster at a specific location and returns monster message and name


        :param coords: (Coordinates) x and y coordinate
        :return: (MonsterMeta) monster name, message and coordinates
        """
        x, y = coords
        return Game.field[x][y].meta()

    @staticmethod
    def change_hero_pos(hero: Optional[Client], way: Way) -> str:
        """
        Changes hero's position on the field

        :param hero: (Client) player who wants to make move
        :param way: (str) direction of movement
        :return: (str) message regarding hero's movement and possible encounter with monster
        """

        x, y = Game.ways[way]

        i = hero.pos[0] = (x + hero.pos[0]) % 10
        j = hero.pos[1] = (y + hero.pos[1]) % 10

        if Game.field[i][j]:
            name, text, _ = Game.encounter((i, j))
            return i, j, "\n" + cs.cowsay(message=text, cow=name)

        return i, j, ""

    @staticmethod
    def attack(pos: Coordinates, name: Name, dmg: int) -> dict:
        """
        Carries out an attack on a monster at a specific location

        :param pos: (int, int) monster coordinates in the field
        :param name: (str) monster name
        :param dmg: (int) damage to be inflicted
        :return: (str, bool) message regarding the attack and boolean flag indicating whether the attack was carried out or not
        """
        data = {
            "here": True,
            "attack": False,
            "attack_name": name,
            "died": False,
        }

        x, y = pos
        if not Game.field[x][y]:
            data["here"] = False
            return data

        monster = Game.field[x][y]

        if monster.name != name:
            return data

        monster.hp -= dmg
        data["hp"] = monster.hp
        data["attack"] = True

        if monster.hp < 0:
            Game.field[x][y] = None
            Monster.pop(name)
            data["died"] = True
        return data


def monster_moving(delay: int) -> None:
    """
    Replace random monster every <delay> seconds.

    :param delay: (int) frequency of monster replacing
    :return: None
    """

    dangeon = Game.field
    monsters = Monster.monsters
    ways = Game.ways

    while True:
        if monsters:
            monster_name = choice(list(monsters))
            monster = monsters[monster_name]
            x, y = monster.coords
            move = choice(list(ways))
            _x, _y = ways[move][0], ways[move][1]
            new_x, new_y = (x + _x) % 10, (y + _y) % 10

            if not dangeon[new_x][new_y]:
                monster.coords = (new_x, new_y)
                dangeon[new_x][new_y] = monster
                dangeon[x][y] = None

                monster_name, text, *args = monster.meta()
                hello_msg = cs.cowsay(message=text, cow=monster_name)

                for clt_name, clt in Client.client_list.items():
                    clt.locale.install()
                    msg = _("{} moved one cell {}").format(monster_name, move)
                    clt.writer.write(msg.encode())

                    if clt.pos == list(monster.coords):
                        clt.writer.write(hello_msg.encode())
            else:
                continue
        sleep(delay)


async def start_server(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    """
    Get user connections

    :param reader: (asyncio.StreamReader) pipe to read
    :param writer: (asyncio.StreamWriter) pipe to write
    :return: None
    """
    host, port = writer.get_extra_info("peername")
    print(f"New connection from {host}:{port}")

    login = await reader.readline()
    login = login.decode().strip()

    # User doesn't connecting (login already used or other reason)
    if not Client.connect(login, f"{host}:{port}"):
        writer.write(f"User with login {login} already exists.\n".encode())
        print(f"Disconnect {host}:{port}")
        writer.close()
        await writer.wait_closed()
        return

    # object of client
    client = Client.client_list[login]
    client.writer = writer

    for name, clt in Client.client_list.items():
        if clt is client:
            writer.write(str(client).encode())
            await writer.drain()
        else:
            clt.locale.install()
            msg = _("New user:\nName: {}\nAddress: {}\n").format(
                login, f"{host}:{port}"
            )
            clt.writer.write(msg.encode())
            await clt.writer.drain()

    while not reader.at_eof():
        data = await reader.readline()
        msg = shlex.split(data.decode().strip())
        match msg:
            case ["move", direction]:
                new_x, new_y, monster_msg = Game.change_hero_pos(client, direction)
                client.locale.install()
                ans = _("Moved to ({}, {})").format(new_x, new_y)
                writer.write((ans + monster_msg).encode())
                await writer.drain()

            case ["addmon", *args]:
                try:
                    monster_name = args[0]
                    monster_msg = args[args.index("hello") + 1]
                    monster_hp = int(args[args.index("hp") + 1])
                    monster_coords = int(args[args.index("coords") + 1]), int(
                        args[args.index("coords") + 2]
                    )

                    new_monster = Monster(
                        monster_name, monster_msg, monster_hp, monster_coords
                    )

                    *tmp, replace = Game.add_monster(new_monster)

                    for name, clt in Client.client_list.items():
                        if clt is client:
                            client.locale.install()
                            ans = _("Added monster {} to {} saying {}").format(
                                monster_name, monster_coords, monster_msg
                            )
                            writer.write(ans.encode())
                        else:
                            clt.locale.install()
                            ans = _("{} added monster {} to {} saying {}").format(
                                client.name, monster_name, monster_coords, monster_msg
                            )
                            clt.writer.write(ans.encode())
                except:
                    pass

            case ["attack", *args]:
                data = Game.attack(client.pos, args[0], int(args[1]))
                if not data["here"]:
                    client.locale.install()
                    ans = _("No monster here")
                    writer.write(ans.encode())
                    await writer.drain()
                elif data["here"] and not data["attack"]:
                    client.locale.install()
                    ans = _("No {} here.").format(data["attack_name"])
                    writer.write(ans.encode())
                    await writer.drain()
                else:
                    for clt_name, clt in Client.client_list.items():
                        if clt is client:
                            client.locale.install()
                            if not data["died"]:
                                ans = _("{} now has {} hp").format(
                                    data["attack_name"], data["hp"]
                                )
                            else:
                                ans = _("{} died.").format(data["attack_name"])
                            writer.write(ans.encode())
                            await writer.drain()
                        else:
                            clt.locale.install()
                            if not data["died"]:
                                ans = _("{} attack {}.\n{} now has {} hp").format(
                                    client.name,
                                    data["attack_name"],
                                    data["attack_name"],
                                    data["hp"],
                                )
                            else:
                                ans = _("{} attack {}.\n{} died.").format(
                                    client.name,
                                    data["attack_name"],
                                    data["attack_name"],
                                )
                            clt.writer.write(ans.encode())
                            await clt.writer.drain()

            case ["sayall", *text]:
                for clt_name, clt in Client.client_list.items():
                    if not clt is client:
                        clt.writer.write(
                            (client.name + ": " + " ".join(text).strip()).encode()
                        )
                        await clt.writer.drain()

            case ["locale", loc]:
                if loc == "ru_RU.UTF8":
                    client.locale = RU
                else:
                    client.locale = ENG

                client.locale.install()
                ans = _("Set up locale: {}").format(loc)
                writer.write(ans.encode())
                await writer.drain()

            case ["quit"]:
                break

    for clt_name, clt in Client.client_list.items():
        if not clt is client:
            clt.locale.install()
            ans = _("{} disconnect.").format(login)
            clt.writer.write(ans.encode())
            await clt.writer.drain()

    Client.disconnect(login)
    print(f"Disconnect {host}:{port}")
    writer.close()
    await writer.wait_closed()


async def run_server() -> None:
    """
    Run server

    :return: None
    """
    thr = threading.Thread(target=monster_moving, args=(3000,))
    thr.start()
    server = await asyncio.start_server(start_server, "0.0.0.0", 1337)
    async with server:
        await server.serve_forever()


def run():
    asyncio.run(run_server())
