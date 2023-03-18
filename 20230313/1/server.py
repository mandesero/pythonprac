import cowsay as cs
import shlex
import asyncio

from defaults import WEAPONS


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

    def __init__(self, hero):
        self.field = [[None] * 10 for _ in range(10)]
        self.hero = hero

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
        i = self.hero.pos[0] = (x + self.hero.pos[0]) % 10
        j = self.hero.pos[1] = (y + self.hero.pos[1]) % 10

        msg = [f"Moved to ({i}, {j})"]
        if self.field[i][j]:
            msg += self.encounter(i, j)

        return msg

    def attack(self, pos, name, dmg):
        msg = "No monster here"
        i, j = pos
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
            else:
                msg = f"No {name} here"

        return msg


async def echo(reader, writer):
    host, port = writer.get_extra_info("peername")
    player = Hero()
    dungeon = Game(player)

    while not reader.at_eof():
        data = await reader.readline()
        msg = shlex.split(data.decode().strip())
        ans = ""
        print(msg)
        match msg:
            case way if len(way) == 1 and way[0] in Game.ways:
                ans = "\n".join(dungeon.change_hero_pos(way[0]))

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

            case ["attack", *args]:
                print("Attack")
                ans = dungeon.attack(player.pos, args[0], int(args[1]))

            case ["Connect"]:
                ans = "<<< Welcome to Python-MUD 0.1 >>>"

            case _:
                ans = "Error"

        writer.write(ans.encode())
        await writer.drain()

    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(echo, "0.0.0.0", 1337)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
