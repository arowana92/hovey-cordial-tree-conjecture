"""Find labeled starting intervals for arbitrary splits of two-edge arms."""

import argparse
import ctypes
import json
from pathlib import Path


def seed(library, a, b, cutoff):
    result = (ctypes.c_int * (3*(a+b)))()
    offsets = (0, -1, 1, -2, 2, -3, 3, -4, 4)
    for trial in range(120):
        lower = -a-b+offsets[trial % len(offsets)]
        if library.armsearch(a, b, lower, cutoff, 1991+trial, 25000, result):
            return [a, b, cutoff, lower, [list(result[i:i+3]) for i in range(0,len(result),3)]]
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("library")
    args = parser.parse_args()
    library = ctypes.CDLL(str(Path(args.library).resolve()))
    library.armsearch.argtypes = [ctypes.c_int]*4 + [ctypes.c_uint, ctypes.c_int,
                                                    ctypes.POINTER(ctypes.c_int)]
    frames = []
    for b in range(1, 4):
        for a in range(4, 10):
            record = seed(library, a, b, 4) or seed(library, a, b, 6)
            if record is None:
                raise RuntimeError(f"missing expandable interval at {(a,b)}")
            frames.append(record[:3])
            print(json.dumps(record, separators=(",", ":")))
    for total in range(2, 42):
        for b in range(1, total//2+1):
            a = total-b
            eligible = False
            for x,y,cutoff in frames:
                extra = total-x-y
                if (a,b) == (x,y) or (a >= x and b >= y and (b-y)%3 == 0 and
                                       extra%6 == 0 and extra >= 6*(cutoff-1)):
                    eligible = True
                    break
            if not eligible:
                record = seed(library, a, b, 0)
                if record is None:
                    raise RuntimeError(f"missing finite interval at {(a,b)}")
                print(json.dumps(record, separators=(",", ":")))


if __name__ == "__main__":
    main()
