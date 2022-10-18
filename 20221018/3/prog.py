from string import punctuation
from collections import defaultdict

try:
    w = int(input())
    words = defaultdict(int)
    while (buff := input()):
        for i in punctuation:
            buff = buff.replace(i, " ")
        for word in buff.split():
            if len(word) == w and word.isalpha():
                words[word.lower()] += 1
except EOFError:
    pass

if words:
    t = max(words.items(), key=lambda x: x[-1])[-1]
    print(*sorted([word for word in words if words[word] == t]))
