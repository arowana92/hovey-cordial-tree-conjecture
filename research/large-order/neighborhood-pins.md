# Excluding a fixed forest with components of diameter at most four

**Theorem.** For every fixed finite forest $F$ whose components have diameter at most four, there is a constant $C_F$ such that every tree of order at least $C_F k$ that contains no induced copy of $F$ is $k$-cordial. This holds at every positive modulus. Equivalently, in any sequence of counterexamples with $|T|/k$ tending to infinity, each such $F$ eventually occurs as an induced subgraph.

For example, fix $t$. Above a constant times $k$, a counterexample would contain $t$ pairwise nonadjacent trees, each consisting of a center, $t$ neighbors and $t$ original leaves at each of those neighbors. The numerical constant is allowed to depend on $t$.

## Prescribed labels with few prescribed neighbors

Let $H$ be a tree of order $h\le Ak$, and let $P$ be a set in one bipartition of $H$ with distinct prescribed residues modulo $k$. Suppose at most $u$ vertices have more than $D$ neighbors in $P$. Both the vertex and edge counts can be bounded solely in terms of $A,D,u$, independently of all other degrees in $H$.

Give the exceptional vertices outside $P$ label zero. The vertex count at any residue is initially at most $u+1$. There are no edges between prescribed sites. At any one additional fixed vertex, edges to prescribed sites have distinct sums, so these contribute at most $u$ to a weight bin. There are at most $u$ edges between the additional fixed vertices. The initial edge count per bin is at most $2u$.

Root each component induced by the remaining vertices and label it in parent-before-child order. A vertex now meets at most $D$ prescribed neighbors, at most $u$ additional fixed neighbors and at most one previously labeled vertex of its own component. Write $d=D+u+1$ and $Q=\max(2u+2,4\lceil A\rceil(d+1))$. At any time fewer than $2h$ observations have been assigned across the two histograms. Fewer than $2h/Q\le k/(2(d+1))$ bins have count at least $Q$. Avoid those bins for the new vertex and its at most $d$ edge observations. Each bin forbids at most $d+1$ residue choices. Some label remains, and insertion adds at most $d$ observations to one bin. The final counts are at most $Q+d$.

## A linear bound from the distribution of leaf parents

Fix integers $b\ge1,D,u\ge0$. Write $H$ for the subtree induced by the nonleaves of $T$. Call a vertex of $H$ rich if it has at least $b$ neighbors that are leaves of $T$. Suppose at most $u$ vertices of $H$ have more than $D$ rich neighbors in $H$. Any counterexample then has order $O_{b,D,u}(k)$.

Indeed, for a counterexample the [nonleaf bound](hall-pools.md#bounds-for-every-counterexample) gives $h\le Ak$ with absolute $A$. Sites below the richness threshold contribute at most $bh$ leaves. Rank the rich sites in each bipartition separately by their leaf populations. The first fifteen ranks contribute $O(k)$ by the [degree theorem](gap-path.md). The [interval and path estimate](interval-paths.md#nested-intervals-of-parent-labels) with $\delta=1/2$ bounds the sum of $rp_r$ over existing dyadic ranks from 16 through $\sqrt k$ by $O(k)$.

For the dyadic ranks from $\sqrt k$ through $k$, use the [shared jump lists](leaf-routing.md#sharing-the-leaves-at-different-population-sizes) with fixed lower exponent $1/2$. The number of digits at these ranks is bounded by an absolute constant. Every holder belongs to the ranked rich sites in the chosen bipartition, and holders have distinct labels. Apply the preceding pinning lemma, which has no upper restriction on the number of sites. It supplies a constant bound for both histograms and their difference. In the sharing proof this replaces the sparse-pinning estimate (2), its only use of the upper rank restriction. The discarded populations, the threshold in (4) and the resulting dyadic sum are consequently all bounded by constants times $k$. A rank $r$ pays for the populations from $r$ through $2r-1$, including a truncated final interval. Beyond rank $k$, the [single-size bound](leaf-routing.md#a-sufficient-condition-at-one-population-size) at $r=k$ gives a constant population at each site, and there are at most $Ak$ sites. This proves the claimed order bound, enlarging its constant at the finitely many small moduli by the [unrestricted bound](interval-paths.md).

## Extracting induced components

For a nonempty $F$ take $t=|V(F)|$, $b=t$ and $D=u=2t-2$. If the neighborhood hypothesis fails, at least $2t-1$ centers have at least $2t-1$ rich neighbors. Choose $t$ of these centers in the same bipartition. Two centers share at most one neighbor, since $H$ is acyclic. At each center at most $t-1$ rich neighbors are adjacent to any other chosen center. Select $t$ private rich neighbors there, and $t$ original leaves at each.

All centers lie in one bipartition and all chosen rich neighbors in the other. Privacy excludes edges from a chosen neighbor to a different chosen center. The selected leaves have degree one in $T$. Hence the selected vertices induce exactly the claimed disjoint depth-two trees. Each connected component of $F$ has a center of eccentricity at most two and embeds as a connected subtree of one of these trees. A connected subtree in a tree is induced. Taking one copy per component produces an induced $F$. This proves the theorem. The empty forest occurs in every tree.

## Reproduction

The checker independently recounts bins on prescribed-site trees and tests extraction by examining every edge of the original host at the selected vertices. The replay checks 21,270 prescribed-site labelings and 1,761 extraction instances, including 875 induced witnesses and structured hosts through order 12,064. [Construction](../large_order_neighborhood_pins.py) · [Independent checks](../check_large_order_neighborhood_pins.py)

~~~sh
python3 -B -m research.check_large_order_neighborhood_pins
~~~
