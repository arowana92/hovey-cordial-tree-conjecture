# Exact cordiality from a long bare path at every modulus

**Theorem.** Fix $D\ge3$ and $s\ge1$. There is a length $L(D,s)$ for which the following holds simultaneously at every positive modulus. If a tree has at most $s$ vertices above degree $D$ and has a path with at least $L(D,s)$ internal vertices all of degree two, then the tree is $k$-cordial. The ends of the path can lie anywhere. There is no bound on the distances between the high-degree vertices, their degrees, or the tree order.

**Consequence.** Fix $l,s$. Among trees obtained from a tree with at most $l$ leaves by attaching arbitrary leaf populations at at most $s$ vertices, there are only finitely many counterexample pairs $(T,k)$ up to isomorphism. In particular, any fixed finite tree can be arbitrarily subdivided and decorated at boundedly many sites. Once the total number of subdivisions is sufficiently large, all such trees work at **every** modulus.

To see this, the degree of the original tree is at most $l$. Suppressing its degree-two vertices leaves boundedly many edges in terms of $l$, including the separate case of a path. Marking $s$ more vertices splits these edges into boundedly many segments. Each segment still has degree-two internal vertices after the decorations. A long segment gives the theorem. With all segments short the ordinary order, hence the number of nonleaf vertices after decoration, is bounded. Apply the [finiteness theorem at bounded nonleaf count](universal-hub.md#cordiality-and-finite-exceptions). This conclusion allows both the lengths and the leaf populations to vary together.

There is also a restriction on every remaining counterexample in the degree class. Delete the leaves directly adjacent to its high-degree vertices, leaving $h$ vertices and $l$ leaves, with $h\ge2$. In this ordinary tree suppress degree-two vertices except at the original sites. The resulting tree has at most $2l+s$ edges, including the case of a path. Each corresponding segment has at most $L(D,s)$ edges, since its interior vertices also have degree two in the original tree. Consequently
$$
h-1\le L(D,s)(2l+s).
$$
Together with the [concentration theorem](concentrated-leaves.md), this confines any counterexample sequence at growing moduli in this class to ordinary trees of sublinear order in $k$ and with a positive proportion of leaves if that ordinary order grows.

## A bridge giving a prescribed edge weight

Given two labeled endpoints $p,q$, put 21 new vertices between them. The new edge multiset can equal the multiset of the 21 new labels plus one prescribed weight $w$. For use in a sparse tree we need the following more precise placement. All 21 labels are affine functions of one parameter with bounded nonzero integer slopes. Any two equal slopes have distinct intercepts modulo $k$, for all sufficiently large $k$. This includes zero endpoint labels.

Grow ten vertices from $p$. For parameter $X$ the first arrival is $a=X$ if $p\ne0$ and $a=X+1$ if $p=0$. The second is $b=X+p$. The first step contributes $[b]-[X]$ to the edge histogram minus the vertex histogram. After the second arrival the terminal is $a+b$. In general place the running terminal as the next vertex, then add its parent label to the terminal. Use three ordinary arrivals in the ten-vertex arm and four in an eleven-vertex arm. Use the [seven-edge transfer](../large-order/GapPath.lean) on the last seven, from $X$ to the terminal. Each entire arm now adds identical vertex and edge histograms. At the end of the shorter arm the arrival is $9X+c_p$ and at the end of the longer one it is $14Y+c_q$, where the constants are the respective arrivals at parameter zero. [Lean endpoint and joining identities](PathBridge.lean)

Let $d=w-c_p-c_q$. Set $X=-3d+14z$ and $Y=2d-9z$. The edge joining the two final arrivals weighs $w$, since $9(-3)+14(2)=1$. In order from the exterior endpoint, the slopes before these substitutions are

| Arm | Slopes |
|---|---|
| Ten | $1,1,2,3,-8,5,4,-3,-5,9$ |
| Eleven | $1,1,2,3,5,-13,8,6,-5,-8,14$ |

The initial two intercepts are distinct even at a zero parent. An equality of slopes between arms would require $14a=-9b$. The only multiple of nine in the first row is $+9$, and the second row has no $-14$. Thus any remaining collision within the bridge or with a fixed label excludes only boundedly many $z$, also at composite moduli.

## Keeping the surplus weights available

We prove the theorem for all sufficiently large $k$ first. Call the vertices above $D$ sites. Without sites the [bounded-degree theorem](../bounded-degree/README.md) applies. Remove the leaves directly incident to sites, retaining an ordinary tree of order $h$. At $h\ge\delta k$ the [positive-density theorem](concentrated-leaves.md) already gives exact cordiality, for each fixed $\delta>0$. In the sparse case first take total order $k$. We will choose the constants in the order specified below.

Compress a long bare segment to one edge, saving $31+14C$ internal vertices for the repair. The constant $C$ will depend only on $D,s$. The segment and its endpoints survive the removal of the direct leaves, since an endpoint leaf is adjacent to an internal degree-two vertex. In the compressed ordinary tree take the smallest subtree connecting the sites. Mark all sites and all branch vertices of this connecting subtree. There are at most $2s$ marks. Its edges between successive marks are paths, called chains here. Root the compressed tree at a site with the largest removed population. Give it zero. Give the other marks the distinct positive powers $1,3,9,\ldots$ in any order. Let $P\ge1$ bound all these digits in terms of $s$.

We construct an injection on all but the saved vertices and the direct leaves at zero. Write $E,V$ for the multisets of its actual edge sums and vertex labels, counting the compressed edge. Our invariant at the end of this stage is
$$
E-V=-[0]+\sum_{i=1}^e([t_i]-[s_i]).
$$
Each $s_i$ is an occupied, nonzero vertex label. All $t_i,-t_i$ are distinct and held free of vertex labels. Also $s_i+2t_i\ne0$ modulo $k$. The bound $e\le C$ is independent of the order and populations. Each direct edge from one mark to a child mark of digit $b$ contributes its actual weight in place of $b$. At parent zero this is exact. At any other parent $a$, record $(b,a+b)$. Uniqueness of the base-three digits makes these fixed targets pairwise distinct and disjoint from the marked digits. They and their negatives satisfy all the requirements for large $k$.

Use the [common interval sampling lemma](bounded-error.md#a-common-set-of-intervals-for-the-direct-leaves) with $\eta<1/(4s)$ and with the slope and list bounds required by the individual placements below. It gives a set $S$ of at most $M$ cyclic intervals. Every bounded list of moving forms has at least $ck$ simultaneous choices outside $S$, even with a buffer of radius $\lfloor k/M\rfloor$. Here and below the lemma is used only for nonzero bounded slopes with arbitrary intercepts. The set $T=S\cap(-S)$ has size at least $(1-2\eta)k$ and boundedly many intervals. Remove the marked digits, fixed targets, their negatives and the elements with $2x=0$ from $T$.

**Direct leaves away from zero.** Put their labels in $T$. For a site of digit $p$ and population $m$, use reflected pairs of intervals of total size $2\lfloor m/2\rfloor$, and one singleton when $m$ is odd. Keep a margin of $p$ on each side in both signs. Translating a run of length $r$ and start $a$ by $p$ gives the exact differences
$$
s_j=a+j,\qquad t_j=a+\max(r,p)+j,\qquad 0\le j<\min(r,p).
$$
The targets lie above the run and the negatives of the reflected run's targets lie below it. Thus all protected values are free and mutually distinct, even for a singleton. The unpaired singleton gets a private reflected interval as well.

For detail on capacity and the additional congruence, work on the positive half $1\le x<k/2$ of $T$, with a mirror on the other half. Consume its runs from left to right. For each pair of runs of width $r$ allow $6p+1$ consecutive choices of start in addition to the two margins. The condition $s_j+2t_j=0$ excludes at most three starts per $j$ and orientation, since its slope is $3$ or $-3$. Choose a remaining start and continue after the margin. Do the same for the odd singleton. At each placement either a run is exhausted up to bounded tail waste or one site's demand for pairs or for its singleton is completed. Thus the number of intervals and the wasted space are bounded in terms of $M,P,s$. The positive half has size at least $(1-2\eta)k/2-O_s(1)$, while the demand is at most $(1-1/s)k/2+O(s)$ because the largest population is at zero. This proves availability and a constant bound on the number of recorded pairs. All subsequent moving labels will avoid $S$. The fixed values $\pm t_i$ belonging to these leaves remain available for the repair.

**Repeated short branches.** Consider side branches off the connecting subtree, initially at its marks. Every such branch has bounded degree. There are boundedly many rooted shapes with height below ten (height counts vertices from the top). At each mark and for each such shape save at most three copies and group the rest into $2w$ copies, $w$ odd, as in the [signed interval construction](bounded-error.md#many-copies-of-a-short-branch-in-two-intervals-per-vertex). Use it before assigning any other ordinary vertices. All internal sums in the group give precisely the nonroot vertex intervals. At a parent $p$ its two root intervals shift by $p$, producing the above pairs on each interval. At zero the entire group is exact.

Use a buffer of $P$ on each end of every vertex interval and keep these enlarged intervals pairwise disjoint and outside $S$, avoiding all previously occupied or protected ordinary values. The signed intervals are symmetric, so this also protects the negatives of all new targets. At this stage previous ordinary values lie in boundedly many enlarged intervals and singletons. The number of parameters excluded by interval intersections is $O_{D,s}(h+1)$, by the length-sum count in the signed interval construction. For each of the boundedly many new pairs exclude also $s_j+2t_j=0$. Its slope in the signed scale is three times the nonzero signed root digit, so it excludes boundedly many choices even at composite $k$. Take $\delta$ sufficiently small compared with the common sampling fraction, including $\delta<1/(2M)$. This places every group with the enlarged buffers. The number of errors per group is at most $2P$.

## Connecting the marked vertices and finishing the branches

For each chain with internal vertices, work from its marked parent toward its marked child. While there are more than ten internal vertices remaining, label ten of them as one [neutral batch](linear-hub-batches.md#absorbing-an-entire-bounded-forest-at-once). In the same batch label all currently exposed short side branches in full. Their parents can be at any already assigned vertices. The actual weights of this batch equal its new vertex labels. Only side branches at the new chain vertices are newly exposed. Label the final one through ten internal vertices singly. At such a vertex choose a free label $y$ with parent $q$. If $q\ne0$ record the pair $(y,y+q)$. At the last internal vertex also record $(b,y+b)$, where $b$ is the fixed child mark. The latter accounts for its incoming edge. When two targets arise here their difference is $q-b\ne0$, since the two parent and child marks or vertices are distinct. To finish all sides, while a tall side branch exists process ten vertices along a longest path in it and all currently exposed short branches as one neutral batch. Give the final short vertices single labels by the same rule.

Initially at most three short branches per site and shape remain. After a neutral batch, any newly exposed short branches hang off its ten path vertices. Across all chains only $O(s)$ runs of at most ten single steps can add further exposed branches before a batch clears them. Consequently every batch size and the number of final single vertices are bounded by constants in $D,s$. All neutral batches have bounded nonzero slopes; equal slopes already have distinct intercepts. For a single choice keep $y$ and the targets and their negatives outside $S$ and outside the previously occupied and reserved values. Each prospective target is $y+q$ with $q\ne0$ or $y+b$ with $b\ne0$, so no positive target is identically $y$. The only other equal-slope target comparison uses $q\ne b$ as above. Opposite-sign collisions discard boundedly many choices, as do the extra conditions $y+2(y+q)\ne0$ and $b+2(y+b)\ne0$. Each batch or single step thus costs $O_{D,s}(h+1)$ exclusions after common sampling, up to an additive constant depending on $M,D,s$.

Each marked child has now had its incoming edge accounted for. Every other labeled vertex except zero contributed its label as desired, subject only to the recorded pairs. This proves the displayed histogram formula. The list sizes and slope bounds in all sampling calls depend only on $D,s$, including the fixed-size repairs below. Choose them first, then the palette and $M$, then an integer upper bound $C$ for the number of pairs from leaf runs, groups, chains and final single vertices. None of these bounds depends on the length of the segment removed. Finally decrease $\delta$ for all linear exclusion bounds and take $k$ sufficiently large for all additive constants.

## Repairing the actual weights

Let the compressed edge join vertices labeled $u,v$. Withhold this one edge. Starting at $u$, grow a neutral batch of ten bare vertices. Its last label $p$ is fresh and differs from zero, all $s_i$ and all $\pm t_i$. For each pair $(s,t)$ use fourteen new vertices. Use the seven-edge path twice, first transferring $s$ to $z$, then $z$ to $t$. Their combined addition to $E-V$ is $[s]-[t]$. Two of the arrivals are the reserved constants $t,-t$. The twelve moving arrivals have the [intercept table](polynomial-hub.md) reproduced here for clarity.

| Slope in $z$ | Intercepts |
|---|---|
| $1$ | $0,p,s,t$ |
| $-2$ | $-p,-p-s-2t,-p-s-t$ |
| $-1$ | $0,-p$ |
| $2$ | $p+s,p+s+t$ |
| $3$ | $p+s+2t$ |

The second row needs $s+2t\ne0$ as well as $s+t\ne0$ and $t\ne0$. The first was imposed throughout. The second holds because $s$ is occupied and $-t$ was kept free. The first row is distinct by construction. Use the common palette for the moving arrivals and exclude collisions with sparse values or within the path. The last arrival is moving, so the next parent again has all the required inequalities. Use any spare $14(C-e)$ vertices in neutral batches of fourteen, treating the first seven as ordinary and the last seven as the closing transfer. The neutral-batch proof gives the same slope separation on this fixed path length.

Finish with the 21-vertex bridge to $v$, prescribing the original edge sum $u+v$. It restores exactly that contribution while placing all new labels outside $S$ and the sparse forbidden set. The original path has now been restored, with all its weights computed from the actual adjacent labels. It has $31+14C$ new vertices in total. We have $E=V-[0]$. Place the remaining unused residues on the direct leaves at zero. This gives a bijection with precisely the nonzero residues on the edges at order $k$.

For orders below $k$ in the sparse range, pad by direct leaves at a site and restrict the resulting labeling. Above $k$ induct on the direct populations, keeping the same ordinary tree and sites. Remove one direct leaf if $n\equiv1\pmod k$ and otherwise $(n-1)\bmod k$ leaves. There are enough because $h<\delta k$. Restore a single deficient edge weight in the first case and use [Hall's distinct-leaf extension](../counterexample-bound.md#removing-leaves) in the other. The bare segment survives every step. This proves exact cordiality at every tree order for sufficiently large $k$. There are finitely many smaller $k$. Each has a finite order threshold above which every tree is cordial by the [general large-order theorem](../large-order/linear.md). Increase the required bare length beyond these finitely many thresholds. This gives one $L(D,s)$ valid for all $k$.

## Reproduction

The checker evaluates both endpoints and all actual edge sums, including the joining edge. Its whole-tree checks rebuild the original parent relation with the designated internal edge subdivided or with a pendant path attached, then check both histograms. The checker covers 15,332 modular bridge identities, 144 injective bridges and 28 whole trees with 1,074,670 actual edges. Fourteen of the trees use internal subdivisions. The examples use explicit interval sets and path lengths sufficient for their own error counts. The uniform palette and length threshold in the theorem come from the counting arguments above. [Constructor](pendant_repair.py) · [Independent edge checks](check_pendant_repair.py)

~~~sh
python3 -B -m research.hub.check_pendant_repair
python3 -B -m research.hub.check_bounded_error
lean research/hub/PathBridge.lean
lean research/large-order/GapPath.lean
~~~
