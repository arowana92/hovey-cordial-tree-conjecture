# Radius-two trees with prescribed numbers of branching neighbors

**Theorem.** Fix a vertex within distance two of every vertex of a finite tree. Let $c$ be the number of its neighbors that have children when the tree is rooted there. Every such tree is cordial at every positive modulus if $c\le5$, or if $c$ is odd and $7\le c\le33$. The child counts, the number of additional leaves at the root, and the tree order are unrestricted.

The integer construction for $c=3$ needs no certificate. The case $c=4$ uses 150 small integer labelings. For odd $c$, a separate sufficient test requires only one pair of integer permutations for each pair of distinct ranks up to $(c-1)/2$. We verify all 120 pairs through rank 16.

## Enough to label the tree at its own order

Write $o$ for the root and $d$ for its degree. We will construct distinct integer vertex labels filling an interval of length $n$ on any tree of the indicated type with $n$ vertices. Its edge sums fill that interval except for one integer. At modulus $n$ this gives the required bijection. The position of the omitted integer can vary with the tree.

Here is why the order-$k$ construction suffices for **each fixed $c$** at arbitrary modulus $k$. If $n<k$, adjoin ordinary leaves at $o$ up to order $k$ and restrict. If $n>k$ and $d\ge k-1$, the [wide first level lemma](subdivided-stars.md#a-radius-two-tree-with-a-wide-first-level) applies. Otherwise form a core from $o$, its $d$ neighbors and $k-1-d$ grandchildren. If $k-1-d\le c$, take at most one grandchild from each neighbor. The resulting partially subdivided star is [cordial at every modulus](subdivided-stars.md). If $k-1-d>c$, choose at least one from each nonleaf neighbor, preserving $c$, and use the order-$k$ theorem. Every remaining vertex is a leaf at a parent in the core. Add the first leaf to supply the missing edge weight. Hall's extension at order $1\bmod k$ attaches all further leaves. This argument also permits any number of ordinary leaves added to the integer construction by using consecutive new integers at the upper end. On each such leaf, its label equals its edge weight since $o$ has label zero.

The cases $c\le2$ are caterpillars. [Hovey's caterpillar theorem](https://doi.org/10.1016/0012-365X(91)90254-Y)

## Constructing the interval for odd $c$

Let $c=2m+1$. Arrange the child counts as $t_1\ge\cdots\ge t_c\ge1$. Label their parents in the order
$$
1,-1,2,-2,\ldots,m,-m,m+1 .
$$
Write $P_r$ for the first $r$ parent labels. A layer takes one child from each of these $r$ parents. There are $e_r=t_r-t_{r+1}$ layers of rank $r$ with $t_{c+1}=0$.

For a cycle of integers, each consecutive pair $x,y$ including the last-to-first pair can supply a child labeled $x$ at parent $y-x$. Its weight is $y$. A translated cycle therefore assigns its own integer set on both vertices and edges. For $a\ge1$, let $z$ list $0,\ldots,a-1$ by taking alternately the smallest and largest remaining entry. Define the list $W_a$ as $z$ followed by $a+z$ in reverse order. As a cycle it uses precisely the directed differences $\pm1,\ldots,\pm a$. Its two joins give $\pm a$ and the two traversals of $z$ give the other differences. Its entries fill $[0,2a-1]$.

Suppose all labels fill $[L,U]$ and the unused weight is $L$. A path of depths $0=x_0,x_1,\ldots,x_t$ visiting $[0,t]$ once gives children of labels $L-x_i$ at parents $x_i-x_{i-1}$. Their weights fill the newly enlarged interval up to the new unused weight $L-x_t$. When $x_t=t$, we can continue from the new minimum.

Use one full layer first. The child of $m+1$ receives $-m-1$ and its edge weighs zero. Use $W_m$ as a cycle above $m+1$ for the paired parents, omitting this cycle at $m=0$. The labels now fill an interval with the minimum unused as a weight. Remove this layer from the multiplicities.

- A rank-one layer extends the depth path by one. Every even layer of rank $2a$ uses the cycle $W_a$ above the current interval.
- Two odd layers of the same rank $2a+1$, $a\ge1$, use the cycle $W_a$ above the interval and the depth path $W_{a+1}$ followed by $2a+2$ below. The open part of $W_{a+1}$ has differences $\pm1,\ldots,\pm a$ and $a+1$. Appending $2a+2$ contributes a second $a+1$. The new minimum is the unused weight.
- A single odd layer of rank $2a+1$ can finish the construction. Use the depth path $W_{a+1}$ alone. Its last depth is $a+1$, leaving one missing weight in the enlarged interval.

These rules alone prove the order-$n$ assertion for any odd $c$ whenever, after the first layer, at most one odd rank greater than one has odd multiplicity. In particular they always suffice at $c=3$. When there are more remaining single layers, pair them in order of rank and use the following test before the final single layer, if any.

### Two distinct odd ranks

For ranks $2a+1,2b+1$ with $1\le a<b$, put $l=a+b+2$ and $u=a+b$. Seek lists of parent labels $p_1,\ldots,p_l$ and $q_1,\ldots,q_u$. Their combined multiset must be $P_{2a+1}$ together with $P_{2b+1}$. Require
$$
\{x-p_x:1\le x\le l\}=[0,l-1],\qquad
\{x-q_x:1\le x\le u\}=[1,u].
$$
On the lower side use label $L-x$ at parent $p_x$. On the upper side use label $U+u+1-x$ at parent $q_x$. The two conditions give exactly the enlarged interval of weights except for its new minimum $L-l$. For instance at $(a,b)=(1,2)$ the respective lists are $(-2,2,1,3,1)$ and $(-1,-1,2)$.

The [certificate](odd-layer-pairs.jsonl) gives these two lists for every $1\le a<b\le16$. The interval construction applies whenever all the required pairs have witnesses. No bound on the multiplicities enters the test. Establishing these integer permutations for all pairs would prove the tree theorem for every odd $c$.

## Four nonleaf neighbors

Write $e_1,e_2,e_3,e_4$ for the layer multiplicities, with $e_4\ge1$. Retain $f_1=\min(e_1,4)$, $f_2=0$, and for $i=3,4$ let $f_i=e_i$ if $e_i<4$, otherwise $f_i=4+(e_i\bmod2)$. These give exactly 150 possible tuples. For each, the [seed certificate](four-branch-seeds.jsonl) gives a lower interval endpoint, four parent labels in decreasing child-count order, and a parent label for each remaining vertex label in increasing order. The hub is zero. Direct verification gives distinct vertex labels filling the interval and distinct edge weights in it. The first two parents are always $1,-1$. If any $f_i\ge4$, the missing weight is the interval minimum. If $f_3\ge4$ or $f_4\ge4$, the four parent labels are $1,-1,3,-2$.

Restore the discarded layers. Rank one uses successive lower depths, and rank two uses the upper two-cycle with differences $1,-1$. Discarded layers at ranks three and four occur in pairs. For a pair of rank-three layers use the lower depth path
$$
0,1,2,5,4,3,6 .
$$
For two rank-four layers use the lower path $0,1,2$ and two translated upper cycles $(0,3,1)$ and $(2,5,4)$ in one interval of six integers. This gives two copies of each of $1,-1,3,-2$. Each lower path leaves the new minimum unused. If the seed's unused weight is elsewhere, only rank-two layers could have been discarded and they use only the upper cycle. This finishes all four-branch profiles.

## Verification

The standard-library checker verifies the list of required ranks and seed profiles, all displacements, multiplicities, interval claims and seed endpoint conditions. It also generates and checks 3,270 full tree labelings by recomputing endpoint sums. The proofs above cover the unbounded tree orders and child counts.

~~~sh
python3 -B -m research.hub.branch_levels
~~~

The optional search program can generate fresh witnesses. The two-rank search uses OR-Tools CP-SAT. Both parts checkable from the published data use only standard Python. [Construction and independent checks](branch_levels.py) · [Witness search](level_search.py)
