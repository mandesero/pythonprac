import shlex

s = input()
t = input()

print(a := shlex.join(["register", s, t]))
print(shlex.split(a))
