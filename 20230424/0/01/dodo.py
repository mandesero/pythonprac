#!/usr/bin/env python3
import glob


def task_png():
    return {
        'actions': ['cat diagram.dia > diagram.png',],
        'file_dep': ['diagram.dia',],
        'targets' : ['diagram.png',],
    }


def task_erase():
    for i, file in enumerate(glob.glob("*.png")):
        yield {
            'name': f'{i}',
            'actions': [f'rm -f {file}',],
        }


def task_mini():
    for size in (8, 16, 32):
        yield {
            'actions': [f'cat diagram.dia > diagram{size}.png',],
            'file_dep': ['diagram.dia',],
            'name': f'do{size}',
            'targets': [f'diagram{size}.dia',]
        }


def task_icon8():
    return {
        'actions': [f'cat diagram8.png > 8.icon',],
        'task_dep': ['mini:do8',],
    }