#!/usr/bin/env python3


import sys
import gettext
import os

popath = os.path.join(os.path.dirname(__file__), "po")

translation = gettext.translation("counter", popath, fallback=True)
_, ngettext = translation.gettext, translation.ngettext

def main():
    while buff := sys.stdin.readline():
        print(ngettext("{} word entered", "{} words entered", len(buff.split())).format(len(buff.split())))

    

if __name__ == "__main__":
    main()

