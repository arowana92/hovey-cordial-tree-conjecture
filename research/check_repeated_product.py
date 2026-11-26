"""Direct histogram checks for repeated-tree products."""

from random import Random

from research.check_odd_quotient import balanced, histogram, low_slots, piece
from research.rainbow.generate import rainbow
from research.rainbow.verify import rooted_shapes


def verify(lab, edges, k):
    assert len(edges) == len(lab)-1
    groups = list(range(len(lab)))

    def root(i):
        while i != groups[i]:
            groups[i] = groups[groups[i]]
            i = groups[i]
        return i

    for i, j in edges:
        a, b = root(i), root(j)
        assert a != b
        groups[a] = b
    counts = histogram((lab[i]+lab[j] for i, j in edges), k)
    assert balanced(histogram(lab, k)) and balanced(counts)
    return counts


def product_tree(q, quotient, part, links, m, w):
    lab, edges = part
    c = w+m*(q//2)
    reps = [None]*m
    for a in range(m):
        b = (w-a) % m
        if reps[a] is None:
            if a == b:
                reps[a] = a+m*((c-2*a)//m*pow(2, -1, q) % q)
            else:
                reps[a], reps[b] = a, c-a
    full = [(reps[x]+m*i) % (q*m) for i in range(q) for x in lab]
    s = len(lab)
    tree = [(i*s+a, i*s+b) for i in range(q) for a, b in edges]
    tree.extend((i*s+a, j*s+b) for (i, j), (a, b) in zip(quotient, links))
    counts = verify(full, tree, q*m)
    missing, = set(range(q)) - {(i+j) % q for i, j in quotient}
    assert counts[(c+m*missing) % (q*m)] == min(counts)
    return (full, tree), (c+m*missing) % (q*m)


def corona(q, quotient, sizes, m):
    lab, edges = [], []
    centers = []
    for i, s in enumerate(sizes):
        center = len(lab)
        centers.append(center)
        for j in range(s):
            if j:
                edges.append((center, len(lab)))
            lab.append(m*i+j % m)
    edges.extend((centers[i], centers[j]) for i, j in quotient)
    verify(lab, edges, q*m)


def main():
    rng = Random(1991)
    mixed = rooted = stars = 0
    for q in [3, 5, 7]:
        for p in rooted_shapes(q).values():
            f = [0]+rainbow(tuple(j-1 for j in p[1:]), q)
            quotient = [(f[i], f[j]) for i, j in enumerate(p) if i]
            missing, = set(range(q)) - {(a+b) % q for a, b in quotient}
            r = missing*pow(2, -1, q) % q
            for m in [1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 15]:
                for s in sorted({m, m+1, 2*m-1}):
                    part = piece(s, m, rng.getrandbits(1), rng)
                    lab, _ = part
                    w = rng.choice(low_slots(part, m))
                    index = {a: [i for i, x in enumerate(lab) if a == x] for a in range(m)}
                    links = []
                    for _ in quotient:
                        a = rng.randrange(m)
                        links.append((rng.choice(index[a]), rng.choice(index[(w-a) % m])))
                    product_tree(q, quotient, part, links, m, w)
                    mixed += 1
                    for i, a in enumerate(lab):
                        if (2*a-w) % m == 0:
                            new, slot = product_tree(q, quotient, part, [(i, i)]*(q-1), m, w)
                            root = r*s+i
                            assert (2*new[0][root]-slot) % (q*m) == 0
                            rooted += 1
                            break
                    corona(q, quotient, [s]*q, m)
                    sizes = [s+rng.getrandbits(1) for _ in range(q)]
                    sizes[r] = s+1
                    corona(q, quotient, sizes, m)
                    stars += 2
    part = ([0, 1, 2], [(0, 1), (1, 2)])
    m, b = 3, 1
    for q in [3, 5, 3, 7]:
        quo = [(i, i+1) for i in range(q-1)]
        part, w = product_tree(q, quo, part, [(b, b)]*(q-1), m, 2*part[0][b] % m)
        b = (q//2)*len(part[0])//q + b
        m *= q
        assert (2*part[0][b]-w) % m == 0 and len(set(part[0])) == m
    print("Mixed products, rooted products, coronas:", mixed, rooted, stars)
    print("Final iterated product order:", m)


if __name__ == "__main__":
    main()
