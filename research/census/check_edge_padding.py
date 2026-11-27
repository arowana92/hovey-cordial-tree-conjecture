"""Independent actual-sum checks for a uniform leaf plus edge insertion."""
from collections import Counter
from random import Random

from .edge_padding import leaf_packet, padded_tree, period


def check_packet(k,a,b,p):
    leaf,row = leaf_packet(k,a,b,p)
    assert sorted([leaf,*row]) == list(range(k))
    w = Counter((u+v)%k for u,v in zip([a]+row,row+[b]))
    w[(leaf+p)%k] += 1
    w[(a+b)%k] -= 1
    assert all(w[i] == 1 for i in range(k))


def freq(values,k):
    c = Counter(values)
    return [c[i] for i in range(k)]


def check_period(k,vs,es,a,b):
    row = period(k,a,b,vs,es)
    v = freq(row,k)
    w = freq([(x+y)%k for x,y in zip([a]+row,row+[b])],k)
    w[(a+b)%k] -= 1
    for counts,old in ((v,vs),(w,es)):
        new = [c+(i in old) for i,c in enumerate(counts)]
        assert max(new)-min(new)<=1


def main():
    rng = Random(260208)
    packets = periods = trees = 0
    for k in range(5,36):
        for a in range(k):
            for b in range(a,k):
                check_packet(k,a,b,0)
                packets += 1
        for _ in range(100):
            check_packet(k,*(rng.randrange(k) for _ in range(3)))
            packets += 1
    for k in list(range(5,101))+[125,128,250,256,1001,4096]:
        for j in range(2*min(k,100)):
            size = j%k
            vs = set(rng.sample(range(k),size))
            es = set(rng.sample(range(k),(size-1)%k))
            if k%4 == 0 and size%2 and j%2:
                half = rng.sample(range(k//2),(size-1)//2)
                es = set(half) | {x+k//2 for x in half}
            if k%4 != 2 or any((x+k//2)%k not in es for x in es):
                check_period(k,vs,es,rng.randrange(k),rng.randrange(k))
                periods += 1
        for _ in range(12):
            n = rng.randrange(2,26)
            p = [-1]+[rng.randrange(i) for i in range(1,n)]
            length = (k-1)*(n-2)+rng.randrange(2*k)
            old,row = padded_tree(k,p,length)
            assert len(old)==n and len(row)==length
            weights = [(old[i]+old[p[i]])%k for i in range(2,n)]
            weights.extend((a+b)%k for a,b in zip([old[0]]+row,row+[old[1]]))
            for values in (old+row,weights):
                c = freq(values,k)
                assert max(c)-min(c)<=1
            trees += 1
    print("uniform leaf and edge packets",packets,"fixed-core periods",periods,"padded trees",trees)


if __name__ == "__main__":
    main()
