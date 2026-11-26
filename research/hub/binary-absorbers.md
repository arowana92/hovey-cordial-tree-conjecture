# Arbitrary binary branches at a one-hub core

**Theorem.** Let $H$ be a finite tree with a specified vertex $o$. Suppose every vertex other than $o$ has degree at most three. For every sufficiently large modulus $k$, adding any number of leaves at $o$ produces a $k$-cordial tree. There is no bound on the degree of $o$, the number of branch vertices, or the height. The threshold may depend on $H$.

More generally, any one of the 29 pendant trees certified below, attached at a nonzero-depth vertex, suffices even if the entire rest of the tree has unrestricted degrees. Two pendant stars of arbitrary positive sizes sharing an external parent also suffice. All conclusions use ordinary endpoint sums.

## Absorbing a surplus from the rest of the tree

Temporarily remove a pendant subtree $S$ attached to a vertex $P\ne o$, retaining $P$ and $o$ in the old tree. Give $o$ label zero, its $d$ neighbors the labels $1,\ldots,d$, and initialize a running integer at $Y=d+1$. Visit the remaining vertices in any parent-before-child order. At each one assign the running integer as its label and then add its parent's label to the running integer. Let $L$ be the terminal value.

The old vertices have distinct nonnegative labels. All lie below $L$, and $P$ has a label $0<p<L$. Each non-hub edge in the growth step has sum equal to the next running value. Thus, in multiset notation, the old edge weights equal the old vertex labels less $0,Y$ plus $L$. If there are no growth steps, $Y=L$ and those terms cancel. The underlying positive running recurrence is also described in Ellingham's discussion of sum graphs. His strong sum-graph problem imposes restrictions on nonedges as well. [Ellingham, *Sum graphs from trees*, Section 2](https://math.vanderbilt.edu/ellingmn/paper/sgft/sgft-final-2p.pdf)

Supply rational labels to $S$ satisfying all of the following:

- Exactly one vertex has label $L$. All its other labels lie outside $[0,L]$, and all its vertex labels are distinct.
- The edges of $S$, including its boundary edge at $P$, use the new vertex labels except $L$, together with zero.

The surplus $L$ is now a vertex label and zero is used as a weight. The entire tree has distinct vertex labels and weights, with $Y$ its only unused weight. Clear denominators, reduce at any modulus above the integer span, and use the periodic list of leaves at zero. [One-hub equivalence](rational.md) · [Leaf extension](README.md)

For example, a downward path of four new vertices can receive
$$
-p-L,\quad L,\quad -L,\quad -p.
$$
The four weights are $-L,-p,0,-p-L$. This handles a pendant path of four at any non-hub vertex, with an arbitrary tree on the other side.

## Which binary trees need a certificate?

Regard a branch at $o$ as a rooted tree growing away from $o$. Every non-hub vertex has at most two children. Write a leaf as `()` and another vertex as parentheses enclosing its children's codes in lexicographic order. Keep these seven small trees as possible remainders:
~~~
()  (())  ((()))  (()())  ((()()))  ((())())  ((()())())
~~~
They have orders one through five. An empty, one-element or two-element multiset drawn from these seven gives exactly $1+7+28=36$ possible trees upon adjoining a new root. Seven are the remainders themselves. The archive supplies a pendant construction for each of the other 29.

A binary subtree with no certified subtree among itself and its descendants must be one of the seven remainders, by induction on order. If a branch contains a certified **proper** descendant subtree, its parent is different from $o$ and the positive construction applies to all of $H$. In the remaining case each child subtree of the branch root is a remainder. The entire branch is then one of the 36 trees, of order at most eleven. The verifier checks a coprime order for each nonsingleton one. The [branch lemma](branches.md) attaches any sequence of them at the hub; singleton branches can always take fresh labels.

## Checking every boundary ratio

Normalize by $L$ and put $r=p/L\in(0,1)$. A generic template gives each vertex an affine form $ar+b$. One is identically one. For each other form the checker tests its two endpoint values $b,a+b$ to ensure its entire open interval lies below zero or above one. It adds the coefficient pairs along every edge, including the external form $r$, and compares the edge multiset with the vertex forms minus one plus zero.

Distinct forms can coincide at only one ratio. The checker computes every such ratio in $(0,1)$ exactly, then intersects the collision sets across generic templates for that shape. A special-ratio record can cover a remaining point by direct rational addition. For example one seven-vertex tree uses a separate labeling at $p/L=1/3$. This check quantifies over every boundary ratio.

The archive contains 32 templates for the 29 shapes. The verifier reconstructs all 36 transitions independently from the seven remainders, validates the identities, and recomputes vertex labels and ordinary endpoint sums on 406 complete trees. The universal conclusion follows from the induction and the exact boundary-ratio check. [Certificate](binary-absorbers.jsonl) · [Independent verification and construction](binary_absorbers.py)

~~~sh
python3 -B -m research.hub.binary_absorbers
~~~

## Two pendant stars with arbitrary numbers of leaves

Suppose two children $A,B$ of a non-hub vertex $P$ have only leaf children and have at least one each. Remove both subtrees and use the same positive construction. Give $A,B$ labels $-p-L,-p$ respectively. Give one child of $A$ label $L$ and one child of $B$ label $-L$. The four new weights are $-L,-p,0,-p-L$, so the labeling has unused weight $Y$.

If any star leaves remain, call a star with a remaining leaf $A$ before assigning the labels. Give its next leaf label $Y+p+L$, consuming the gap $Y$. This label exceeds $L$, the old maximum. For each remaining leaf subtract its negative parent's label from the current gap to get its label. Every new label strictly exceeds the previous maximum and every new edge consumes the preceding gap. This proves the assertion with unrestricted star sizes. When $P=o$, either nontrivial star already supplies the earlier short-branch construction. [Anchor lemma](branches.md)
