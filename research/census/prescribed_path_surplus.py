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


def prescribe(k,a,b,surplus,port):
    if k<2 or min(a,b)<0 or (a+b)%k or a+b<k:
        raise ValueError('expected a nontrivial path of order one modulo the modulus')
    target = (port-surplus)%k
    factor = least_prime(k)
    if k%2:
        row = short_odd(k,a,b,target)
    elif a+b+1 >= 12*(k//factor)+13:
        row = ranks_to_labels(marked(a,b,gcd(k,target) if target else 0),a,False)
    else:
        raise ValueError('outside the proved pair-prescription range')
    unit = unit_for(k,row[a]%k,target)
    return [(surplus+unit*x)%k for x in row]
