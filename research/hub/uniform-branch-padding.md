# A uniform leaf bound for repeated paths and rooted branches

**Two-site theorem.** Fix a finite tree $H$ with ordered adjacent vertices $z,w$. Fix a path length $t\ge2$. Attach any numbers of disjoint $t$-edge paths at $z$ and $w$. There is a computable constant $C(H,z,w,t)$ such that adding two more two-edge paths and any number of direct leaves at least $C$, all at $z$, gives a super edge-magic tree. The same conclusion holds if each repeated branch consists of a parent and any fixed number $r\ge1$ of leaf children, joined to its site by the parent. The threshold is independent of both branch counts.

In particular, before adding anything, a tree in either family of order $n$ has an injective integer vertex labeling with distinct integer edge sums, each contained in an interval of length at most $n+C+4$. It is $k$-cordial whenever $k\ge n+C+4$. This follows by restricting the completed labeling. If the tree already contains the two specified short paths and sufficiently many direct leaves, the full all-modulus conclusion applies directly. For a single edge as the core and path lengths two or three there are stronger unpadded results. [Length two](subdivided-double-stars.md) · [Length three](three-edge-paths.md)

## Six copies of a rooted tree

Let $A$ be a set of $t$ integer representatives modulo $t$. A branch specification consists of a site label $c$, a tree on the vertex offsets $A$, and a root offset $p$. Require its internal edge sums, together with $c+p$, to use $A$ exactly once. Different branch shapes and different roots may be used with the same $A$.

Give each integer its unique coordinates $ti+a$ with $a\in A$. At defect $d\ge1$ assign speed $-1,0,1$ as $i\le-d$, $-d<i<d$, or $i\ge d$. Suppose a seed tree has vertex interval $[L,U]$ and weight interval $[L+1,U]$. Both contain rows $1-d$ through $d-1$ in every column. Its sites are stationary and the endpoint speeds on each edge add to its weight speed.

Choose a positive $s$ divisible by four with $s\ge2d-1$. Move every old vertex and weight by $3st$ times its speed. In both enlarged intervals the available rows in every column are $S=\pm[d,d+3s-1]$. Each interval extends by $3st$ at both ends. This follows column by column from the interval identity. [Lean proof of the row identity](RadiusTwoIntervals.lean)

A perfect Langford sequence partitions the positions $1,\ldots,2s$ into pairs $i<j$ whose differences are precisely $d,\ldots,d+s-1$. Write $x=d+s+i-1$, $y=d+s+j-1$. The triples $(x,-y,y-x)$ and their negatives partition $S$. The cited existence theorem applies to both parities of $d$ at the stated orders. [Simpson, *Langford sequences: perfect and hooked*](https://doi.org/10.1016/0012-365X(83)90008-0) · [Jordon and Mitchell, introduction](https://doi.org/10.1016/j.disc.2021.112719)

Choose one branch specification for each pair of opposite triples. Give its tree a bipartition. For $(u,v,w)$ and each cyclic rotation, put vertices of the first part at $tu+a$ and those of the second part at $tv+a$. Do this also for the negative triple. Each vertex column uses exactly the six rows of the pair. On internal edges the row is $u+v=-w$ in the column of the offset sum. On the incoming edge the row is that of the root, in column $c+p$. Each weight column therefore uses the same six rows. This fills all slots and attaches six copies at the specified site. Choices for different pairs are independent.

## Constructing an expandable seed at adjacent sites

Give $z,w$ the labels $0,g$ for any prescribed positive $g$. Start with $H$ and any finite residual list of branches at either site, forming a tree $K$. Orient edges away from the central edge. Give the other children of 0 distinct positive labels larger than $g$. Start a counter at $A_0$ above all these labels and $g$. Give children of $g$ the successive values of the counter, increasing it by $g$ after each. Then process remaining unlabeled vertices in parent-before-child order. Give each the current counter value and increase the counter by its positive parent label. Write $Y$ for its final value.

The difference of the weight and vertex multisets is $-[0]-[A_0]+[Y]$, where $[x]$ denotes a single occurrence. Indeed each assignment replaces the current counter value by the next one in this difference. If $Y>A_0$, add a two-edge path at zero with successive labels $A_0-Y,Y$. Both labels are new and its net contribution is $[A_0]-[Y]$. Only label $q=0$ is now missing among the weights. If $Y=A_0$, choose $q=A_0$ and use a first path with labels $-q,q$. Its last edge has weight zero and the missing weight is $q$.

Choose $d$ large enough that all current labels, edge sums and $q$ have speed zero. Add a second two-edge path at zero with successive labels $M+q,-M$, where $M$ is sufficiently large. This replaces the missing weight $q$ by the minimum label $-M$. The new parent has positive speed, the tip negative speed and their sum is stationary. Fill every unoccupied integer in $[-M,M+q]$ with a leaf at zero. Each such leaf has its own label as weight, so the result has consecutive weights and satisfies the speed condition. Take $M$ sufficiently large that both intervals contain every stationary row in every column. This proves the seed assertion for arbitrary residual branches.

For a finite list of branch types, reduce each requested count modulo 24 and use these residual counts in $K$. There are now only finitely many defects and starting leaf counts. Write the removed count of type $j$ as $6s_j$. The total $s=\sum_j s_j$ is divisible by four. Whenever $s\ge2d-1$, assign $s_j$ opposed pairs to type $j$. Otherwise the requested counts are bounded because $d$ is fixed for the residual profile. For each of these finitely many exceptions use the full list in the seed construction. The maximum of the resulting starting leaf counts is a computable $C$. Any additional direct leaf at zero takes the next upper label, which is also its weight.

## Branches covered by the theorem

For a parent with $r$ leaf children put $t=r+1$ and $A=[-1,r-1]$. At site zero use root 0, which has each other offset as a child. At site $g=r$ use root $-1$. Its incoming weight is $r-1$ and the internal weights run from $-1$ through $r-2$.

For a path on $t$ branch vertices, join a site to the first endpoint of the following list, or join the other site to its last endpoint.

| $t$ | Offsets in path order | Second site $g$ |
| --- | --- | ---: |
| $2m+1$ | $m,-1,m-1,-2,\ldots,1,-m,0$ | $m$ |
| $2m$ | $m-1,-1,m-2,-2,\ldots,0,-m$ | $2m-1$ |

In either row the internal sums decrease by one at each step, starting one below the first offset and ending at $-m$. The incoming weight is the first offset at either site. Thus the weights use exactly the vertex offsets.

**Any rooted super edge-magic branch at one site.** Fix such a tree $B$ on $t\ge2$ vertices and any root $v$. Its vertex labels can be translated until its consecutive edge sums omit just the upper endpoint $U$ of its vertex interval. If $v$ has that largest label, first reflect its labeling and realign the intervals. The gap $g=U-f(v)$ is then positive. At site $g$, the incoming weight supplies $U$. Thus arbitrarily many copies of $B$ at $w$ satisfy the same uniform two-path and leaf bound at $z$. In particular, each of the [all-modulus integer families](../../README.md) supplies possible branches when the stated result there is super edge-magic.

## Several sites of an arbitrary core

The following version allows nonadjacent sites and several branch types. Give the $h$ vertices of a fixed core distinct nonnegative integer labels, including zero, with distinct edge sums. Choose a finite collection of branch specifications as above, all using the same $A$ and existing site labels. The same uniform conclusion holds using exactly $2h+1$ extra two-edge paths at zero. The number of extra direct leaves has a computable threshold independent of every branch count.

To see this, keep all core labels. Assign fresh positive labels above all old labels and weights to all newly attached children of zero. Start a counter above those numbers. For every other new vertex, in parent-before-child order, use the counter as its label, then increase the counter by its positive parent label. These added edges contribute only one possible surplus weight beyond the previous ones. The edge sums are distinct and there are at most $h$ weights outside the vertex labels. Zero is a missing weight. Match the surplus weights $w$ bijectively to the missing vertex labels $v$ other than zero.

For each match choose a fresh sufficiently large $J$ and add two paths at zero with successive labels $(J-w,w)$ and $(v-J,J)$. Their contributions to the multiset difference sum to $[v]-[w]$. Here $w$ is positive and outside the original labels. Taking $J$ large avoids all previously used labels and pending surplus weights. This leaves just zero missing. Until there are exactly $2h$ stationary auxiliary paths, add a further path with successive fresh labels $(q-u,u)$ where $q$ is the currently missing weight. The new missing weight is $u$, and any sufficiently large positive $u$ works. Finish with one extreme path and fill the interval as in the adjacent-site proof. The finite-profile argument then applies unchanged.

For example, take any super edge-magic tree $B$ and align its offset sums to omit its largest offset $U$. A copy attached at offset $p$ can be joined to a site labeled $U-p$. These site labels run through $0,\ldots,t-1$. Thus copies of the same tree can be attached by different vertices at different sites, provided the core labeling has the prescribed distinct site labels and distinct edge sums. At pairwise nonadjacent specified sites one can always complete the core labels greedily with sufficiently large distinct positive integers when zero is already specified. At each assignment only finitely many new equalities with previous edges are forbidden, and two new edges at the same vertex have different labeled neighbors.

## Reproduction

The independent checker verifies the two starting intervals, the exact underlying core, the auxiliary paths, the number and location of filler leaves, and the speed equations. It then reconstructs 204 full expanded trees from 68 seeds. It checks every vertex and edge, the recovered rooted branch shapes and their multiplicities at the specified sites. Cases include both seed repairs, stars with one through six tips, path lengths two through eleven, and three different branch choices in the same expansion.

For these whole-tree checks use $s=2d-1$. At this order the pairs $i,\ s+(2i\bmod s)$ for $0\le i<s$ on zero-based positions give the required differences directly, since $s$ is odd. The infinite proof uses Simpson's theorem for all sufficiently large orders divisible by four. [Constructor](branch_packets.py) · [Independent verification](check_branch_packets.py)

~~~sh
python3 -B -m research.hub.check_branch_packets
~~~
