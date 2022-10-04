def binary_search(elem, seq):
    if not seq:
        return False
    if seq[t := ((len(seq) - 1) // 2)] == elem:
        return True
    if seq[t] < elem:
        return binary_search(elem, seq[t + 1:])
    else:
        return binary_search(elem, seq[:t])
    return False

print(binary_search(*eval(input())))
