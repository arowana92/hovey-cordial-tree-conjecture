"""Find fresh expanding seed assignments with the specified structural parameters."""

import argparse
import json

from .all_radius_two import check_frame, layer_options, records, required, slope
from .even_layer_search import assign


def regenerate(base, seconds):
    p, bands, sigma, layouts = next(row for row in records("radius-two-frames.jsonl") if len(row[0]) == base)
    options = layer_options(p, bands)
    found = []
    for residues, cutoff, center, _ in layouts:
        def compatible(x, v):
            return slope(x, cutoff, center) + slope(v, cutoff, center) == slope(x+v, cutoff, center)

        result = assign(p, required(p, options, residues), seconds, compatible)
        if isinstance(result, str):
            raise RuntimeError(f"Seed search at degree {base}, residues {residues}: {result}")
        found.append([residues, cutoff, center, result])
    check_frame(p, bands, sigma, found)
    return [p, bands, sigma, found]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base", type=int, choices=(19, 21, 23, 32, 34, 36))
    parser.add_argument("--seconds", type=float, default=30)
    args = parser.parse_args()
    print(json.dumps(regenerate(args.base, args.seconds), separators=(",", ":")))
