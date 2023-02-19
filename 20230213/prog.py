#!/usr/bin/python3
from glob import iglob

def get_branches():
    return [branch.split('/')[-1] for branch in iglob('../.git/refs/heads/*', recursive=True)]


def main():
    print(*get_branches(), sep='\n')


if __name__ == "__main__":
    main()
