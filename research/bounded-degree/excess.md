# Allowing unbounded maximum degree

**Theorem.** Fix an integer $D\ge3$ and $0<\epsilon<1$. For every sufficiently large $k$ in terms of $D,\epsilon$, every finite tree $T$ with
$$
E_D(T):=\sum_{v\in V(T)}\max(0,\deg_T(v)-D)\ \le\ k^{1-\epsilon}
$$
is $k$-cordial. There is no restriction on tree order, on the locations of the high-degree vertices, or on the primality of $k$.

For example, the theorem allows a vertex of degree $D+\lfloor k^{0.9}\rfloor$ when all other degrees are at most $D$, or the same total excess distributed among adjacent vertices. The bounded-degree assertion discussed by Müyesser and Pokrovskiy is the case $E_D(T)=0$. We use their preprint's Lemma 4.9 on an auxiliary tree of maximum degree at most $D+1$. [Primary embedding theorem](https://arxiv.org/html/2509.05280v2#S4) · [Bounded-degree proof and embedding hypotheses](README.md#complete-the-prescribed-labels)

## Forest lemma

Fix $D\ge3$ and $0<\delta<1$. Consider $k-1$ free vertices in a rooted forest with $c$ components. The free degree counts one parent edge at every vertex, including every component root's edge to a prescribed external label. Define $E_D(F)$ using these free degrees. If $c+E_D(F)\le k^{1-\delta}$, then for sufficiently large $k$ every boundary assignment permits distinct free labels avoiding any specified residue and distinct weights on all $k-1$ edges. Translate the forbidden residue to zero as in the bounded-degree argument.

**Cutting edges.** Reserve two distinct terminal vertices that are not component roots, if available. Otherwise the only nontrivial component is a path rooted at an endpoint. Reserve its far endpoint and protect its penultimate vertex. Indeed, each nontrivial component has a nonroot terminal, and a rooted tree with only one terminal is a path. There is a nontrivial component since $c=o(k)$. In the one-terminal case the path has order at least $k-c$.

At every vertex with more than $D-1$ children, cut just enough outgoing edges to retain $D-1$. Keep the incoming edges of the reserved leaves, possible even when they are siblings since $D-1\ge2$. This makes $q_0=c+E_D(F)$ components of degree at most $D$. Each new component root still has a specified original edge, either to an external boundary constant or to the actual free vertex that was its parent.

Cut five more internal edges with disjoint endpoints. Choose both endpoints away from the current roots, the parents of previous cuts, the reserved leaves and any protected penultimate vertex. There are $k-1-q_0$ available internal edges before these exclusions. The residual degrees are bounded, so only $O_D(q_0+1)$ edges are excluded even after all five choices. In particular, each of these five cut parents is different from every final component root. Write $q=q_0+5$.

**Places for the new edges.** In the resulting forest let $P_*$ consist of the $q$ component roots and every free parent of a cut edge. Give each distinct vertex $v$ in this set its own variable $X_v$, even when it appears in several roles. Outside the closed neighborhoods of $P_*$, the reserved leaves and the protected vertex, choose an independent set of sites. Greedy selection gives at least $(k-O_D(q))/(D+1)$ sites in total. Sort the components $C_0,\ldots,C_{q-1}$ by nonincreasing numbers of selected sites. Write $r_i$ for their roots. In the original forest the incoming edge at $r_i$ has weight
$$
W_i=X_{r_i}+a_i,
$$
where $a_i$ is its given external constant or the variable of its free parent.

Add a dummy vertex $o$ of label zero. If $a_0$ is the constant zero, join $o$ to $r_0$. Otherwise join $o$ to a site $t$ in $C_0$ and prescribe $W_0$ at $t$. In either case the edge has weight $W_0$.

Choose a permutation $\sigma$ of $1,\ldots,q-1$ such that $i=\sigma(j)$ satisfies both $i\ne j$ and $a_i\ne X_{r_j}$ as formal expressions. To apply Hall's theorem, use $j$ as the left index and $i$ as the right. Each right index forbids at most two left indices, its own and possibly its parent's index. At least four of the five extra cut edges are on the right, even after excluding index 0. Each of their parents is outside the roots, so a single left index is eligible for at least three of these right indices. Sets of one or two left indices therefore meet Hall's condition, and a set of at least three has all right indices as neighbors.

For $1\le j<q$ choose a fresh site $s_j$ in $C_0\cup\cdots\cup C_{j-1}$, join it to $r_j$, and prescribe
$$
X_{s_j}=W_{\sigma(j)}-X_{r_j}.
$$
The first $j$ components have at least $j(k-O_D(q))/((D+1)q)$ sites, since they have the largest site counts. This exceeds $j$ for sufficiently large $k$, and at most $j$ have already been used. The new graph $U$ is a tree on $k$ vertices since every new component joins an earlier one exactly once. It has maximum degree at most $D+1$. Each new edge has its corresponding original weight as an algebraic identity. This uses the actual variable for each cut parent. Even a parent that is another component's root retains one consistent label throughout.

**Choosing the labels.** Let $P$ comprise $P_*$, the sites used, and $o$. Its label expressions are zero, the individual $X_v$, possibly $W_0$ at $t$, and the expressions at $s_j$. They are formally distinct. Each expression at $s_j$ has its unique negative coefficient at $r_j$ because the matching excludes both kinds of cancellation. The optional $W_0$ is either a sum of two distinct variables or differs from $X_{r_0}$ by a nonzero constant. The edge-weight expressions induced on $P$ are also distinct. They consist of weights on original internal edges between vertices of $P_*$ and the $W_i$. The sites are independent and have no old edges to $P_*$. Each of the resulting weight expressions represents a different incoming edge of the original forest, counting boundary edges.

A pairwise union bound would require $q^2\ll k$. A greedy choice works here for $q=o(k)$. Order the variables by any parent-before-child order of the **original** forest. In the list of edge expressions the latest variable is always the child of the represented edge, so each variable is latest at most once. In the vertex list it is latest at most four times. It can occur last in its own single-variable label, in the one optional $W_0$, as the positive child of at most one matched edge, and as the negative root of at most one matched edge. A free parent in $W_i$ always comes before its child.

Consider inequalities between two labels in the same list (vertex or edge). For pairs with different latest variables, at most $O_D(q)$ inequalities are decided at any one variable, since only constantly many expressions have it as latest. There are only $O_D(q)$ pairs with the same latest variable **in total**. If its coefficient cancels in a difference, test that difference at its own last surviving variable. Comparisons with a constant satisfy the same bounds. A constant difference is already nonzero. Each nonconstant difference has coefficients of absolute value at most two and excludes at most two choices of its final variable, over any cyclic group of order $k>2$. Thus only $O_D(q)$ values are excluded at any step, fewer than $k$ for all sufficiently large $k$. This yields a rainbow injection on $P$ satisfying every edge replacement.

**The embedding.** Complete $P$ to a degree core $Q$ and impose the two group sums exactly as in the bounded-degree proof. Here are the size details needed for the larger $q$. Add the one or two reserved leaves, then at most eleven vertices per degree class, so each class is exhausted or represented at least six times both inside and outside $Q$. In the one-leaf case keep the penultimate vertex out. Its degree is two and all but $O(q)$ vertices along the original long path still have degree two. Add two isolated vertices of the same degree $d\ge2$ to $U[Q]$, retaining the degree-class condition. A class with $\Omega_D(k)$ such vertices exists, and only $O_D(q)$ positions are excluded. Thus $|Q|=O_D(q)=O_D(k^{1-\delta})$. Take the embedding lemma's constant $\mu$ sufficiently small in terms of $D$ and smaller than $\delta$, so $|Q|\le k^{1-\mu}$ for large $k$.

Keep the labels on $P$ and greedily label the other core vertices except the reserved leaves and those last two vertices. Each step costs $O_D(q)$ exclusions. Give the reserved leaves and one of the degree-$d$ vertices independent uniform labels, and force the last label by the vertex sum. At most four labels are now variable. Every remaining vertex equality involves at least one of these four, so there are only $O_D(q)$ such tests. Every new edge sum involves a reserved leaf, hence at most two edge sums are variable and only $O_D(q)$ comparisons remain. Finally there are $O_D(q)$ comparisons with the missing weight. As in the preceding proof, that weight has coefficient $d-1$ on each reserved leaf; every edge sum omits at least one such variable. Each tested equality has probability at most $O_D(1/k)$. Thus the probability of any failure is $O_D(q/k)<1$. [Core construction and sum calculation](README.md#complete-the-prescribed-labels)

Lemma 4.9 now gives a bijective rainbow embedding of $U$ extending the specified core. Removing $o$ and restoring **all** cut and external edges keeps the weight multiset unchanged. This proves the forest lemma.

## Induction for the tree theorem

Use the largest-child-last preorder and the same induction as in the [bounded-degree theorem](README.md#from-forests-to-unrestricted-tree-orders). In the case with a nonempty suffix of $t\le k-1$ vertices, all crossing edges originate at at most $2+\log_2 t$ distinct vertices. The sum of their degrees is at most
$$
D(2+\log_2 t)+E_D(T).
$$
This bounds the number $c$ of suffix components. The suffix's free degrees are at most the original degrees, so $E_D(F)\le E_D(T)$. Padding to $k-1$ vertices along a terminal path preserves this inequality because $D\ge3$. The forest lemma therefore needs to handle at most
$$
c+E_D(F)\le D(2+\log_2 k)+2k^{1-\epsilon}\le k^{1-\epsilon/2}
$$
for sufficiently large $k$. Use $\delta=\epsilon/2$. The retained prefix and the single-leaf deletion in the other induction case preserve the original excess bound. This proves the theorem.

Consequently, along any sequence of counterexamples with $k\to\infty$, for every fixed $D\ge3$ and $0<\epsilon<1$ one must eventually have $E_D(T)>k^{1-\epsilon}$. A smallest counterexample at each modulus has fewer than $k$ leaves, and the sum of degree excesses above two is the number of leaves minus two. Thus for such minimum counterexamples the total excess above any fixed $D$ lies between $k^{1-\epsilon}$ and $k$ for every fixed $\epsilon>0$ and sufficiently large $k$. [Leaf and degree bounds](../counterexample-bound.md)

## Reproduction

The following standard-library check builds the cuts and finds a perfect matching, assigns the affine labels in the original parent order, and verifies the two embedding sums. It reconstructs the original forest from the cuts and evaluates boundary weights using the actual pinned parent values. Its 90 fixtures include adjacent high-degree vertices and repeated external boundary values.

~~~sh
python3 -B research/bounded-degree/check_excess.py
~~~
