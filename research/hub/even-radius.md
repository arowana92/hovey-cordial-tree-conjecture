# Even moduli and trees of radius two

**Theorem.** Let $k=2s$. If a tree has a vertex $o$ within distance two of every vertex and $\deg(o)\ge s-1$, the tree is $k$-cordial. The tree can have any finite order. At order $2s$ this gives a bijection with pairwise distinct edge sums.

## A subgroup criterion

Let $q,s\ge2$. Let a tree on $qs$ vertices consist of a connected core $C$ of order $s$ and leaves attached to it. For each core vertex $v$, let $m_v$ be the number of attached leaves. There is a bijective labeling in $\mathbb Z_{qs}$ with distinct weights that maps the core onto the subgroup $q\mathbb Z_{qs}$ **if and only if** there is a bijection $v\mapsto h_v$ of the core onto $\mathbb Z_s$ such that

1. the internal edge sums $h_v+h_w$ are distinct modulo $s$, and
2. $\sum_v m_vh_v=0\pmod s$.

Indeed, label $v$ by $qh_v$. Outside the core, each leaf and its edge belong to the same nonzero coset of the subgroup. In any requested labeling every such coset occurs in full on both leaves and edges. Subtracting their sums gives condition 2, and the internal edges give condition 1.

Conversely, take one copy of its parent's digit $h_v$ for every attached leaf. These $(q-1)s$ entries sum to zero. Partition them into $q-1$ zero-sum groups of size $s$. While at least $2s$ entries remain, the Erdős–Ginzburg–Ziv theorem supplies $s$ entries summing to zero. The final group has zero total by subtraction. For group $j$, give its leaves labels $j+qt_i$ for $1\le j<q$, choosing $t_i$ to fill $\mathbb Z_s$. Since the parent digits of this group sum to zero, Hall's permutation theorem allows $t_i$ and $t_i+h_{v(i)}$ both to run through $\mathbb Z_s$. This fills coset $j$ once on vertices and edges. The core labels and internal edge sums fill the zero coset except for one missing weight. [Erdős, Ginzburg and Ziv (1961)](https://www.renyi.hu/~p_erdos/1961-25.pdf) · [Marshall Hall Jr. (1952)](https://doi.org/10.1090/S0002-9939-1952-0050579-7)

If $C$ is a star, every bijection of its vertices already satisfies condition 1. Thus the complete test is the existence of a permutation of $0,\ldots,s-1$ with zero scalar product against the list of counts. Nagy's Theorems 1.3 and 1.5, Proposition 1.4 and Lemma 2.2 give the exact exceptions for the residues of this list. At odd $s$ the exception has $s-2$ copies of $a$ and two entries $a+b,a-b$ for a unit $b$. At even $s$ this same exception requires even $a$, and there is also the exception in which all entries have the same odd residue modulo the full power of two dividing $s$. [Zoltán Lóránt Nagy, *Permutations over cyclic groups*](https://arxiv.org/pdf/1211.6875)

## Order exactly twice the subgroup size

Suppose first that the tree has order $2s$. We give the argument for $s\ge5$; at $s\le4$ the tree theorem for $k\le8$ applies. Take $o$ and $s-1$ neighbors as the star core, including every neighbor with a child. There are at most $s-1$ such neighbors since each requires two vertices other than $o$. All $s$ vertices outside the star are leaves. Their parent counts $m_v$ are nonnegative integers with sum $s$. In particular $m_o=\deg(o)-(s-1)$.

For these counts the exceptions simplify. A count equal to $s$ gives the all-zero list of residues and satisfies condition 2 directly. Otherwise each count is already its own least nonnegative residue. In the two-exceptional-entry pattern $(s-2)a\le s$ forces $a\le1$. At $a=0$ the two positive counts are $b,s-b$. At $a=1$ the two other counts must sum to two and differ from one, so they are zero and two. This last pattern can occur only for odd $s$. In the homogeneous even exception every count is positive, forcing every count to be one.

If there are just two positive counts, deleting the leaves leaves a path of at most three vertices, so Hovey's caterpillar theorem applies. In the all-ones case the tree is a partially subdivided star. In the odd case with counts $0,2,1,\ldots,1$, it is also a partially subdivided star if $m_o=2$. The remaining two shapes have the following direct labelings. [Hovey's caterpillar theorem](https://doi.org/10.1016/0012-365X(91)90254-Y) · [Partially subdivided stars at every modulus](subdivided-stars.md)

Write $E(i)=(0,i)$ and $O(i)=(1,i)$ in $\mathbb Z_2\times\mathbb Z_s\cong\mathbb Z_{2s}$, and label the hub $E(0)$. Call a two-edge path attached at the hub a leg, and a neighbor with two leaf children a fork.

- **When $m_o=0$**, there are $s-2$ legs and a fork. For $i\notin\{-1,0,1\}$ use a leg $E(i),O(i)$, listed from the hub outward. Its weights are $E(i),O(2i)$. Give the fork label $E(-1)$ and its children $E(1),O(-1)$. The last leg is $O(0),O(1)$. Including the hub, these six vertices fill the unused vertex labels. The five new weights are $E(-1),E(0),O(-2),O(0),E(1)$. Only $O(2)$ remains missing.
- **When $m_o=1$**, there are $s-3$ legs, a fork and two ordinary hub leaves. For $i\notin\{-2,-1,0\}$ use a leg $E(i),O(-2i-3)$. Its weights are $E(i),O(-i-3)$. Give the fork label $O(-1)$ and its children $E(-1),O(1)$. Give the two hub leaves $E(-2),O(-3)$. With the hub these fill the unused vertex labels. The five new weights are $O(-1),O(-2),E(0),E(-2),O(-3)$. Only $E(-1)$ remains missing.

Multiplication by two permutes $\mathbb Z_s$ for every odd $s$. This verifies the vertex coverage and weight distinctness in both formulas and finishes the order-$2s$ case.

## Every order

At order smaller than $k$, add leaves to $o$ to reach order $k$ and restrict the bijective labeling. At larger order the [wide first level lemma](subdivided-stars.md#a-radius-two-tree-with-a-wide-first-level) already gives the result for $\deg(o)\ge k-1$. Otherwise take $o$, all its neighbors and enough of their children to form a core of order exactly $k$. Its degree at $o$ still satisfies the hypothesis. Give it the order-$k$ labeling just proved. Every additional vertex is a leaf whose parent is already present. Add one leaf to supply the missing edge weight, giving a cordial core of order $1\bmod k$. The partial Hall extension in the same lemma now adds every remaining leaf in batches. This proves the theorem.

## Reproducible checks

The checker constructs the two exceptional shapes with their stated labels, converts the product-group coordinates to ordinary residues, checks the branch sizes and recomputes every vertex and edge count. Separately it enumerates the partitions of $s$ and tests the zero scalar product directly. It also searches for full labelings with core labels constrained to the subgroup in small instances of the general criterion.

~~~sh
python3 -B -m research.hub.even_radius
~~~
