"""Build a high-label hub and count histograms before and after a matching expansion."""

from collections import Counter
from random import Random

from .regular_joint import single_tips
from .two_site_arms import block, nonzero_arms, signed_jumps


def short(b, leaves, k):
    """At 2b<k, use an interval excluding zero or complete one full period."""
    half = b//2
    pairs = [(2*j % (2*half+1)-j, half+j+(b%2))
             for j in range(1,2*half+1)]
    if leaves < k-2*b:
        if b%2:
            pairs.append((-half-1,half+1))
        occupied = {0}
        for a,z in pairs:
            occupied.update((a%k,z%k,(a+z)%k))
        return pairs,[x for x in range(k) if x not in occupied][:leaves]
    if b % 2:
        pairs = [(2*j%b-j, half+1+j) for j in range(b)]
    used = {v%k for pair in pairs for v in pair}
    singles = [x for x in range(k) if x not in used]
    singles.extend(i%k for i in range(1,leaves-len(singles)+1))
    return pairs,singles


def even_period(b):
    if b % 2:
        return [(2*j%b-j, b//2+1+j) for j in range(b)]
    if b <= 20:
        return list(single_tips(b).items())
    s = (b-8)//2
    def move(x):
        return x+s*((x>=4)-(x<=-4))
    frame = [(move(a),move(z)) for a,z in single_tips(8).items()]
    return frame+[(d,10+s+j) for j,d in enumerate(signed_jumps(4,s))]


FOUR = {
    (2,1): [0,1,2,1,3], (2,2): [0,1,1,2,2,3], (2,3): [0,1,1,3,2,2,3],
    (3,0): [0,1,1,2,3,3], (3,1): [0,1,1,2,3,3,2],
    (3,2): [0,0,1,1,3,2,2,3], (3,3): [0,0,1,1,1,2,2,3,3],
    (4,0): [0,1,0,3,2,1,2,3], (6,0): [0,0,0,1,1,2,2,1,2,3,3,3],
    (2,4): [0,1,0,1,2,2,3,3],
}


def four_parts(b, leaves):
    row = FOUR[b,leaves]
    return list(zip(row[:2*b:2],row[1:2*b:2])),row[2*b:]


def construct(k,b,leaves):
    if k == 1:
        return [(0,0)]*b,[0]*leaves
    pair_prefix, plain_prefix = [],[]
    if k == 4:
        if b%4 == 2 and leaves%4 == 0:
            if b >= 6:
                pair_prefix,_ = four_parts(6,0)
                b -= 6
            elif leaves >= 4:
                pair_prefix,plain_prefix = four_parts(2,4)
                b -= 2
                leaves -= 4
            else:
                raise ValueError("the central vertex of the five-vertex path")
        pair_prefix.extend(four_parts(4,0)[0]*(b//4))
        plain_prefix.extend(list(range(4))*(leaves//4))
        b,leaves = b%4,leaves%4
        pairs,singles = four_parts(b,leaves) if b >= 2 else short(b,leaves,k)
    elif k % 2 == 0:
        periods,b = divmod(b,k//2)
        if periods:
            pair_prefix = even_period(k//2)*periods
        pairs,singles = short(b,leaves,k)
    else:
        periods,b = divmod(b,k)
        pair_prefix = [(x,x) for x in range(k)]*periods
        half = k//2
        while leaves and b >= half:
            tip,arms = block(k,0)
            pair_prefix.extend(arms)
            plain_prefix.append(tip)
            b -= half
            leaves -= 1
        if b <= half:
            pairs,singles = short(b,leaves,k)
        elif k == 3:
            pairs,singles = [(1,2),(0,2)],[]
        else:
            pairs,singles = list(nonzero_arms(k)),[]
            _, extra = block(k,0 if half%2 else 1)
            extra = sorted(extra,key=lambda arm: arm[0]%k != 0)
            pairs.extend(extra[:b-half])
    return pair_prefix+pairs,plain_prefix+singles


def verify(k,b,leaves,rng):
    pairs,tips = construct(k,b,leaves)
    assert len(pairs) == b and len(tips) == leaves
    labels,parents = [0],[-1]
    for a,z in pairs:
        parents.extend((0,len(labels)))
        labels.extend((a%k,z%k))
    parents.extend([0]*leaves)
    labels.extend(x%k for x in tips)
    def check(mod, f, edges):
        for values in (f.values(),[(f[i]+f[j])%mod for i,j in edges]):
            c = Counter(values)
            bins = [c[x] for x in range(mod)]
            assert max(bins)-min(bins) <= 1, (k,b,leaves,mod)
    check(k,dict(enumerate(labels)), [(p,i) for i,p in enumerate(parents) if i])
    assert labels.count(0) == max(Counter(labels).values())
    if k%2:
        # Keep the hub as a singleton. At the ends of each of its branches
        # lift the quotient vertex to a matched pair with independent ports.
        f,edges = {0:0},[]
        for i,p in enumerate(parents[1:],1):
            old = 0 if p == 0 else 2*p-1+rng.randrange(2)
            entry = labels[i] if labels[i]%2 == f[old]%2 else labels[i]+k
            f[2*i-1],f[2*i] = entry,(entry+k)%(2*k)
            edges.extend(((old,2*i-1),(2*i-1,2*i)))
        check(2*k,f,edges)


def main():
    rng = Random(1991172)
    cases = doubled = 0
    for k in range(1,61):
        for b in range(2*k+2):
            for leaves in sorted({0,1,2,k//2,max(0,k-2*b-1),max(0,k-2*b),k,k+1,2*k+3}):
                if (k,b,leaves) == (4,2,0):
                    continue
                verify(k,b,leaves,rng)
                cases += 1
                doubled += k%2
    print("high-center trees",cases,"matching expansions",doubled)


if __name__ == "__main__":
    main()
