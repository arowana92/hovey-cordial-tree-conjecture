# Leaf extensions of arbitrary cores and a diameter-five criterion

Let $H$ be any tree on $h$ vertices. Attach $m_v$ new leaves at each vertex $v$, and put $M=\sum_v m_v>0$. The following results give one integer labeling with consecutive vertex labels and consecutive edge sums. In particular the resulting tree is super edge-magic and is $k$-cordial for every positive $k$.

**Theorem 1.** For every $H$, it suffices that
$$
\min_v m_v\ \ge\ 2^{(h+18)/2}(h+1)\sqrt M .
$$
In particular, for every fixed tree, attaching the same number $m$ of leaves at every vertex works for every sufficiently large $m$. No labeling of $H$ is assumed. For comparison, Theorem 2.1 of Figueroa-Centeno, Ichishima and Muntaner-Batle treats equal leaf counts at every vertex of an odd-order graph admitting a particular super edge-magic labeling. [*Magical coronations of graphs*](https://ajc.maths.uq.edu.au/pdf/26/ajc_v26_p199.pdf)

Only **five** vertices actually need a population condition. For $h\ge5$ choose two leaves $x,y$ of $H$ and any three-vertex path in $H-\{x,y\}$. Let $w=\min(m_x,m_y)$ and let $r$ be the minimum $m_v$ on the path. It suffices that
$$
rw\ \ge\ 2^{h+18}(h+1)^2 M. \tag{1}
$$
The other $m_v$ may be zero. The two leaves are vertices of the original core, so each can receive leaves of its own. Their deletion leaves a connected tree with at least three vertices. For $h<5$ the core is a path or a star. Adding leaves to a path gives a caterpillar, and adding leaves to a star gives a tree of diameter at most four. This also covers those cases of Theorem 1. [Diameter-four theorem](all-radius-two.md)

**Theorem 2.** In a tree of diameter five, delete all leaves once. The remaining core consists of the adjacent centers and their neighbors having children away from the central edge. Let $h$ be its order, $M$ the number of deleted leaves and $t$ the fifth largest number of leaf children among those neighbors, excluding the two centers. If at least five such neighbors exist and
$$
t^2\ \ge\ 2^{17}(h+1)^3 M, \tag{2}
$$
the original tree is super edge-magic. This works for every placement of the five branches on the two sides of the central edge. The centers themselves can have any number of leaf neighbors.

The constants give sufficient bounds. The construction has directly checkable tests at smaller populations as well. The proof has two parts. First, place the core so the requested parent labels have weighted average near $1/2$. Then use permutations on integer intervals to realize exactly the requested leaf counts.

## Rounding rotations with only a linear number of extra leaves

Suppose the current vertex and edge intervals are $[L,U]$ and $[L+1,U]$. A block of length $n$ uses one child for each $0\le i<n$. Above the interval choose label $U+1+i$ and parent $\pi(i)-i$, where $\pi$ permutes $[0,n-1]$. Below it choose label $L-n+i$ and parent $1+\pi(i)-i$. Both operations extend the two intervals and preserve the missing weight at the minimum. Write $j=0,1$ for the respective parent offset.

A rotation $R(i)=(i+a)\bmod n$ at $n=a+b$ has $b$ displacements $a$ and $a$ displacements $-b$, for positive $a,b$. The following way to use a fraction of a rotation bounds the number of extra leaves in terms of $n$.

**Partial rotation lemma.** For $0\le t\le n/2$, one can retain $t$ positions of this rotation and complete them to a permutation. Among the retained positions the number with displacement $a$ differs from $tb/n$ by less than one. Every other position has its parent label in $\{-1,0,1\}$, for either offset $j$.

Let $m=n-t$ and fix a phase $0\le\beta<1$. Put $i$ in $C_\beta$ if $\lfloor m(i+1)/n+\beta\rfloor>\lfloor mi/n+\beta\rfloor$. Retain the rotation on the complement. Its intersection with the first $b$ positions has the claimed size by telescoping. The $m$ remaining targets are $R(C_\beta)=C_{\beta'}$ where $\beta'=\{\beta-ma/n\}$. Match these two sets in increasing order. Position number $z$, counted from one, is $\lceil n(z-\beta)/m\rceil-1$, and similarly for the targets.

For an upper block choose $\beta=0$ if $\{-ma/n\}\le1/2$. Otherwise choose $\beta=\{ma/n\}$ so $\beta'=0$. The change of phase has absolute value at most $1/2$ and $n/m\le2$, so each displacement is $-1,0$ or $1$. For a lower block take $\beta=0$. Now $\beta'\ge\beta$, so each displacement is $-2,-1$ or $0$. Adding the lower offset one gives the same three parent labels. Lean verifies the rotation of the phase and both displacement bounds in integer coordinates. [Lean arithmetic proof](PartialRotation.lean)

## Exact completion of a labeled core

Let $p_v$ be the distinct integer labels of the $h$ core vertices, including the three available parents $-1,0,1$. Put $D=2+\max_v |p_v|$. A seed may already have used some of the requested leaves. From the remaining counts set aside $B,B,2B$ leaves at $-1,0,1$, respectively, and then up to $A$ leaves at each core vertex, taking all if fewer than $A$ remain. Use
$$
K=2h+2,\qquad A=4K+2,\qquad B=JD,\qquad J=4K+h(A+4K)+2.
$$
Suppose the first reserves are available, and the remaining working counts $n_p$ satisfy $0\le W'=\sum p n_p\le M'=\sum n_p$.

Split the working counts over the reals into an upper list of total displacement zero and a lower list of total displacement zero after subtracting one from each parent. To see this, choose lower mass $W'$ of weight $W'$. A uniform fraction has weight $(W')^2/M'\le W'$, and taking the largest $W'$ units of mass has weight at least $W'$ since parent labels are integers. Interpolate. The endpoint cases take the whole list on one side. On each side match a positive displacement $a$ to a negative displacement $-b$ in real multiples of the rotation above, exhausting at least one type per step. Zero displacements use singleton blocks. There are at most $K$ block coefficients over the two sides. [Detailed real allocation](radius-threshold.md#completing-integer-intervals-using-rotations)

Use the integer part of each coefficient. For a fractional part $\lambda$ of a rotation coefficient, add two partial rotations with $t=\lfloor\lambda n/2\rfloor$, omitting them if $t=0$. The combined retained count of each of the two required displacements differs from its intended fractional count by less than four. Indeed, rounding $t$ costs less than two occurrences, and each partial rotation costs less than one additional occurrence. Rounding a singleton loses less than one. Across all blocks each parent's requested count therefore changes by at most $4K$. A parent with working count zero has no retained occurrences. The $A$ leaves set aside at each active parent cover every excess. The unspent counts from this part, including the set-asides, are at most $A+4K$ per parent. The unretained positions of the partial rotations use at most $4KD$ additional leaves altogether, charged to the three initial reserves, since $n\le2D$.

For each leftover leaf at $p>1$, take a lower block with parents $p,0,\ldots,0$ of length $p$. For $p<0$, take an upper block with parents $1,\ldots,1,p$ of length $1-p$. Both are permutations by direct substitution. The ordinary leftovers require at most $h(A+4K)D$ further leaves at $0,1$. Each unspent reserve leaf at $-1$ can now be added together with one at $1$. There are at most $B$ of these and the reserve at $1$ started at $2B$. Unused leaves at $0$ or $1$ extend the upper or lower endpoint singly. The definition of $B$ funds all these operations.

## Placing an arbitrary core

Label the chosen path, in order, $-1,1,0$. Its edge sums are $0,1$. Grow the rest of $H-\{x,y\}$ in parent-before-child order. For a required child at $p\ge0$, put it at $U+1$ with $p$ filler leaves immediately above it at $-1$. The child edge occupies the top weight and the other edges fill the rest. For $p<0$, put the child at $U+1-p$ with $-p$ leaves at $1$ in the preceding positions. These steps introduce only positive core labels. The increase is at most $|p|+1$, so $U+1$ at most doubles at each step here.

Write $p,q$ for the already placed parents of $x,y$. One can now give $x$ any sufficiently negative label $X$ and $y$ any sufficiently positive label $Y$. Place $Y$ first by the upper rule at $q$, padding at $0$ as necessary. When $p>0$ the lower block of length $p$ places $X$ at its bottom, after padding below at $1$. When $p\le0$, set $a=1-p$, $b=Y-1$ and take $b\ge a$. In a lower block on $[0,b]$ use the cycle
$$
0\longmapsto b\longmapsto b-a\longmapsto b-a-1\longmapsto\cdots\longmapsto 0
$$
and fix unused positions. If $b=a$, the cycle is just $0,b,0$. The first row uses one leaf at $Y$, the second row places the required child at $p$ immediately below the current interval, and all other parents are $0$ or $1$. Padding below first gives the desired $X$. These rules use only the three designated parents for fillers, except for at most one leaf at $Y$.

More precisely all choices $X\le-F$, $Y\ge F$ are feasible for $F=2^{h+4}$. The initial endpoints and $p,q$ are bounded by the preceding doubling estimate. Begin at $X=-F,Y=F$. If $m_y\le m_x$, decrease $X$ by the fewest nonnegative steps that put $\sum_v p_vm_v\le M/2$, then increase $Y$ by the nearest nonnegative number of steps to that target. If $m_x<m_y$, first increase $Y$ until the sum is at least $M/2$ and finish by decreasing $X$. This gives
$$
M/4\le W=\sum_v p_vm_v\le3M/4
$$
because the last step size is $w\le M/2$. The changes in either coordinate, multiplied by its population, are at most $(F+3)M$: the starting sum is between $-FM$ and $FM$, and the first crossing overshoots by at most its step size. It follows that $D\le4FM/w$. The implementation can start at the smaller threshold given by the current interval endpoints.

The size bound can also use the height of the core. Let $b_j$ count vertices of $H-\{x,y\}$ at positive distance $j$ from the initial path. Process one whole distance level at a time. Each parent on that level was already present at its start, so $U+1$ grows by a factor at most $1+b_j$. Thus $F=8\prod_j(1+b_j)$ suffices. In (1) the factor $2^{h+18}$ may be replaced by $2^{16}\prod_j(1+b_j)$, giving a polynomial bound in $h$ at any fixed core diameter.

The finished seed has at most $4D$ filler leaves. Its upper endpoint is at most $Y+\max(q,0)$ and its lower endpoint is either $X$ or $X-b$. All filler parents have magnitude at most one except the single possible leaf at $Y$, so using the seed changes the weighted sum by at most $5D$. Condition (1) implies $r\ge2000(h+1)^2D$ and $w\ge1$. This supplies the seed and the first reserves. To check that removing leaves keeps $0\le W'\le M'$, the change in weighted sum is at most $5D+B+AhD$, and the number removed is at most $4D+4B+Ah$. Their sum is less than $M/4$, since $J\le40(h+1)^2$, $Ah\le10(h+1)^2$, and $M\ge r$. Thus the exact completion applies. A consecutive interval has balanced residue counts at every modulus. This proves Theorem 1.

## Both sides of a central edge

For Theorem 2 choose the five largest branches. If both sides occur, let $u$ be the center on the majority side and $v$ the other center. Label the central edge $2,-2$. Give two selected parents at $u$ the labels $-1,0$ and one at $v$ the label $1$. These five vertices occupy $[-2,2]$ with weights $[-1,2]$. Choose another selected parent at $u$ as $x$, and the remaining selected parent as $y$.

If all five are at $u$, give $u,v$ the labels $2,-3$. Give three selected parents at $u$ the labels $-1,0,1$, and give one branch parent at $v$ the label $3$. Such a branch exists because the diameter is five. Add a filler leaf labeled $-2$ at $0$. The vertices are $[-3,3]$ and the weights are $[-2,3]$. The two other selected parents serve as $x,y$.

Place the remaining branch parents above the interval by the upper rule. Each insertion has width at most four because the parent is a center. Here one can take $F=8(h+1)$ for the two adjustable labels, so $D\le32(h+1)M/t$. Both $r,w$ are at least $t$, and (2) implies $r\ge2000(h+1)^2D$. The same resource and moment bounds apply, including the one initial filler in the second case. This proves Theorem 2.

## Verification

The standard-library constructor uses rational arithmetic for the allocations. Its checker independently counts attachments at every core vertex, reconstructs the seed edges and tests every block's full permutation. For the order-233,005 example it also constructs every edge and recomputes both intervals directly. The other examples use repeated blocks, including an order-9,000,000,000,009 tree and all six placements of the five selected branches across the central edge. The separate rotation check verifies 17,188 permutations and their retained counts. [Construction and checker](many_leaf_parents.py)

~~~sh
python3 -B -m research.hub.many_leaf_parents
lean research/hub/PartialRotation.lean
~~~
