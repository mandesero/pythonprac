import cowsay as cs
import shlex as sx
import cmd

from custom_monster import cust_mstr
from defaults import WEAPONS, COMPLETE


def complete(text, line, begidx, endidx):
    args = sx.split(line)

    match args:
        case ["attack"]:
            key, command = "", "attack"
        case ["attack", t]:
            if t == "with":
                key, command = "with", "attack"
            else:
                key, command = "", "attack"
        case ["attack", _, "with"]:
            key, command = "with", "attack"
        case ["attack", _, "with", _]:
            key, command = "with", "attack"

    return [s for s in COMPLETE[command][key] if s.startswith(text)]


class Game(cmd.Cmd):
    field = [[None] * 10 for i in range(10)]
    pos = [0, 0]

    def do_addmon(self, args):
        """
        Добавление монстра на поле.

        addmon <monster_name> hello <hello_string> hp <hitpoints> coords <x> <y>

        Параметры:
            <monster_name> : имя монстра (см. allow_monsters - список допустимых монстров);
            hello          : строка приветствие, которую выводит монстр;
            hp             : здоровье монстр;
            coords         : координаты монстра на поле;

        """

        command = sx.split(args)

        name = command[0]
        message = command[command.index("hello") + 1]
        hp = int(command[command.index("hp") + 1])
        x, y = (
            int(command[command.index("coords") + 1]),
            int(command[command.index("coords") + 2]),
        )

        if name not in (cs.list_cows() + ["jgsbat"]):
            print("Cannot add unknown monster")
            return

        flag = self.field[x][y] is None
        self.field[x][y] = [message, name, hp]
        print(
            f"Added monster {name} to ({x}, {y}) saying {sx.quote(message)} with hp {hp}"
        )
        if not flag:
            print("Replaced the old monster")

    def do_move(self, args):
        """
        Перемещение по полю.

        move [up|down|right|left]
        """

        way = sx.split(args)[0]
        match way:
            case "up":
                self.pos[1] = (self.pos[1] + 1) % 10
            case "down":
                self.pos[1] = (self.pos[1] - 1) % 10
            case "right":
                self.pos[0] = (self.pos[0] + 1) % 10
            case "left":
                self.pos[0] = (self.pos[0] - 1) % 10

        print(f"Moved to ({self.pos[0]}, {self.pos[1]})")
        self.onecmd(f"encounter {self.pos[0]} {self.pos[1]}")

    def do_encounter(self, args):
        x, y = list(map(int, sx.split(args)))
        if monster := self.field[x][y]:
            if monster[1] == "jgsbat":
                print(cs.cowthink(message=monster[0], cowfile=cust_mstr))
            else:
                print(cs.cowsay(message=monster[0], cow=monster[1]))
            monster[-1] -= 1

    def do_allow_monsters(self, args):
        """
        Список допустимых имен монстров.
        """
        print(*(cs.list_cows() + ["jgsbat"]))

    def do_attack(self, args):
        """
        Атаковать монстра (стандратная атака наносит 10 урона).

        attack <name> with <weapon>

        Параметры:
            <name>         : имя монстра (см. allow_monsters - список допустимых монстров);
            <weapon>       : оружие для атаки;
        """
        name = None
        weapon = "sword"
        if args := sx.split(args):
            match args:
                case name, _, weapon:
                    name = name
                    weapon = weapon
                case _, weapon:
                    weapon = weapon
                case name:
                    name = name[0]

        if monster := self.field[self.pos[0]][self.pos[1]]:
            if name and name != monster[1]:
                print(f"No {name} here")
                return

            damage = WEAPONS[weapon] if monster[-1] >= WEAPONS[weapon] else monster[-1]
            monster[-1] -= damage

            print(f"Attacked {monster[1]}, damage {int(damage)} hp")
            if monster[-1]:
                print(f"{monster[1]} now has {monster[-1]}")
            else:
                print(f"{monster[1]} died")
                self.field[self.pos[0]][self.pos[1]] = None
        else:
            print(f"No {'monster' if not name else name} here")

    def complete_attack(self, text, line, begidx, endidx):
        return complete(text, line, begidx, endidx)

    def complete_attach(self, text, line, begidx, endidx):
        return complete(text, line, begidx, endidx)

    def do_exit(self, args):
        """
        Завершает работу коммандной строки.
        """
        return 1


def main():
    print("<<< Welcome to Python-MUD 0.1 >>>")
    Game().cmdloop()


if __name__ == "__main__":
    main()
