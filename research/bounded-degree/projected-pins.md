# Prescribed labels and both frequency lists on a large tree

**Cordial precoloring theorem.** Fix $D\ge3$ and $0<\delta<1$. Let a tree have $n$ vertices, let $p$ vertices have arbitrary prescribed labels in $\mathbb Z_k$, and put $e=\sum_v(\deg(v)-D)_+$. Suppose
$$
 k+p+e\le n^{1-\delta},\qquad n/k\ge C_D(p+e+1),
$$
where $C_D$ is a sufficiently large constant and $n$ is sufficiently large in terms of $D,\delta$. At $k\ge2$ the prescribed labels extend to a cordial labeling, with exactly one exception. Failure requires even $k$, order $n=qk+1$, every odd-degree vertex prescribed, and a prescribed sum on those vertices of parity different from $qS$, where $S=\sum\mathbb Z_k$.

The prescribed positions can be adjacent and can carry repeated residues. The degree bound applies to the auxiliary embedding used below; the original tree can have unbounded degrees. In particular for each $\gamma>0$ it suffices asymptotically that $n\ge[k(p+e+1)]^{1+\gamma}$.

## Prescribing the frequency lists

Let $V_x,C_x$ be desired nonnegative counts of vertices and edges, respectively, of totals $n,n-1$. For a count list let $m(F)=\sum_x x F_x$ in $\mathbb Z_k$. Write $P$ for the prescribed positions, with labels $a_v$, and $d_v$ for original degrees. Put
$$
 A=m(V)-\sum_{v\in P}a_v,\qquad B=m(C)-\sum_{v\in P}d_va_v .
$$
Choose an unprescribed degree $d_*$ and define $g=\gcd(k,d_v-d_*:v\notin P)$. The exact test is
$$
                                g\mid B-d_*A .
$$
Necessity follows by summing labels, then summing at both endpoints of every edge. Different choices of the unprescribed degree give the same test.

Here are sufficient size hypotheses for the converse. Set $M=2+\max_x(V_x,C_x)$, $H=M-\min_x(V_x,C_x)$ and $K=p+3e+12(D+1)$. Require $kH+p+e\le n^{1-\delta}$ and $M>(D+3)(2K+2H+2)$. These permit frequency lists with spread greater than one. In the balanced case $H\le3$, and the hypotheses of the first theorem suffice after decreasing $\delta$ slightly.

## Lowering degrees while preserving projected sums

There are at most $e$ vertices of degree greater than $D$. Choose $d_*\le D$ occurring most often among unprescribed vertices of degree at most $D$. Protect one unprescribed representative of every original unprescribed degree. The remaining unprescribed degree-$d_*$ vertices provide more than $e$ available sites for large $n$, since their class before protection has size at least $(n-p-e)/D$.

Root at an available site. At every vertex of degree greater than $D$, cut enough child edges to leave degree at most $D$, retaining the incoming edge. There are exactly $e$ cuts. Reconnect each detached component at the child endpoint of its cut, using a distinct available site in the already joined components as new parent. Process detached components containing an available site first. The root component starts with a site, and every such attachment replenishes at least one site. By the time only empty components remain, the total original supply suffices. This produces a tree $U$ of degree at most $D+1$. We will give each replacement site the **same residue modulo $k$** as the original parent. Restoring the original edges will then preserve every projected weight.

Form a set $Q$ in $U$ containing the pins, the representatives, the original cut parents and the replacement sites. For each auxiliary degree class, add positions until either all are included or at least six are inside and six outside. At most eleven additions per class are needed. There are at most $D+e$ represented original degrees, so $|Q|\le K$.

Assign low residues on $Q$. Give the representatives at degrees $d\ne d_*$ values $x_d$ solving
$$
             \sum_{d\ne d_*}(d-d_*)x_d=B-d_*A .
$$
This is possible by the gcd test. Keep every prescribed label, set other ordinary marks provisionally to zero, then give each replacement site its original parent's low residue. Every such site originally had degree $d_*$, so these copies do not affect the difference moment. Use the protected representative at $d_*$ to make the sum of all marks equal $m(V)$. The original-degree weighted sum on the marks is now $m(C)$. Reconnection preserves that sum modulo $k$, because both positions whose degrees change on each moved edge are marked at the same residue. Thus the same two low moment identities hold with the degrees of $U$.

## Lifting the small embedding and filling its palettes

Work in the cyclic group of order $N=kM$. Lift each marked label within its prescribed fiber, making the lifted vertices distinct and the sums on induced marked edges distinct modulo $N$. When labeling a new mark, fewer than $(D+2)|Q|$ high digits are forbidden: each previously occupied vertex excludes at most one, and each of at most $D+1$ old neighbors can collide with fewer than $|Q|$ previous edge sums. The marked induced graph is a forest. Two new edge sums at the same step are distinct because their other endpoints already have different lifts.

Choose a vertex target set containing all lifted marks and having exactly $V_x$ entries over $x$. Choose its sum to equal the sum of the lifted marks in $\mathbb Z_N$. Do the same for a color set with counts $C_x$, protecting every induced edge sum and prescribing the auxiliary-degree weighted sum of the lifts. For either palette, one must omit between two and $H$ elements from each fiber. In all fibers except zero make these omissions arbitrarily outside the protected set. In the zero fiber make all but two. The remaining required sum of omissions is a multiple of $k$ by the low moment identity. In high digits it asks for two distinct elements of $\mathbb Z_M$ of a prescribed sum. The occupied and already omitted entries exclude at most $2(|Q|+H)$ first choices, and equality of the pair excludes at most two. The hypothesis on $M$ suffices.

Now $0\le N-n\le kH$. For a sufficiently small embedding exponent $\alpha<\delta$ one has $n\ge N-N^{1-\alpha}$ and $|Q|\le N^{1-\alpha}$. Lemma 4.9 of Müyesser and Pokrovskiy extends the lifted embedding of the degree core, with precisely the two selected palettes. Project modulo $k$ and restore the cut edges. This realizes the stipulated counts and all original prescriptions. The use of a larger cyclic group here allows repeated low labels even at adjacent prescribed vertices. [Primary embedding theorem](https://arxiv.org/html/2509.05280v2#S4) · [Earlier projection for ordinary trees](projection.md)

## The parity criterion for balanced counts

For $1\le j<k$, the sum of $j$ distinct residues can be anything in $\mathbb Z_k$. If the edges have $j$ high bins, fix any balanced vertex profile, then choose the high edge bins so that $B=d_*A$. If the edge bins are uniform, $n=qk+1$ and $m(C)=qS$. Choosing the single high vertex bin allows $A$ to vary arbitrarily. The solvability condition reduces to
$$
     \gcd(k,d_v:v\notin P)\ \mid\ qS-\sum_{v\in P}d_va_v.
$$
This gcd is at most two. Otherwise every unprescribed vertex would have degree at least three. Since the prescribed ones have degree at least one, the tree degree sum would force $n\le2p-2$, contrary to the size assumptions. The gcd equals two exactly when $k$ is even and all odd-degree vertices are prescribed. This proves the precoloring theorem, including necessity. [Subset-sum construction](../census/long-bridge.md#choosing-balanced-targets)

## A near-linear bridge for two arbitrary old orders

Fix $\gamma>0$. At all sufficiently large $k$, a path with $t\ge k^{1+\gamma}$ new vertices joins **any two independently cordial labeled trees** while keeping all labels. The only obstruction is even $k$, final order $qk+1$, and the wrong parity at the old odd-degree sites in the resulting tree. There is no degree bound on either old tree.

Choose balanced final profiles satisfying the endpoint moment as in the [explicit long-bridge theorem](../census/long-bridge.md#choosing-balanced-targets). Subtract the two old profiles to obtain the desired internal vertex counts and bridge-edge counts. On the path alone, include the two endpoints in its vertex targets and prescribe their actual labels $a,b$. Each desired count differs from its path average by a bounded absolute constant, since each old tree was cordial. They are nonnegative for large $k$. Here $p=2$, $e=0$, $H=O(1)$, and every free position has degree two. The gcd test is exactly the path-edge moment $a+b$ plus twice the sum of the internal labels. The lifted-palette theorem therefore applies. The square-root-density Hamilton path theorem of Müyesser and Pokrovskiy also gives the prescribed-endpoint conclusion on lifted palettes when the omissions satisfy its stronger size bound. [*A random Hall–Paige conjecture*, Theorem 6.9](https://doi.org/10.1007/s00222-025-01328-x)

## Reproduction

~~~sh
python3 -B research/bounded-degree/check_projected_pins.py
~~~

The [constructor](projected_pins.py) supplies the bounded-degree tree, the marked embedding in the larger cyclic group and both target sets. The [checker](check_projected_pins.py) reconstructs both projected histograms, the large-group moment sums, the pin labels and all edge changes on complete trial assignments. The large-order theorem uses the primary embedding result for the remaining vertices. The checker covers 212 cordial and 212 further prescribed target pairs, with 1,296 replicated attachment labels in the cordial tests. It verifies four parity obstructions, eight incompatible frequency pairs, and 24,576 independent small moment tests by literal enumeration. The fixtures include adjacent prescribed vertices with identical labels and adjacent high-degree parents.
