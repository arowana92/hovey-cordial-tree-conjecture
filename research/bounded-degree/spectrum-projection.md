# Prescribed edge frequencies at every divisor of the vertex order

Fix $D\ge3$ and $0<\epsilon<1$. Let $F$ be a tree or a simple connected unicyclic graph on $n$ vertices. Choose any divisor $k$ of $n$ and put $t=n/k$, $G=\mathbb Z_k$ and $S=\sum G$. The required vertex distribution is exactly $t$ in each residue. Fix a label $a$ at a specified vertex $r$. On a unicyclic graph take $r$ on the cycle, away from the unique junction if the graph has just one leaf.

Specify an entire edge histogram $H$ of nonnegative counts summing to $|E(F)|$. Write $J=\sum_{x\in G}(t-H(x))_+$ for the total shortfall from $t$. Edge $uv$ may have an additive offset $\eta_e$, with at most $b$ exceptions to one common offset. Assume
$$
                    E_D(F)+b+J\le n^{1-\epsilon}.
$$
Define the two residues and the degree coefficients by
$$
     A=\sum_{x\in G} x H(x)-tS-\sum_e\eta_e,\qquad C=tS-A,
     \qquad c_v=\deg_F(v)-1.
$$

**Theorem.** For all sufficiently large $n$, uniformly in every **proper divisor** $k$ of $n$, the specified labeling exists exactly under the conditions below.

| Graph | Necessary and sufficient condition |
|---|---|
| Tree, any anchor | $\gcd(k,c_v:v\ne r)\mid A-c_ra$ |
| Cycle | $C=0$ |
| Unicyclic graph, one leaf | Every target under the size hypothesis works |
| Unicyclic graph, at least two leaves | $\gcd(k,c_v:v\in V(F))\mid A$ |

At the remaining divisor $k=n$, the [bijective tree and ring theorem](edge-histograms.md) applies. On a tree anchored at a path endpoint it also requires $C\ne2a$. On a one-leaf graph it requires $C\ne0$. With shifted ring edges the additional condition at $k=n$ is the two-edge-tail test proved below. These statements supply all divisors, including fixed small moduli as $n$ grows.

In particular, at every proper divisor $k$ a simple unicyclic graph with a leaf, ordinary weights and the stated excess bound admits a labeling in which **both** vertex and edge residues occur exactly $t$ times. Opening any cycle edge then inserts these $n$ vertices in place of an edge of any labeled tree and increases every bin by $t$. Prescribe one port to equal the opposite old endpoint, choosing the regular port on a one-leaf graph. For a cycle with no leaves the same property holds precisely when $tS=0$, or equivalently when $k$ is odd or $t$ is even. Old degrees, old labels and old order are arbitrary.

## Sparse offsets on bijectively labeled rings

At $k=n$, allow the offsets in the unicyclic theorem, with $b$ counted in the size bound and $A$ computed as above. On a cycle and on a ring with at least two leaves the stated moment and gcd conditions still suffice. Include the original nonzero offsets among the main cuts of the [paired reconnection proof](edge-histograms.md#choosing-the-edges). If the opening itself has an offset, use its adjusted weight as $w$. After adding the fictitious shifts on the paired edges, the sum of all offsets is still $-A$. The two-free-leaf congruence and exhausted-degree identity are therefore unchanged. All original marked-edge forms retain the same variable coefficients. The new constants do not identify forms with different coefficients.

With one leaf $y$ and junction $j$ the necessary relation is $x_y=x_j+C$. If the tail has length two, write $jzy$ for its vertices. Whenever
$$
                          C+\eta_{zy}-\eta_{jz}=0
$$
the two incident weights at $z$ must be equal. Thus **some bin of $H$ must contain at least two edges**. This and $C\ne0$ are all the conditions. When the equality fails the ordinary one-leaf construction works directly, since these are the only two original edge forms that can have the same variable coefficients after eliminating $y$.

In the forced-equality case choose a repeated bin $p$ and one omitted bin $q$, which exists because $H$ has size $n$. Write $X_j=Z$, $X_y=Z+C$ and $X_z=p-\eta_{jz}-Z$. Both actual tail sums are $p$. Add the fictitious offset $q-p$ on $zy$ and reserve this pair of bins from the remaining selections. The two temporary weights are now the distinct constants $p,q$. Mark $j,z,y$ before choosing the other paired and private edges. The anchor is a regular cycle vertex, so $Z$ is free. The labels $Z,Z+C$ differ, and comparison with the third label excludes at most two values at a time. Outside the two tail edges only the cycle edges at $j$ use this variable among the original weights. Neither $z$ nor $y$ occurs in any other original edge. All private coefficient vectors are preserved. The remaining constants from paired edges are omitted bins distinct from both $p$ and $q$. This gives the same $O_D(1+E_D+b+J)$ exclusions per variable as in the [pin assignment](edge-histograms.md#assigning-the-pins). Undoing the fictitious offset uses one extra occurrence of $p$ and recovers the target even when more copies of $p$ were prescribed.

## Lifting a target and tuning an offset

Assume $t>1$. Normalize the common offset to zero, translating the entire edge histogram by the same amount. In each fiber of $\mathbb Z_n\to\mathbb Z_k$, assign the $H(x)$ occurrences to distinct lifts as far as possible. Any further copies may all use the first lift. This gives a target $H'$ of size $|E(F)|$ on $\mathbb Z_n$ with exactly $J$ omitted residues. The reduction of its histogram is $H$. A permutation of the $n$ vertex labels reduces to $t$ occurrences of every label. [Lean proof of the fiber allocation and distinctness](HistogramLift.lean)

Fix any lift $a'$ of $a$ and lift all original offsets, using zero at ordinary edges. Write $S'=\sum\mathbb Z_n$, $A'=\sum H'-S'-\sum_e\eta'_e$ initially. Reduction of $S'$ is $tS$, so $A'$ reduces to $A$. On any one edge, increasing its lifted offset by $kj$ retains its actual weight modulo $k$ and replaces $A'$ by $A'-kj$. Only one more edge becomes exceptional in the following gcd and cycle cases.

* On a tree away from the path-end exception, put $h'=\gcd(n,c_v:v\ne r)$. A multiple of $k$ can make $A'-c_ra'$ zero modulo $h'$ exactly if $\gcd(h',k)\mid A-c_ra$. Since $k\mid n$, the latter gcd is precisely the downstairs divisor. On a ring with at least two leaves the same proof applies. Here $\sum c_v=n$, so deleting the anchor coefficient does not change the gcd with either $k$ or $n$.
* On a cycle prescribe $A'=S'$ exactly by the same adjustment. This is possible precisely when $A=tS$ modulo $k$.
* On an endpoint-rooted path choose a lift $C'$ of $C$ which differs from $2a'$ modulo $n$. At least two lifts are available. Changing a lifted offset by a multiple of $k$ sets $S'-A'=C'$. The path has an unpinned degree-two vertex, so the gcd test is automatic.
* On a one-leaf graph choose a nonzero lift $C'$ of $C$. On the two-edge tail, if present, choose the lift of $\eta_{zy}$ so that $C'+\eta'_{zy}-\eta'_{jz}\ne0$ modulo $n$. At most one of its $t$ lifts is forbidden. Now set $S'-A'=C'$ by adjusting a different edge outside that tail. The original tail weights may still agree after reduction. Both adjustments preserve their prescribed offsets modulo $k$.

Absorb the at most two extra shifts by decreasing $\epsilon$ slightly. The order-$n$ theorem gives the bijection upstairs, proving sufficiency. Necessity follows directly by incidence counting with $t$ copies of every vertex label. In particular, on the one-leaf graph the prescribed difference between the tip and junction can now be zero, since their equal projected labels may be distinct lifts. The asymptotic threshold is determined by $D,\epsilon$ and the [primary tree embedding lemma](https://arxiv.org/html/2509.05280v2#S4).

## Reproduction

The [lifting routine](spectrum_projection.py) constructs the actual omitted bins, extra copies and two possible offset changes. The [independent checker](check_spectrum_projection.py) reduces the full upstairs histogram bin by bin, verifies every offset modulo $k$, recomputes the downstairs moments from graph incidences and checks the prescribed embedding cores. It accepted 408 targets and rejected 72, including 278 successful proper nontrivial quotients. Six additional bijective constructions realized a repeated weight forced on a two-edge tail. The finite checks verify the lifting and core calculations. The completion of the core uses the embedding theorem.

~~~sh
lean research/bounded-degree/HistogramLift.lean
python3 -B research/bounded-degree/check_spectrum_projection.py
python3 -B research/bounded-degree/check_edge_histogram.py
~~~
