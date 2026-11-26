# A growing core with arbitrary leaf populations at two vertices

**Theorem.** Let $H$ have order $h\ge2$, with any two distinct vertices $a,b$. Define
$$
N(h)=(100(h+1))^{8\lceil\log_2(2h)\rceil+1}.
$$
At every modulus $k>100(h+N(h)+1)^{14}$, adjoining any numbers of leaves at $a$ and $b$ gives a $k$-cordial tree. In particular, for every sufficiently large $k$ this holds uniformly for **all cores of order at most $2^{\sqrt{\log_2 k}/16}$**, including arbitrary choices of the two sites and independent leaf populations. Either population can be zero. There is no upper bound on the order of the decorated tree.

For **every** positive modulus, it also suffices that each of the two populations be at least $N(h)$. In this regime the same integer labeling works at all moduli. We prove a quasipolynomial bound on the number of leaves needed for the [two-hub interval construction](two-hubs.md). The previous construction inserted one required vertex or one subdivision at a time. Here each group of insertions uses only endpoint labels present before that group.

## Keeping track of intervals

Keep vertex labels $[L,U]$, hub labels $0,1$, and edge sums $[L+1,U]$. A leaf at hub zero extends the upper end by one. A leaf at hub one extends the lower end by one. When inserting a required child of a parent $p>0$, give it label $L-p$ and fill the intervening vertices with leaves at zero. If $p\le0$, give it $U+1-p$ and fill the intervening vertices with leaves at one. All newly created edges between a required parent and child have one endpoint in $(-\infty,0]$ and the other in $[1,\infty)$.

Suppose an edge with endpoints $p>0$ and $q<0$ must be replaced by a three-edge path. Use new interior vertices
$$
x=\min(L-p,\ p+2q-U-1),\qquad y=p+q-x
$$
in that order starting at $p$. The middle edge has the removed weight $p+q$. Add the following filler vertices, with integer ranges including the left endpoint and excluding the right.

| Hub | Lower ranges | Upper ranges |
|---|---|---|
| 0 | $[x+1,x+p)$ | $[U+1,y+q)$ |
| 1 | $[x+p,L)$ | $[y+q,y)$ |

These ranges, $x,y$ and the old interval partition $[x,y]$. Their weights, the retained old weights and the three path weights partition $[x+1,y]$. In the lower band the edge $px$ supplies $x+p$ and the leaves supply $[x+1,x+p)$ and $[x+p+1,L+1)$. In the upper band $qy$ supplies $y+q$ and the leaves supply $[U+1,y+q)$ and $[y+q+1,y+1)$. The middle edge restores the removed weight. All three path edges cross the same partition of the integers.

An edge with endpoints zero and $q>1$ is also eligible. Reflect all coordinates by $z\mapsto1-z$, interchange the roles of the two hubs, perform the operation, and reflect back. This exchanges the intervals with $[1-U,1-L]$ and $[2-U,1-L]$. Thus every crossing edge other than the edge between the two hubs is eligible.

## The cost of a group of insertions

Write $W=U-L+1$ at the start of a stage. If a stage inserts at most $h$ children of previously present parents, each extends one end by at most $W+1$. Its final width is at most $100(h+1)W$.

If a stage subdivides at most $h$ previously present eligible edges, their endpoints all have absolute value at most $W$. After **each** subdivision the current sum of interval endpoints equals the sum of the original endpoints of that edge, because $x+y=p+q$. Reflection preserves this statement in the original coordinates. Thus the current $|L+U|$ is at most $2W$ throughout the stage, including before the first subdivision. In reflected coordinates the bound is $2W+2$ and the old edge endpoint magnitudes are at most $W+1$. In either coordinate system, the lower-end extension at one operation is
$$
L-x=\max(p,L+U+1-p-2q)\le6(W+1).
$$
The upper-end extension is $y-U=(L-x)+(p+q-L-U)\le 11(W+1)$. Therefore this stage too costs a multiplicative factor at most $100(h+1)$. Subdivided edges may share old endpoints. No operation in a stage needs a new endpoint of another operation of that stage.

## Arbitrary odd subdivisions in one stage

Suppose $j$ different original edges cross the partition, with endpoints $p_i\ge1$ and $q_i\le0$. Choose any counts $s_i\ge1$ and replace edge $i$ by a path of $2s_i+1$ edges. A single construction handles all these lengths. It also works on the edge between the two hubs. Put $S=\max s_i$, $W=U-L+1$ and use step sizes
$$
M_i=8(W+1)(Sj+i),\qquad 1\le i\le j.
$$
For a single edge take just $M_1=8(W+1)$. Within edge $i$, write $p,q,s,M$ for its data and use the two lists $P(t)=p+tM$, $Q(t)=q-tM$, for $0\le t\le s$. Visit indices $0,s,1,s-1,\ldots$ until all indices have occurred. Starting at $p$, alternate copies $P,Q$ on this outbound list, cross to the other copy at the last index, then return through the indices in reverse using the opposite copies. The endpoints are $p,q$. The absolute successive index differences are $s,s-1,\ldots,1$, so the edge sums are the original $p+q$ and the pairs $p+q\pm tM$ for $1\le t\le s$.

Each lower new vertex $q-tM$ has an associated weight $p+q-tM$ strictly above it. Each upper new vertex $p+tM$ has an associated weight $p+q+tM$ at or below it. Across all jobs the positive band centers $tM_i$ are distinct and separated by at least $8(W+1)$. In fact an equality $t(Sj+i)=u(Sj+f)$ with $t\ne u$ would imply $Sj\le |uf-ti|<Sj$ since both products on the right are positive and at most $Sj$. With $t=u$ it forces $i=f$. All original vertex magnitudes are at most $W$ and original edge sums at most $2W$ in magnitude. Thus the lower occupied bands lie entirely below $L$ and the upper ones above $U$, in distinct bands containing their own weight.

Between successive new lower vertices (or the last lower vertex and $L$), the left vertex's associated weight lies in the gap, including its right endpoint and excluding its left. Above $U$ the same rule holds using the right vertex's associated weight. In each gap $(v,w]$ with target $y$, give the leaves with labels $v+1,\ldots,y-1$ to hub zero and those with labels $y,\ldots,w-1$ to hub one. Their weights fill the whole gap except $y$. This proves both interval identities for the single combined extension. The new width is at most $100(W+1)(S+1)^2(j+1)$, and at most $20(W+1)(S+1)$ for a single edge. The construction uses the alternating index order of the [odd hub path](two-hubs.md#paths-that-start-the-construction).

## Building the hub path and the exterior forest

Let $d$ be the distance between the hubs. Start an odd path with the ordinary interval labeling of width $d+1$. At distances two and four use the published path-and-twig seeds of width at most nine, or its residual caterpillar case. Every further leaf distribution on a residual caterpillar is cordial at all moduli by Hovey's caterpillar theorem. For even $d\ge6$, start with the six-edge seed of width nine. Elongate one crossing edge by $(d-6)/2$ pairs in a single stage. This produces the path at all even distances at least six with width at most $100(d+1)$. All its edges cross the partition except the one same-side edge already present in the six-edge seed. Assign the resulting path vertices in order to the original hub path. [Path and twig seeds](two-hubs.md#paths-that-start-the-construction) · [Hovey, *A-cordial graphs*](https://doi.org/10.1016/0012-365X(91)90254-Y)

Protect the resulting core path and any seed twig. Orient the exterior away from the seed. First work on the unlabeled exterior shape, recording the following operations in order. Let $m$ be its current size, $l$ its number of leaves and $b'$ its number of vertices with at least two children.

- If $l\ge m/8$, remove all exterior leaves.
- Otherwise, in every maximal chain of vertices with exactly one child remove its first two vertices, keep its third, and repeat. Remove a final pair if present. Each removed pair contracts its three-edge connection to one edge. Two pairs can share a retained endpoint. There is at least one retained vertex between consecutive removed pairs on a chain.

There are at most $b'+l$ unary chains. Indeed their starts are component roots or children of branching vertices. With $f$ exterior components there are $f$ roots and $b'+l-f$ children of branching vertices in total, by counting edges. Also $b'\le l$. A chain of length $s$ loses at least $(s-1)/2$ vertices. Thus the second operation removes at least $(m-2(b'+l))/2\ge(m-4l)/2>m/4$. Either operation reduces the exterior to at most $7m/8$. Six stages more than halve every positive size, so at most $6\lceil\log_2(2h)\rceil$ stages suffice.

Reverse the stages. A removed leaf uses the child insertion. A contracted pair uses an eligible edge subdivision, because every edge outside the protected seed crosses the partition and cannot join the two hubs. These properties hold inductively for each new edge. The width before growing the exterior is at most $100(h+1)$ and the exterior takes at most $6\lceil\log_2(2h)\rceil$ stages, so the final width is at most $N(h)$. All filler leaves attach to the two designated hubs. This proves the simultaneous large-population claim, since arbitrary additional leaves at either site can extend the appropriate interval. Consecutive integers have balanced frequencies modulo every positive $k$.

## When one population is small

If either population is less than $N(h)$, put all of that population into the core and root it at the other site. Its order is at most $h+N(h)$. The [direct modular theorem](modular-injection.md) works for every population at the remaining site once $k>100(h+N(h)+1)^{14}$. Together with the interval construction this proves the theorem. The base-two logarithm of this cutoff is at most $112(\log_2 h)^2+O(\log(2h))$. Substitution gives the stated growing-core bound.

**Bounded distance from the hub path.** Suppose every original core vertex is at distance at most $r$ from that path. The path or twig seed has width at most $100(h+1)$ at **every** hub distance. Insert the remaining children in breadth-first levels. In each level every parent was already present, and each child costs at most the initial width of that level since $0,1$ are present. Thus width $100(h+1)^{r+1}$ suffices. The same population argument gives $k>100(h+100(h+1)^{r+1}+1)^{14}$. At fixed $r$, all cores of order at most $k^{1/(14(r+1)+1)}$ therefore work uniformly at large $k$.

## A bound in terms of the number of core leaves

Let $l$ count the undirected leaves of the original $h$-vertex core, before any added leaves. Mark both hubs and every vertex of degree different from two. There are at most $2l$ marks, and every segment between consecutive marks has positive length. Retain lengths up to six. Replace any greater length by five or six of the same parity. The compressed tree has order $b\le 12l+1$.

Use the interval construction on this compressed tree. For each segment to be elongated choose a crossing edge in its retained part. On a hub path of odd length all edges cross, and on an even hub path of length at least six at most one fails. A segment outside the hub path has crossing edges throughout except possibly on the short seed twig, which has at most two edges. A segment cannot pass from the hub path to an exterior edge through an unmarked vertex. Thus every retained segment of length five or six that needs expansion permits the choice. In a residual distance-two or distance-four caterpillar there are no such segments, since every exterior branch is a single leaf and the hubs are marked.

Apply the simultaneous subdivision lemma to these distinct chosen edges, with $j\le2l$ jobs and $S\le h/2$. Its width bound gives the following sufficient threshold at **each** site for interval completion outside the residual caterpillar cases:
$$
B(h,l)=100\bigl(N(12l+1)+1\bigr)(h+1)^2(l+1).
$$
Indeed $(S+1)^2(j+1)\le(h+1)^2(l+1)$ for $h\ge2$. With no jobs the compressed width already suffices. It follows that **all** two-site populations work for $k>100(h+B(h,l)+1)^{14}$. For a fixed number of core leaves this is a polynomial modulus cutoff $O_l(h^{28})$, regardless of branching depth or either hub's position.

More uniformly, at all sufficiently large $k$ one may take simultaneously
$$
h\le k^{1/30},\qquad l\le 2^{\sqrt{\log_2 k}/100}.
$$
Indeed the logarithm to base two of the cutoff is at most $28\log_2(h+1)+112(\log_2(l+1))^2+O(\log(2l))$. The two leading contributions together are strictly smaller than $\log_2 k$ by a fixed proportion under the displayed bounds. This allows polynomial-length branches in the original core as well as arbitrarily large leaf populations at the two hubs.

## Reproduction

The constructor records filler labels as half-open ranges, even when the number of leaves is too large to list. The independent check sums the range boundary changes for the original vertex labels and for the actual edge sums after each filler range is shifted by its hub label. These differences determine the two entire multiplicity functions. It verifies 10,005 marked cores, checks the caterpillar structure in 225 residual cases, and covers 32 larger cores through order 8,193. The largest verified interval contains 50,350,902,485,010,787,039 integers, including the explicitly tested extra populations. A further 1,265 replays check the compressed-core construction, with up to 30 simultaneous subdivisions. [Constructor](two_hub_contraction.py) · [Independent range and modular checker](check_two_hub_contraction.py)

~~~sh
python3 -B -m research.hub.check_two_hub_contraction
~~~
