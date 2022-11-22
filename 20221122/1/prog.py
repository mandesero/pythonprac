import sys

buff = sys.stdin.buffer.read()
n = buff[0]
L = len(buff[1:])

step = L / n
ans = [buff[:1], ]
for i in range(n):
    tmp = buff[int(i * step) + 1:int((i + 1) * step) + 1]
    if tmp:
        ans.append(tmp)

ans = ans[:1] + sorted(ans[1:])
res = b""
for i in ans:
    res += i
sys.stdout.buffer.write(res)
