#!/usr/bin/env python3


import cowsay as cs
import shlex
import cmd
import sys
import socket
import asyncio
import threading
import readline

from custom_monster import cust_mstr
from defaults import WEAPONS


list_cows = cs.list_cows() + ["jgsbat"]


class Game(cmd.Cmd):
    def __init__(self, s):
        super().__init__()
        self.s = s

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
            self.s.send((msg.strip() + "\n").encode())
        elif args[0] not in list_cows:
            print("Cannot add unknown monster")
        else:
            print("Invalid arguments")

    def do_up(self, args):
        self.s.send(("up\n").encode())

    def do_down(self, args):
        self.s.send(("down\n").encode())

    def do_left(self, args):
        self.s.send(("left\n").encode())

    def do_right(self, args):
        self.s.send(("right\n").encode())

    def do_attack(self, args):
        """Атаковать монстра (стандратная атака наносит 10 урона).

        attack <name> with <weapon>

        Параметры:
            <name>         : имя монстра (см. allow_monsters - список допустимых монстров);
            <weapon>       : оружие для атаки;
        """

        match args := shlex.split(args):
            case [t, "with", weapon]:
                if weapon in WEAPONS:
                    self.s.send(
                        (" ".join(["attack", t, str(WEAPONS[weapon])]) + "\n").encode()
                    )
                else:
                    print("Unknown weapon")
            case [t]:
                self.s.send(
                    (" ".join(["attack", t, str(WEAPONS["sword"])]) + "\n").encode()
                )
            case _:
                print("Invalid arguments")

    def do_sayall(self, args):
        message = "sayall " + args + "\n"
        self.s.send(message.encode())

    def do_quit(self, args):
        self.s.send("quit\n".encode())
        self.onecmd("exit")

    def do_exit(self, args):
        """
        Завершает работу коммандной строки.
        """

        return 1


def get_reponse(s):
    while True:
        ans = s.recv(2048).decode()
        if ans:
            if ans.strip() == "Goodbye":
                break

            print("\n" + ans + "\n")
            print(
                f"\n{cmdline.prompt}{readline.get_line_buffer()}",
                end="",
                flush=True,
            )


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 1338))
        s.send(f"{sys.argv[1]}\n".encode())
        start(s)


def start(s):
    print("<<< Welcome to Python-MUD 0.1 >>>")
    print("Active session:")
    print(s.recv(1024).decode())

    global cmdline
    cmdline = Game(s)
    gm = threading.Thread(target=get_reponse, args=(s,))
    gm.start()
    Game(s).cmdloop()


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 1338))
        s.send(f"{sys.argv[1]}\n".encode())
        main()
