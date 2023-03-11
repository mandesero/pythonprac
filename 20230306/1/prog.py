import cowsay as cs
import shlex as sx
import cmd

from custom_monster import cust_mstr


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
