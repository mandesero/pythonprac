#!/usr/bin/python3
import cowsay
import sys
import argparse


def main():
    '''
    Возможные коровы
    ['owl', 'moose', 'hellokitty', 'blowfish', 'turtle', 'dragon-and-cow', 'bunny', 'milk', 'turkey', 
    'eyes', 'armadillo', 'taxi', 'happy-whale', 'three-eyes', 'frogs', 'lobster', 'TuxStab', 'mutilated', 
    'octopus', 'kitten', 'stegosaurus', 'bill-the-cat', 'supermilker', 'default', 'ghost', 'dragon', 'tux', 
    'bud-frogs', 'seahorse', 'kiss', 'elephant', 'head-in', 'whale', 'moofasa', 'www', 'koala', 'meow', 
    'satanic', 'stimpy', 'skeleton', 'lollerskates', 'llama', 'cower', 'kitty', 'sheep', 'clippy', 
    'elephant2', 'fat-banana', 'banana', 'elephant-in-snake', 'cheese', 'small', 'udder', 'cat', 'daemon', 
    'surgery', 'flaming-sheep']
    '''
    parser = argparse.ArgumentParser()

    # Positional
    parser.add_argument("message", type=str)

    # Optional 
    parser.add_argument("-l", default="default", help="The name of the cow (valid names from list_cows)")

    args = parser.parse_args()

    if args.l in cowsay.list_cows():
        print(cowsay.cowsay(message=args.message, cow=args.l))
    else:
        print("Такой коровы не существует")


if __name__ == "__main__":
    main()
