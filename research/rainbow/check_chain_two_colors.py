"""Check all three literal old colors and every split of the 24 leaves."""
from argparse import ArgumentParser
from hashlib import sha256
from itertools import product
from pathlib import Path


def check(path):
    data=path.read_bytes()
    all_labels=set(range(1,27))
    pos=0
    for a,b,p in product(range(27),repeat=3):
        for j in range(25):
            row=int.from_bytes(data[pos:pos+5],'little')
            pos+=5
            x,y=row&31,(row>>5)&31
            bits=row>>10
            assert x in all_labels and y in all_labels and x!=y and bits>>27==0
            leaves=all_labels-{x,y}
            second={v for v in range(27) if bits&(1<<v)}
            assert len(second)==j and second<=leaves
            edges=[(p,x),(x,y)]+[(b if v in second else a,v) for v in leaves]
            assert len({(s+t)%27 for s,t in edges})==26
    assert pos==len(data)
    print('verified',pos//5,'labelings, SHA-256',sha256(data).hexdigest())


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('certificate',type=Path)
    check(parser.parse_args().certificate)
