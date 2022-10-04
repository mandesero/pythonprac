def pareto(*args):
    cmp = lambda x, y: (x[0] <= y[0] and x[1] <= y[1]) and (x[0] < y[0] or x[1] < y[1])
    ans = []
    for i in range(len(args)):
        flag = True
        for j in range(len(args)):
            if i != j and cmp(args[i], args[j]):
                flag = False
                break
        if flag:
            ans.append(args[i])
    return tuple(ans)


print(pareto(*eval(input())))
