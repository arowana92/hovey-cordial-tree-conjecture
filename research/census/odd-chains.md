# Joining copies of any super edge-magic tree

**Theorem.** Let $B$ be any super edge-magic tree of order $n\ge2$. Label it bijectively by $f$ onto $[0,n-1]$ with ordinary edge sums $[h,H]$, $H=h+n-2$. Choose any two vertices $a,b$, possibly equal, such that $f(a)+f(b)$ is either $h-1$ or $H+1$. Join an odd number of copies of $B$ in a path. Use the copy of $a$ for every join at an even position and the copy of $b$ for every join at an odd position. The resulting tree is super edge-magic.

At least one usable pair always exists. Indeed $1\le h\le n-1$ and one may choose the vertices labeled $\lfloor(h-1)/2\rfloor$ and $\lceil(h-1)/2\rceil$. At odd $n$ the two eligible targets differ by the odd number $n$, so one is even and gives a **single common attachment vertex**. Its half is in $[0,n-1]$, since $H\le2n-3$. Thus every super edge-magic tree, including every tree through order 26, gives an infinite family at every modulus. Each output can be used as a new piece. [Integer census](README.md)

The same conclusion holds with any odd quotient tree $Q$ admitting a balanced $\alpha$-labeling. The path positions above are replaced by its two bipartition classes. This gives an integer construction even if the piece and quotient orders share factors.

## Integer construction

By complementing $f$ when necessary, take $f(a)+f(b)=h-1$. Write $q=|Q|=2t+1$. The case $q=1$ is immediate. In sum form a balanced $\alpha$-labeling $g$ allocates $[0,t]$ to the larger quotient class $U$ and $[t+1,2t]$ to the smaller class $V$. Interchanging the lower and upper classes by complementing $g$ achieves this orientation when necessary. The quotient sums fill $[t+1,3t]$. Thus the within-class ranks $r_u=g(u)$ and $r_v=g(v)-t-1$ have sums $[0,2t-1]$ on the quotient edges. The path has this labeling by alternating $0,t+1,1,t+2,\ldots,t-1,2t,t$.

Assign each copy an index $i$, arranging all indices $0,\ldots,2t$ once. At a piece vertex $v$ use label $q f(v)+i$ if $v$ lies in the piece bipartition class of $a$. On the other class use $q f(v)+((i+t+e)\bmod q)$ for a common $e\in\{0,1\}$. For each vertex of $B$ the small digits cover all $q$ positions once. For each edge the small digit sums fill $[t,3t]$ as the index varies. This is the [odd digit identity](StarDigits.lean) for $e=0$; for $e=1$, translation by $t+1$ is inverse to translation by $t$, giving the same unordered pairs. All internal weights consequently form one interval starting at $qh+t$, of length $q(n-1)$.

If $a,b$ are in the same piece bipartition class, use indices $i=g$ and $e=0$. The joining sums are $q(h-1)+g(u)+g(v)$, exactly $[qh-t,qh+t-1]$.

If they are in opposite classes, write $t+1=2d+e$ with $e\in\{0,1\}$ and give copy $w$ index $(d+g(w))\bmod q$. At a $U$ port the small digit is $d+r_u$. At a $V$ port it is $d+e+r_v$, because the two shifts add to $q+e$ after including the lower endpoint $t+1$ of the $V$ interval. These displayed digits are already between zero and $2t$. Their sums fill $2d+e+[0,2t-1]=[t+1,3t]$. Hence the joins again fill exactly the $q-1$ integers immediately below the internal weights. This proves the theorem.

The earlier odd-copy disjoint-union construction also gives consecutive internal sums. The choice of indices above supplies the missing joining weights at the two specified piece vertices. [Odd disjoint unions](https://www.researchgate.net/publication/268891852_On_edge-magic_labelings_of_certain_disjoint_unions_of_graphs) · [Related modular rooted products](../repeated-product.md)

## Checks

The independent checker takes every rooted shape through order eight as a piece (orders at least two), finds its own labeling by permutation enumeration and tests every port pair at either end of its sum interval. With 40 balanced quotient labelings it reconstructs 33,040 full trees, checking the original attachment vertices, the integer vertex interval and all actual edge sums. Both same-side and opposite-side ports and both interval ends occur. [Construction](odd_chain.py) · [Direct verifier](check_odd_chain.py)

~~~sh
python3 -B -m research.census.check_odd_chain
~~~
