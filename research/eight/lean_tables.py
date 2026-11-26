"""Reindex the eight-label witnesses and emit finite leaf-insertion transitions for Lean."""

import argparse
import gzip
import json
from pathlib import Path


def normalize(row):
    """Return canonical parents and the map from input positions to canonical positions."""
    length = len(row)
    children = [[] for _ in row]
    roots = []
    shapes = [None]*length
    for i in reversed(range(length)):
        children[i].sort(key=lambda j:shapes[j])
        shapes[i] = tuple(shapes[j] for j in children[i])
        p = row[i]
        if p < 8:
            roots.append(i)
        else:
            children[p-8].append(i)
    roots.sort(key=lambda j:(row[j],shapes[j]))
    order = []
    stack = roots[::-1]
    while stack:
        i = stack.pop()
        order.append(i)
        stack.extend(reversed(children[i]))
    ren = [0]*length
    for j,i in enumerate(order):
        ren[i] = j
    canonical = bytes(row[i] if row[i]<8 else 8+ren[row[i]-8] for i in order)
    return canonical,ren


def collect(source):
    levels = [{} for _ in range(9)]
    levels[0][b''] = b''
    with gzip.open(source,'rt') as stream:
        for line in stream:
            kind,parents,witnesses = json.loads(line)
            if kind != 'extension':
                continue
            r = len(parents)
            base = bytes(-1-p if p<0 else 8+p for p in parents)
            by_deficit = [None]*8
            for labels in witnesses:
                weights = [0]*8
                for i,p in enumerate(base):
                    weights[(labels[i]+(p if p<8 else labels[p-8]))%8] += 1
                for d in range(8):
                    if by_deficit[d] is None and all(1<=v+(j!=d)<=2 for j,v in enumerate(weights)):
                        by_deficit[d] = labels
            for shift in range(8):
                row = bytes((p+shift)%8 if p<8 else p for p in base)
                canon,ren = normalize(row)
                if canon in levels[r]:
                    continue
                table = bytearray(8*r)
                for d,labels in enumerate(by_deficit):
                    offset = ((d+2*shift)%8)*r
                    for i,x in enumerate(labels):
                        table[offset+ren[i]] = (x+shift)%8
                levels[r][canon] = bytes(table)
    return levels


def make_tables(out):
    source = Path(__file__).with_name('certificate.jsonl.gz')
    levels = collect(source)
    keys = [sorted(level) for level in levels]
    row_offsets = []
    step_offsets = []
    out.mkdir(parents=True,exist_ok=True)
    with (out/'rows.txt').open('wb') as rows,(out/'steps.txt').open('wb') as steps:
        for r,order in enumerate(keys):
            row_offsets.append(rows.tell())
            step_offsets.append(steps.tell())
            next_index = {row:i for i,row in enumerate(keys[r+1])} if r<8 else {}
            for row in order:
                rows.write(bytes(x+32 for x in row+levels[r][row]))
                if r==8:
                    continue
                for p in range(8+r):
                    nxt,ren = normalize(row+bytes([p]))
                    j = next_index[nxt]
                    steps.write(bytes([32+(j%64),32+(j//64)%64,32+j//4096]
                                      +[x+32 for x in ren]))
    # The Lean proof only uses values for which the finite checker verifies each
    # required witness and each insertion. These offsets just locate the records.
    arrays = {'sizes':list(map(len,keys)),'rowOffsets':row_offsets,'stepOffsets':step_offsets}
    with (out/'Data.lean').open('w') as file:
        file.write('import Std\nnamespace Cordial.Eight.Data\n')
        for name,entries in arrays.items():
            file.write(f'def {name} : Array Nat := #[{",".join(map(str,entries))}]\n')
        for name in ('rows','steps'):
            file.write(f'def {name} : ByteArray := (include_str "{name}.txt").toUTF8\n')
        file.write('end Cordial.Eight.Data\n')
    print('Forest states by order:',arrays['sizes'],flush=True)


if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output',type=Path)
    make_tables(parser.parse_args().output)
