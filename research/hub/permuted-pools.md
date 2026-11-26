# A positive-density core with many independent attachment sites

**Theorem.** Fix $0<\delta,\epsilon<1$. For all sufficiently large $k$, let $H$ be a tree with
$$
\delta k\le |H|=h\le k
$$
and at most $k^{1-\epsilon}$ leaves. Choose at most $k^{1-\epsilon}$ vertices of $H$ and add arbitrary numbers of leaves at them. Every resulting tree is $k$-cordial. The population at each site varies independently and the decorated order is unbounded.

In particular this proves the order-$k$ rainbow labeling and the order-$(k+1)$ harmonious labeling in this range. Relative to the [single-site positive-density theorem](long-branches.md), the difficulty is that leaves assigned to different parents need different translations from their vertex residues to their edge residues.

We prove the order-$k$ assertion first. Write $G=\mathbb Z/k$, $m=k-h$. The case $m\le1$ follows from the [degree-excess theorem](../bounded-degree/excess.md), since total excess above three is at most the original leaf count plus one. The proof below also permits arbitrarily small positive $m\ge2$.

## The part of the tree to be embedded

Mark every chosen site and every vertex of $H$ of degree different from two. There are $O(k^{1-\epsilon})$ segments between marks. Take $t=\lceil2(\log k)^7\rceil$. On each segment place two disjoint chains of the same number of interior vertices, a multiple of $t+1$, leaving fewer than $2(t+1)$ interior vertices outside. Put the first chain of each pair into collection 1 and the second into collection 2. In each collection let $r$ count all successive blocks of $t+1$ vertices and $c$ count the nonempty chains. Each block will be a path of $t$ edges. The extra edges between successive blocks of a chain are its connectors. Put $g=(t+1)r/k$. We have $2gk=h-|V_0|$, where $V_0$ denotes the vertices outside both collections or, after labeling, their labels. Thus $g\ge\delta/3$ and $g\le1/2$ at large $k$.

Prescribe distinct labels for $V_0$ and the first and last vertices of every nonempty chain, with distinct weights on the forest of edges outside chain interiors. This uses $O(k^{1-\epsilon}\log^8 k)$ vertices and edges. Assign greedily in component order: each new label has at most one previously assigned neighbor in this forest. Write $W_0$ for its weight set and $F_i$ for the sum of the prescribed first and last labels in collection $i$. All sites were marked, so their labels are now known. Let $m_p$ be the required number of new leaves at label $p$ and $\Sigma=\sum_p p m_p$ in $G$.

We need core vertex and color pools $A,C$, respectively, each of size $h$. The color pool includes one unused color $s$. Every leaf of label $x$ and prescribed parent $p$ uses the color $x+p$. If the leaves occupy exactly the complements of the two pools, then
$$
\sum C=\sum A-\Sigma.
$$
The weights internal to paths and connectors must sum to $2(\sum A-\sum V_0)-F_1-F_2$, by counting each incidence on the chains. Thus the required value is
$$
s=2\sum V_0+F_1+F_2-\sum W_0-\sum A-\Sigma. \tag{1}
$$

## Permuting the random coordinates

Round the numbers $k m_p/m$ up or down to integers $b_p$ summing to $k$, with errors at most one. In the list containing $b_p$ copies of $p$, replace one entry by the residue making the sum zero. Hall's prescribed-differences theorem gives a permutation $\pi$ of $G$ whose jumps $\pi(x)-x$ realize the list. Designate the changed entry as a dummy and retain the original grouping for all other entries. This permutation is chosen before drawing any random sets. [Marshall Hall Jr., *A combinatorial problem on abelian groups*](https://doi.org/10.1090/S0002-9939-1952-0050579-7)

At each $x$ independently sample a vertex collection index for $x$ and a color collection index for **$\pi(x)$** according to the joint probability matrix
$$
\begin{pmatrix}
1-2g&0&0\\
0&g^2&g-g^2\\
0&g-g^2&g^2
\end{pmatrix}.
$$
Index zero means outside the collections. Let $A_0$ be the union of vertex collections and $C_0$ the union of color collections. Then $C_0=\pi(A_0)$. For each $i=1,2$ the indicator that $x$ belongs to vertex collection $i$ and the indicator that $\pi(x)$ belongs to color collection $i$ are independent Bernoulli variables of mean $g$. These pairs are independent across $x$. Therefore the *entire* vertex-indicator array for a collection is independent of its own color-indicator array, even after the color coordinates are permuted.

Within each vertex collection choose start, middle and end roles with probabilities $1/(t+1),(t-1)/(t+1),1/(t+1)$. Within each color collection choose path and connector roles with probabilities $t/(t+1),1/(t+1)$. Make these refinements independently given the indices. With $q=r/k$, each collection has exactly the random input law of the prescribed-bijection path-factor lemma and of the random perfect-matching theorem. The four robust conclusions hold simultaneously with high probability. The start, end and connector densities are $q$ of order $1/(\log k)^7$, and the middle density is bounded below. [Müyesser and Pokrovskiy, Theorem 3.1 and Lemma 3.2](https://arxiv.org/html/2509.05280v2#S3.SS1) · [Published random Hall–Paige paper, Lemma 6.22](https://discovery.ucl.ac.uk/id/eprint/10205648/1/Pokrovskiy_s00222-025-01328-x.pdf)

## Meeting every leaf demand

In an unchanged group of jump $p$, the candidate leaf sources $x\notin A_0$ have images $x+p\notin C_0$. Their count has binomial law of mean $(1-2g)b_p$, up to the one dummy entry. Put $d=|\{p:m_p>0\}|$. The total expected absolute deviation of the group counts from their means is at most $\sum_p\sqrt{b_p}\le\sqrt{dk}$. The total difference between the means and the required counts is $O(d+|V_0|+1)$, since $(1-2g)k=m+|V_0|$. By Markov's inequality the total counting discrepancy is $o(k^{1-\epsilon/4})$ with high probability. For example use threshold $k^{1-\epsilon/3}$ on the stochastic deviation. Discard candidate arcs using any prescribed vertex or fixed color, at most $O(k^{1-\epsilon}\log^8 k)$ arcs; discard the dummy and keep up to $m_p$ candidates of each type. All but $o(k^{1-\epsilon/4})$ required leaves are assigned. The number of unused sources outside $A_0$ and unused colors outside $C_0$ is also $o(k^{1-\epsilon/4})$ with high probability, by the same discrepancy estimate.

For every $p,d'\in G$, there are simultaneously $\Omega_\delta(k)$ residues $y$ with
$$
y\in A_0,\qquad y+p\in C_0,\qquad y+d'\in C_0. \tag{2}
$$
Each trial requires at most three underlying $A_0$ coordinates, namely $y,\pi^{-1}(y+p),\pi^{-1}(y+d')$. Repeated coordinates are allowed. Each coordinate appears in at most three trials for fixed $p,d'$, so a greedy choice gives at least $k/9$ disjoint trials. Their success probabilities are at least $(2g)^3$. Chernoff's inequality followed by a union bound over $k^2$ choices proves (2).

Give each remaining leaf a fresh source in $A_0$ and a fresh target in $C_0$ with its prescribed jump. Property (2) with $d'=p$ supplies these after excluding all pins and previous repairs. The numbers of edits to the two original random unions are $o(k^{1-\epsilon/4})$. Take $A,C$ to be the complements of the final leaf sources and targets. They contain all prescribed vertex labels and all $W_0$, respectively.

Compute $s$ by (1). If $s\notin C\setminus W_0$, choose a placed leaf with source $x$, jump $p$ and old target $x+p\ne s$; there are at least two distinct leaf targets. Move this leaf to $y\in A$, with $y+p$ and $y+s-x$ in $C\setminus W_0$, avoiding all pinned vertices at $y$. Property (2) with $d'=s-x$ permits this even after the edits. The two specified colors are different. The new core vertex sum is $\sum A+x-y$, so the new value of (1) is $s+y-x$. It remains available after the move, and every leaf population is unchanged.

## Completing the paths

Adjust the two vertex collections and their roles to partition $A\setminus V_0$, with the exact sizes and specified first and last labels. Adjust the four color roles to partition $C\setminus(W_0\cup\{s\})$ into path and connector sets of sizes $tr$ and $r-c$ per collection. These sizes add correctly since $|W_0|=|V_0|+2c-1$. With high probability all random role sizes differ from their means by at most $k^{1/2+1/20}$. The edits cost $o(k^{1-\gamma})$ for some fixed $\gamma>0$ in terms of $\epsilon$; one may take $\gamma=\epsilon/10$. This includes the fixed labels. For each nonzero displacement between any two distinct fine color roles, $\Omega(k/(\log k)^{14})$ shifted pairs are available before edits. Their indicators at distinct color coordinates are independent, so this follows by taking a matching in the shift cycles and applying Chernoff's inequality. Enough pairs remain to adjust three of the role sums by one exchange each with the fourth. Their required sums add correctly by (1). This is the [four-sum construction](long-branches.md#joint-choice-of-the-random-sets).

For each collection apply the perfect matching theorem to all ends except the last end of each chain and all starts except its first start, using exactly the connector colors. The necessary sum is the sum of all end and start labels minus $F_i$. Arrange the matched edges in groups of the required lengths. They determine a bijection from all starts to all ends, including the prescribed endpoints. The path-factor lemma now supplies the chains with exactly their assigned vertices and path colors; the required sum is the sum of start and end labels plus twice the sum of the middle labels. The matching tolerance $q^{10^{18}}k/(\log k)^{10^{18}}$ and the path tolerance $k^{1-\gamma}$ both dominate the edits at sufficiently large $k$. The cyclic group is not elementary abelian of exponent two here. Adding the fixed forest and the assigned leaves produces the original tree with all vertices distinct and only $s$ unused among its edge weights. [Detailed chain reconstruction](long-branches.md#reassembling-the-tree)

Finally consider arbitrary populations on this same $H$. Below order $k$ add temporary leaves at one site and restrict the order-$k$ labeling. If there are no sites, the degree-excess theorem applies directly. Above order $k$, use induction on the total order $n$. For $n=1\bmod k$ remove one added leaf and restore the deficient edge weight. Otherwise remove $(n-1)\bmod k$ added leaves, use induction at order $1\bmod k$, and restore them by the Hall distinct-leaf lemma avoiding the one surplus vertex label. Enough added leaves exist since $h\le k$. [Leaf extension for arbitrary prescribed parents](../counterexample-bound.md#removing-leaves)

## Reproduction

The checker enumerates the full two-coordinate role law with a nontrivial permutation, exhausts Hall's condition on small groups, and verifies pool complements, actual leaf jumps, prescribed inclusions, and the omitted-color equation on prime and composite moduli. A separate set of interval-labeled trees checks the moment on the original edges. The asymptotic completion uses the primary random embedding results cited above. [Finite pool operations](permuted_pools.py) · [Independent checks](check_permuted_pools.py)

~~~sh
python3 -B -m research.hub.check_permuted_pools
~~~
