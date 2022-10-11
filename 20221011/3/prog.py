import sys
s = sys.stdin.read()
nr = s.count('.')
nw = s.count('~')
s = s.splitlines()
a, b = len(s), len(s[0])
new_a = a - 2
new_nw = nw // new_a if nw % new_a == 0 else nw // new_a + 1
new_nr = nr // new_a
field = "#" * a + "\n"
for _ in range(new_nr):
    field += "#" + "." * new_a + "#\n"

for _ in range(new_nw):
    field += "#" + "~" * new_a + "#\n"

field += "#" * a

print(field)
nr = field.count('.')
nw = field.count('~')
length = len(str(nr + nw) + str(max(nr, nw))) + 1
if nr >= nw:
    print(("."*20).ljust(20), f"{nr}/{nr + nw}".rjust(length))
    print(("~"*round(nw/nr*20)).ljust(20), f"{nw}/{nr + nw}".rjust(length))
else:
    print(("."*round(nr/nw*20)).ljust(20), f"{nr}/{nr + nw}".rjust(length))
    print(("~"*20).ljust(20), f"{nw}/{nr + nw}".rjust(length))
