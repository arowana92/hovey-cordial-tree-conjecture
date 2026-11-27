# A single integer labeling for every modulus from $n+h-1$ onward

**Theorem.** Let $T$ be a tree of order $n\ge3$ with $h$ nonleaf vertices. It has an injective integer labeling with pairwise distinct edge sums such that both the vertex labels and the edge sums fit in intervals of length at most $n+h-1$. Interval length counts integer positions, including both endpoints. Reducing this one labeling modulo **any** $k\ge n+h-1$ gives a $k$-cordial labeling. In particular, $k\ge n+2\nu-2$ suffices when the matching number is $\nu$. [Matching bound $h\le2\nu-1$](README.md#an-unbounded-order-consequence)

Żak introduced the harmonious order, the smallest usable modulus for an injective or surjective harmonious labeling. Montgomery, Pokrovskiy and Sudakov proved the asymptotic injective result for arbitrary finite abelian groups, for every fixed relative surplus and sufficiently large tree order. The construction here gives an explicit integer span for each individual tree and permits a prescribed core labeling. [Żak](https://doi.org/10.1016/j.disc.2009.05.010) · [Montgomery, Pokrovskiy and Sudakov, Theorem 1.5](https://doi.org/10.4171/JEMS/982)

## Placing the leaves

The nonleaves induce a tree. Number them $0,\ldots,h-1$ in breadth-first order with siblings consecutive. Along the sequence of edges leading to the next child, the child index increases strictly and the parent index never decreases. The core weights are therefore distinct integers in $[1,2h-3]$ for $h\ge2$. At $h=1$ the tree is a star and labeling its center zero and leaves $1,\ldots,n-1$ suffices.

Let $a$ be the number of core weights below $h-1$ and $b$ the number above $h-1$. Thus $a+b\le h-1$. Put a leaf below the core if its parent label is at least $a$, and above the core otherwise. Write $l,u$ for the two leaf counts.

* Below, start at label $-1$ and work downwards through the leaves in order of **nonincreasing** parent label. If the next candidate weight is already a core weight, skip that candidate label and continue downwards with the same parent. Candidate weights decrease strictly, including between leaves. They never exceed $h-2$. At most $a$ labels can be skipped.
* Above, start at label $h$ and work upwards in order of **nondecreasing** parent label. Candidate weights increase strictly and are at least $h$. At most $b$ labels can be skipped.

The two scans have disjoint weights and avoid the core weights. All vertex labels lie in $[-l-a,h+u+b-1]$, of length at most $n+h-1$. All lower weights are at least $-l-a+a=-l$. All upper weights are at most $h+u+b-1+a\le2h+u-2$. The old weights and the near ends of the two scans fit in the same interval $[-l,2h+u-2]$, also of length $n+h-1$. This proves the theorem. Orders one and two have direct labelings.

For example, a leaf-rich tree on 100 vertices with 12 nonleaves has one explicit integer labeling that works at every modulus from 111 upward, regardless of the arrangement and degrees of those 12 vertices. For a tree concentrated on a particular path, the separate path bound can give a smaller cutoff. [Path bound](level-hosts.md)

## Prescribed integer labels, edge weights and offsets

More generally, keep any distinct core labels with minimum zero and any set $W$ of distinct old integer edge weights, including weights with prescribed offsets. For each new leaf give its effective shift, the parent's label plus the leaf-edge offset. Let $P,Q$ be the smallest and largest shifts. Choose
$$
H=\max(1+\max f_{\rm core},Q-P).
$$
Lower candidates start at $-1$ and upper ones at $H$, so their weight ranges are separated by $Q-1<H+P$. Define
$$
a=|\{w\in W:w<Q\}|,\qquad b=|\{w\in W:w\ge H+P\}|,\qquad
A=\min(W\cup\{H+P\}),\qquad B=\max(W\cup\{Q-1\}),
$$
and put $D=\max(a+b,B-A+1-H)$. With $r$ leaves, **$H+r+D$ positions suffice for each of the two intervals**.

Use the threshold $A+a$ in place of $a$ for deciding which shifts go below. The same monotonicity charges at most $a,b$ skips on the two sides. All labels lie between $-l-a$ and $H+u+b-1$. For the weights, the threshold puts the lower scan at or above $A-l$, and the upper scan strictly below $A+H+u+D$. The near end of the lower scan is at most $Q-1\le B<A+H+D$ and the near end of the upper scan is at least $H+P\ge A$. The whole core lies between $A$ and $B$ in its edge weights. The resulting weight interval has the asserted length. The ordinary construction above is available with any bijective core numbering that makes its ordinary sums distinct.

## Verification

Lean proves existence of the monotone scan with an output for every requested shift, strict increase in both coordinates of interest, exclusion of every old weight and the bound of one skipped position per forbidden entry. Reflecting both labels and shifts gives the decreasing scan. Lean also checks the common weight window for the two scans and the core. The breadth-first core construction and its reduction to this lemma are given above. [Lean proof](LeafIntervals.lean) · [Integer constructor](leaf_intervals.py)

A separate checker recomputed the actual original edge sums for all 7,813 rooted trees of orders one through twelve, 108 relabeled trees with growing leaf populations, and 2,250 independently offset cases with prescribed core weights. It checked both integer spans and injectivity in each of five moduli beginning at the stated bound. [Checker](check_leaf_intervals.py)

~~~sh
lean research/census/LeafIntervals.lean
python3 -B -m research.census.check_leaf_intervals
~~~
