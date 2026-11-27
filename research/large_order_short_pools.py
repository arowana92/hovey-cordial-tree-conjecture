"""Short explicit order test by packing consecutive degree-two correction sites."""
from .census.euler_subdivision import fill_gaps, skeleton
from .large_order_check import balanced_target, histograms, moment
from .large_order_hall_pools import pairs_for


def cyclic_split(f):
    """f = flag*(1-z)^2 e0 + 2h + (1+z)g with g>=-2 and g+zg<=3."""
    k = len(f)
    if k<3 or sum(f) or moment(f)%k:
        raise ValueError("a cyclic zero-mass, zero-moment vector is required")
    boundary = (moment(f)//k)%2 if k%2==0 else 0
    support = []
    bit = boundary
    for a in f:
        bit ^= a%2
        support.append(bit)
    if k%2 and sum(support)%2:
        support = [1-v for v in support]
    flag = int(k%2==0 and moment(support)%2!=0)
    for j in range(2):
        support[j] ^= flag
    positions = [i for i,x in enumerate(support) if x]
    g = [0]*k
    for i,j in zip(positions[::2],positions[1::2]):
        g[i],g[j] = 1,-1
    displacement = -moment(g)
    distance = displacement//2 if k%2==0 else displacement*pow(2,-1,k)%k
    start = next(i for i,x in enumerate(g) if x>=0)
    g[start] -= 2
    g[(start+distance)%k] += 2
    numerator = [x-g[i]-g[i-1] for i,x in enumerate(f)]
    for i,e in enumerate((1,-2,1)):
        numerator[i] -= flag*e
    return flag,[x//2 for x in numerator],g


def allocate(pool,labels,desired,vertices):
    buckets = [[] for _ in desired]
    k = len(desired)
    for p,t in pairs_for(desired):
        if vertices:
            buckets[-p%k].append((p+t)%k)
        else:
            buckets[p].append(t)
    for i,x in pool:
        labels[i] = buckets[x].pop()


def label(k,parents,root=None):
    """Construct the labeling whenever the stated block packing succeeds."""
    if k<5:
        raise ValueError("the construction uses at least five residues")
    neighbors,pins,runs = skeleton(parents,root)
    f = [None]*len(parents)
    for j,p in enumerate(pins):
        f[p] = j%k
    cursor = [1]*len(runs)
    pools = [[],[],[]]
    exceptional = []
    # A copy of a block at every p gives r centers per neighbor residue.
    blocks = [(9,1),(4,0),(3,0),(3,0),(2,2),(1,1)]
    for r,kind in blocks+[(1,3),(1,4)]:
        stride = 2*r+2
        segment = 0
        for p in range(k if kind<3 else 1):
            while segment<len(runs) and len(runs[segment])-cursor[segment]<stride:
                segment += 1
            if segment==len(runs):
                raise ValueError("insufficient path segments for the block profile")
            i = cursor[segment]
            sites = runs[segment][i:i+stride-1]
            cursor[segment] += stride
            if kind>=3:
                # Both swaps together add (1,-2,1) to the first weight bins.
                values = (2,-1,2) if kind==3 else (2,-2,3)
                for v,x in zip(sites,values):
                    f[v] = x%k
                exceptional.append(sites[1])
                continue
            step = int(kind==2)
            for j,v in enumerate(sites[::2]):
                f[v] = (p+j*step)%k
            for v,left in zip(sites[1::2],sites[::2]):
                pools[kind].append((v,f[left]))
    copies = (10,10,2)
    for j,pool in enumerate(pools):
        allocate(pool,f,[copies[j]]*k,j==0)
    gaps = []
    for run in runs:
        gap = []
        for v in run:
            if f[v] is None:
                gap.append(v)
            elif gap:
                gaps.append(gap)
                gap = []
        if gap:
            gaps.append(gap)
    fill_gaps(k,neighbors,f,gaps)
    n = len(f)
    v,e = histograms(parents,f,k)
    # With a single gap at the common moment difference, further leaves at
    # a zero root can be added in any quantity while preserving balance.
    gap = (moment(v)-moment(e))%k
    base = balanced_target(n,k)
    vt = [base[(i-gap)%k] for i in range(k)]
    et = list(vt)
    et[gap] -= 1
    leaf = next(x for x in pins if x!=root and len(neighbors[x])==1)
    f[leaf] = (f[leaf]+moment(vt)-moment(v))%k
    v,e = histograms(parents,f,k)
    dv,de = [x-y for x,y in zip(vt,v)],[x-y for x,y in zip(et,e)]
    flag,h,g = cyclic_split(de)
    if flag:
        i,j = exceptional
        f[i],f[j] = f[j],f[i]
    for j,row in enumerate((dv,h,g)):
        allocate(pools[j],f,[copies[j]+x for x in row],j==0)
    return f
