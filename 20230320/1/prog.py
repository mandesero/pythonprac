import cowsay as cs
import shlex
import cmd
import sys
import socket

from custom_monster import cust_mstr
from defaults import WEAPONS

list_cows = cs.list_cows() + ["jgsbat"]


class Game(cmd.Cmd):
    @staticmethod
    def send_recv_server(msg):
        s.send((msg.strip() + "\n").encode())
        ans = s.recv(1024).decode().strip().replace("'", "")

        if len(t := ans.split("\n")) == 3:
            print(cs.cowsay(message=t[1], cowfile=cust_mstr)) if t[
                1
            ] == "jgsbat" else print(cs.cowsay(message=t[1], cow=t[2]))
        else:
            print(ans)

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

        if len(args := shlex.split(args)) == 8 and args[0] in list_cows:
            msg = "addmon " + shlex.join(args)
            Game.send_recv_server(msg)
        elif args[0] not in list_cows:
            print("Cannot add unknown monster")
        else:
            print("Invalid arguments")

    def do_up(self, args):
        Game.send_recv_server("up")

    def do_down(self, args):
        Game.send_recv_server("down")

    def do_left(self, args):
        Game.send_recv_server("left")

    def do_right(self, args):
        Game.send_recv_server("right")

    def do_attack(self, args):
        """
        Атаковать монстра (стандратная атака наносит 10 урона).

        attack <name> with <weapon>

        Параметры:
            <name>         : имя монстра (см. allow_monsters - список допустимых монстров);
            <weapon>       : оружие для атаки;
        """

        match args := shlex.split(args):
            case [t, "with", weapon]:
                if weapon in WEAPONS:
                    Game.send_recv_server(" ".join(["attack", t, str(WEAPONS[weapon])]))
                else:
                    print("Unknown weapon")
            case [t]:
                Game.send_recv_server(" ".join(["attack", t, str(WEAPONS["sword"])]))
            case _:
                print("Invalid arguments")

    def do_exit(self, args):
        """
        Завершает работу коммандной строки.
        """
        return 1


def main():
    print("<<< Welcome to Python-MUD 0.1 >>>")
    print(s.recv(1024).decode().strip())
    Game().cmdloop()


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 1337))
        s.send("Connect\n".encode())
        main()
