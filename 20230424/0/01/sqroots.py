#!/usr/bin/env python3

import socket


def sqroots(coeffs: str) -> str:
    try:
        a, b, c = map(int, coeffs.split())
        if a == 0:
            raise ValueError

    except Exception:
        raise ValueError

    D = b * b - 4 * a * c
    if D < 0:
        return ""
    if D == 0:
        return "%.2f" % (-b / (2 * a))
    roots = ["%.2f" % ((-b + D**0.5) / (2 * a)), "%.2f" % ((-b - D**0.5) / (2 * a))]
    roots.sort()
    return f"{roots[0]} {roots[1]}"


def sqrootnet(coeffs, _socket):
    _socket.sendall((coeffs + "\n").encode())
    return _socket.recv(1024).decode()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as _socket:
        _socket.connect(("localhost", 1337))
        coeffs = input()
        print(sqrootnet(coeffs, _socket))


if __name__ == "__main__":
    main()
