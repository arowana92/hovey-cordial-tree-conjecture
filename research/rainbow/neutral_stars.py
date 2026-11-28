"""Exact uniform-increment witnesses for two stars at arbitrary old parents."""
from math import gcd


def criterion(k,s,t,a,b):
    if k<1 or min(s,t)<1 or (s+t)%k:
        raise ValueError("two positive star orders must total a multiple of k")
    delta=(b-a)%k
    if s+t>=2*k:
        return delta%gcd(k,s-1,2)==0
    return any(delta%g==0 and (g>1 or s*delta%k!=0)
               for g in (gcd(k,s-1),gcd(k,t-1)))


def complement(q,x,y,first):
    return [q-int(i==x)-int(i==y)-v for i,v in enumerate(first)]


def fill_cosets(k,h,first,extra):
    # Everything outside the subgroup is still unused by the first star.
    index=gcd(k,h)
    length=k//index
    assert extra%length==0 and 0<=extra<=k-length
    for representative in range(1,extra//length+1):
        for i in range(representative,k,index):
            first[i]+=1


def single_period(k,s,delta):
    for h in range(1,k):
        if h==delta or ((s-1)*h+delta)%k: continue
        length=k//gcd(k,h)
        remainder=(s-1)%length
        first=[0]*k
        for j in range(1,remainder+1):
            first[-j*h%k]=1
        fill_cosets(k,h,first,s-1-remainder)
        return h,0,first,complement(1,h,0,first)
    return None


def double_period(k,s,delta):
    assert s<=k
    first=[0]*k
    if delta==0:
        leaves=s-1
        for i in range(1,k):
            first[i]=min(2,leaves)
            leaves-=first[i]
        return 0,0,first,complement(2,0,0,first)
    length=k//gcd(k,delta)
    remainder=(s-1)%length
    if remainder%2:
        h=delta
        long=(remainder+1)//2
        y=long*h%k
        arcs=((h,long),(delta,long-1))
    else:
        if length%2:
            h=((length+1)//2)*delta%k
        else:
            assert delta%2==0
            h=delta//2
            length=k//gcd(k,h)
            remainder=(s-1)%length
        half=remainder//2
        y=(half+1)*h%k
        arcs=((h,half),(delta,half))
    x=(y+h)%k
    for start,size in arcs:
        for j in range(size):
            first[(start+j*h)%k]+=1
    fill_cosets(k,h,first,s-1-remainder)
    return x,y,first,complement(2,x,y,first)


def translate(result,offset):
    x,y,left,right=result
    k=len(left)
    t=offset%k
    return (x+t)%k,(y+t)%k,left[-t:]+left[:-t],right[-t:]+right[:-t]


def reverse(result):
    x,y,left,right=result
    return y,x,right,left


def build(k,s,t,a,b):
    if not criterion(k,s,t,a,b): return None
    q=(s+t)//k
    if q==1:
        result=single_period(k,s,(b-a)%k)
        if result is not None: return translate(result,a)
        return reverse(translate(single_period(k,t,(a-b)%k),b))
    batches=min((s-1)//k,q-2)
    other=q-2-batches
    left_size,right_size=s-k*batches,t-k*other
    if left_size<=right_size:
        result=translate(double_period(k,left_size,(b-a)%k),a)
    else:
        result=reverse(translate(double_period(k,right_size,(a-b)%k),b))
    x,y,left,right=result
    return x,y,[n+batches for n in left],[n+other for n in right]
