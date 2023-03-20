#!/usr/bin/env python3

import cmd
import shlex
import threading
import time
import readline
import sys
import socket
import asyncio

lock = threading.Lock()


class CowsayClient(cmd.Cmd):
    @staticmethod
    def send_recv_server(msg, need=True):
        s.send((msg.strip() + "\n").encode())
        if need:
            ans = s.recv(1024).decode().strip().replace("'", "")
            return ans

    def do_login(self, args):
        resp = CowsayClient.send_recv_server("login " + args.strip())
        print(resp)

    def do_say(self, args):
        CowsayClient.send_recv_server("say " + args.strip(), need=False)

    def do_yield(self, args):
        CowsayClient.send_recv_server("yield " + args.strip(), need=False)

    def do_who(self, args):
        resp = CowsayClient.send_recv_server("who")
        print(resp)

    def do_cows(self, args):
        resp = CowsayClient.send_recv_server("cows")
        print(resp)

    def complete_login(self, text, line, *args):
        with lock:
            cows = shlex.split(
                CowsayClient.send_recv_server("cows")[13:].replace(",", "")
            )
            return [s for s in cows if s.startswith(text)]

    def complete_say(self, text, line, *args):
        with lock:
            if len(text.split()) <= 1:
                who = shlex.split(
                    CowsayClient.send_recv_server("who")[12:].replace(",", "")
                )
                return [s for s in who if s.startswith(text)]

    def do_exit(self, args):
        return 1


def get_messages():
    while True:
        if not lock.locked():
            ans = s.recv(1024).decode().strip().replace("'", "")
            if ans:
                print(ans + "\n")
                print(
                    f"\n{cmdline.prompt}{readline.get_line_buffer()}",
                    end="",
                    flush=True,
                )


def main():
    global cmdline
    cmdline = CowsayClient()
    gm = threading.Thread(target=get_messages, args=())
    gm.start()
    cmdline.cmdloop()


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 1337))
        main()
