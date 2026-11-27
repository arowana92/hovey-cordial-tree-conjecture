"""Check actual path growth on trees with short internal edges and long terminal arms."""

from random import Random
from research.biased.prime_paths import terminal_tree


def main():
    rng = Random(1125)
    cases = 0
    for k in (2,3,5,6,7,8,9,10,11,12,13,17,19):
        for m in range(2,31):
            # All internal edges can remain short. Include both a star and deep branching.
            coarse = [[] for _ in range(m)]
            for v in range(1,m):
                coarse[0 if m%5==0 else rng.randrange(v)].append(v)
            C = [[] for _ in range(m)]
            for u,row in enumerate(coarse):
                for v in row:
                    L = 1 if coarse[v] else max(1,k-2)+(rng.randrange(4) if m%2 else 0)
                    pred = u
                    for j in range(1,L):
                        w = len(C)
                        C.append([])
                        C[pred].append(w)
                        pred = w
                    C[pred].append(v)
            b = [rng.randrange(k) for _ in C]
            f = terminal_tree(k,C,b)
            w = [(f[u]+f[v]+b[v])%k for u,row in enumerate(C) for v in row]
            assert len(w)==len(C)-1 and all(0<=z<k for z in f)
            for values in (f,w):
                bins = [values.count(i) for i in range(k)]
                assert max(bins)-min(bins)<=1
            cases += 1
    print(f"{cases} terminal-arm trees with arbitrary edge offsets.")


if __name__=='__main__':
    main()
