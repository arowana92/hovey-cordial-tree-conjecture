"""Generate signed-moment certificates from an unrooted census stream."""

import argparse
import ctypes
from itertools import product
import json
from pathlib import Path


def parents(word, p):
    stack, result = [], []
    for bit in f"{word:0{2*p}b}":
        if bit == "1":
            result.append(stack[-1] if stack else -1)
            stack.append(len(result)-1)
        else:
            stack.pop()
    return result


def nullspace(rows, p):
    a = [list(row) for row in rows]
    n = len(a[0])
    pivots = []
    for col in range(n):
        j = len(pivots)
        idx = next((i for i in range(j,len(a)) if a[i][col]),None)
        if idx is None:
            continue
        a[j],a[idx] = a[idx],a[j]
        inv = pow(a[j][col],-1,p)
        a[j] = [inv*x%p for x in a[j]]
        for i,row in enumerate(a):
            if i != j and row[col]:
                a[i] = [(x-row[col]*y)%p for x,y in zip(row,a[j])]
        pivots.append(col)
    basis = []
    for col in range(n):
        if col not in pivots:
            v = [0]*n
            v[col] = 1
            for i,j in enumerate(pivots):
                v[j] = -a[i][col]%p
            basis.append(v)
    return basis


def record(lib, p, par):
    array = ctypes.c_int*p
    def compute(bias, mode):
        out = array()
        ok = lib.direction(p,array(*par),array(*bias,0),out,mode)
        if not ok:
            if mode == 1:
                raise RuntimeError(f"no witness at {par}, {bias}")
            return [0]*p
        return list(out)
    n = p-1
    scalar = compute([0]*n,2)[0]
    columns, cases = [], []
    if not scalar:
        for j in range(n):
            result = compute([int(i==j) for i in range(n)],0)
            assert result[0] == 0
            columns.append(result[1:])
        basis = nullspace([*zip(*columns),[1]+[0]*(n-1)],p)
        for coeff in product(range(p),repeat=len(basis)):
            if next((a for a in coeff if a),1) != 1:
                continue
            bias = [sum(a*v[i] for a,v in zip(coeff,basis))%p for i in range(n)]
            scale = pow(next((a for a in bias if a),1),-1,p)
            bias = [a*scale%p for a in bias]
            cases.append([bias,compute(bias,1)])
    return [par,scalar,columns,sorted(cases)]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prime",type=int,choices=(2,3,5,7,11,13))
    parser.add_argument("library")
    parser.add_argument("stream")
    args = parser.parse_args()
    lib = ctypes.CDLL(str(Path(args.library).resolve()))
    p = args.prime
    with open(args.stream,"rb") as stream:
        while data := stream.read(8+p):
            if len(data) != 8+p:
                raise ValueError("truncated tree record")
            par = parents(int.from_bytes(data[:8],"little"),p)
            print(json.dumps(record(lib,p,par),separators=(",",":")))
