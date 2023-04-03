#!/usr/bin/env python3

from calendar import month
from datetime import datetime
import sys


def restcalend(yr=None, mn=None):
    if not (yr and mn):
        yr, mn, _= str(datetime.now()).split('-')
    s = month(int(yr), int(mn)).split('\n')
    table = [[line[i:i+2] for i in range(0, len(s[1]), 3)] for line in s[1:-1]]
    file = open("out.txt", 'w')

    print("Calendar" +'\n'+ "=" * len("Calendar") + '\n', file=file)
    print('+' + '-' * 20 + '+', file=file)
    print('|' + s[0].rjust(20) + '|', file=file)
    print('+', end='', file=file)

    for i in range(len(s[1])):
        print('+', end="", file=file) if i % 3 == 2 else print('-', end="", file=file)
    print('+', end='', file=file)
    print(file=file)
    for j, line in enumerate(table):
        print('|', end='', file=file)
        print(*line, sep='|', end='', file=file)
        print('|', end='', file=file)
        print(file=file)
        print('+', end='', file=file)
        for i in range(len(s[1])):
            print('+', end="", file=file) if i % 3 == 2 else print('-', end="", file=file)
        print('+', end='', file=file)
        print(file=file)

    file.close()
    with open("out.txt", "r") as file:
        return file.read()


if __name__ == "__main__":
    print(restcalend(int(sys.argv[1]), int(sys.argv[2])))

