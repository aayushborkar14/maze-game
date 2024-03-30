import numpy as np
import sys


def proc(i):
    return (i % 8) * 875 + (i >> 3)


if len(sys.argv) != 3:
    print("Usage: python tmx_csv_to_npy.py <input_file> <output_file>")
    sys.exit(1)

a = np.loadtxt(sys.argv[1], delimiter=",", dtype=int)
np.save(sys.argv[2], proc(a - 1))
