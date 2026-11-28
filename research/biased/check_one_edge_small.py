"""Independently check the marked-edge exceptions and growth with offsets at one vertex."""
from itertools import combinations_with_replacement, product
from math import gcd
from pathlib import Path
from random import Random
import subprocess
import sys

from research.eight.generate import forests
from research.eight.prefix_growth import construct
from research.rainbow.spine_counts import rooted


def exceptions(k,n,a,b):
    if all(not child for side in (a,b) for child in side):
        if n==k:
            return {d for d in range(k) if d%gcd(len(a)+1,k)}
        if (len(a),len(b))==(4,5):
            return {1,3,7,9}
    if k==n==10:
        for t in (2,3):
            if {a,b}=={((),)*(8-t),(((),)*(t-1),)}:
                return {5}
    return set()


def finite(program,k,n):
    inputs,expected = [],[]
    for m in range(1,n//2+1):
        left,right=forests(m-1),forests(n-m-1)
        pairs = combinations_with_replacement(left,2) if 2*m==n else product(left,right)
        for a,b in pairs:
            parents=[]
            def grow(tree,parent):
                v=len(parents)
                parents.append(parent)
                for child in tree:
                    grow(child,v)
            grow(a,-1)
            mark=len(parents)
            grow(b,0)
            inputs.append(' '.join(map(str,(k,n,mark,*parents[1:]))))
            expected.append(sum(1<<d for d in exceptions(k,n,a,b)))
    rows=subprocess.run([program],input='\n'.join(inputs)+'\n',text=True,capture_output=True,check=True)
    actual=list(map(int,rows.stdout.split()))
    assert actual==expected
    counts=[sum(rooted(i).values()) for i in range(n)]
    total=sum(counts[i]*counts[n-i] if 2*i<n else counts[i]*(counts[i]+1)//2
              for i in range(1,n//2+1))
    assert total==len(actual)
    print('modulus',k,'order',n,'marked shapes',total,'literal inputs',total*k,
          'failures',sum(bin(mask).count('1') for mask in actual))


def sample_growth(k):
    rng=Random(81+k)
    prefixes=trees=0
    for n in range(1,5*k+1):
        for _ in range(12):
            parents=[-1]+[rng.randrange(v) for v in range(1,n)]
            offsets=[rng.randrange(k) if p==0 else 0 for p in parents]
            # The k+1 vertex star supplies one old leaf of each effective boundary color.
            auxiliary=[-1]+[0]*k+[1+offsets[v] if p==0 else k+p
                                    for v,p in enumerate(parents) if v]
            additions=construct(k,auxiliary,[0,*range(k)])
            if additions is None:
                assert n==k
                continue
            known={0:0}
            vc,ec=[1]+[0]*(k-1),[0]*k
            for v,x in additions:
                v-=k
                assert parents[v] in known
                ec[(known[parents[v]]+x+offsets[v])%k]+=1
                vc[x]+=1
                assert max(ec)-min(ec)<=1 and max(vc)-min(vc)<=1
                known[v]=x
            assert len(known)==n
            trees+=1
            prefixes+=n
    print('modulus',k,'star-supported growth trees',trees,'connected prefixes',prefixes)


if __name__=='__main__':
    program=Path(sys.argv[1]).resolve()
    for k,n in ((8,8),(9,9),(10,10),(10,11)):
        finite(program,k,n)
    for k in (8,9):
        sample_growth(k)
