# Completing a partial labeling with a prescribed missing edge weight

**Theorem.** Fix $D$ and $0<\epsilon<1$. At every sufficiently large $k$, take a $k$-vertex tree $U$ of degree at most $D$, prescribe labels on any set $P$ of size at most $k^{1-\epsilon}$, and prescribe the missing edge weight $w\in G=\mathbb Z_k$. The following tests are necessary and sufficient for a bijection keeping the pins and realizing all weights in $G\setminus\{w\}$.

First require that the pins be distinct and that all induced pinned edges have distinct sums avoiding $w$. Let $S=\sum G$.

* **At least two unpinned leaves.** Put $c_v=d_U(v)-1$. The remaining condition is
  $$
             \gcd(k,c_v:v\notin P)\ \mid\ -w-\sum_{v\in P}c_v x_v .
  $$
* **At most one unpinned leaf.** Put $d_v=d_U(v)-2$, let $I$ consist of the unpinned positions with $d_v\ne0$, and set $T=-S-w-\sum_{v\in P}d_vx_v$. If $I$ is empty, require $T=0$ in $G$. Otherwise put $a=\gcd(|d_v|:v\in I)$ and $u_v=d_v/a$. Try the at most $D$ solutions $Y$ of $aY=T$ in $G$. One must pass the test below.

For each $v\in I$ use a variable $X_v$. On $P\cup I$ form the list of all vertex labels and, separately, the list of induced edge sums together with the constant $w$. For each pair within either list write the difference as $C+\sum_{v\in I}q_vX_v$. If $q$ is an integer multiple $b u$ of the primitive vector $u$, require $C+bY\ne0$ in $G$. This includes the zero multiple. All the comparisons can be made directly from the data.

In particular, with at least three unpinned branching vertices in the second case, only the divisibility $\gcd(k,d_v:v\in I)\mid T$ remains after the initial pin test. A comparison has at most two positive and two negative unit coefficients, whereas $u$ has at least three positive entries. Constant comparisons either come from the initial data or from edges sharing an unpinned endpoint and having different pinned neighbors. The latter have distinct sums by injectivity of the pins.

With two unpinned leaves the same test allows unbounded degrees. A caterpillar gives a sharp square-root scale for arbitrary pin placements. [Degree reduction and obstruction](excess-pins.md)

## Two or more free leaves

Subtracting the sum of all vertex labels from the edge sum yields $\sum(d_U-1)x=-w$. This proves necessity of the first gcd condition. Reserve two unpinned leaves. Some degree $2\le d\le D$ occurs linearly often, since $\sum(d_U-1)=k-2$. Put $g=\gcd(k,d-1)$. For each nonzero residue of $c_v$ modulo $g$ among unpinned vertices choose a representative. Some ordinary degree-$d$ vertex is unpinned, so the coefficient gcd with $g$ is the divisor in the criterion. Choose representative label residues modulo $g$ to realize the missing coefficient sum modulo $g$. Lift their labels greedily within their residue classes. A new vertex must avoid occupied labels and previously used or forbidden colors at its boundedly many neighbors. Two simultaneously formed edges have different sums because the previously labeled neighbors are distinct. Each step excludes $O_D(|P|+1)$ of the $k/g$ possible labels.

Now enlarge the pins and the reserved leaves to a degree core, giving any new ordinary pins labels zero modulo $g$ with the same exclusions. Two isolated abundant-degree positions solve the exact coefficient sum via $(d-1)(x+y)$, then the reserved leaves solve the remaining vertex sum. For the last pair the weights on the two leaf edges collide for at most two first-label choices. This gives a partial rainbow embedding in the desired palettes, with vertex sum $S$ and degree-weighted sum $S-w$. The core has size $O_D(|P|+1)$. Lemma 4.9 completes it while keeping the original pins. [Müyesser and Pokrovskiy, primary embedding lemma](https://arxiv.org/html/2509.05280v2#S4)

## Few free leaves and the primitive moment

The full edge sum is also $2S+\sum(d_U-2)x$, giving the necessary relation $\sum_{v\in I}d_vX_v=T$. There are at most $|P|+1$ leaves in this case, and at most that many branching vertices. Thus $Q_0=P\cup I$ has size $O(|P|+1)$ and contains every non-degree-two vertex. If $I$ is empty then its coefficient sum is already determined. Otherwise any extension determines $Y=\sum u_vX_v$, so every forced inequality in the test is necessary.

Conversely take a passing $Y$. Since $u$ is primitive, Bézout gives a particular solution $p$ of $\sum u_v p_v=Y$ modulo $k$. Pick $j\in I$, write $b=u_j\ne0$, and use the family
$$
             X_i=p_i+bZ_i \ (i\ne j),\qquad
             X_j=p_j-\sum_{i\ne j}u_i Z_i .
$$
Every member satisfies the prescribed primitive moment. A difference with coefficients $q$ is constant as an integer-coefficient form on this family precisely when $bq_i=q_j u_i$ for all $i\ne j$. Equivalently $q$ is rationally proportional to $u$, hence an integer multiple since $u$ is primitive. Its constant value modulo $k$ is just the one checked in the test. This reasoning also covers a single variable, where each possible $Y$ fixes its label.

All remaining comparisons have a nonzero parameter coefficient of absolute value $O_D(1)$. A parameter occurs only at its own vertex and at $j$, and in the boundedly many edge forms through them. Therefore $O_D(|P|+1)$ comparisons involve each parameter. At the last surviving parameter each equality forbids $O_D(1)$ residues of $G$. For sufficiently large $k$, greedy assignment produces distinct labels on $Q_0$ with distinct edge sums outside $w$.

Add six mutually isolated degree-two vertices outside the neighborhood of $Q_0$. Choose fresh labels on four, then use a pair sum to make the marked labels sum to $S$. There are still six degree-two positions outside the core, and all other degree classes are exhausted. Its degree-weighted sum is $2S+\sum(d_U-2)x=S-w$, so the same embedding lemma proves sufficiency.

## Moving old branches to prescribed sites

For a cordiality application, attach $U$ by one edge from a vertex of a labeled old core to a pinned free vertex. Set $w$ to the sum on that entering edge. From any old vertex move arbitrarily many pendant branches to a free vertex pinned at the same label, with each old branch moved only once and the remaining old part connected. Each moved edge keeps its weight. When the test passes, every vertex and edge bin gains one: the internal weights contribute $G\setminus\{w\}$ and the entering edge supplies $w$. The old outside degrees and the number of branches moved at the given sites do not enter the test.

## Verification

~~~sh
python3 -B research/bounded-degree/check_partial_gap.py
~~~

The [constructor](partial_gap.py) implements both criteria and produces the actual degree-core embedding. The [checker](check_partial_gap.py) verifies every pin, induced weight, degree class and moment on 164 successful targets, exercises 55 arithmetic or forced-equality obstructions and four locally invalid inputs, and enumerates actual solutions of primitive congruences in 3,072 separate comparisons to check the forced-form calculation.
