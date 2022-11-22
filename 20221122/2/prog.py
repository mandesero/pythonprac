import sys


a = sys.stdin.buffer.read()
a = a.decode('utf-8').encode("latin-1").decode('cp1251', errors='replace')
sys.stdout.buffer.write(a.encode('utf-8'))
