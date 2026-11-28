"""Verify full prescribed targets against original trees with unrestricted joint degrees."""
from collections import Counter
from random import Random

from check import adjacency
from check_port_threshold import construct
from check_two_leaf_repair import inspect
from port_degree_reduction import reduce_degree


def main():
    rng = Random(1751991)
    successful = blocked = max_degree = retries = 0
    for base in (1009,1536,2025,3072):
        for joint_load in (4,12,24):
            k = base*(1+joint_load//8)
            stem = k-2*joint_load
            tree = [(v-1,v) for v in range(1,stem)]
            # Two neighboring hubs are joined by an edge that can be redistributed.
            for i in range(2*joint_load):
                tree.append((2+i%2,stem+i))
            adj = adjacency(k,tree)
            leaves = [v for v in range(k) if len(adj[v])==1]
            for ps in (leaves[:1],[2,2],[2,3,2,3],leaves,
                       leaves[:-1]+[2]*4,leaves[:3]+[2]*7+[3]*5):
                old = [i%k for i in range(len(ps))]
                for e in (set(),{0},set(range(k-1)),set(range(0,k,3))):
                    vh = set(rng.sample(range(k),(len(e)+1)%k))
                    removed = [rng.randrange(k) for _ in range(len(ps)-1)]
                    data = construct(k,tree,ps,old,removed,e,vh,rng,reduce_degree)
                    if data is None:
                        assert not e and k%2==0 and (sum(removed)-sum(old)-sum(range(k)))%2
                        count = Counter(ps)
                        assert all((len(row)+count[v])%2==0 for v,row in enumerate(adj))
                        blocked += 1
                        continue
                    draw,(aux,labels,absent,dup,gap,holes) = data
                    inspect(k,tree,ps,old,removed,e,vh,(aux,labels,absent,dup[1],gap[1],holes))
                    assert max(map(len,adjacency(k,aux)))<=5
                    retries = max(retries,draw)
                    max_degree = max(max_degree,max(map(len,adj)))
                    successful += 1
    print('unrestricted-degree targets',successful,'original maximum degree',max_degree,
          'auxiliary degree at most five','parity obstructions',blocked,'maximum draws',retries)


if __name__=='__main__':
    main()
