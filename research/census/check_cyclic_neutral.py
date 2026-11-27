"""Compare the two-branch decision with direct labeling and the prime formula."""

from math import isqrt

from research.census.check_prime_neutral import brute
from research.census.cyclic_neutral import construct
from research.census.prime_neutral import construct as prime_construct


def main():
    yes = no = exact = prime = 0
    for k in range(4, 70):
        for a in range(1, k - 2):
            for b in range(1, k - a - 1):
                ordinary = k - 2 - a - b
                rows = construct(a, b, ordinary)
                if k <= 12:
                    assert brute(k, a, b) == (rows is not None), (k, a, b)
                    exact += 1
                if all(k % d for d in range(2, isqrt(k) + 1)):
                    assert (prime_construct(a, b, ordinary) is None) == (rows is None)
                    prime += 1
                if rows is None:
                    no += 1
                else:
                    assert [v for v, _, _ in rows] == list(range(k))
                    assert [r for _, r, _ in rows] == [-1, -1]+[0]*a+[1]*b+[-1]*ordinary
                    labels = [z for _, _, z in rows]
                    assert set(labels) == set(range(k))
                    weights = {(z + (labels[r] if r != -1 else 0)) % k for _, r, z in rows}
                    assert len(weights) == k, (k, a, b)
                    yes += 1
    print("uniform blocks", yes, "excluded splits", no, "direct exhaustive comparisons",
          exact, "independent prime comparisons", prime)


if __name__ == "__main__":
    main()
