# Matching transfers at twice an odd modulus

Let $m$ be odd and suppose every finite tree is $m$-cordial. This hypothesis holds for every odd $m\le21$. Write $n$ for the order of a tree and $\nu$ for its maximum matching size.

**Small orders.** Every tree with $n-\nu\le m$ is $2m$-cordial. Add a new leaf to each of the $n-2\nu$ unmatched vertices. Match each new leaf to its parent, obtaining a perfect matching on $2(n-\nu)$ vertices. Its quotient has order at most $m$, so an $m$-cordial labeling of the quotient has distinct vertex labels and distinct weights. The [matching lift](matching-expansion.md) gives distinct vertex labels and distinct weights on the completed tree modulo $2m$. Restrict to the original tree.

**One exposed vertex.** Every tree of order $2s+1$ with a matching of size $s$ is $2m$-cordial if any of the following holds:
$$
s<m,\qquad 2(s\bmod m)<m,\qquad s\equiv-1\pmod m.
$$
In particular at **22 labels** this covers all such trees of order at most 21, and all such trees of orders congruent to $1,3,5,7,9,11,21$ modulo 22.

The small-order assertion applies when $s<m$. For the second assertion we can expose a leaf. Starting at the exposed vertex, if it is internal, follow a nonmatching edge and then a matching edge to a new vertex. At each subsequent internal vertex there is another nonmatching edge to follow. All other vertices are matched, and acyclicity prevents repetition. Toggling the resulting alternating path moves the exposed vertex to its final leaf. The singleton is immediate.

Remove the exposed leaf, leaving a perfect-matching tree. Its $2m$-cordial labeling comes from the quotient theorem. If $r=s\bmod m>0$, the $2m$ vertex residues have $2m-2r$ minimum-frequency choices, and the edge residues have $2m-2r+1$. When $2r<m$, the two counts total more than $2m$. Thus some minimum vertex choice translates by the parent's label to a minimum weight. Assign it to the returning leaf. When $r=0$ the vertex counts are constant and one can fill the unique deficient weight.

Finally let $s\equiv-1\pmod m$. Add a leaf at the exposed vertex and match it to its parent. The quotient of this new perfect matching has order $s+1$ divisible by $m$. In its lift the vertex histogram is uniform. Odd weights correspond exactly to matching edges and are uniform, while the even weights contain the one deficiency. Deleting the added leaf and its odd edge reduces two full counts by one and preserves cordiality. This also explains why the argument needs to know which edge is deleted.

## Equal-sized pieces on a quotient of arbitrary order

**Theorem.** Take any $m$-cordial quotient tree $Q$ at odd $m$. Replace each vertex by a copy of a $t$-vertex tree $B$ with a bijective cordial labeling modulo $t$. Let $d$ be its omitted edge residue. For each edge of $Q$, join the corresponding pieces using any two vertices whose template labels sum to $d$ modulo $t$. The result is $tm$-cordial. Both the quotient order and the common factors of $t,m$ are unrestricted. In particular, at odd $t$ a single attachment vertex with label $d/2$ works for every join.

Choose representatives $R_a$ of the template digits modulo $tm$ such that $R_a+R_{d-a}=C$ for a single lift $C$ of $d$. For each two-element orbit take one lift freely and determine the other by subtraction. At a fixed digit solve $2j=(C-2a)/t\pmod m$ and use $a+tj$. The oddness of $m$ supplies the inverse. This is the same representative construction used for a [bijectively labeled quotient with a piece of arbitrary order](repeated-product.md).

In the piece at quotient label $x$ give digit $a$ the full label $R_a+tx$. In every vertex digit the high-coordinate counts copy the quotient vertex histogram up to translation. Each internal weight digit occurs on one template edge, and its copies have weights $R_a+R_b+2tx$. Doubling permutes $\mathbb Z_m$, so these high-coordinate counts are also a permuted quotient vertex histogram. The joining edges have weights $C+t(x+y)$ and reproduce the quotient edge counts in the remaining digit. The balanced histograms of consecutive sizes $|Q|$ and $|Q|-1$ together have range at most one.

Different tree shapes can be used at different quotient vertices if they have the same full representative set and the same set of internal offset sums modulo $tm$, with $t-1$ distinct digits. Require a common full offset sum for every join in the missing digit. The same row-by-row proof applies. Thus this includes mixtures with nonisomorphic pieces as well as the [perfect-matching and star lifts](matching-expansion.md).

**Even-modulus obstruction to this construction.** Suppose $m$ is even, the quotient has $m$ vertices, and the same bijective low-digit labeling occurs in every copy of a template of order $t\ge2$, with all joins in its missing digit. Even arbitrary high coordinates cannot give a bijective rainbow labeling of the assembled tree under these restrictions. In the $m$ copies of a single template edge, the high coordinates at each endpoint must permute $\mathbb Z_m$ by vertex injectivity. The high coordinates of the $m$ weights must permute it as well. But their sum is twice the sum of $\mathbb Z_m$ plus $m$ times the fixed carry, hence zero modulo $m$. The sum of a permutation is $m/2$ modulo $m$. This obstructs these fixed low digits only.

## Reproduction

The verifier enumerates rooted piece shapes up to order seven, constructs quotient trees at several order remainders, varies joining ports, and checks the final histograms directly, including unused residues. It checks 1,512 products of a single piece type and 160 products mixing nonisomorphic trees. The matching tests reconstruct 80 small-order restrictions, 5,124 single-leaf additions and 398 single-leaf deletions. [Independent checks](check_matching_transfers.py)

~~~sh
python3 -B -m research.check_matching_transfers
~~~
