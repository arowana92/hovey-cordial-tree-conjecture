# Contracting a connected set of leaf parents modulo a divisor

**Two adjacent sites.** Fix $D\ge3$. In a finite tree choose adjacent vertices $a,b$ and assume every other vertex has degree at most $D$. Let $m_a,m_b$ count their adjacent leaves outside $\{a,b\}$, and let $h$ be the order after removing those leaves. At every sufficiently large **even** modulus $k$, the tree is $k$-cordial whenever
$$
\min(m_a,m_b)\ge h-2.
$$
The threshold for $k$ depends only on $D$. The order, number of ordinary branches, and degrees at the two sites are unrestricted. In particular any sequence of counterexamples with two adjacent exceptional vertices and even $k\to\infty$ must have $h=o(k)$ and one of the two leaf populations below $h-2$. [Concentration theorem](concentrated-leaves.md)

If $k\equiv2\pmod4$, a second sufficient condition is that at **each** site the number of leaf neighbors is at least the number of nonleaf neighbors outside the two sites. This can allow much smaller populations when the branches are long. More generally at $k=dq$ for fixed $d\ge2$ and $\gcd(d,q)=1$, it suffices to have $m_i\ge(d-1)B_i$ at both sites, where $B_i$ counts the ordinary branches incident to $i$ outside the common edge.

**A fixed connected set of sites.** Fix a finite tree $P$ with distinguished vertices $a,b$ and choose $d\ge2$. Assume $P$ has distinct labels $t_v\in\mathbb Z_d$, with $t_a=0,t_b=1$, whose edge sums are its vertex labels with one omission $e$. Write $s=|P|$. In a tree containing $P$, suppose all vertices outside $P$ have degree at most $D$. Delete every leaf outside $P$ adjacent to $P$, leaving an ordinary core $H$ of order $h$. Write $m_v$ for the number removed from $v\in P$ and put
$$
L=d(h-s+1)-h.
$$
For all sufficiently large multiples $k$ of $d$, if $m_a,m_b\ge L$, the full tree is $k$-cordial at every order. The other populations may be arbitrary. An edge with digits $0,1$ gives the first theorem at $d=2$. For every fixed $P,a,b$, **all sufficiently large primes $d$** meet the digit hypothesis. Use the integer one-site certificate rooted at $a$, reduce modulo a prime exceeding its span, and multiply by the inverse of the nonzero label at $b$. Thus the connected set may include the whole path between nonadjacent leaf parents at any fixed distance. [Integer certificate](universal-hub.md)

## A nonzero omitted weight in the quotient

In the [linear modulus bound for rooted trees](linear-hub-batches.md), the omitted weight can be chosen nonzero whenever the rooted tree has an edge away from its root. Indeed the construction pairs equal short root branches before its bounded batches. If the residual tree is a star centered at the root, keep one pair of nontrivial short branches that would otherwise be removed. Such a pair exists in this case. This increases the initial bound on short components by at most two. If the residual height is at most four, its order is bounded in terms of $D$ and the integer construction for a nonstar uses weight zero. In the anchor case zero occurs at the first positive-child step or at the delayed edge. In the four-site case two opposite labels are adjacent. For larger height the final four-site modular construction likewise uses weight zero. Restoring the reflected pairs preserves the omission. This gives a constant $K_D$ such that modulus $q>K_D(|U|+1)$ suffices for any rooted $U$ with degrees at most $D$ outside its root and with an edge away from its root. [Anchor construction](branches.md) · [Four-site proof](universal-hub.md#restoring-the-four-sites-and-their-leaves)

Contract $P$ in $H$ to one root to get $U$ of order $u=h-s+1$. Its degrees away from the root are bounded. If $h>s$, at least one ordinary branch has two vertices, since all direct exterior leaves were removed. Give $U$ distinct labels modulo $q=k/d$, zero at the root, with edge weights equal to those vertex labels except for one **nonzero** residue $g$. The unique edge of weight zero has both endpoints outside the root, since no other vertex label is zero.

## Filling the fibers at order exactly $k$

Use the $q$ fibers $j+q\mathbb Z_d$ in $\mathbb Z_k$, with $0\le j<q$. A leaf at a vertex with label $tq$ has weight in the same fiber as its own label, and its digit increases by $t$ modulo $d$. Place each site $v$ at $qt_v$. Lift the nonroot vertices of $U$ to arbitrary representatives of their quotient labels. This labels the original tree $H$. Changing the lift of an endpoint of the quotient-zero edge changes its weight through every digit in fiber zero. Choose it to give weight $qe$. Every other ordinary edge keeps its original quotient weight, including each edge from its actual site in $P$.

There are $u$ occupied vertex fibers and exactly $L=du-h$ unused vertex labels in them. The following steps spend only leaves from $a,b$ in those fibers.

1. In fiber zero the site edges have the site digits except $e$ as their weights. The ordinary edge just assigned supplies $e$. Fill every unoccupied digit with a leaf at $a$, using that same digit as a weight.
2. In an occupied nonzero fiber other than $g$, one vertex digit $A$ and one weight digit $C$ have been spent. On the cyclic interval from $C$ up to but excluding $A$, use a leaf at $b$ at each digit, advancing its weight by one. At all other unoccupied digits use leaves at $a$. The new weights cover exactly the complement of $C$. If $A=C$ the interval is empty.
3. In fiber $g$ a single vertex digit $A$ has been spent and every weight is available. Let $j$ be the sum modulo $d$ of the digits of all remaining requested leaf parents, represented in $[0,d-1]$. Use $j$ leaves at $b$ on the interval from $A-j$ up to but excluding $A$. Use $d-1-j$ leaves at $a$ at the other unoccupied digits. Exactly one weight digit, $A-j$, is omitted. This completes every occupied fiber. Each of $a,b$ initially had at least $L$ requests, enough for all three steps together.

The remaining number of requests is $d(q-u)$ and their digit sum is zero modulo $d$. Partition them into zero-sum blocks of size $d$. While at least $2d$ remain, Erdős–Ginzburg–Ziv supplies such a block, and a final block has sum zero by subtraction. For each block on one empty fiber, Marshall Hall's permutation theorem gives an enumeration of all digits whose translates by the prescribed parent digits also enumerate all digits. Assign those leaves to their actual requested sites. This covers every vertex residue and all weights except the single omitted digit in fiber $g$. In particular step 3 accommodates the parity at $d=2$. [Erdős, Ginzburg and Ziv (1961)](https://www.renyi.hu/~p_erdos/1961-25.pdf) · [Marshall Hall Jr. (1952)](https://doi.org/10.1090/S0002-9939-1952-0050579-7)

## Passing to arbitrary orders

For $h=s$ the nonleaf count is bounded by $s$, so the known finite-exception result covers all sufficiently large $k$. Otherwise fix $\delta>0$ small enough, in terms of $D,d$, that $h<\delta k$ gives both $q>K_D(u+1)$ and $h+2L<k$ for large $k$. If $h\ge\delta k$, all degrees above $D$ in $H$ occur in $P$ and all ordinary leaves adjacent to those high vertices belong to $P$. There are at most $s$ of each. The positive-density theorem applies at every order, with arbitrary leaf populations at the $s$ sites. [Fixed nonleaf count](endpoint-hub.md) · [Positive-density theorem](concentrated-leaves.md)

For $h<\delta k$ the fiber argument proves the order-$k$ base. At smaller orders pad at $a$ to order $k$ and restrict the resulting injection. For $n>k$ keep at least $L$ leaves at each of $a,b$. At $n\equiv1\pmod k$ remove one excess leaf. Otherwise remove $t=(n-1)\bmod k$ excess leaves at any sites. The resulting order is at least $k>h+2L$, so enough excess leaves are available in both cases. Induct on $n$, then restore one leaf at the deficient weight or $t$ leaves with distinct labels and weights avoiding the prefix's surplus label. This proves the theorem. [Arbitrary parent shifts](../counterexample-bound.md#removing-leaves)

## Fewer leaves when the two factors are coprime

Take $P$ to be the edge $ab$ and $\gcd(q,d)=1$. The quotient has an additive section $f(x)=d(d^{-1}\bmod q)x\pmod {dq}$. Place every ordinary nonroot vertex with quotient label $x$ at $f(x)$. The labels of the two sites are $0,q$. Their joining edge supplies digit one in fiber zero. The ordinary quotient-zero edge already supplies digit zero there, since both its endpoints lie outside the two sites.

For every other occupied nongap fiber the vertex and weight digits agree, except precisely in the $B_b$ fibers of ordinary neighbors of $b$. Indeed each edge between exterior vertices has weight $f(x+y)$, and a site edge at $a$ has the weight of its child. At $b$ the weight is the child's label plus $q$. These neighbors have distinct quotient labels, and their own edges supply the weight of their quotient fiber, so none is in the gap fiber. The cyclic interval in step 2 uses exactly $d-1$ leaves at $b$ in each of these $B_b$ fibers and zero in every other fiber. Fiber zero uses only leaves at $a$.

At order $k$ in the sparse case name the site with more leaves $a$. For $\delta$ sufficiently small it has $m_a\ge(k-h)/2\ge L$. The other site needs only $F=(d-1)B_b$ leaves before step 3. The flexible interval uses $(m_b-F)\bmod d$ more leaves at $b$, which is affordable whenever $m_b\ge F$. The rest of its demand is divisible by $d$. Full fibers may now each be filled entirely at one site. To pass to larger orders, retain only the two reserves $(d-1)B_a,(d-1)B_b$ when removing leaves. Their sum is at most $(d-1)(h-2)$, so the same small $\delta$ leaves enough excess for each reduction. At smaller orders, padding preserves both lower bounds. The dense case was already settled without a population bound. Taking $d=2$ gives the assertion at $k\equiv2\pmod4$.

## Reproduction

The constructor lifts the actual exterior edges, then places one leaf per requested digit. The checker recounts labels, endpoint sums and populations on 2,808 expanded trees with 350,163 vertex assignments, including cases at the population threshold and with additional sites. It checks 354 further coprime lifts starting at the forced population $F$, and 398 nonzero omissions on contracted trees that would otherwise lose all their branches to pairing. Lean proves existence and uniqueness of the preimage of each requested weight in steps 2 and 3 after rotating the omitted digit to zero. [Constructor](cluster_lift.py) · [Independent checker](check_cluster_lift.py) · [Lean interval lemma](FiberInterval.lean)

~~~sh
python3 -B -m research.hub.check_cluster_lift
python3 -B -m research.hub.check_linear_hub_batches
lean research/hub/FiberInterval.lean
~~~
