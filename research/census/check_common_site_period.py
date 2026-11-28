"""Construct and replay one-period extensions with equal old parent labels."""
from collections import Counter
from pathlib import Path
from random import Random
import subprocess
import sys

from research.rainbow.check_cut_growth import forest


def quotient(parents):
    k = len(parents)
    depths = [0]
    for p in parents:
        depths.append(depths[p]+1)
    internal = set(parents)-{0}
    tips = set(range(1,k+1))-internal
    eligible = internal if len(tips)==2 else tips
    y = next(v for v in sorted(eligible) if depths[v]>=3)
    edges = [(p or y,v) for v,p in enumerate(parents,1)]
    adj = [set() for _ in range(k+1)]
    for u,v in edges:
        assert u!=v and v not in adj[u]
        adj[u].add(v)
        adj[v].add(u)
    assert sum(len(adj[v])==1 for v in range(1,k+1))==len(tips)-int(y in tips)
    cycle = [y]
    while parents[cycle[-1]-1]:
        cycle.append(parents[cycle[-1]-1])
    spine = set(cycle)

    def branch(v,prev):
        sub = sorted(branch(u,v) for u in adj[v]-spine-{prev})
        return '('+''.join(word for word,_ in sub)+')', [v]+[u for _,ids in sub for u in ids]

    blocks = {v:branch(v,0) for v in cycle}
    options = [cycle[i:]+cycle[:i] for i in range(len(cycle))]
    options += [row[::-1] for row in options]
    row = min(options,key=lambda vs:[blocks[v][0] for v in vs])
    key = '.'.join(blocks[v][0] for v in row)
    order = row+[u for v in row for u in blocks[v][1][1:]]
    assert sorted(order)==list(range(1,k+1))
    return key,order,y


def main(search):
    rng = Random(271127)
    joins = trees = 0
    for k in range(11,31):
        cases = []
        for tips in range(1,8 if k in (26,27) else 5):
            for _ in range(12):
                parents = forest(rng,1,0,tips,k)
                cases.append((parents,quotient(parents) if tips>1 else None))
        keys = [obj[0] for _,obj in cases if obj]
        run = subprocess.run([search,str(k)],input='\n'.join(keys)+'\n',text=True,
                             capture_output=True,check=True)
        rows = iter(run.stdout.splitlines())
        for parents,obj in cases:
            trees+=1
            if obj:
                key,order,anchor = obj
                word,*values = next(rows).split()
                assert word==key
                x = dict(zip(order,map(int,values)))
                assert len(values)==k
                shift = x[anchor]
            else:
                x = {i: i//2+(k//2+1 if i%2 else 0) for i in range(1,k+1)}
                shift = 0
            for a in range(k):
                labels = [a]+[(x[v]-shift+a)%k for v in range(1,k+1)]
                weights = [(labels[p]+labels[v])%k for v,p in enumerate(parents,1)]
                target = Counter(range(k))
                assert Counter(labels[1:])==target and Counter(weights)==target
                assert Counter(labels)[a]==2
                joins+=1
        assert next(rows,None) is None
    print(f"rooted trees={trees} labeled extensions={joins}")


if __name__=="__main__":
    main(Path(sys.argv[1]).resolve())
