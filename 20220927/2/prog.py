arr = list(eval(input()))
metric = lambda x: (x * x) % 100
for j in range(len(arr) - 1):
    for i in range(len(arr) - 1):
        if metric(arr[i]) > metric(arr[i + 1]):
            arr[i], arr[i + 1] = arr[i + 1], arr[i]

print(arr)
