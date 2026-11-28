# Prescribing the missing weight of an attachment forest

Orient a forest $F$ on $k-1$ vertices away from its $m$ roots. Root $r_i$ has one incoming edge from a prescribed old parent of label $b_i$. Write $a_v$ for its vertices' numbers of children. We prescribe distinct nonzero labels $x_v$ on a set $P$ of new vertices and seek a permutation of $\mathbb Z_k\setminus\{0\}$ that gives every edge weight except a specified $w$, including the incoming edges. The forbidden vertex label zero is a normalization of the surplus on the old core.

Fix $D\ge3$ and $0<\epsilon<1$. Set $e=\sum_v(a_v+1-D)_+$, $M=m+|P|+e+1$, and let $B$ be the maximum number of internally adjacent pinned neighbors of any unpinned vertex. Assume two unpinned **nonroot** vertices have no children. For all sufficiently large $k$, require $M\le k^{1-\epsilon}$ and $(B+1)M\le c_D k$ with a sufficiently small positive constant $c_D$.

**Theorem.** The desired permutation exists if and only if both of the following tests pass.

- Write the internal edge weights as $X_u+X_v$ and the entering weights as $X_{r_i}+b_i$, replacing the pinned variables by their values. Distinct edges must give distinct affine functions of the remaining variables modulo $k$. No edge may give the constant $w$.
- The integer $h=\gcd(k,a_v:v\notin P)$ must divide $w+\sum_i b_i+\sum_{v\in P}a_vx_v$.

The first test includes possible collisions between a boundary edge and an internal edge at an unpinned root. For the second, subtract the sum of the free vertex labels from the sum of the internal and entering edge weights. The difference is $\sum a_vX_v+\sum b_i=-w$. These observations prove necessity.

## Routing the entering weights

Reserve the two free terminals. Some augmented degree $d=a_v+1$ in $[2,D]$ occurs at linearly many nonroot vertices. Indeed $\sum a_v=k-1-m$, and vertices of augmented degree above $D$ contribute only $O_D(e)$ to that sum. Let $g=\gcd(k,d-1)$. Mark one free representative for each nonzero coefficient residue $a_v\bmod g$. Assign their labels modulo $g$ to solve the required coefficient sum including the pins. The representative coefficients together with $g$ have gcd $h$, since some free position has augmented degree $d$. Other free base variables receive residue zero initially.

Make two extra cuts on disjoint edges away from the pins, roots, representatives, reserved leaves and all vertices of augmented degree above $D$. Treat a cut $uv$ directed to $v$ as another entering edge with target weight $X_u+X_v$. We now have $m+2$ component roots with target weights, including the original $X_{r_i}+b_i$. For each of these roots $r$, cut a separate private ordinary edge $st$ directed toward $t$. Choose all these edges disjoint, also away from the neighbors of the initially marked and high-degree vertices. This needs $O(m)$ edges. All high-degree vertices together have degree sum $O_D(e)$, and outside them each forbidden vertex costs at most $D$ incident edges. Thus a greedy matching supplies the cuts.

Assign the target formerly at $r$ to the private root $t$, and assign $X_s+X_t$ to $r$. For each of the $2(m+2)$ components, select a pool of sites of original augmented degree $d$. Exclude the marks, all endpoints of cuts, reserved leaves, high vertices and their neighbors, and select mutually nonadjacent sites. In total there are $\Omega_D(k)$ sites, as the excluded neighborhoods have size $O_D(M)$ and the remaining choices have bounded degree.

Keep a principal component with largest pool. If its root is a private root $t$, swap its assigned weight with the assignment of one of the first two extra cut roots other than its own partner. This other root is a fresh variable absent from the displaced target. Consequently the principal assignment is always a sum of two private free variables. Add a single dummy vertex of label zero and join it to a site in the principal component with label equal to that assignment. Process the remaining components in decreasing order of pool size. Join each root $r$ to a site of an earlier component and set the site label to its assigned weight minus $X_r$. The first $j$ pools have at least their proportional share of all sites, so $j$ earlier uses cannot exhaust them for large $k$. This builds a tree $U$ of order $k$. Its auxiliary edges realize exactly the entering and cut weights. All endpoints of changed edges are marked.

## Assigning and extending the marks

Use independent variables for each free root, representative and endpoint of a cut. Fix the original pins. A site subtracting a free root has a negative variable private to that site, absent from its own positive terms. A site subtracting a pinned root has two private positive variables from its ordinary edge. The additional swap, if used, subtracts a free extra root absent from the displaced target. The dummy site has its own private pair as its positive terms. These observations distinguish all the site forms from one another and from the base labels. Include the dummy label zero in the vertex comparisons. Since distinct nonzero values were prescribed, all constant vertex comparisons pass.

The edge forms to be checked are original induced internal edges and entering weights, with removed edges represented by their matching wires. Include $w$ as an additional forbidden color. The first test makes all constant comparisons legal. In these lists each variable occurs in $O_D(B+1)$ forms. Each original vertex is adjacent to at most one original root other than itself. Representatives add at most $D$ neighbors. All private endpoints and sites were selected away from high vertices, and the original root of each component occurs in only one entering weight. Each vertex in a private edge or one of the two extra cuts occurs in only a bounded number of site forms. Thus, among $O_D(M)$ marked entries, only $O_D((B+1)M)$ comparisons involve any one variable. Distinct affine forms with nonzero variable coefficients have differences with coefficients of absolute value at most two. At the last variable in each such difference at most two values are excluded in its coset of size $k/g$. Choose the variables successively. This produces distinct marked vertex labels and distinct induced weights avoiding $w$.

All newly selected sites had original coefficient $d-1$, zero modulo $g$. On the marks the sum of the vertex labels is the same before and after adding the dummy. Equality of the changed weights gives
$$
 \sum_{v\text{ marked}}(d_U(v)-1)X_v
   =\sum_{v\text{ originally marked}}a_vX_v+\sum_i b_i
   \equiv -w\pmod g ,
$$
where the right sum includes the sites among the original forest vertices. There are linearly many untouched degree-$d$ positions, so the gcd on the remaining free vertices of $U$ divides $g$. The tree has two free leaves, $O_D(M)$ pins and total excess above $D+2$ at most $O_D(e+1)$. Each remaining unpinned vertex has at most $B+O_D(1)$ pinned neighbors by the same neighborhood count. Reducing the constant $c_D$ and the exponent $\epsilon$ for this application, the [prescribed-tree theorem](excess-pins.md) extends the marks with missing weight $w$. Delete the dummy and restore the cuts and the entering edges. The actual edge multiset is preserved. This proves sufficiency. The external asymptotic input is [Müyesser and Pokrovskiy's embedding lemma](https://arxiv.org/html/2509.05280v2#S4).

## Changing one parent without relabeling the forest

Suppose only a single root $r_j$ is pinned at $x\ne0$. Replace its parent label $b_j$ by $c\ne b_j$, leaving every other boundary value fixed. The same permutation serves both choices exactly when its first missing weight is $x+c$. The local test passes automatically. For the two needed free nonroot terminals and sizes as above the criterion is consequently
$$
          \gcd(k,a_v:v\ne r_j)\mid (a_{r_j}+1)x+c+\sum_i b_i.
$$
If the root label is free, let $l$ be the gcd of $k$, all the other child counts and $a_{r_j}+1$. Then $l\mid c+\sum_i b_i$ is necessary and sufficient. The congruence has a nonzero solution for $x$, since the gcd without $a_{r_j}+1$ divides the bounded positive coefficient $d-1$. Also $l\mid m$ by summing the coefficients and using $\sum a_v=k-1-m$. In particular, when $k$ and $m$ are coprime, any change at one parent permits a shared labeling. This includes all sufficiently large prime moduli in this regime.

The divisor can matter at arbitrarily large orders. For fixed $l\ge2$ and $m$ a positive multiple of $l$, take large $k$ divisible by $l$. Give $r_j$ exactly $l-1$ children, and every other vertex either zero or $l$ children. Such a forest is obtained by starting with the $m$ roots and attaching $l-1$ leaves at $r_j$, then attaching $l$ leaves at a time to an existing terminal until reaching order $k-1$. Keep $r_j$'s children count fixed. The gcd for a free root is exactly $l$. Incorrect parent sums rule out a shared permutation even with bounded degrees. Each individual boundary labeling remains a separate question.

On a full period, deleting one suitable terminal or a singleton yields an exact extension test with no pin prescriptions. Projection then gives a theorem for every divisor of the forest order. [Uniform increments at every modulus](forest-period.md)

## Reproduction

The [constructor](forest_spectrum.py) produces both auxiliary trees and the actual marked labeling supplied to the embedding lemma. The [independent verifier](check_forest_spectrum.py) checks the original internal and entering weights against both auxiliary edge multisets, and recomputes the two degree-core moments and degree classes. It verified 68 prescribed-gap targets, 12 arithmetic exclusions, 12 forced local conflicts and four shared rows at composite moduli, including repeated parent colors and vertices of unbounded-degree type.

~~~sh
python3 -B research/bounded-degree/check_forest_spectrum.py
~~~
