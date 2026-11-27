"""Check completed edge-weight rows on each unrooted tree at five odd primes."""

import gzip
from itertools import combinations
import json
from pathlib import Path

from research.biased.verify import free_count, shape_key


def modulo_constant(row, p):
    return tuple((v-row[0])%p for v in row)


def differences(p):
    allowed = set()
    for i,j in combinations(range(p),2):
        for unit in range(1,p):
            row = [0]*p
            row[i],row[j] = unit,-unit
            allowed.add(modulo_constant(row,p))
    return allowed


def check(p):
    allowed = differences(p)
    catalog = set()
    regular = 0
    with gzip.open(Path(__file__).with_name(f"p{p}.jsonl.gz"),"rt") as stream:
        for line in stream:
            parents = json.loads(line)[0]
            tree = shape_key(parents)
            assert tree not in catalog
            catalog.add(tree)
            edges = [{i,u} for i,u in enumerate(parents) if u>=0]
            rows = [tuple(int(i in e) for i in range(p)) for e in edges]
            rows.append(tuple(-sum(col) for col in zip(*rows)))
            degrees = [0]*p
            for i,j in combinations(range(p),2):
                diff = modulo_constant([a-b for a,b in zip(rows[i],rows[j])],p)
                adjacent = diff in allowed
                if j<len(edges):
                    assert adjacent==bool(edges[i]&edges[j])
                if adjacent:
                    degrees[i] += 1
                    degrees[j] += 1
            maximum = max(sum(i in e for e in edges) for i in range(p))
            assert (len(set(degrees))==1)==(maximum in (2,p-1))
            regular += len(set(degrees))==1
    assert len(catalog)==free_count(p)
    return len(catalog),regular


if __name__=="__main__":
    for p in (3,5,7,11,13):
        count,regular = check(p)
        print(f"p={p}: {count} trees, {regular} regular row graphs")
