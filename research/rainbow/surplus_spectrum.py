"""Generate explicit maximum-size rainbow rows, including failed boundary orbits."""
import argparse
import json
from .generate import boundary_orbits,forests,native_search,parent_vector,rainbow


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('modulus',type=int)
    parser.add_argument('--native')
    args = parser.parse_args()
    k = args.modulus
    solve = native_search(args.native,k) if args.native else rainbow
    for forest in forests(k-1):
        for colors in boundary_orbits(forest,k):
            ps = parent_vector(forest,colors)
            try:
                labels = solve(ps,k)
            except ValueError:
                labels = []
            print(json.dumps([ps,labels],separators=(',',':')))


if __name__=='__main__':
    main()
