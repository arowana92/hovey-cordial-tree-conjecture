"""Find interval labelings for two centers with branches of length three."""

import argparse
import ctypes
import json
from pathlib import Path


def seed(library, a, b, defect):
    n = 2+3*(a+b)
    out = (ctypes.c_int * (4*(a+b)))()
    offsets = (0, -1, 1, -2, 2, -3, 3, -4, 4)
    for trial in range(160):
        lower = -(n//2)+offsets[trial % len(offsets)]
        if library.pathsearch(a, b, lower, defect, 1991+trial, 5000, out):
            arms = [list(out[i:i+4]) for i in range(0, len(out), 4)]
            return [a, b, defect, lower, arms]
    raise RuntimeError(f"missing seed at {(a,b,defect)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("library")
    args = parser.parse_args()
    library = ctypes.CDLL(str(Path(args.library).resolve()))
    library.pathsearch.argtypes = [ctypes.c_int]*4 + [ctypes.c_uint, ctypes.c_int,
                                                     ctypes.POINTER(ctypes.c_int)]
    frames = [(2,0,1), (1,1,1)] + [(a,0,2) for a in range(6,12)]
    for a,b,d in frames:
        print(json.dumps(seed(library, a, b, d), separators=(",", ":")))
    for n in range(2,24):
        for b in range(n//2+1):
            a = n-b
            if any(a >= x and b >= y and (n == x+y or
                   ((n-x-y)%6 == 0 and n-x-y >= 6*(2*d-1))) for x,y,d in frames):
                continue
            print(json.dumps(seed(library, a, b, 0), separators=(",", ":")))


if __name__ == "__main__":
    main()
