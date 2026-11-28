# Prescribing both frequency lists on a tree with one fixed label

Let a tree $T$ have $n$ vertices and $k$ labels. Fix a vertex $r$ at residue $a$. The weight of $uv$ is $x_u+x_v+\eta_{uv}$ in $G=\mathbb Z_k$. All but $b$ offsets have a common value. Prescribe two lists $V,H$ of nonnegative integers indexed by $G$, with totals $n,n-1$. Write $m(F)=\sum_x xF_x$. Put $t=\lceil n/k\rceil$, $N=tk$, $J(F)=\sum_x(t-F_x)_+$, and $E_D(T)=\sum_v(\deg(v)-D)_+$.

**Theorem.** Fix $D\ge3$ and $0<\epsilon<1$. Suppose $N$ is sufficiently large in terms of $D,\epsilon$ and
$$
                  E_D(T)+b+J(V)+J(H)\le N^{1-\epsilon}.
$$
Define $A=m(H)-m(V)-\sum_e\eta_e$, $C=m(V)-A$ and $c_v=\deg_T(v)-1$. There exists a labeling with exactly the two specified histograms and the prescribed root label if and only if all the following conditions hold.

1. $V_a>0$.
2. $\gcd(k,c_v:v\ne r)$ divides $A-c_ra$.
3. If $T$ is a path and $r$ is an endpoint, put $u=C-a$. Require $V_u>\mathbf1_{u=a}$.

This includes $k\nmid n$, repeated labels in either list, and $k>n$ when the shortfall is small enough. For balanced lists and $k\le n^{1-\epsilon}$ their two shortfalls are at most $2k$ in total. Thus any pair of balanced lists passing the tests works for sufficiently large $n$ if $k+b+E_D(T)\le n^{1-\epsilon}$, after decreasing the exponent to absorb constants. The number of exceptional incidences can exceed $n/k$. The [multiple-pin result](projected-pins.md) treats many prescribed vertices under its own size conditions.

For necessity, sum all edge weights and subtract the vertex sum and the offsets. This gives $\sum_v c_v x_v=A$. Subtract once more to obtain $\sum_v(\deg(v)-2)x_v=-C$. On a path its two endpoint labels therefore sum to $C$ and must be available in $V$ with their actual multiplicities.

## A near-spanning tree with two prescribed palettes

First consider an auxiliary tree $U$ of bounded degree, order $n\le N$, and two subsets $P,Q$ of $\mathbb Z_N$ of sizes $n,n-1$. Write $p=\sum P$, $q=\sum Q$. Let $K$ be a set of pins whose labels lie injectively in $P$ and whose induced edge sums lie injectively in $Q$. Suppose $|K|+N-n$ is polynomially sublinear in $N$.

With at least two free leaves the pins extend if
$$
 \gcd(N,\deg_U(v)-1:v\notin K)\mid q-p-\sum_{v\in K}(\deg_U(v)-1)x_v .
$$
If all vertices of degree other than two are pinned, the equality $\sum_{v\in K}(\deg_U(v)-2)x_v=q-2p$ suffices. Only these two cases will be used.

For the first case reserve two free leaves. Choose an abundant degree $d\ge2$ and let $g=\gcd(N,d-1)$. Choose one free representative of each nonzero residue of $\deg_U(v)-1$ modulo $g$ that occurs. The divisibility condition allows the missing coefficient sum modulo $g$ to be assigned to those representatives. In each degree class enlarge the marked set to contain at least six vertices or the whole class, leaving at least six outside every unexhausted class. Count the reserved leaves among the marks. Lift the representatives within their assigned residue classes and label the other new marks by multiples of $g$. Avoid occupied labels, holes in $P$, and choices giving used or forbidden sums on edges to labeled neighbors. Bounded degrees and the sublinear number of holes leave choices in each coset.

At two additional isolated, mutually nonadjacent degree-$d$ positions solve $(d-1)(x+y)$ for the exact remaining coefficient sum. The right side is divisible by $g$. Avoid used labels and the holes of $P$ on both positions. Use the reserved leaves to make the plain label sum $p$ by choosing their two labels with prescribed sum. Avoid the occupied labels and all holes, including those in $Q$ on the two incident edges. A collision between these two edge sums excludes at most two choices. The degree-weighted sum is now $q$. With all exceptional degrees already pinned, add six isolated ordinary vertices. Choose four labels arbitrarily in the remaining palette and the final pair to reach $p$. The given degree-minus-two equation guarantees degree-weighted sum $q$.

These are rainbow embeddings of small degree cores. The unused abundant degree class still has at least six vertices. Lemma 4.9 extends each core in the exact palettes $P,Q$. The tree order condition follows from $N-n$ being polynomially sublinear. One may take the exponent in the embedding lemma smaller than the exponent of every size bound used here. [Müyesser and Pokrovskiy, Lemma 4.9](https://arxiv.org/html/2509.05280v2#S4) · [Degree-core construction with a single omitted color](partial-gap.md)

## Repeated vertex and edge labels upstairs

Work for now in $\mathbb Z_N$ with a tree on $n\le N$ vertices and two nearly injective multisets of the required sizes. Use $V,H,A,C$ for these upstairs data in this section. Subtract the common edge offset and translate the target edge colors accordingly. This leaves both moments unchanged.

For each vertex occurrence above the first in an occupied bin $p_i$, choose a distinct absent residue $q_i$. Replace that occurrence temporarily by $q_i$. This gives the set $P$ of size $n$. A selected vertex $v_i$ will carry $q_i$ temporarily and $p_i$ finally. Write $d_i=\deg_T(v_i)$ and $e_i=p_i-q_i$. Temporarily add $e_i$ to the offset on **every** edge at $v_i$. Returning its actual label preserves each of these weights when the added offset is removed. Similarly pair each extra edge occurrence $b_j$ with a distinct missing residue $h_j$. This gives the set $Q$ of size $n-1$. On a remote edge prescribe endpoint labels $Z_j,b_j-Z_j$ and add the temporary offset $h_j-b_j$. Undoing this offset replaces the color $h_j$ by $b_j$.

Here are the placement and compatibility details. Let $M$ be one plus the degree excess, number of exceptional offsets and numbers of absent vertex and edge bins. Cut the original shifted edges and cap the other degrees at $D$. Mark the cut endpoints and the anchor. If two original leaves other than the anchor are still unmarked, reserve two. Choose an abundant original degree $2\le d\le D$, put $g=\gcd(N,d-1)$ and mark a nonanchor representative of each nonzero $c_v\bmod g$ occurring off the anchor. Such a degree occurs linearly often by $\sum c_v=n-2$ and the degree excess bound. Otherwise mark all non-degree-two vertices. There are $O(M)$ of them since all but at most two leaves were touched by the initial marks. In this case use $d=2$.

Place the vertex copies at degree-$d$ positions at distance at least three from all initial marks, reserves and earlier copy positions. There is one prescribed exception. On a path anchored at an endpoint, the other endpoint must carry $C-a$. When this equals $a$, assign one extra occurrence of $a$ to that far endpoint, using its paired $q_i$ temporarily. The multiplicity condition supplies the occurrence. When it differs from $a$, use the first occurrence at the far endpoint. Ordinary copy positions remain remote from both endpoints. Mark each switched vertex and all its neighbors, and cut the incident edges. A fixed-radius neighborhood of $O_D(M)$ vertices still has size $O_D(M)$ because any set $X$ has degree sum at most $D|X|+E_D$. There are enough eligible places even if the number of copies exceeds $\sqrt N$.

Choose the remote edges for repeated edge colors as an induced matching outside the neighborhoods of all these positions. Cut and mark them. Use the [paired reconnection](edge-histograms.md#choosing-the-edges) with one private edge per cut and independent new sites. At each site pair the private endpoints allow the two original temporary weights to be exchanged. The auxiliary tree $U$ has bounded degree, all changed endpoints are in the pin set $K$, and its induced pinned-edge multiset equals the original temporary one. With reserves use sites of original degree $d$. Without reserves all unmarked original positions have degree two. These choices cost $O_D(M)$ positions.

Let $z$ denote temporary vertex labels and $x$ the corresponding actual labels. The required original equations on $z$, before the edge-copy offsets, are
$$
 \sum c_v z_v=A-\sum_i(d_i-1)e_i,qquad
 \sum(\deg_T(v)-2)z_v=-C-\sum_i(d_i-2)e_i .
$$
The integer identities for all switches hold before reduction modulo $N$. [Lean check of the edge and both moment corrections](HistogramLift.lean)

With reserves impose the first equation modulo $g$ on the pins. Every copy site has $c_v=d-1$, so both its prescribed temporary label and its correction vanish modulo $g$. The anchored term is fixed. The prescribed edge-pair endpoints contribute multiples of $\gcd(N,c_v:v\ne r)$. The chosen representatives span precisely the remaining attainable subgroup modulo $g$, so the assumed gcd condition suffices. Without reserves impose the second equation exactly. When there are two nonanchor leaves, eliminate one of their labels using the other and the marked branch labels. On an endpoint-rooted path the equation fixes the far temporary label, including $q_i$ when that endpoint received the extra occurrence of $a$.

The greedy pin assignment from the [edge-histogram proof](edge-histograms.md#assigning-the-pins) also enforces membership in the two palettes. Append each vertex hole outside $P$ to the vertex inequality list and each color outside $Q$ to the edge inequality list. All fixed temporary vertex labels are distinct, and all fixed edge-pair colors are distinct and in $Q$. An edge incident with a fixed vertex-copy position has the neighbor variable plus the actual label $p_i$ and original offset. Each variable vertex neighbors at most one such position and cannot also neighbor the anchor or a fixed path endpoint, by the separation. Thus repeated values of $p_i$ create no identical edge forms. At a fixed far endpoint of a long path the two endpoint edges have different neighbor variables. The two eliminated leaves in the other case have one incident edge each, so the last free leaf variable still has coefficient of magnitude at most two in each affected edge comparison. The fresh private variables distinguish the site forms as in the cited proof.

In parent-before-child order each variable is last in boundedly many edge forms, except for the substituted leaf, whose comparisons are handled by putting the other leaf variable last among the original variables. The added fixed copy positions cost at most one further incident fixed-neighbor edge per variable. Private variables come after the ordinary variables. Each nonconstant form also has $O(M)$ forbidden palette values to avoid. Thus the earlier $O_D(M)$ exclusions at each greedy step still suffice, including inside a required residue class. This gives injective pins with injective induced colors in $P,Q$.

For clarity, the congruence on $U$ follows by summing the actual exchanged weights on the pins. The total temporary offset is
$$
        B'=\sum\eta_e+\sum_i d_i e_i+\sum_j(h_j-b_j).
$$
Since every changed edge has pinned ends, the auxiliary pinned coefficient sum equals the original pinned coefficient sum in temporary labels plus $B'$. The degree-minus-two sum changes by the same amount. Also $\sum P=m(V)-\sum_i e_i$ and $\sum Q=m(H)+\sum_j(h_j-b_j)$. These identities give exactly the two palette-core conditions above. With reserves an untouched degree-$d$ position remains, so the auxiliary coefficient gcd divides $g$. Without reserves all remaining auxiliary degrees are two. Complete the embedding, undo the reconnections, return the vertex copies and remove the edge-copy offsets. Each bin then has its specified true count.

## Projection to the requested modulus

Use $N=tk$ as in the theorem. In each residue class $x$ allocate its first $\min(t,F_x)$ occurrences to the lifts $x,x+k,\ldots$ in order. Assign each further occurrence to the lift $x$. Do this independently for the two lists. The numbers of absent bins upstairs are exactly $J(V)$ and $J(H)$. Since $N-n\le J(V)$, the tree is near-spanning. The projected counts are exact bin by bin. [Lean verification of the slot allocation](HistogramLift.lean)

Use $a$ itself for the root lift. Let $A',C'$ denote the upstairs moments with the initial offset lifts. They reduce to $A,C$ modulo $k$. Increasing any one lifted offset by a multiple of $k$ preserves all prescribed weights after projection. Put $h'=\gcd(N,c_v:v\ne r)$. Such a change makes $A'-c_ra$ divisible by $h'$ precisely when the downstairs gcd condition holds, since $\gcd(k,h')=\gcd(k,c_v:v\ne r)$.

On an endpoint-rooted path instead choose an available occurrence above $u=C-a$ after consuming the root occurrence. Such an occurrence exists exactly under condition 3. Adjust one edge lift to make $C'$ the sum of the chosen endpoint lifts. In the case of equal lifts the upstairs copy construction uses their two distinct occurrences. The coefficient gcd of a sufficiently long endpoint-rooted path is one. Only one additional exceptional edge has been introduced. Apply the upstairs result and reduce the labels modulo $k$.

## Exterior forests with prescribed parent colors

Let a rooted forest on $m$ new vertices have component parent colors $b_1,\ldots,b_j$. Count the entering edges in the desired histogram $H$, and prescribe $V$ on the new vertices, so both totals are $m$. Adjoin a dummy vertex of fixed label zero with an edge to every component root. Take $V+[0]$ upstairs in the theorem's input tree of order $m+1$, with offset $b_i$ on entering edge $i$. Under the stated size bounds on that augmented instance, the exact test is
$$
           \gcd(k,\#\mathrm{children}(v):v\text{ in the forest})
               \mid m(H)-m(V)-\sum_i b_i .
$$
For a single path rooted at its endpoint also require a forest occurrence of $2m(V)+b_1-m(H)$, the forced tip label. Deleting the dummy gives the actual prescribed boundary sums with all old labels fixed. This allows one to specify the entire frequency change produced by an attachment.

## Verification

The [quotient constructor](tree_palettes.py) allocates the actual occurrences and adjusts the offset. The [embedding constructor](edge_histogram.py) builds the temporary tree, switches and pinned degree core. A [separate checker](check_tree_palettes.py) recounts the two projected histograms and all induced original and auxiliary edge weights under both choices of vertex labels. It checks connectivity, every pin, all degree classes and both embedding moments. The checks accepted 246 cores and rejected 18 inputs. In 107 successful cases the vertex distribution overflowed a fiber, in 160 the edge distribution did so, and two used a repeated endpoint label even upstairs. The checker also tested the necessary conditions and lift on 7,518 complete small labelings. The large-order completion is the application of Lemma 4.9 above.

~~~sh
python3 -B research/bounded-degree/check_tree_palettes.py
python3 -B research/bounded-degree/check_edge_histogram.py
python3 -B research/bounded-degree/check_partial_gap.py
lean research/bounded-degree/HistogramLift.lean
~~~
