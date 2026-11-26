# Every counterexample has order at most a constant times k log²(2k)

**Theorem.** For an absolute $C$, every $k$-counterexample has fewer than $Ck\log^2(2k)$ vertices. The [degree bound](flexible-path.md) remains $O(k\log(2k))$. These estimates apply to every tree and every modulus. At each particular modulus the earlier explicit quadratic bound is also available.

The [interval-rounding refinement](primitive.md) improves the order bound to $O(k\log(2k))$.

Two changes in the [dyadic correction proof](dyadic.md) give the order bound. An integer correction of zero mass and zero first moment needs only **squared** differences, one type per dyadic stride. Also the location of each leaf switch can be rounded along with its vertex and edge labels, so its prescribed locations have almost equal supplies without a binomial error term.

## An integer decomposition using one stride per term

Write $(\tau f)_i=f_{i-1}$ and $D_s=\tau^s-I$. Put $J=\lceil\log_2(2k)\rceil+2$. If an integer vector on the residues has sum zero, first moment zero modulo $k$, and $\|f\|_\infty\le D$, then
$$
f=\sum_s D_s^2 w_s,\qquad \|w_s\|_\infty=O(D+J).
$$
Here $s$ ranges over at most $J$ powers of two, with integer vectors $w_s$. This holds over composite and prime moduli.

First lift $f$ to an interval of length $2k$ with ordinary sum and ordinary first moment zero. If $q=\sum i f_i/k$, choose $u_i$ of total $-q$ differing by at most one. Put $f_i-u_i$ at $i$ and $u_i$ at $i+k$. This projects back to $f$ and the entries have magnitude at most $2D+1$.

In local coordinates pad an interval vector of length $m\ge5$ with a zero at each end, so its entries now occupy positions $1,\ldots,m$. Call this vector $F$. We will subtract $D_1^2 h$ with $h$ supported on $0,\ldots,m-1$, and recurse separately on the even and odd positions of the residual. Over the reals take $h_i^*=-F_{i+1}/4$. The residual is
$$
G_i^*=(F_{i-1}+2F_i+F_{i+1})/4.
$$
Both parity fibers of $G^*$ have zero mass and zero local first moment. For example, four times the even local moment is $2(M_e+M_o)+F_o=0$, where $M_e,M_o$ denote the local first moments of the parity fibers of $F$, and $F_o$ is its odd mass. This is the original ordinary moment. The odd assertion follows from zero global moment and the two zero masses.

For an integer replacement $h$, write $H_e,H_o$ for its two parity totals and $N_e,N_o$ for its two local first moments. If $F_e$ is the even mass of $F$, the exact conditions that the even residual have mass and moment zero are
$$
H_e-H_o=F_e/2,\qquad 2(N_e-N_o)+H_e-2H_o=M_e .
$$
Indeed at even indices $D_1^2 h$ takes the two even neighboring entries with coefficient one and the intervening odd entry with coefficient minus two. The total $F_e$ is even by the global mass and moment conditions. Choose $H_o$ nearest its real value with parity $F_e/2-M_e$ and set $H_e=H_o+F_e/2$. Both errors are at most one. Choose $N_o$ nearest its real value and obtain $N_e$ from the second equation. Both moment errors are at most two, since the real totals satisfy both equations. The global identities then imply the required odd mass and moment as well.

Each parity list of $h^*$ has length $u\ge2$. Round successive prefix sums down, use differences as entries, and set the last prefix instead to the chosen total. Each entry changes by at most two. Summation by parts shows the resulting first moment is within $2u+2$ of its target, using the prefix errors at most one and the chosen moment error at most two. Correct this integer discrepancy by unit transfers between coordinate zero and coordinates at distances at most $u-1$. At most $\lceil(2u+2)/(u-1)\rceil\le6$ transfers suffice: take distance $u-1$ until the last smaller transfer. Thus each entry of $h$ differs from $h^*$ by at most eight. Each new residual entry is within 32 of the averaging formula for $G_i^*$.

After a split the global stride doubles. Local length is at most $(m+3)/2$, so there are at most $J$ levels. At length at most four, take two successive prefix sums to obtain an integral second antiderivative. Its tail vanishes by the two ordinary moment conditions and its magnitude is at most 16 times the current bound. At every level the bound on residual entries grows by at most 32. Thus every recorded coefficient has magnitude $O(D+J)$ before projection. Different fibers at a fixed stride occupy distinct congruence classes modulo that stride. Padding expands either end of the global support by at most the sum of the earlier strides, and every stride used is $O(k)$. The total interval still has length $O(k)$, so projection back modulo $k$ aggregates only a bounded number of coefficients in any bin at each stride. Telescoping proves the decomposition.

## Labeling the parts with few constraints

We use the [group rounding lemma](flexible-path.md#subdividing-edges-with-controlled-multiplicities). If a choice contributes at most $d$ unit entries to histogram or quota rows, one choice per group can attain the sum of their individual means to within $2d$ in every row.

For the unplanted part of a tree, a variable either labels one vertex, or labels two nonadjacent vertices with fixed offsets. The latter arise from pairs of leaf parents. Identify the vertices controlled by the same variable. The multigraph of edges between variables has no loops, and any $a$ variables span at most $2a-1$ edges, since the original graph on at most $2a$ vertices was a forest. A fixed unary observation may also prescribe a vertex bin or an edge to an already planted neighbor. In the application there are only a bounded number of such initial observations per variable.

Remove an independent set of current vertices of degree at most eight, counting parallel edges. At least half of the vertices have degree at most eight by the edge bound, and greedy selection in that set retains at least a ninth of them. Repeat for $O(\log(2n))$ layers. In reverse order each variable has at most eight incident edges to earlier variables. Assign to it its own unary observations and these edge observations. Each now depends on its label with unit coefficient, giving a uniform bin for a uniform choice of the base residue. No two variables of this layer are adjacent. Rounding their columns therefore incurs only constant error per row per layer. All free vertex and edge lists together lie within $O(\log(2n))$ per bin of the appropriate averages. The same argument on the free forest with planted degree-two triples uses one variable per free vertex and at most one additional pinned-neighbor observation at a buffer.

## Enough switches at every required location

For a possible counterexample the [earlier order estimate](flexible-path.md) gives $\log(2n)=O(J)$, and its maximum degree $\Delta$ is $O(kJ)$. Use the [two kinds of switches](dyadic.md#supplies-on-leaves-at-different-parents) with *both strides equal to* $s$. A switch then changes exactly one histogram by a signed $D_s^2\mathbf e_x$ and preserves the other. The duplicate middle label or weight in such a switch is permitted. We need $R=C_1J$ switches of each kind and sign at each $x,s$, with a sufficiently large absolute $C_1$. The total requirement is $O(kJ^2)$.

If fewer than $n/32$ vertices are leaves, there are a positive fraction of $n$ disjoint five-vertex sites of degree two as in the earlier proof. Use its paired triples for both signs and both choices $z=0,1$, with exact equal supplies over $x$. Their planted vertices and internal edges have exactly uniform aggregate counts, including at even $k$ by the paired doubled residues. Label the free part by the preceding layer argument. Keep an unplanted degree-two vertex and a leaf for the two moment changes. This uses at most a small fraction of the available sites when $n\ge CkJ^2$.

Otherwise pair leaf parents in the two bipartition classes separately, sorting by their leaf counts. As in the earlier proof, capacity is at least $(L-2\Delta)/2$ leaf pairs for $L$ leaves. Assign disjoint parent pairs to each combination of stride, sign and kind. Assign exactly $(R+10)k$ actual leaf pairs to each combination, discarding the surplus capacity of its last parent pair. The demand and the discarded capacity are respectively $O(kJR)$ and $O(\Delta J)$, both $O(kJ^2)$. A sufficiently large $C$ leaves at least one unplanted leaf.

First label the nonleaves with the required offsets $P,P-s$ for a vertex switch and $P,P+s$ for an edge switch. Use the layer argument on the identified parent pairs. Next give **each actual leaf pair** a choice among all locations $x\bmod k$. In the forward orientation a vertex switch takes vertex labels $x,x+2s$, which switch to $x+s,x+s$ at the two parents. For an edge switch prescribe weights $x,x+2s$ and compute vertex labels by subtracting the parents. The reverse orientations start with the switched lists, with the same parent offsets. For every fixed pair of parent labels a uniform $x$ gives a uniform count contribution per bin in both histograms.

Include one more unit entry in the row for the chosen combination and $x$. Each column contributes two vertex entries, two edge entries and one quota entry, for total mass five. Give the unplanted leaves their usual residue choices in the same step, contributing one vertex and one edge apiece. The group rounding lemma changes every histogram bin and every location quota by at most ten from its mean. Every location quota was $R+10$ in the mean, so all required supplies are at least $R$. The resulting whole-tree histograms deviate from their averages by $O(J)$.

Finally in the path case adjust the independent vertex and edge moments by the unplanted degree-two vertex and leaf. In the leaf case choose balanced targets for which the two required moments agree and use the unplanted leaf for that common change. At least one of $n,n-1$ has a nonzero remainder, and sums of subsets of such a size attain every residue. These steps change only constantly many bins and spare the switches. The [original moment argument](dyadic.md) gives the details. Apply the squared-difference decomposition to each residual, which now has zero mass and zero moment. All coefficients are $O(J)$, so the two supplies permit every required signed change. Both target histograms are attained. This excludes a counterexample when $n\ge CkJ^2$ and proves the theorem.

## Verification

The independent arithmetic check reconstructs every entry by adding three explicit terms per coefficient. It covers 1,475 exhaustive small vectors and 200 larger vectors. Four contracted-tree and quota checks reconstruct the observations from the uncontracted edges. Twelve whole trees, of orders up to 69,920, exercise 531 switches and verify the final counts of the original edges and vertices. Lean checks the rounded parity choice and the resulting moment equation. The general order bound follows from the estimates above. [Integer construction](../large_order_diagonal.py) · [Reconstruction and whole-tree checks](../check_large_order_diagonal.py) · [Lean arithmetic](SquaredSplit.lean)

~~~sh
python3 -B -m research.check_large_order_diagonal
lean research/large-order/SquaredSplit.lean
~~~
