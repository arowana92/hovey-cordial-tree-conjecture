"""Check the path targets in the one-leaf proof on actual cut graphs."""
from random import Random


def inspect(k,vertices,edges,marks,missing_vertex,missing_weights):
    assert len(edges)==len(vertices)-1
    degree = {i:0 for i in vertices}
    pairs = []
    for i,j in edges:
        degree[i] += 1
        degree[j] += 1
        if i in marks and j in marks:
            pairs.append((i,j))
    ends = [i for i,d in degree.items() if d==1]
    assert len(ends)==2 and set(ends)<=marks and max(degree.values())==2
    total = k*(k-1)//2
    vsum = total-(missing_vertex or 0)

    def valid(labels,holes):
        colors = [(labels[i]+labels[j])%k for i,j in pairs]
        return (len(set(labels.values()))==len(labels) and missing_vertex not in labels.values()
                and len(set(holes))==missing_weights and len(colors)==len(set(colors))
                and set(colors).isdisjoint(holes)
                and (2*vsum-sum(labels[i] for i in ends)-total+sum(holes))%k==0)
    return valid


def main():
    rng = Random(492503)
    cases = 0
    for k in (19,20,25,26,27,31,36,45,63,64,81):
        for c in range(3,k):
            J,Y = 0,k-1
            tail = [(0,c)]+[(i-1,i) for i in range(c+1,k)]
            ring = [(i,(i+1)%c) for i in range(c)]
            P = tail[-1][0]
            openings = range(c) if k<=27 else {0,1,c-1,rng.randrange(c)}
            for cut in openings:
                u,v = ring[cut]
                if k%2==0:
                    B = 1
                    edges = ring[1:]+tail
                    valid = inspect(k,set(range(k)),edges,{J,Y,B},None,1)
                    assert any(valid({J:0,Y:k//2,B:t},[t]) for t in range(1,k) if t!=k//2)
                    cases += 1
                    continue
                port = u or v
                B = c-1 if port==1 else 1
                omit = 0 if B==1 else c-1
                path = ring[:omit]+ring[omit+1:]+tail
                valid = inspect(k,set(range(k)),path,{J,Y,B,port},None,1)
                for D,F in [(0,1),(1,0),(k-1,1),rng.sample(range(k),2)]:
                    assert any(valid({port:0,J:h,B:(D-h)%k,Y:(h+F-D)%k},[F]) for h in range(k))
                    cases += 1
                for port in (u,v):
                    B = c-1 if port==1 else 1
                    omit = 0 if B==1 else c-1
                    edges = ring[:omit]+ring[omit+1:]+tail[:-1]
                    valid = inspect(k,set(range(k-1)),edges,{J,P,B,port},0,2)
                    for a in {1,k//3,k-1}:
                        for _ in range(600):
                            h = a if port==J else rng.randrange(1,k)
                            t = rng.randrange(1,k)
                            r = h if P==J else rng.randrange(1,k)
                            if valid({port:a,J:h,B:t,P:r},[(h+t)%k,(r-h)%k]):
                                break
                        else:
                            raise AssertionError((k,c,cut,port,a))
                        cases += 1
                B = c-1 if cut==0 else 1
                omit = 0 if B==1 else c-1
                edges = [e for i,e in enumerate(ring) if i not in (cut,omit)]
                edges += [(u,k),(k,v)]+tail[:-1]
                valid = inspect(k,set(range(k-1))|{k},edges,{k,J,B,P},None,1)
                for h in range(1,k):
                    if any(valid({k:0,J:h,B:(-h)%k,P:r},[(r-h)%k])
                           for r in ([h] if P==J else range(1,k))):
                        break
                else:
                    raise AssertionError((k,c,cut))
                cases += 1
    print('checked pinned path targets',cases)


if __name__=='__main__':
    main()
