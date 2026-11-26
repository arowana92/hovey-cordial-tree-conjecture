# Neutral collections of pendant stars at any prescribed label

Let $B_d$ be a rooted vertex with $d\ge1$ leaf children. Attach copies of $B_d$ to a vertex labeled $p$ by an edge from $p$ to each new root. For every $d$, **$4d$ copies admit a labeling in which their new vertex labels and their new edge weights are the same set**. The label $p$ is prescribed and can have any additive order in $\mathbb Z_k$. If $N$ counts all new vertices and the number of forbidden residues, $k>20(N+10)$ suffices. Every new label and every new weight avoids the forbidden set. Different groups, arities and attachment sites can be treated successively at the same linear bound with $N$ counting all of them.

A single leaf at a nonzero prescribed $p$ cannot have this property. A leaf below a newly attached root supplies a second endpoint sum that can compensate for the shift by $p$. The construction uses all actual sums, including the edges from $p$.

### Parent of order greater than two

Use $d$ pairs of progressions of two root labels each. At the first pair choose a parameter $A$ and use progressions starting at $A$ and $-A-3p$. At each later pair choose a new $T$ and start at $T$ and $-T-p$. In each progression starting at $x$ the two roots are $x,x+p$. Their incoming weights are $x+p,x+2p$. This leaves an excess at the head $x+2p$ and a deficit at the tail $x$.

The four first roots are $A,A+p,-A-3p,-A-2p$. For every positive progression (first start in a pair), assign a child labeled $x+2p$ at $A$ and a child labeled $x+2p+A$ at $-A-2p$. Their weights are $x+2p+A$ and $x$. For every negative progression use the parents $-A-3p,A+p$ instead. The two successive jumps again sum to $-2p$. In both cases, combining these children with the two roots closes the deficit. Each of the four first roots receives exactly $d$ children. The children used for a progression need not be attached to its own roots.

In each later pair the four roots $T,T+p,-T-p,-T$ form two opposite pairs. For each opposite pair $z,-z$ assign one child $b$ below $z$ and a child $b+z$ below $-z$. Their two weights exchange their labels. Repeat with fresh parameters until each such root also has $d$ children.

At the first step the eight labels to keep distinct are
$$
 A,\ A+p,\ A+2p,\quad -A-3p,\ -A-2p,\ -A-p,\quad 2A+2p,\ -2A-4p.
$$
Equal slopes have different offsets since $p,2p\ne0$. Exclude $A\in\{0,-p,-2p,-3p\}$. At each later step the corresponding triples are $T,T+p,T+2p$ and $-T-p,-T,-T+p$, and the two middle child labels are $T+2p+A,-T-2p-A$. The four exclusions on $A$ make each repeated-slope list distinct. Exclude zero from the occupied positions so every opposite root pair can use the two-child exchange.

### Parent of order at most two

Use $d$ groups of four roots. If $p=0$, take $A,2A,-A,-2A$ in a group. If $p\ne0$ and $2p=0$, take $A,A+p,-A,-A+p$. The root weights permute the roots in either case. The last two roots are the negatives of the first two. The same two-child exchange gives all $d$ children at each root.

### Simultaneous avoidance and a tree consequence

At each parameter step there are at most eight affine forms. Their slopes are nonzero integers of magnitude at most two. Avoiding $m$ occupied residues, including zero, excludes at most $16m$ choices. An unequal-slope pair excludes at most four choices, since a congruence with nonzero coefficient $j$ has at most $|j|$ solutions modulo $k$. Equal-slope comparisons already hold. Even allowing the four extra exclusions, fewer than $16(N+1)+4\binom82+5$ values are forbidden. This is less than $20(N+10)$. The argument works over composite moduli and its constant is independent of $d$.

For example take a rooted core with every nonroot degree at most $\Delta$. At any of its vertices attach arbitrarily many copies of any $B_d$ with $1\le d\le D$, independently across sites and arities. Write $h$ for the resulting order. For fixed $\Delta,D$ and every $k>C_{\Delta,D}(h+1)$ the enlarged tree has distinct labels with its specified root at zero, and edge sums equal to the vertex labels with one omission. It therefore stays $k$-cordial after adjoining **any number of additional direct leaves at that root**. To see this, retain fewer than $4d$ added copies per site and arity, setting aside whole groups of $4d$. The retained nonroot degrees are bounded by $\max(D+1,\Delta+\sum_{d=1}^D(4d-1))$. Apply the earlier linear cutoff to the retained tree, then restore all groups using the theorem above, avoiding the occupied vertex labels. Each restoration preserves the omitted label. [Linear cutoff](linear-hub-batches.md) · [Periodic leaf extension](README.md#uniform-witnesses-for-large-moduli)

### Reproduction

Lean verifies the two multiset identities over the integers, which descend modulo $k$. The independent checker exercises every parent residue at six moduli, then recounts both histograms of larger whole trees with multiple sites and a surplus of leaves. [Lean proof](NeutralStars.lean)

~~~sh
python3 -B -m research.hub.check_neutral_star_blocks
lean research/hub/NeutralStars.lean
~~~
