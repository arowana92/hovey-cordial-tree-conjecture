# A common parent color and a singleton on a divisible core

**Theorem.** Let $k\ge2$, and fix a $k$-cordial coloring of a tree of order divisible by $k$. Write $D$ for its unique deficient edge weight. Attach a rooted forest of $1\le t\le k-1$ vertices, including at least one singleton component. All component roots have neighbors of a common old color $b$. Pad the forest to $k-1$ vertices with singleton components, then adjoin a temporary root adjacent to every component root. Suppose this $k$-vertex tree has a bijective labeling with distinct edge sums. The given core labeling extends if $D=2b$ or $D-2b\ne -(D-2b)$ in $\mathbb Z_k$.

In particular, at every odd modulus for which all $k$-vertex trees have bijective rainbow labelings, **every** such attachment extends. This includes every odd modulus from 3 through 27 by the integer labeling census. In a least ordinary counterexample at any such modulus, a vertex with a union of branches of size $s$ including a singleton therefore excludes order $s\bmod k$ for $1\le s<k$. Removing the union would leave a connected smaller core of divisible order. [Integer labeling census](../census/README.md)

**Proof.** Designate one original singleton. Write $r$ for the temporary root's label in the bijection $f$. For either sign $u\in\{1,-1\}$ use $u(f-r)+b$ on the augmented tree. The temporary root then has color $b$. Substitution of the actual old parents preserves every entering weight. The $k-1$ free labels are distinct and avoid $b$, and the $k-1$ weights are distinct. In coordinates centered at $2b$, the two signs give weight sets $W$ and $-W$, where $W$ omits just one residue.

If $D-2b\ne -(D-2b)$, at least one of these weight sets contains $D-2b$. Choose that sign. If the edge of weight $D$ belongs to a padded singleton, exchange the labels of that singleton and the designated original singleton. Their entering weights are exchanged because their parents have the same color. Remove the padding. The $t$ retained vertex labels are distinct, and the $t$ retained weights are distinct and include $D$. Starting with uniform vertex counts and one edge deficiency gives the required balance in both histograms.

If $D=2b$, give the designated singleton label $b$ first. Its edge fills $D$ and its label becomes the sole surplus. Use either affine labeling on the rest of the original forest. Its vertex labels are distinct and avoid $b$, and its new edge weights are distinct. At an odd modulus every nonzero residue differs from its negative, proving the assertion.

The [checker](check_divisible_singleton.py) constructs augmented caterpillars with integer interval labelings, removes the padding, substitutes actual core vertices, and recounts both histograms. At odd moduli through 35 it verified 22,012 joins, including 900 with $D=2b$ and 8,435 requiring the transfer of the deficient weight from a padded leaf. The proof applies to every eligible augmented tree.

~~~sh
python3 -B -m research.rainbow.check_divisible_singleton
~~~
