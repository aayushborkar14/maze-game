import sys

import numpy as np


def proc(i, x, y):
    return np.where(i < 0, -1, (i % x) * y + (i // x))


if len(sys.argv) != 6:
    print(
        "Usage: python tmx_csv_to_npy.py <input_file> <output_file> <starting_gid> <x> <y>"
    )
    sys.exit(1)
starting_gid = int(sys.argv[3])
x = int(sys.argv[4])
y = int(sys.argv[5])
a = np.loadtxt(sys.argv[1], delimiter=",", dtype=int)
np.save(sys.argv[2], proc(a - starting_gid, x, y))
