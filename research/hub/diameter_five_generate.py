"""Emit order-k diameter-five labeling witnesses, in canonical shape order."""

import argparse
import ctypes
import sys
from functools import lru_cache


@lru_cache(None)
def partitions(total, minimum=1):
    if total == 0:
        return ((),)
    return tuple((a,) + tail for a in range(minimum, total+1)
                 for tail in partitions(total-a, a))


def generate(k, library, out):
    search = ctypes.CDLL(library).diameter_five_search
    ptr = ctypes.POINTER(ctypes.c_int)
    search.argtypes = [ctypes.c_int, ptr, ptr, ctypes.c_uint32, ctypes.c_int]
    array = ctypes.c_int*k
    labels = array()
    row = 0
    for s in range(2, (k-2)//2+1):
        other = k-2-s
        for a in partitions(s):
            if a[-1] == 1:
                continue
            for b in partitions(other):
                if b[-1] == 1 or (s == other and a > b):
                    continue
                row += 1
                parents = [-1, 0]
                for center, parts in enumerate((a, b)):
                    for size in parts:
                        branch = len(parents)
                        parents.extend([center] + [branch]*(size-1))
                tree = array(*parents)
                for trial in range(8):
                    if search(k, tree, labels, row + 2654435761*trial, 30000):
                        break
                else:
                    raise RuntimeError(f"Search exhausted at {a}, {b}")
                out.write(bytes([len(a), *a, len(b), *b, *labels]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("modulus", type=int, choices=range(6, 256), metavar="K")
    parser.add_argument("library")
    args = parser.parse_args()
    generate(args.modulus, args.library, sys.stdout.buffer)
