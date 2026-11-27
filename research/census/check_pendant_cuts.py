"""Test every abstract short suffix and every equality pattern of its boundary colors."""
from itertools import combinations_with_replacement, product


def eligible(parts):
    mass = runs = 0
    previous = None
    for size,color in sorted(parts):
        if color != previous:
            if runs and size < mass+runs:
                return False
            runs += 1
        mass += size
        previous = color
    return True


def check():
    accepted = 0
    for t in range(22,26):
        for a in range(t-11,t):
            z = t-a
            for count in range(1,min(z,3)+1):
                for sizes in combinations_with_replacement(range(1,z+1),count):
                    if sum(sizes) != z:
                        continue
                    for colors in product(range(count),repeat=count):
                        parts = list(zip(sizes,colors))
                        if not eligible(parts):
                            continue
                        for new in range(count+1):
                            if not eligible(parts+[(a+25-t,new)]):
                                raise AssertionError((t,a,parts,new))
                            accepted += 1
    print(accepted, 'padded two-side boundary assignments')


if __name__ == '__main__':
    check()
