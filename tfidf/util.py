# -*- coding: utf-8 -*-
import os
import inspect

ROOT_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def get_path(fp):
    return os.path.join(ROOT_PATH, fp)


def read_lines(fp, add_root=True):
    lines = []

    if add_root:
        fp = get_path(fp)

    with open(fp, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            line = line.strip('\r\n')
            line = line.strip('\ufeff')
            lines.append(line)

    return lines


def remove_file(fp):
    fp = get_path(fp)
    if os.path.exists(fp):
        os.remove(fp)


if __name__ == '__main__':
    print(ROOT_PATH)
