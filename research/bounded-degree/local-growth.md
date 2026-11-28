# A local condition for cordial growth at large moduli

**Theorem.** Fix $D\ge3$ and $0<\epsilon<1$. For all sufficiently large $k$, suppose every connected subtree $A$ of a finite tree $T$ on **at most $k$ vertices** satisfies
$$
                  E_D(A)+b(A)\le k^{1-\epsilon}.
$$
Here $E_D(A)=\sum_{v\in A}(\deg_A(v)-D)_+$ uses degrees **inside the subtree**. The quantity $b(A)$ counts edges of $A$ whose additive offset differs from a fixed value common to the test. For ordinary cordiality take all offsets to be zero. From any specified vertex, the size-ordered depth-first preorder has a single labeling cordial on every prefix. Its first label and all traversal ties can be specified. The order of $T$, the number of exceptional edges, and the total excess of $T$ can all be arbitrarily large.

In particular, for every fixed $D,\epsilon$, an ordinary counterexample at sufficiently large $k$ must contain a connected subtree on at most $k$ vertices with more than $k^{1-\epsilon}$ degree excess above $D$. The same holds for a tree and an assignment of offsets for which the stated growth order fails, counting its exceptional edges as well.

## Covering an interval by three small subtrees

At the start of a nonempty block of $t\le k-1$ free vertices, the earlier prefix is connected. The forest of the block has one entering edge per component. Its components appear in groups according to their old parents, deepest parent first. Every group except possibly the last consists of complete child subtrees, and the last group contains at most one partly traversed child subtree. The [preorder interval bound](sparse-offset-growth.md#a-whole-growth-order) gives at most $1+\log_2 t$ distinct entering parents.

Cover the last group together with all its entering edges by taking its parent and all its block vertices. This is a connected subtree on at most $t+1$ vertices. Do the same for the penultimate group if present, writing $r$ for its parent. If there are still earlier groups, they all lie inside a single child subtree $C$ of $r$ that contains the vertex visited last before the block. The earlier groups' parents and entering edges also lie in $C$. The traversal began this child before it began any unvisited child of $r$. Consequently $|C|$ is at most the order of the first subsequently visited child subtree of $r$. That subtree belongs to the penultimate group and was visited in full, so $|C|\le t$. This gives at most **three** connected covering subtrees, each of order at most $t+1$. They cover every component with its entering edge. All entering edges at any one parent are together in one covering subtree.

Write $F$ for the internal forest and $q$ for its number of components. Assign each parent to the covering subtree just specified. Summing its degree there gives
$$
     q \le D(1+\log_2 t)+\sum_A E_D(A).
$$
Also $E_D(F)+b(F)\le\sum_A(E_D(A)+b(A))$, assigning each component to its cover. Thus $E_D(F)+b(F)+3q=O_D(k^{1-\epsilon}+\log k)$. For large $k$ this is at most $k^{1-\epsilon/2}$. The [block extension with prescribed old labels](sparse-offset-growth.md#a-whole-growth-order) applies at every step and proves the theorem.

## Inspecting smaller neighborhoods

Fix $0<\alpha\le1$ and $0<\delta<1$. It suffices to test all connected subtrees on at most $m=\lceil k^\alpha\rceil$ vertices and require $E_D(A)+b(A)\le m^{1-\delta}$ there. In particular any ordinary counterexample must contain a subtree violating this bound at **each** such fixed polynomial scale once $k$ is sufficiently large.

To see this, partition the edges of any connected subtree $H$ of order at most $k$ into connected pieces of at most $m-1$ edges. Process a rooted $H$ from children to parents. Pass upwards a connected remainder of fewer than $a=\lfloor m/2\rfloor$ edges, allowing a remainder of zero edges consisting of its root. At a vertex $v$, collect the remainders of its children, each with its edge to $v$. As soon as the collection has at least $a$ edges, export it as one piece and start again at $v$. A child contributes at most $a$ edges, so an exported piece has at most $2a-1\le m-1$. Export the final remainder at the root if nonempty. Apart from this last piece every piece has at least $a$ edges, so the number $p$ of pieces is $O(k/m+1)$. A singleton needs no edges.

If $v$ occurs in $r_v$ pieces, their degrees there sum to $\deg_H(v)$. The overlap costs at most $D(r_v-1)$ in the excess bound. Summing all piece orders counts $|E(H)|+p$, giving $\sum_v(r_v-1)=p-1$. Exceptional edges are partitioned exactly. Therefore
$$
 E_D(H)+b(H)\le \sum_A(E_D(A)+b(A))+D(p-1)
      =O_D(k m^{-\delta}+m^{1-\delta})=O_D(k^{1-\alpha\delta}).
$$
The first theorem applies with any fixed positive exponent less than $\alpha\delta$.

**Separated high-degree vertices.** As a different application, fix $0\le\rho<\beta\le1$. Suppose vertices of degree exceeding $D$ have degree at most $k^\rho$ and are pairwise at distance at least $k^\beta$. The tree has the stated cordial growth order for all sufficiently large $k$. Indeed, in a connected subtree of order at most $k$ with at least two such vertices, take from each one an initial path of length $\lfloor(k^\beta-1)/2\rfloor$ toward another. These paths are disjoint. The subtree thus meets at most $O(k^{1-\beta}+1)$ high-degree vertices and its total internal excess is $O(k^{1-\beta+\rho})$. The same estimate holds with zero or one high-degree vertex.

## Verification

The [checker](check_local_growth.py) reconstructs the actual child subtrees and entering edges on 159,201 preorder intervals. It verifies the size and connectivity of each cover and checks every edge of the block together with its parent. In 686 intervals it uses all three subtrees. It also checks the edge partition, overlap count and excess inequality in 460 separate instances, including stars. The embedding step is the [large-modulus growth theorem](sparse-offset-growth.md), which uses [Müyesser and Pokrovskiy, Lemma 4.9](https://arxiv.org/html/2509.05280v2#S4).

~~~sh
python3 -B research/bounded-degree/check_local_growth.py
~~~
