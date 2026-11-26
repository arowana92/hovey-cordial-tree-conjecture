# Bounded maximum degree and large moduli

**Theorem.** For every fixed positive integer $\Delta$ there is a $k_0(\Delta)$ such that every finite tree of maximum degree at most $\Delta$ is $k$-cordial for every $k\ge k_0(\Delta)$. The order of the tree is unrestricted. The proof works for composite and prime moduli.

Müyesser and Pokrovskiy announced this regime in their concluding remarks and described a possible extension of their embedding theorem to some vertices of logarithmic degree. Here we derive the result using their bounded-degree embedding lemma as stated. The construction replaces the boundary edges of a forest by edges in a bounded-degree tree, preserving their weights as a multiset. We give the proof for the stronger prescribed-boundary statement first. [Müyesser and Pokrovskiy, *On the Graham–Sloane harmonious labelling conjecture*, version 2, §6](https://arxiv.org/html/2509.05280v2#S6)

## A prescribed-boundary forest

**Lemma.** Fix $\Delta\ge2$ and let $k$ be sufficiently large in terms of $\Delta$. Let $F$ be a forest on $k-1$ free vertices with $1\le c\le k^{1/3}$ rooted components. Give each component root one edge to an external parent of arbitrary prescribed label in $G=\mathbb Z/k\mathbb Z$. Suppose each free vertex has degree at most $\Delta$, counting these edges. For every $u\in G$, the free vertices admit a bijection to $G\setminus\{u\}$ such that the $k-1$ weights, including those on the boundary edges, are distinct.

Subtract $u$ from every prescribed label. It suffices to solve with forbidden label zero, since adding $u$ back to every vertex shifts all weights by $2u$. Number the components from $0$ to $c-1$, with component 0 largest. Write $r_j$ for the roots and $b_j$ for the normalized boundary labels. Component 0 has at least $(k-1)/c$ vertices.

### Replace the boundary edges

Retain all internal edges of $F$ and add a new vertex $o$ with label zero. The following $c$ new edges make the resulting graph $U$ a tree on exactly $k$ vertices. Prescribe provisional labels $X_j$ at $r_j$. We will choose their values after specifying the edges.

1. If $b_0=0$, join $o$ to $r_0$. Otherwise join $o$ to a fresh site $t$ in component 0, with prescribed label $X_0+b_0$. This edge always has the first original boundary weight $X_0+b_0$.
2. For $c=1$ this finishes the construction. For $c=2$, join $r_1$ to $o$ if $b_1=0$. Otherwise join $r_1$ to a fresh site of prescribed label $b_1$ in component 0. This gives weight $X_1+b_1$.
3. For $c\ge3$, choose a cyclic permutation $\sigma$ of $\{1,\ldots,c-1\}$. For each such $j$ join $r_j$ to a fresh site $s_j$ in component 0 with prescribed label
   $$
   X_{\sigma(j)}+b_{\sigma(j)}-X_j.
   $$
   The new edge at $r_j$ has the original boundary weight at $r_{\sigma(j)}$.

To choose the sites, reserve the following leaves for the next step. If component 0 has at least two vertices without children, reserve two of them. Otherwise it is a path rooted at an endpoint. Reserve its far endpoint and protect its penultimate vertex. Choose all fresh sites distinct and nonadjacent to each other and outside the closed neighborhoods of $r_0$ and the reserved or protected vertices. This is possible greedily. At each pick at most $O_\Delta(c+1)$ sites are excluded, whereas the component has at least $(k-1)/c$ vertices. In particular the reserved leaves retain degree one. Each new edge joins different components at the moment of insertion if we attach $o$ first and the other components afterwards. The maximum degree of $U$ is at most $D=\Delta+1$.

Let $P$ be the vertices with prescribed labels, including $o$, all roots and all selected sites. The only edges induced on $P$ are precisely the new edges. Choose the $X_j$ independently and uniformly in $G$. Any two of the displayed vertex labels either differ by a nonzero constant or their difference has a nonzero variable coefficient of absolute value at most two. In detail, the variable coefficient vectors are the unit vectors, a possible second copy of $e_0$ separated from the first by $b_0\ne0$, and the distinct vectors $e_{\sigma(j)}-e_j$. The possible two constant labels are $0$ and $b_1\ne0$. Distinct desired boundary weights have different variable indices. Over a composite modulus a nonzero coefficient $a$ yields at most $\gcd(|a|,k)$ solutions in that variable. The probability of any specified nonconstant collision is at most $2/k$. There are $O((c+1)^2)$ comparisons, so for sufficiently large $k$ there is an injective assignment on $P$ whose edge weights are distinct. Fix it. Every extension has exactly the required correspondence between new and original boundary weights.

### Complete the prescribed labels

We use the following implication of Müyesser and Pokrovskiy's Lemma 4.9. Take a bounded-degree tree $U$ on $k$ vertices, $G=\mathbb Z/k\mathbb Z$, and $S=\sum_{g\in G}g$. Let $Q$ be an induced subforest in which every degree class of $U$ is either exhausted or represented by at least six vertices both inside and outside $Q$. For some fixed, sufficiently small $\mu>0$ in terms of $D$, suppose $|Q|\le k^{1-\mu}$. If $\phi$ labels $Q$ injectively with distinct edge sums and
$$
\sum_{v\in Q}\phi(v)=S,\qquad
w=S-\sum_{v\in Q}d_U(v)\phi(v)
$$
is absent from the edge sums of $Q$, the lemma gives a bijection on $U$ extending $\phi$ whose edge sums are precisely $G\setminus\{w\}$. Indeed, these are its vertex and color targets, of sizes $k$ and $k-1$. For $k>2$ our cyclic group is never an elementary abelian 2-group. Retention of $\phi$ is explicit in the forward construction in the proof of Theorem 2.3. [Definition 2.1 and Theorem 2.3](https://arxiv.org/html/2509.05280v2#S2) · [Lemma 4.9 and the extension implication](https://arxiv.org/html/2509.05280v2#S4)

Start $Q$ with $P$ and the one or two reserved leaves. Enlarge it to satisfy the degree-class condition. For each class, if fewer than six vertices remain outside, take all of them. Otherwise, if fewer than six are inside, take enough to reach six, then take the remainder as well if fewer than six would be left outside. This costs at most eleven extra vertices per class. In the one-leaf case we can keep the penultimate vertex out of $Q$. It has degree two, and all but $O(c+1)$ vertices of the long primary path still have degree two, so this class has ample alternatives. The reserved leaf is then isolated in $U[Q]$.

There is a degree $d\ge2$ occurring $\Omega_D(k)$ times, since $\sum_{v\in U}(d_U(v)-1)=k-2$ and the degrees are bounded by $D$. Add two vertices $z,z'$ of this degree, outside the closed neighborhood of $Q$, nonadjacent to each other and different from the protected penultimate vertex if present. These conditions exclude only $O_D(c+1)$ vertices. Both new vertices are isolated in $U[Q]$, the degree-class condition persists, and $|Q|=O_D(c+1)\le k^{1-\mu}$ for large $k$ (take $\mu<1/2$).

Let $Y$ denote the set of reserved leaves. Greedily label $Q\setminus(Y\cup\{z,z'\})$, keeping the labels on $P$. At each step avoid used vertex labels and choices that give an existing edge weight. At most $O_D(|Q|)$ values are excluded. Edges added simultaneously at one vertex have distinct weights because their other endpoints already have distinct labels.

Give the leaves of $Y$ and $z$ independent uniform labels in $G$. Force the last label $\phi(z')$ by the sum condition $\sum_Q\phi=S$. Each new vertex equality has probability at most $2/k$, including $\phi(z)=\phi(z')$. Any new edge of $U[Q]$ contains a reserved leaf, and each such leaf has at most one edge there. Two reserved leaves cannot be adjacent in a tree of this order. Hence any new edge-weight collision has probability at most $1/k$. The missing weight has the form
$$
w=C+(d-1)\sum_{y\in Y}\phi(y)
$$
for a fixed $C\in G$, since the pair $z,z'$ has equal degree and their label sum is fixed once the leaf labels are given. With two reserved leaves, each edge sum omits at least one of their variables. With one leaf, it is isolated in $Q$, so every edge sum omits its variable. Therefore the probability that any particular edge sum equals $w$ is at most $(d-1)/k$. A union bound over $O_D(|Q|^2)$ conditions is less than one for sufficiently large $k$ because $c\le k^{1/3}$. This proves the existence of $\phi$ with both required sums and no collisions.

Apply the extension lemma to $U$. Delete $o$ and replace the $c$ auxiliary edges by the actual boundary edges. The same weight multiset is retained, and the remaining labels are precisely the nonzero residues. This proves the forest lemma.

## From forests to unrestricted tree orders

Root any finite tree and perform preorder depth-first traversal, visiting a largest child subtree last at every vertex. A nonempty prefix is connected. Suppose it leaves a nonempty suffix of $t$ vertices. If the tree has maximum degree at most $\Delta$, the suffix has at most $\Delta(2+\log_2 t)$ components.

To see this, each crossing edge leaves either the last prefix vertex or one of its ancestors. Mark the proper ancestors having an unvisited child. At a marked ancestor, the child toward the last prefix vertex was processed before some unvisited largest child, so the latter's subtree is at least as large as the former's. Going upwards through the marked ancestors at least doubles the subtree size at each one. If there are $a\ge1$ marks, the unvisited largest child of the top mark has at least $2^{a-1}$ vertices. All are in the suffix, so $a\le1+\log_2 t$. Each marked ancestor and the last prefix vertex contribute at most $\Delta$ crossing edges. A connected prefix in a tree has exactly one crossing edge per outside component.

Fix $k$ large enough for the forest lemma and for $\Delta(2+\log_2 k)\le k^{1/3}$. Proceed by strong induction on the order $n$, starting with a single vertex. If $n>1$ and $n\equiv1\pmod k$, remove one leaf. The smaller tree has uniform vertex counts and a unique deficient edge weight. Give the leaf the label producing that weight.

In all other cases write $n=mk+1+t$ with $1\le t\le k-1$ and $m\ge0$. Take the prefix of order $mk+1$. Its cordial labeling by induction uses one surplus vertex label $u$ and has uniform edge counts. The suffix has at most $k^{1/3}$ components by the traversal bound. If $t<k-1$, extend one terminal vertex by a path to bring the free order to $k-1$. This keeps the component count and the bound on degrees, using $\Delta\ge2$. Apply the forest lemma with the actual boundary labels and restrict to the original suffix. Its distinct vertex labels avoid $u$, and its distinct weights include all boundary edges. Both histograms on the full tree are balanced. This closes the induction. Trees of maximum degree at most one are immediate.

The argument supplies no numerical value for $k_0(\Delta)$. Its external asymptotic input is the stated bounded-degree embedding lemma. The unrestricted conjecture still allows the maximum degree to grow with the modulus.

## Reproducing the algebra checks

Run the following from the repository root. The program constructs the auxiliary tree and a core assignment, then checks the graph, the boundary weight multiset, the degree-class condition, the vertex sum and the degree-weighted sum directly. Its 384 instances include prime, even composite and odd composite moduli, coincident boundary labels, and primary components with one or several terminal vertices. These checks exercise the construction. The asymptotic extension itself uses the cited embedding lemma.

~~~sh
python3 -B research/bounded-degree/check.py
~~~
