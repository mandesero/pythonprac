class Undead(Exception):
    pass


class Skeleton(Undead):
    pass


class Zombie(Undead):
    pass


class Ghoul(Undead):
    pass


def necro(a):
    d = {
        0: Skeleton,
        1: Zombie,
        2: Ghoul,
    }
    raise d[a % 3]


if __name__ == '__main__':
    a, b = eval(input())
    for i in range(a, b):
        try:
            necro(i)
        except Skeleton:
            print('Skeleton')
        except Zombie:
            print('Zombie')
        except Undead:
            print('Generic Undead')
