"""Verify the remaining prime/shape pairs for four edges away from a hub."""
import argparse
from contextlib import ExitStack
from itertools import product
from math import factorial
from pathlib import Path
import subprocess

from research.biased.generate import nullspace
from research.biased.verify import rank

# Non-singleton components below the hub, using -1 for a hub child.
EXCEPTIONS = (
    (17, (-1,0,-1,2,-1,4)),
    (19, (-1,0,-1,2,2,0)),
    (19, (-1,0,-1,2,3,3)),
    (19, (-1,0,-1,2,-1,4,-1,6)),
    (61, (-1,0,-1,2,3,2)),
)


def query(proc, data):
    proc.stdin.write(" ".join(map(str,data))+"\n")
    proc.stdin.flush()
    sums, witness = proc.stdout.readline().split("|")
    return list(map(int,sums.split())), list(map(int,witness.split()))


def check_labels(p, parents, bias, labels):
    assert len(labels) == len(parents) == len(set(labels))
    assert all(0 < x < p for x in labels)
    weights = [(x+(labels[j] if j >= 0 else 0)+b)%p
               for x,j,b in zip(labels,parents,bias)]
    assert len(set(weights)) == len(labels) and set(weights) <= {0,*labels}


def verify(p, parents, linear, propagation):
    n = len(parents)

    def column(shape, mark):
        size = len(shape)
        unit = [int(i == mark) for i in range(size)]
        original, witness = query(linear,[p,size,mark,*shape])
        alternate, labels = query(propagation,[p,size,0,*shape,*unit])
        assert alternate == original and len(alternate) == size+1 and not alternate[0]
        for found in [witness,labels]:
            if found:
                check_labels(p,shape,unit,found)
        s = p-1-size
        return [factorial(s)*a%p for a in alternate[1:]] + [
            -factorial(s-1)*sum(alternate[1:])%p]*s

    cols = [column(parents,i) for i in range(n)]
    representative = column((*parents,-1),n)
    for i in range(n,p-1):
        c = representative.copy()
        c[i],c[n] = c[n],c[i]
        cols.append(c)
    # The first omitted singleton anchors the common offset shift.
    rows = [*zip(*cols),[int(i == n) for i in range(p-1)]]
    basis = nullspace(rows,p)
    dimension = p-1-rank(rows,p)
    assert len(basis) == dimension and all(not any(v[n:]) for v in basis)
    covered = set()
    for coeff in product(range(p),repeat=dimension):
        if next((a for a in coeff if a),1) != 1:
            continue
        bias = [sum(a*v[i] for a,v in zip(coeff,basis))%p for i in range(p-1)]
        scale = pow(next((b for b in bias if b),1),-1,p)
        bias = [b*scale%p for b in bias]
        assert not any(bias[n:]) and all(sum(a*b for a,b in zip(row,bias))%p == 0 for row in rows)
        assert tuple(bias) not in covered
        _, labels = query(propagation,[p,n,1,*parents,*bias[:n]])
        check_labels(p,parents,bias[:n],labels)
        covered.add(tuple(bias))
        print(f"  offsets {bias[:n]}, active labels {labels}",flush=True)
    assert len(covered) == 1+(p**dimension-1)//(p-1)
    print(f"p={p} shape={parents} kernel dimension={dimension}, {len(covered)} cases",flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("linear",type=Path)
    parser.add_argument("propagation",type=Path)
    args = parser.parse_args()
    with ExitStack() as stack:
        engines = [stack.enter_context(subprocess.Popen(
            [str(binary.resolve())],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True))
            for binary in [args.linear,args.propagation]]
        try:
            for p,shape in EXCEPTIONS:
                verify(p,shape,*engines)
        finally:
            for proc in engines:
                proc.stdin.close()
        assert all(proc.wait() == 0 for proc in engines)
