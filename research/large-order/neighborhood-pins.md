# Excluding a fixed forest with components of diameter at most four

**Theorem.** There is an absolute constant $C$ with the following property. Let $F$ be a nonempty finite forest with $m$ components, each of diameter at most four, and maximum degree $\Delta(F)$. Every tree excluding $F$ as an induced subgraph is $k$-cordial whenever its order is at least
$$
Ck\max\{\sqrt m,\Delta(F),1\}.
$$
This holds at every positive modulus, uniformly over the forest. In particular, along any sequence of counterexamples with $|T|/k$ tending to infinity, each fixed such $F$ eventually occurs as an induced subgraph.

For example, fix $t$. Above an absolute constant times $tk$, a counterexample would contain $t^2$ pairwise nonadjacent trees, each consisting of a center, $t$ neighbors and $t$ original leaves at each of those neighbors.

## Prescribed labels with few prescribed neighbors

Let $H$ be a tree of order $h\le Ak$, and let $P$ be a set in one bipartition of $H$ with distinct prescribed residues modulo $k$. Suppose at most $u$ vertices have more than $D$ neighbors in $P$. Both the vertex and edge counts can be bounded solely in terms of $A,D,u$, independently of all other degrees in $H$.

Let $X$ be the exceptional set, $x=|X|$, and $s=\max(1,\lceil\sqrt x\rceil)$. All vertices of $X$ lie in the bipartition opposite $P$. Let $Y$ consist of vertices outside $P$ with more than $s$ neighbors in $X$. These lie on the side of $P$. The forest on $X\cup Y$ has at least $(s+1)|Y|$ edges and at most $x+|Y|$ edges. Thus $|Y|\le x/s\le s$. Give each vertex of $Y$ label zero.

Root $H$ arbitrarily. For $v\in X$, let $a(v)$ be the prescribed integer label of its parent in $[0,k)$ if that parent lies in $P$, and zero otherwise. Sort $X$ by $a(v)$, and assign the vertex in position $i$, indexed from zero, the label $q_i=\lfloor i/s\rfloor$ reduced modulo $k$. There are at most $s$ different integer values $q_i$, each occurring at most $s$ times. The load from $X$ in a residue bin is at most $s(1+\lceil x/s\rceil/k)\le 2s+A$. Adding $P,Y$ costs at most $1+s$.

Every edge between fixed vertices goes between $X$ and $P\cup Y$. For an edge with child in $X$, its ordinary sum is $a(v)+q_i$. Both summands are nondecreasing over this sublist, so equality forces $q_i$ to stay fixed. The multiplicity of each integer sum is at most $s$. These sums are in $[0,k-1+\lceil x/s\rceil]$, giving at most $s(2+\lceil x/s\rceil/k)\le 3s+A$ per residue. For edges going from $X$ to children in $P$, each fixed integer $q_i$ contributes at most once to each bin, since the prescribed child labels are distinct and each child has a single parent. Edges going from $X$ to children in $Y$ number at most $s$ in total. Thus the fixed edges cost at most $5s+A$ per bin.

Root each component induced by the remaining vertices and label it in parent-before-child order. Each vertex has at most $D$ neighbors in $P$, at most $s$ in $X$, at most $s$ in $Y$ and at most one earlier neighbor in its own component. Write $d=D+2s+1$ and $Q=\max(6s+\lceil A\rceil+2,4\lceil A\rceil(d+1))$. Fewer than $2h$ observations have been assigned across both histograms. Fewer than $2h/Q\le k/(2(d+1))$ bins have count at least $Q$. Avoid those bins for the new vertex and its at most $d$ edge observations. Each bin forbids at most $d+1$ choices. Some label remains, and insertion adds at most $d$ observations to one bin. Both final histograms are bounded by $Q+d=O_A(1+D+\sqrt u)$.

## A linear bound from the distribution of leaf parents

Fix integers $b\ge1,D,u\ge0$. Write $H$ for the subtree induced by the nonleaves of $T$. Call a vertex of $H$ rich if it has at least $b$ neighbors that are leaves of $T$. Suppose at most $u$ vertices of $H$ have more than $D$ rich neighbors in $H$. Any counterexample then has order $O(k(1+b+D+\sqrt u))$, with an absolute implied constant.

Indeed, for a counterexample the [nonleaf bound](hall-pools.md#bounds-for-every-counterexample) gives $h\le Ak$ with absolute $A$. Sites below the richness threshold contribute at most $bh$ leaves. Rank the rich sites in each bipartition separately by their leaf populations. The first fifteen ranks contribute $O(k)$ by the [degree theorem](gap-path.md). The [interval and path estimate](interval-paths.md#nested-intervals-of-parent-labels) with $\delta=1/2$ bounds the sum of $rp_r$ over existing dyadic ranks from 16 through $\sqrt k$ by $O(k)$.

For the dyadic ranks from $\sqrt k$ through $k$, use the [shared jump lists](leaf-routing.md#sharing-the-leaves-at-different-population-sizes) with fixed lower exponent $1/2$. The number of digits at these ranks is bounded by an absolute constant. Every holder belongs to the ranked rich sites in the chosen bipartition, and holders have distinct labels. Apply the preceding pinning lemma, which has no upper restriction on the number of sites. It supplies a constant bound for both histograms and their difference. In the sharing proof this replaces the sparse-pinning estimate (2), its only use of the upper rank restriction. For uniformity, $Q+d=O_A(1+D+\sqrt u)$, so the core defect bound is also $O_A(1+D+\sqrt u)$. The digit count, list multiplicity and rounding error in the sharing proof are absolute at lower exponent $1/2$. Its filling height $L$, population cutoff $64L+4e$ and the coefficient of $k$ in its threshold (4) are all linear in one plus the defect bound. The discarded populations and the resulting dyadic sum therefore cost $O_A(k(1+D+\sqrt u))$. A rank $r$ pays for the populations from $r$ through $2r-1$, including a truncated final interval. Beyond rank $k$, the [single-size bound](leaf-routing.md#a-sufficient-condition-at-one-population-size) at $r=k$ gives a constant population at each site, and there are at most $Ak$ sites. Together with the $bh$ leaves at sites of lower population, this proves the claimed order bound. Both rank arguments require only $k$ sufficiently large in terms of the absolute $A$ and the fixed exponent $1/2$. The finitely many smaller moduli obey $n=O(k)$ by the [unrestricted bound](interval-paths.md), independently of $b,D,u$.

## Extracting induced components

Set $t=\max(1,\Delta(F))$, $b=t$, $D=t+2$ and $u=4m-2$. If the neighborhood hypothesis fails, at least $4m-1$ centers have at least $t+3$ rich neighbors. Choose $2m$ such centers in the same bipartition. Call a rich neighbor shared if it meets at least two of these centers. If there are $j$ shared neighbors and $e$ incidences with them, the induced bipartite forest gives $2j\le e\le 2m+j-1$, hence $e\le4m-2$. At most $m-1$ centers have four or more shared neighbors. Select $m$ centers with at most three. Each has at least $t$ private rich neighbors. Select $t$ there, and $t$ original leaves at each.

All centers are in one bipartition and all chosen rich neighbors in the other. Privacy excludes edges to a different chosen center. The selected leaves have degree one in $T$. The selected vertices thus induce $m$ mutually nonadjacent depth-two trees with the stated original leaves. Each component of $F$ has a center of eccentricity at most two. Both the number of branches at its center and the number of leaves needed on any branch are at most $t$, so it embeds in one of the trees as a connected, hence induced, subtree. Taking one copy per component gives an induced $F$. Therefore an $F$-free tree satisfies the neighborhood hypothesis, and the uniform order estimate is $O(k(1+t+\sqrt m))$. The empty forest occurs in every tree.

## Reproduction

The checker independently recounts bins on prescribed-site trees and tests extraction by examining every edge of the original host at the selected vertices. The replay checks 21,277 prescribed-site labelings and 1,761 extraction instances, including 875 induced witnesses and structured hosts through order 23,142. [Construction](../large_order_neighborhood_pins.py) · [Independent checks](../check_large_order_neighborhood_pins.py)

~~~sh
python3 -B -m research.check_large_order_neighborhood_pins
~~~
