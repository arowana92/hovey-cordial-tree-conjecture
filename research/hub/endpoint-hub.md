# Extending any tree to a super edge-magic tree at one prescribed vertex

**Theorem.** Choose any vertex $o$ of any finite tree $H$. There is an effectively constructible $M(H,o)$ such that for every $m\ge M(H,o)$, adjoining $m$ leaves at $o$ gives a super edge-magic tree. A single integer labeling of that tree gives a cordial labeling at **every** positive modulus by reduction. If $h=|H|$ and $e=h-1-\deg(o)$, one may take $M=32h(h+2)2^e$.

More precisely, $H$ itself has distinct integer labels rooted at zero whose ordinary edge sums use every vertex label except its **minimum or maximum**. Once such a labeling has span $S$, give one new hub leaf each missing integer in the interval. This takes exactly $S+1-h$ leaves. Both the vertex labels and the edge sums are then consecutive intervals. Further leaves extend the opposite end from the omitted weight, preserving both intervals. Translation gives the usual vertex interval $[1,n]$. The consecutive edge sums can be complemented by the consecutive edge labels $n+1,\ldots,2n-1$ to give a constant total on each edge. [Youssef, Theorem 4](https://ajc.maths.uq.edu.au/pdf/43/ajc_v43_p031.pdf)

**Corollary.** For each fixed $b$, only finitely many trees with at most $b$ nonleaf vertices can fail to be super edge-magic. They are effectively testable. Equivalently for this purpose, one can fix a bound on the matching number. On a tree with matching number $t$, a minimum vertex cover has $t$ vertices by König's theorem. If $j$ nonleaf vertices lie outside the cover, the forest they induce together with the cover has at least $2j$ edges, so $j\le t-1$ for a nonempty cover.

To see the finiteness, use the finite [reduction to one unbounded leaf population](bounded-core-spectra.md#reduction-to-one-unbounded-site). All regions with at least two large selected populations are covered by super edge-magic labelings. Each of the remaining finitely many one-site families has only finitely many orders below its threshold by the theorem here. In particular, on any core of fixed order, one sufficiently large leaf population suffices regardless of the other populations.

## Choosing a fringe and labeling the rest

A support is a vertex with a child, rooting at $o$. Stars work directly. If any neighbor of $o$ is a support with at most one support child, use the [anchor proof](branches.md), whose omitted weight is its minimum. Assume henceforth that every support neighbor of $o$ has at least two support children.

Use the deepest nonroot fork $P$ with two or more support children as in the [ordinary construction](universal-hub.md). The support chains below its support children never fork. If some chain has at least three supports, take its last three $a,b,c$ and a child $d$ of $c$, giving a four-site path. Otherwise each support child gives a two-site arm $a,b$. The first site is the support child, and the second is its support child if possible, or one of its leaves. The only remaining descendants of these sites are additional leaves. Retain either two or three such arms as specified below.

When a subtree or several arms have been set aside, give the hub zero, its $D$ neighbors distinct labels $1,\ldots,D$, and start a running integer at $Y=2D+1$. Give each remaining nonneighbor vertex that integer, then increase it by its parent's label, in any parent-before-child order. Write $L$ for the final running integer. The old labels lie in $[0,L)$ and the old edge multiset is the vertex multiset minus $[0]+[Y]$ plus $[L]$. This telescopes even when $Y=L$.

**Choosing an order at a specified boundary.** Suppose all removed vertices lie strictly below some nonroot boundary $q$, of label $p$. If $q$ is a hub neighbor, then $0<p<Y$ and $D<Y-p<Y$. If $q$ lies deeper, we can arrange
$$
p>Y,\qquad z=p-Y>0,\qquad L-z>\max V_{\rm old},\qquad L>p+z.
$$
Let $v$ be its ancestor adjacent to the hub. At depth two, first process another support child of $v$, giving it $Y$, then $q$, giving it $Y+x_v$. Save a leaf descendant of that other child for last. Its parent has label at least $Y>z=x_v$. At greater depth first process the path from the child of $v$ through $q$. Leave a different support child of $v$ until after $q$ and end at a leaf of that child's subtree. Its parent has label greater than $p$. Both orders are feasible since the other subtree is retained. The last increment thus exceeds $z$ and the last assigned value is at least $p$, proving both inequalities.

If a new leaf has parent label $u$ and the current gap is $g$, labeling it $g-u$ fills $g$ and moves the gap to the new label, whenever this label is fresh. At parents $+L,-L$ a pair of leaves can take labels $T,T+L$ whose weights exchange the two labels. Such pairs can be placed arbitrarily far above or below existing labels. We use these facts repeatedly.

## Paths and unequal arms

In the [four-site construction](universal-hub.md#restoring-the-four-sites-and-their-leaves), the two sites at $+L,-L$ pair their leaves and all unpaired leaves are at negative parents. If any leaf is unpaired, the first new label exceeds $L$ and successive ones strictly increase the gap. Place all reserved pairs below the minimum instead of above the maximum. The omitted label is now the maximum.

In the path case this leaves only equal numbers of additional leaves at $b,c$ and none at $a$. Choose the boundary order above at the parent of $a$. Give the path vertices
$$
(a,b,c,d)=(Y-p,\ L,\ -L,\ L+Y-p).
$$
In path order their sums are $Y,d,0,a$. Combined with the old sums they omit $-L$. If $p<Y$, $a$ lies between $D$ and $Y$, and $d>L$. If $p>Y$, $a=-z$ lies strictly between $-L$ and zero, and $d=L-z$ lies above all old labels and below $L$. In both cases all labels are distinct, with $-L$ the minimum. Put the pairs at $b,c$ above the maximum.

For the remaining arms, choose two with unequal end populations if possible, or a pair containing a site with an additional leaf at an intermediate vertex. Either choice gives an unpaired leaf by the four-site proof. Thus we may assume **all** arms at $P$ consist of an intermediate vertex with one child, followed by an end with exactly $t$ leaf children, with the same $t\ge0$ on every arm. The fork $P$ can have any number of direct leaf children.

## At least three equal arms

Set aside three arms and their leaf children. Leave $P$ as boundary of positive label $p<L$. In paired arm order give the six sites
$$
(-p-L,\ L),\qquad (L+Y,\ -L),\qquad (-p,\ p+L+Y).
$$
Their six edge sums are $-L,-p,p+L+Y,Y,0,L+Y$. The new minimum $-p-L$ is omitted. The three positive site labels are at least $L$ and distinct. The three negative labels are distinct. Use the gap rule on the $t$ leaves of the third end, whose parent is positive, moving the minimum strictly down. Place the $t$ pairs from the other ends above the maximum. All other arms and the direct children of $P$ were already labeled in the old tree.

## Exactly two equal arms

Write the two arms as $a,b$ and $c,d$. Set aside the direct leaves of $P$ as well. First suppose that the parent $q$ of $P$ is different from $o$. With $P$ also set aside, choose the special boundary order at $q$ and write $p=x_q$.

Give the five sites $(P,a,b,c,d)$ the following labels, except in the bare case specified below:
$$
(L,\ -L,\ Y-p,\ Y-p-L,\ p+L).
$$
In the order $qP,Pa,ab,Pc,cd$ their edge sums are $d,0,c,b,Y$, where a site in this list denotes its label. This leaves gap $-L$.

- If $p<Y$, the label $b$ is between $D$ and $Y$, $c$ is strictly between $-L$ and zero, and $d>L$. The gap is the minimum. Parents $P,b,d$ are positive, so every remaining leaf moves it strictly down.
- If $p>Y$, write $z=p-Y$. The negative site labels are $-L,-z,-L-z$. For $t>0$, take one leaf from $b$ and then one from $d$, repeated $t$ times. Starting at $g_0=-L$, the intermediate label in pair $j$ is $g_{j-1}+z$ and the final label is $g_j=g_{j-1}-(L+Y)$. Since $L>p+z>2z$, the first intermediate label is strictly between $-L$ and $-z$. The first final label lies below $-L-z$, as does the second intermediate label if present. Subsequently the final labels form a decreasing progression, and the intermediate labels form a disjoint progression displaced by $z$ from the previous final labels, with $0<z<L+Y$. All labels are fresh and $g_t$ is the minimum. Direct leaves at $P$ keep moving it down.
- If $p>Y$, $t=0$ and $P$ has at least one direct leaf, the first such leaf receives $-2L<-L-z$. Continue at $P$ until all leaves have been labeled.
- In the bare case $p>Y$, $t=0$ and $P$ has no direct leaves, use instead $(-L,L,-z,L-z,p-L)$ on the five sites. The edge sums in the same order are again $d,0,c,b,Y$. Here $-L<p-L<-z<0$, and $L-z$ is strictly between the old maximum and $L$. The unused weight is the minimum $-L$.

It remains to consider $P$ adjacent to the hub. Set aside the two arms and direct leaf children but keep $P$ in the old tree. No retained nonhub edge is incident to $P$. Compute $Y,L$ normally. If $L>Y$, change the label of $P$ to $p=3L+1$. Its hub edge changes by the same amount and the multiset formula remains true. Give the four sites $a,b,c,d$ the labels
$$
(Y-L,\ L,\ -p,\ p+Y-L).
$$
Their edge sums are $d,Y,0,a$, leaving minimum $-p$. The last site lies strictly between $L$ and $p$, while $a$ lies strictly between $-p$ and zero. The old labels other than $p$ lie below $L$ and are nonnegative. All remaining leaves have positive parents $P,b,d$.

If $L=Y$, the old tree consists entirely of hub neighbors. On $o,P,a,b,c,d$ use $0,4,-3,1,-2,2$. Their edge sums are $4,1,-2,2,0$, missing the minimum $-3$. Parents $P,b,d$ are positive. Use decreasing gaps for their leaves and any fresh positive labels above four for the ordinary hub leaves. This exhausts the possibilities.

## Size and verification

In all cases using the running integer, $L\le 2h2^e$ since $Y\le 2h$ and each update at most doubles the current integer. In the schemes with extra leaves, initial site labels have magnitude at most $4L$, including the large hub-neighbor label. Each gap step has size at most $4L$. Each reserved pair extends one end by at most $L+1\le 2L$ if placed adjacent to the current range. Thus the span is at most $8(h+1)L$, covered by the stated bound. The explicit six-site seed and the star and anchor cases satisfy the same bound directly.

The structural proof applies at every order. A separate program recomputes the original endpoint sums, checks the omitted extreme and verifies the span. It covers all 53,272 rooted shapes through order fourteen, 3,000 larger trees and 1,080 specified fork profiles. For every rooted shape through order nine it fills the gaps with leaves and checks the two entire integer intervals at the first complete interval and after one and seven additional leaves. Lean verifies the local weight identities and the inequalities used for the paired progression. [Constructor](endpoint_hub.py) · [Direct checks](check_endpoint_hub.py) · [Lean arithmetic](EndpointHub.lean)

~~~sh
python3 -B -m research.hub.check_endpoint_hub
lean research/hub/EndpointHub.lean
~~~

The theorem requires sufficiently many added leaves. It does not settle super edge-magicness or cordiality for every original tree.
