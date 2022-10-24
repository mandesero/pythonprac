from math import *
funcs = {}
count, lines = 1, 1
while (buff := input().split())[0] != 'quit':
    lines += 1
    if buff[0][0] == ":":
        if len(buff) == 2:
            funcs[buff[0][1:]] = eval(f"lambda: {buff[-1]}")
        else:
            name, *args, func = buff
            funcs[name[1:]] = eval(f"lambda {','.join(args)}: {buff[-1]}")
        count += 1
    else:
        name, *args = buff
        print(funcs[name](
            *[eval(i) for i in args]
            )
        )
print(" ".join(buff[1:]).replace('"', '').format(count, lines))
