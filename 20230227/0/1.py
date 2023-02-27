#!/usr/bin/python3

import shlex

buff = input()
s = shlex.join(shlex.split(buff))
print(s)
