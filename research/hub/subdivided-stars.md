# Partially subdivided stars at every modulus

**Theorem.** Start with any star and subdivide any subset of its edges once. The resulting tree is $k$-cordial for every positive integer $k$. Both the number of two-edge legs and the number of unsubdivided edges are unrestricted.

More generally, root a tree of radius at most two at a center $o$. Set aside the leaves adjacent to $o$, of which there may be any number. The remaining neighbors have positive numbers of leaf children. The same conclusion holds in either of the following cases.

1. One neighbor has one child, and the other neighbors can be paired so that partners have equal numbers of children.
2. All the neighbors can be paired in this way, and at least one pair has one child at each neighbor.

The paired child counts can differ between pairs and can be arbitrarily large. Taking them all equal to one gives the first theorem, with cases 1 and 2 giving the odd and positive even numbers of subdivided edges. A star itself is handled by labeling the leaves consecutively at a zero-labeled center.

## A permutation of an interval

For $a\ge1$, alternate the smallest and largest remaining numbers of $[0,a-1]$, starting at zero, to obtain $z_1,\ldots,z_a$. The absolute differences in this list are $a-1,a-2,\ldots,1$. Form the cyclic list
$$
z_1,\ldots,z_a,\quad a+z_a,\ldots,a+z_1 .
$$
Its cyclic directed differences are precisely $1,-1,\ldots,a,-a$ in some order. The two joins contribute $a$ and $-a$, and each internal difference occurs once in each direction. The cyclic list contains all of $[0,2a-1]$.

Suppose the hub has neighbors labeled $\pm1,\ldots,\pm a$ and we attach one new leaf to each. Translate the list to any interval of $2a$ integers. When $v$ is followed by $w$, assign $v$ to the leaf whose parent has label $w-v$. That leaf's edge weighs $w$. Thus the new vertex labels and new edge weights both fill the chosen interval exactly once.

## An odd number of nonleaf neighbors

Write the paired child counts in decreasing order $s_1\ge\cdots\ge s_m\ge1$. Label $o$ by zero, the paired neighbors by $\pm1,\ldots,\pm m$, and the additional one-child neighbor by $m+1$. Give its only child label $-m-1$. Its edge weighs zero.

For each $j\ge1$ up to $s_1$, the partners needing a $j$-th child have labels $\pm1,\ldots,\pm a_j$ where $a_j$ is the number of $s_i\ge j$. Use the cyclic construction on these children. Place their intervals consecutively starting at $m+2$. With $m=0$ no such intervals are required. The complete set of vertex labels is an integer interval starting at $-m-1$. The edge weights occupy the same interval except for its minimum. Further leaves at $o$ extend both intervals by successive integers above their maximum. Every interval has balanced residue counts modulo every $k$, proving case 1.

## Extending a balanced pair of histograms

Write $V,E$ for the vertex and edge histograms modulo $k$. Suppose the hub is labeled zero, both histograms are balanced, and $V-E$ is one unit at a residue $s$. We may then attach any number of additional leaves at the hub. When $V$ is nonuniform, $s$ must be among its higher counts, or $E$ would have two counts differing by two. Add each residue with a low vertex count once, bringing $V$ to uniformity. The edge counts then have a unique deficiency at $s$. Add $s$, then each other residue once. These steps preserve balance after each leaf, and this last list can repeat. If $V$ starts uniform, begin directly with $s$.

## An even number of nonleaf neighbors

Let there be $m\ge1$ pairs as above, with $s_m=1$. For the moment omit all ordinary leaves at $o$. Write $L=2m+2\sum_i s_i$ for the number of edges. We give two choices of integer labels.

- Place the paired neighbors at $\pm1,\ldots,\pm m$ and use the cyclic construction on the successive layers starting at $m+1$. The vertices fill $[-m,-m+L]$, and the edge weights have the same multiset with zero removed.
- Omit the last pair and apply the odd construction to the other pairs and one of the two omitted neighbors. The resulting vertices fill an interval beginning at $-m$, with that minimum absent from the edge weights. Give the last neighbor label $-m-1$ and its child label 1. Its edges weigh $-m-1$ and $-m$. Now the **edges** fill $[-m-1,-m-1+L-1]$, and the vertex multiset is that interval together with one additional 1.

Suppose $k\ge m+3$ and put $r=L\bmod k$. If $r\ge m$, use the first construction. When $r=k-1$ its vertex histogram is uniform. Otherwise its high residues are the first $r+1$ residues of the interval and include zero, at offset $m$. Removing one zero therefore gives a balanced edge histogram. If $r<m$, use the second construction. Its first $r$ interval residues are the high edge counts. The residue 1, at offset $m+2<k$, lies outside that set, so adding one occurrence leaves the vertex histogram balanced. In each case $V-E$ is one unit, and the preceding extension adds all ordinary hub leaves.

For $k\le m+2$ the hub has degree at least $2m\ge k-1$. The following lemma completes case 2.

## A radius-two tree with a wide first level

**Lemma.** A tree of radius at most two with at least $k-1$ neighbors at its chosen center is $k$-cordial. More generally, it suffices that its maximum degree be at least $k-1$.

At a cordial core of order $1\bmod k$, all edge counts are uniform and one vertex residue has a surplus, for $k\ge2$. We may attach up to $k-1$ vertices whose parents are already present: Hall's permutation theorem gives distinct labels avoiding the surplus and distinct new weights. In a batch of exactly $k$ vertices the final vertex may even have a parent among the preceding $k-1$. After those $k-1$ are labeled, vertices are uniform and one edge weight is missing. Choose the last label to supply it. This restores a cordial core of order $1\bmod k$. In particular, any number of leaves with already labeled parents may now be added in batches. The case $k=1$ is immediate. [Hall's theorem and the partial permutation argument](../counterexample-bound.md#removing-leaves)

Let $d$ be the hub degree, including its ordinary leaf neighbors. For $d=k-1$, add all neighbors, then one grandchild as the last member of a batch, if there is a grandchild. All remaining vertices now have labeled parents. For $d\ge k$, first add $k\lfloor d/k\rfloor$ neighbors in complete batches, choosing neighbors with the most children first. If every remaining neighbor has no children, all remaining vertices are ready to be labeled. Otherwise at least $k$ grandchildren of already labeled neighbors are available. Add the remaining $d\bmod k$ neighbors and enough of those available grandchildren to complete one batch. Again every remaining vertex has a labeled parent. This proves the first assertion.

If $d<k-1$ and a neighbor has degree at least $k-1$, that neighbor has at least $k-2$ children. The case $d=1$ is a star. For $d\ge2$, take the hub, its $d$ neighbors and $k-d$ children of that neighbor. This core of order $k+1$ is a caterpillar, hence cordial by Hovey's theorem. All other vertices are leaves at already labeled parents. The same argument works whenever the two most populous neighbors together have at least $k-d$ children: the core then has a three-vertex spine. [Hovey, *A-cordial graphs*](https://doi.org/10.1016/0012-365X(91)90254-Y)

## A single-order test for all radius-two trees

**Corollary.** At each fixed modulus $k$, every tree of radius at most two is $k$-cordial if and only if every such tree of order exactly $k$ is $k$-cordial. The test uses at most the number of integer partitions of $k-1$, including the empty partition at $k=1$. Each part records one hub neighbor together with all its children.

For sufficiency, extend any smaller tree to order $k$ by adding leaves at a center. Restricting a cordial labeling on exactly $k$ vertices preserves distinct labels and distinct weights. If there is a larger counterexample, choose a smallest one within the radius-two family, of order $n>k$. A star is cordial, so take its center $o$ of degree at least two. The wide-first-level lemma excludes hub degree at least $k-1$. In particular the number $c$ of nonleaf neighbors of $o$ is smaller than $k$. The number of original leaves is $L=n-1-c$.

If $n$ is one modulo $k$, delete one leaf and label the smaller tree by minimality. Its vertex counts are uniform and one edge weight is deficient, so the leaf can supply it. Otherwise put $t=(n-1)\bmod k$. Since $n>k$, we have $t\le n-1-k<L$. Delete $t$ original leaves, retaining a smaller tree of radius at most two and order one modulo $k$. By minimality and the partial Hall extension in the lemma, all $t$ leaves can be restored. Both cases contradict minimality. The case $k=1$ is immediate.

## Verification and related results

The program checks the integer intervals and the underlying tree shapes on 924 multisets of paired child counts. It also constructs actual modular labels for partially subdivided stars at $1\le k\le96$ with zero through $2k$ two-edge legs, and checks both histograms after each prefix through two periods of additional leaves. For many two-edge legs the implementation uses the [balanced construction for $k$ identical branches](../repeated-branches.md) to reduce their number first. These finite checks exercise the formulas; the proofs above give unrestricted parameters.

~~~sh
python3 -B -m research.hub.subdivided_stars
~~~

Consecutive vertex and edge intervals are the strongly indexable, or super edge-magic, route to cordiality at every modulus. Youssef proved the implication in Theorem 4. Fukuchi and Oshima studied super edge-magic constructions for diameter-four trees, and Meng's more recent construction suite treats equal-leg spiders. The arguments here give the hub labels, the placement of ordinary leaves, and the modular choice between the two even-case templates explicitly. [Youssef, *On k-cordial labelling*](https://ajc.maths.uq.edu.au/pdf/43/ajc_v43_p031.pdf) · [Fukuchi and Oshima, *Super-edge-magic labelings of a family of trees with diameter 4*](https://www.pphmj.com/article.php?act=art_abstract_show&art_id=3265&flag=next) · [Meng, equal-leg spider constructions](https://zenodo.org/records/22652143) · [Reproducible checks](subdivided_stars.py)
