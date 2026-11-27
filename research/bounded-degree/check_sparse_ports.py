"""Check sparse-port local classifications and the actual auxiliary cut-tree moments."""
from collections import Counter
from random import Random

from check_unicyclic_core import inspect
from sparse_ports import construct


def star(k,lengths,center_port,unmarked):
    edges = []
    pos = 1
    ends = []
    for i,n in enumerate(lengths):
        edges.append((0,pos))
        edges.extend((v-1,v) for v in range(pos+1,pos+n))
        pos += n
        if i!=unmarked:
            ends.append(pos-1)
    assert pos==k
    return edges,ends+([0] if center_port else [])


def check(k,edges,ports,old,removed,rng):
    result = construct(edges,ports,old,removed,rng)
    if result is None:
        return False
    aux,cut,labels,unpaid,credits,pairs,wires = result
    inspect(k,aux,cut,labels)
    assert set(edges)==set(aux[:cut])|set(pairs)
    assert Counter((labels[a]+labels[b])%k for a,b in wires)==Counter(w for _,w in unpaid)
    assert [(labels[a]+labels[b])%k for a,b in pairs]==credits
    entering = Counter((a+labels[r])%k for r,a in zip(ports,old))
    changed = Counter(w for _,w in unpaid)+Counter(w%k for w in removed)
    assert entering+Counter(credits)==changed
    return True


def main():
    rng = Random(1991327)
    yes = no = 0
    for k in (413,504,625,720,1024):
        for count in (2,3,4,5,7):
            for center_port in (False,True):
                for unmarked in (-1,0):
                    lengths = [1,1]+[3]*(count-2)
                    lengths[-1] += k-1-sum(lengths)
                    edges,ports = star(k,lengths,center_port,unmarked)
                    if len(ports)<2:
                        continue
                    for old,removed in [([0]*len(ports),[0]*(len(ports)-1)),
                        ([rng.randrange(k) for _ in ports],[rng.randrange(k) for _ in ports[1:]])]:
                        success = check(k,edges,ports,old,removed,rng)
                        yes += success
                        no += not success
                        if unmarked==0 and len(ports)>=3:
                            assert success
                        if count==3 and not center_port and unmarked==-1 and not any(old+removed) and k%2:
                            assert not success
        # Three branch vertices or two distinct degree-three joints.
        for t in (4,5,6):
            edges = [(i-1,i) for i in range(1,k-t+2)]
            ports = [0,k-t+1]
            for j in range(t-2):
                v = k-t+2+j
                edges.append(((j+1)*7,v))
                ports.append(v)
            for _ in range(10):
                old = [rng.randrange(k) for _ in ports]
                removed = [rng.randrange(k) for _ in ports[1:]]
                assert check(k,edges,ports,old,removed,rng)
                yes += 1
    print('verified sparse-port embedding cores',yes,'local obstructions',no)


if __name__=='__main__':
    main()
