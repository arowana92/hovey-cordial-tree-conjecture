# An exact parity obstruction for inserting a tree at distinct ports

**Theorem.** Fix $D$ and $0<\epsilon<1$. For every sufficiently large $k$, remove $t-1$ edges of a prescribed $k$-cordially labeled tree. Attach each resulting component to a distinct port of a tree $U$ on $k$ new vertices, where $1\le t\le k^{1-\epsilon}$ and $\Delta(U)\le D$. Write $W_j$ for the removed weights, $a_i$ for the old entering labels, $r_i$ for the free ports, $S=\sum\mathbb Z_k$, and $T=\sum W_j-\sum a_i-S$ in $\mathbb Z_k$. The prescribed old labels extend **unless all four conditions hold**.

1. The modulus $k$ is even.
2. Every free degree $d_U(v)+\mathbf1_{v\text{ a port}}$, counting its entering edge, is even.
3. All old edge bins have the same size.
4. $T$ is odd.

When all four hold, extension is impossible. When extension is possible, in each histogram the net increment is one per bin, with at most one transfer of an extra unit from an old high bin to an old low bin.

**Smallest-counterexample consequence.** At sufficiently large $k$, a smallest counterexample has no connected $k$-vertex part of maximum internal degree at most $D$ with between one and $k^{1-\epsilon}$ edges to its complement at distinct vertices of the part. Remove the part and connect the outside components by a tree on their old attachment vertices. By minimality this smaller tree has a cordial labeling. Its edges cannot be uniform. Indeed the original order would then be one modulo $k$, already excluded by deleting and restoring a single leaf. The theorem restores the entire part. There is no restriction on the outside degrees or the number of leaves of the part.

## Necessity and actual obstructions

If all old edge bins are uniform, they must again be uniform after insertion, which adds $k$ net edges. Their net sum must therefore be $S$. When $k$ and every free degree are even, the contributions from all free labels vanish modulo two. The actual net edge sum is $\sum a_i-\sum W_j\pmod2$. Thus odd $T$ rules out every choice of free labels.

For an explicit family take even $t\ge4$ and even $k\ge t+3$. Use a subdivided $t$-arm star on $k$ free vertices with all tips as ports. Take the old star with center zero and one leaf of each residue. Remove $t-1$ leaf edges at labels $0,\ldots,t-2$, using those detached leaves as old sites. In the remaining component choose an old site of parity opposite to $S$. The old stars are cordial with uniform edge counts, the deleted labels cancel the detached sites, and $T$ is odd. This obstructs extending the specified labeling. The resulting tree may be labeled afresh.

## Which old bins can move

At least two leaves outside the ports suffice by the [two-leaf theorem](two-leaf-repair.md), and one such leaf suffices by the [uniform classification](sparse-ports.md) for $t\ge3$. We treat one and two ports separately below. For the remaining case assume every leaf is a port and $t\ge3$. Put
$$
 \delta_v=d_U(v)-2+\mathbf1_{v\text{ a port}},\qquad
 h=\gcd(k,\delta_v:v\in U).
$$
All coefficients are nonnegative and sum to $t-2>0$. For $h=1$, the uniform theorem applies with at least two positive positions. With a single positive position $h=\gcd(k,t-2)=1$ and the [single-joint repair](three-port-repair.md) applies. Hence take $h>1$. This number is bounded in terms of $D$, so $k/h>1$ for large $k$.

Write $E=B_e-F_e$ if a low old edge bin $B_e$ is duplicated and a high bin $F_e$ is omitted, and $E=0$ for no change. Similarly write $V=B_v-F_v$ for vertices, or zero. Equating the net sum of edge labels to $S+E$ gives the required moment on the positive positions
$$
                        \sum_v\delta_v x_v=T+E-2V.                 \tag{1}
$$
We first arrange divisibility by $h$. We can always use at least one genuine transfer outside the exceptional parity case.

For any divisor $m\mid k$, if no transfer takes a high bin to a low bin with difference $b\pmod m$, the high set is a union of classes modulo $\gcd(m,b)$. Indeed the allowed steps generate that subgroup, and failure of every transfer makes the high set forward invariant. Its size is a multiple of $k/\gcd(m,b)$. This includes the empty high set for a uniform profile. The two high-set sizes are consecutive residues $e,(e+1)\bmod k$ for edges and vertices.

- If $h\mid T$, some histogram has a mixed class modulo $h$. Otherwise both high sizes would be multiples of $k/h$. Make a transfer within that class.
- If $h\nmid T$, first try $E=-T\pmod h$. On failure $e$ is a multiple of $k/s$ for $s=\gcd(h,T)$. If $h$ is odd, the required vertex step is $T/2\pmod h$, with division in the residue group. Its failure would force the vertex high size to be a multiple of the same $k/s$. If both $h,T$ are even, the required step is $T/2\pmod{h/2}$, whose failure forces divisibility by $2k/s$. Either contradicts consecutiveness.
- It remains that $h$ is even and $T$ odd. Failure of the edge step forces $e$ even, since $s$ is odd. If $e=0$ the four parity conditions hold. Otherwise make any odd edge transfer. Such a transfer exists between nonempty high and low sets because the opposite-parity steps connect the group. Now $T+E$ is even, and the required vertex step is $(T+E)/2\pmod{h/2}$. Its failure would force the vertex high size to be a multiple of $k/\gcd(h/2,(T+E)/2)$, which is even, although that size is odd.

For each genuine transfer whose difference class $b\pmod h$ is feasible, we may keep one endpoint fixed and vary the other over at least $k/(2h)$ residues with the same difference modulo $h$. To see this, cycle through the classes $i\mapsto i+b$, each of size $N=k/h$. A feasible move joins a class with some high bins to one with some low bins. If no feasible pair has at least $N/2$ choices on one side, its destination has more than $N/2$ high bins. Its successor must have no low bins. Continuing around the cycle forces the starting class to be entirely high, contradicting the bound at the chosen feasible pair.

## Pinned labels at the joints

Use the transfers above. With no genuine edge transfer, use a common artificial $B_e=F_e$ to be chosen freely. Mark all ports and all positive positions. These include every vertex of original degree different from two. The marks must have distinct labels avoiding $F_v$ when it exists. Their induced edges and all entering edges must have distinct weights avoiding $F_e$.

Suppose $J$ is the only positive position, with $d=\delta_J=t-2$. For each compatible choice of transfers, $d x_J=T+E-2V$ has $h\ge2$ solutions. Vary one endpoint of a genuine transfer as above, fixing everything else. Each fixed old attachment label, a fixed vertex gap, or a fixed value $F_e-a_J$ when $J$ is a port excludes at most two choices of the varying bin for which it can solve the equation. This follows because its coefficient on the right is $\pm1$ or $\pm2$. There are $O_D(1)$ fixed exclusions since $t\le D+1$. Among the required joint inequalities at most one varies with the selected bin, namely the vertex gap or the prescribed edge gap minus $a_J$. At most one of the $h$ solutions equals that value. Choose a joint label avoiding all exclusions. An artificial gap can now be chosen different from the joint entering weight. Give the other ports independent distinct fresh labels. A short arm from $J$ to port $i$ has weight different from its entering weight because $x_J\ne a_i$. All remaining comparisons cost only boundedly many choices per port.

With at least two positive positions, start with a particular solution of (1). An artificial edge gap can be chosen arbitrarily. Apply the [affine family in the sparse-port proof](sparse-ports.md#choosing-the-labels-in-the-other-cases) to preserve (1). Every old comparison in that proof has a nonzero variable coefficient. A vertex or an entering edge cannot be identically equal to a prescribed gap since its unit coefficient vector is not proportional to $\delta$. An internal edge sum can be constant only if the positive support consists of its two endpoints with **equal** coefficient $c$. In that case their sum has $\gcd(k,c)=h\ge2$ possible values. Choose the particular solution whose sum avoids $F_e$, by adding $k/h$ to one endpoint if necessary. All remaining gap and collision equalities exclude $O_D(1)$ choices at their last variable, with $O_D(t)$ such comparisons per variable. The pinned embedding therefore exists in both cases.

## Realizing both transfers at once

There are $k-O_D(t)$ ordinary degree-two nonports. Select $t$ disjoint segments of nine such vertices, plus one additional segment if a vertex transfer is used. Keep their closed neighborhoods disjoint and away from the initial marks. Greedy selection works since each selected segment or initial mark forbids only $O_D(1)$ potential centers at distance at most ten.

In each of the first $t$ segments delete a middle edge $bc$ and add a wire across it joining two vertices at distance two from $b,c$ on the two outer sides. Both cut endpoints remain as leaves. Pin them to fresh labels of sum $W_j$ on the first $t-1$ cuts, and $B_e$ on the last. Pin each wire to the exact entering weight assigned to that segment, using two fresh labels. The only auxiliary edges induced on these new marks are the wires, and their weights are distinct and avoid $F_e$. Each change reconnects the two sides of its own cut, giving a tree even when the segments lie along different paths.

For a vertex transfer remove the middle vertex $z$ of the extra segment, which will ultimately carry $B_v$. Let $b,c$ be its two neighbors. Choose fresh labels for them so $P=B_v+x_b$ and $Q=B_v+x_c$ are distinct and avoid $F_e$ and every previously pinned edge weight. Join the two sides by a wire between positions at distance two beyond $b,c$, prescribed to have weight $P$. The missing vertex label $F_v$ is avoided throughout these choices. A prescribed pair sum admits two fresh distinct labels after excluding only $O_D(t)$ choices. The auxiliary graph $A$ is a tree, and every auxiliary position of degree different from two is marked.

Without a vertex transfer use vertex palette $G$ and color palette $G\setminus\{F_e\}$. With a vertex transfer use $G\setminus\{F_v\}$ and $G\setminus\{F_e,Q\}$. For the marks, the correction $\sum(d_A-2)x$ after the ordinary cuts and wires is $-S-F_e-2V$, from (1) by subtracting the cut sums and adding the wire sums. The extra segment changes it by $-x_b-x_c+P=2B_v-Q$. Thus the final correction is $-S-F_e$ without the vertex transfer and $-S-F_e+2F_v-Q$ with it.

Add six mutually isolated ordinary degree-two positions away from the marks. Use the last two to make the sum of marked labels equal the vertex-palette sum. At least six degree-two positions remain outside, and every other degree class is exhausted. Twice the vertex sum plus the computed correction is exactly the color-palette sum. The induced sums are distinct in that palette. Lemma 4.9 completes the prescribed rainbow labeling of $A$. Undoing the ordinary cuts and wires contributes $B_e$ after accounting for the old edges. In the vertex case the extra segment restores $Q$ in addition, and reinstates $z$ as the second copy of $B_v$. This realizes both target histograms. [Müyesser and Pokrovskiy, Lemma 4.9](https://arxiv.org/html/2509.05280v2#S4)

## One and two ports

With one port and at least two nonport leaves the uniform proof applies directly. Its divisor divides $t-2=-1$. No internal cut pair is needed. In the one component choose an anchor away from the marks and connect it to a nonneighboring site of the frequent internal degree. This closes the auxiliary cycle and supplies the entering weight. The representative and two-leaf adjustments proceed as in the multiple-component proof. With just one nonport leaf the free tree is a path attached at its tip. A full pendant path period extends every prescribed labeling uniformly at every modulus. [Pendant path construction](../counterexample-bound.md#shortening-paths)

With two ports and at least two nonport leaves use the two-leaf theorem. With exactly one nonport leaf $Y$ there is precisely one positive position $J$, with coefficient one. The uniform sparse-port theorem handles $T\ne0$. For $T=0$ we need only make $T'=T+E-2V$ nonzero. Any genuine edge transfer works if the old edge profile is nonuniform. If it is uniform then the vertex profile has a single high bin, and we choose a low bin at a difference not annihilated by two. In the pinned construction give $J$ the variable $X$ and $Y$ the label $X-T'$, independently varying the remaining ports. As in the uniform sparse-port proof, any comparison with identical variable vectors is already separated by $T'\ne0$. No vertex label, entering weight or pinned internal weight is constant: the latter has coefficient sum two. The gap comparisons and ordinary or extra segments therefore work exactly as above.

With two ports and no nonport leaves the free tree is a path with its tips as ports. Every $\delta_v$ vanishes. Uniform increments work if $T=0$. Otherwise use the transfer argument with $h=k$ to solve $T+E-2V=0$ **exactly**. Only the cases $h\nmid T$ are used, and their divisibility arguments did not require $h$ to be bounded. No variation over a large residue class is needed, since there is no positive position. Give the two port labels independent variables; for large $k$ they are nonadjacent. Their labels and entering weights can be chosen injectively and in the required palettes. The same segments and tree targets realize the selected changes. Failure is exactly the parity case of the theorem.

## Verification

~~~sh
python3 -B research/bounded-degree/check_port_parity.py
~~~

The [constructor](port_parity.py) supplies the transfers, pins and actual cut-tree targets. The [checker](check_port_parity.py) recomputes the signed multiset of every changed edge, both target moments and the degree classes for 1,485 successful targets. Nine use both transfers, 237 use only a vertex transfer, and 1,239 use only an edge transfer. It checks 120 failed parity cases, 12 actual obstructed star inputs, and 203,986 small histogram-pair and target combinations by literal enumeration. The one- and two-port checks add 84 successful targets and four obstructions. These finite checks verify the local calculations. The large-order completion uses the cited theorem.
