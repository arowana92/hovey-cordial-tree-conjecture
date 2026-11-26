# Growing a cordial subtree in full batches

Fix a connected subtree $S$ of a tree $T$. Write $a_d$ for the number of exterior vertices at distance at most $d$ from $S$, and $H$ for the largest distance. A batch may include any vertices whose parents towards $S$ have already appeared. We require $k$ vertices per batch, apart from a possibly shorter final batch.

**Criterion.** Such a sequence exists if and only if $a_d\ge kd$ for every $1\le d<H$. Thus, if $S$ has a cordial labeling and order $1\bmod k$, these ball inequalities suffice for $T$ to be $k$-cordial. Taking $S$ to be a singleton requires no labeling hypothesis. In particular any vertex of degree at least $k(H-1)$ suffices, where $H$ is its eccentricity. This gives a linear degree threshold at bounded height. The case $H\le1$ has no inequalities.

The scheduling part is the unit-job rooted-tree setting of Hu's level algorithm. We give a direct proof for the full batches and final remainder required here. [T. C. Hu, *Parallel Sequencing and Assembly Line Problems* (1961)](https://doi.org/10.1287/opre.9.6.841)

**Necessity.** Reaching distance $d+1$ requires at least $d+1$ batches. After $d$ batches all $kd$ added vertices are within distance $d$.

**Sufficiency.** With $M>0$ exterior vertices, write $M=k(q-1)+r$, $1\le r\le k$. The ball inequalities imply $H\le q$ (for $H>1$, use $a_{H-1}<M$). For $1\le j\le H$, let $F_j$ be the number at depth at least $j$, and $L_j$ the number of terminal vertices there. We have
$$
F_j\le k(q-j)+r,\qquad F_j\le (q-j+1)L_j .
$$
The first inequality uses $M-a_{j-1}$ and $a_0=0$. For the second, cover the depth-$\ge j$ forest by its paths from depth $j$ to a terminal. To reduce the final batch, remove the $r$ deepest terminals. There are at least $r$: otherwise $M\le qL_1\le k(q-1)+L_1<M$. At each depth $j$, at least $F_j-k(q-j)$ terminals must be removed to leave at most $k(q-j)$ vertices there. This requirement is at most $r$. It is also at most $L_j$: if $L_j<k$ use the second inequality, and otherwise use $r\le k$. Taking deepest terminals removes $\min(r,L_j)$ simultaneously at each depth. In particular nothing at depth $q$ remains. At the new order $k(q-1)$ the same ball inequalities hold, by subtracting each remaining tail from the total. Induction constructs the earlier batches. The case $q=1$ removes the whole exterior.

Rooting towards $S$ makes each batch a group of new leaves at existing parents. [Hall's leaf extension](../counterexample-bound.md#removing-leaves) labels the first at most $k-1$ members with distinct labels avoiding the unique surplus and distinct edge sums. At a full batch, the last leaf supplies the then unique deficient edge weight. The order returns to $1\bmod k$, so this works repeatedly. At $k=1$ every tree is cordial directly. For the degree criterion, $a_d\ge a_1\ge k(H-1)\ge kd$ at every required depth.

## Protecting large branches with small total degree excess

Fix $D\ge3$, $\gamma>0$, and $0<\delta<1$. For sufficiently large $k$ a tree $T$ is $k$-cordial whenever it contains a connected subtree $S$ of order $s\ge k^{1+\gamma}$ satisfying
$$
E_D(S)=\sum_{v\in S}(\deg_S(v)-D)_+\le s^{1-\delta}.
$$
In particular a path on at least $k^{1+\gamma}$ vertices suffices, with arbitrary further branches and degrees anywhere on the path or outside it. This assertion concerns the given tree itself, even if smaller counterexamples exist.

Use the [protected leaf deletion](high-degree.md) to obtain a core $C$ containing $S$, with at most $k-1$ leaves outside $S$, whose cordial labelings extend to $T$. If an outside vertex has $b$ children, its contribution to degree excess is at most $(b-1)_+$. Each edge leaving $S$ increases the excess inside $S$ by at most one. In the forest outside $S$, the number of component roots plus $\sum(b-1)_+$ is exactly the number of terminals. Consequently
$$
E_D(C)\le E_D(S)+k-1 .
$$
Put $N=k\lceil |C|/k\rceil\ge s$. With $\rho=\tfrac12\min(\delta,\gamma/(1+\gamma))$, for sufficiently large $k$ we have $k+E_D(C)\le 2k+s^{1-\delta}\le N^{1-\rho}$. The [projection proposition](../bounded-degree/projection.md#a-large-order-sufficient-condition) labels $C$. Restoring the batches labels $T$.

The [checker](../large_order_balls.py) compares the ball criterion with an independent exhaustive search over batches on 17,742 rooted tree and modulus inputs. It also constructs and counts the labels on 112 trees, using singleton and nonsingleton seeds.

~~~sh
python3 -B -m research.large_order_balls
~~~
