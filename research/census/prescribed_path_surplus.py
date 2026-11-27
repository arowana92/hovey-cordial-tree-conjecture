"""Give a marked path of order one modulo k a prescribed mark and surplus."""

from math import gcd

from .four_leaves import available, endpoint, marked, staircase
from .surplus_path import join


def least_prime(k):
    return next(d for d in range(2,k+1) if k%d==0)


def unit_for(k,h,target):
    return next(u for u in range(1,k) if gcd(u,k)==1 and u*h%k==target)


def ranks_to_labels(ranks,mark,upper):
    other = sum((i-mark)%2 for i in range(len(ranks)))
    class_size = len(ranks)-other
    return [x+(other if upper and (i-mark)%2==0 else
               class_size if not upper and (i-mark)%2 else 0) for i,x in enumerate(ranks)]


def joined_rank(a,b,x):
    n = a+b+1
    for near,far,back in ((a,b,False),(b,a,True)):
        if near//2==x:
            row = staircase(n)
        elif available(near+1,x) and available(far,near//2-x):
            row = join(endpoint(near+1,x)[::-1],endpoint(far,near//2-x))
        elif available(near,x-near//2) and available(far+1,x-near//2):
            row = join(endpoint(near,x-near//2),endpoint(far+1,x-near//2))
        else:
            row = None
            for m in (near+2*x+1,near+2*x+2):
                y = (m-1)//2
                if near<m<n and available(n-m,y):
                    row = join(staircase(m)[::-1],endpoint(n-m,y))
                    break
        if row is not None:
            return row[::-1] if back else row
    return None


def odd_base(k,a,b,target):
    if target==0 or gcd(target,k)==1:
        return ranks_to_labels(marked(a,b,0),a,target!=0)
    g = gcd(k,target)
    h = (g-1)//2
    if k+1>=12*h+13:
        return ranks_to_labels(marked(a,b,h),a,True)
    for rank,upper in ((h,True),(g,False)):
        row = joined_rank(a,b,rank)
        if row is not None:
            return ranks_to_labels(row,a,upper)
    # Order-three exceptional mark. Three even blocks with bridge rank j.
    near = min(a,b)
    j = h//3
    assert k==3*g and h==3*j and near==4*j+1
    row = join(join(endpoint(4*j,j),staircase(2*j+2)[::-1]),endpoint(12*j+2,j))
    return ranks_to_labels(row if a==near else row[::-1],a,True)


def extend_periods(row,extra,k):
    for _ in range(extra//k):
        tip = row[-1]
        row.extend((tip+j//2+(k//2+1 if j%2 else 0))%k for j in range(1,k+1))


def short_odd(k,a,b,target):
    # The retained path has k+1 vertices, with whole periods at its two tips.
    left,right = a%k,b%k
    if left==right==0:
        if a>=k:
            left=k
        else:
            right=k
    row = odd_base(k,left,right,target)
    row.reverse()
    extend_periods(row,a-left,k)
    row.reverse()
    extend_periods(row,b-right,k)
    return row


def endpoint_base(k,q,surplus,port):
    """One or two periods, with the prescribed port at the first vertex."""
    target = (port-surplus)%k
    if q==2 and target==k//2:
        half = [x%k for x in ranks_to_labels(staircase(k+1),0,False)]
        row = half[::-1]+half[1:]
    else:
        rank = min(target,k-target)
        row = ranks_to_labels(endpoint(q*k+1,rank),0,False)
        if rank!=target:
            row = [-x for x in row]
    return [(surplus+x)%k for x in row]


def path_deficit(row,k):
    counts = [0]*k
    for x,y in zip(row,row[1:]):
        counts[(x+y)%k] += 1
    return min(range(k),key=counts.__getitem__)


def even_path(k,a,b,surplus,port):
    periods = (a+b)//k
    needed = 1 if k%4==2 else 2
    if min(a,b)==0 and periods>=needed:
        row = endpoint_base(k,needed,surplus,port)
        extend_periods(row,(periods-needed)*k,k)
        return row if a==0 else row[::-1]
    if periods < 2*needed:
        raise ValueError('outside the proved even-modulus range for this mark')
    if a>b:
        return even_path(k,b,a,surplus,port)[::-1]
    tail = needed*k+1
    if b==tail-1:
        # Here a=b and both halves share the mark.
        left = endpoint_base(k,needed,port,port)
        right = endpoint_base(k,needed,surplus,port)
        return left[::-1]+right[1:]
    # The mark is in the divisible prefix. Use its one missing edge weight.
    n = a+b+1-tail
    start = ranks_to_labels(staircase(n),a,False)
    shift = port-start[a]
    start = [(x+shift)%k for x in start]
    missing = path_deficit(start,k)
    return start+endpoint_base(k,needed,surplus,(missing-start[-1])%k)


def prescribe(k,a,b,surplus,port):
    if k<2 or min(a,b)<0 or (a+b)%k or a+b<k:
        raise ValueError('expected a nontrivial path of order one modulo the modulus')
    if k%2==0:
        return even_path(k,a,b,surplus,port)
    target = (port-surplus)%k
    row = short_odd(k,a,b,target)
    unit = unit_for(k,row[a]%k,target)
    return [(surplus+unit*x)%k for x in row]


def long_attachment(k,n,mark,parent,vertices,weights):
    """Attach n path vertices with any residue, given two balanced core histograms."""
    e = 2 if k%4==0 else 1
    reserve = 0 if k%2 else e*k
    remainder = n%k
    spare = n-reserve-remainder*(e*k+1)
    if not 0<=mark<n or spare<0 or n<=reserve:
        raise ValueError('outside the path decomposition range')
    blocks = [k]*(spare//k)+[e*k+1]*remainder
    start = 0
    for chosen,size in enumerate(blocks):
        if start<=mark<start+size+reserve:
            blocks[chosen] += reserve
            break
        start += size
    starts = [0]
    for size in blocks:
        starts.append(starts[-1]+size)
    assert starts[-1]==n
    row = [None]*n
    vcounts,wcounts = list(vertices),list(weights)
    for j in [chosen]+list(range(chosen-1,-1,-1))+list(range(chosen+1,len(blocks))):
        lo,hi = starts[j:j+2]
        if j==chosen:
            site,c = mark-lo,parent
        elif j<chosen:
            site,c = hi-1-lo,row[hi]
        else:
            site,c = 0,row[lo-1]
        size = hi-lo
        if size%k==0:
            part = ranks_to_labels(staircase(size),0,False)
            deficit = path_deficit(part,k)
            shift = c+part[site]-deficit
            part = [(x+shift)%k for x in part]
        else:
            x = min(range(k),key=vcounts.__getitem__)
            w = min(range(k),key=wcounts.__getitem__)
            part = prescribe(k,site,size-1-site,x,(w-c)%k)
        row[lo:hi] = part
        for x in part:
            vcounts[x] += 1
        wcounts[(c+part[site])%k] += 1
        for x,y in zip(part,part[1:]):
            wcounts[(x+y)%k] += 1
    return row
