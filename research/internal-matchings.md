# Matching sizes that guarantee cordiality with arbitrary leaf populations

**Theorem.** Let $T$ be a tree on at least three vertices, let $I$ be the tree induced by its $c$ nonleaf vertices, and let $\nu$ denote maximum matching size. Form the integer interval
$$
J(T)=[c-\nu(I),\,\nu(T)].
$$
If $J(T)$ contains a number congruent to **0 or 12 modulo 13**, then $T$ is 26-cordial. In particular, every 26-label counterexample would have $\nu(T)\bmod13\in\{1,\ldots,11\}$ and $\nu(T)+\nu(I)-c\le10$. These restrictions allow arbitrarily many vertices to be uncovered in a maximum matching.

At $k=2m$ for every odd $m\le25$, the same criterion using a multiple of $m$ in $J(T)$ suffices. For example it applies at 30, 34, 38, 42, 46 and 50 labels with no restriction on tree order. Trees on at most two vertices have immediate cordial labelings.

## Matchings covering the nonleaves

The interval $J(T)$ is exactly the set of possible sizes of matchings that cover every nonleaf. There is a maximum matching with this property. From an exposed internal vertex, alternate nonmatching and matching edges until reaching a leaf at even distance, then exchange the edges of the path. Maximal size excludes an augmenting path and acyclicity prevents revisits. The exchange moves the exposure to a leaf. [Detailed exchange proof](near-matching.md#completing-and-lifting-a-maximum-matching)

Restrict such a matching to $I$, obtaining an internal matching $N$. Every internal vertex without an original leaf neighbor must be covered by $N$. Conversely, any internal matching covering those required vertices extends by matching every remaining internal vertex to one adjacent leaf. Distinct internal vertices use distinct leaves. The resulting matching has size $c-|N|$, since every edge in a tree on at least three vertices has an internal endpoint.

Augment $N$ within $I$ until it reaches size $\nu(I)$. Each exchange preserves the coverage of every previously covered internal vertex, and hence of the required ones. Reattaching leaves after each exchange realizes every size from $\nu(T)$ down to $c-\nu(I)$. The formula $c-|N|$ also proves the lower bound.

## Choosing a divisible seed

Fix a matching of size $j\in J(T)$ that covers all internal vertices. Every unmatched vertex is an original leaf. If $m\mid j$, delete all of these leaves. The remaining connected tree has $2j$ vertices, order divisible by $2m$, and a perfect matching. It is $2m$-cordial by the [odd-modulus matching lift](matching-expansion.md) and the all-tree results at the odd base moduli through 25.

At $m=13$, if $j\equiv12\pmod{13}$ and at least two leaves are uncovered, retain two of them. Now the seed has $2j+2$ vertices, again divisible by 26, and the retained matching covers all but two. The [two-exposure theorem](census/two-exposures.md) supplies its labeling. If fewer than two leaves were uncovered, that theorem already applies to $T$ itself.

Return the omitted leaves in batches of at most $k$, completing each full batch before the final partial batch. On a divisible core choose the first leaf label to fill the unique deficient edge weight. This leaves one surplus vertex residue and uniform edge counts. The [prescribed-parent leaf lemma](counterexample-bound.md#removing-leaves) labels the remaining at most $k-1$ leaves distinctly, avoiding that surplus and giving distinct new weights. A full batch leaves divisible order again. Thus any number of independently situated original leaves can be returned.

The two admissible residues at 26 leave at most eleven consecutive excluded integers. This proves the stated width restriction.

## Adding leaves everywhere on an arbitrary core

Take any tree $H$ of order $c\ge2$ and attach at least one new leaf to every vertex, with the counts allowed to vary independently. The internal tree is exactly $H$ and the maximum matching size of the result is $c$, since each original vertex can match to its own leaf. Therefore the interval is $[c-\nu(H),c]$.

In particular, **if $H$ contains a matching of size 11, every such tree is 26-cordial**, whatever the leaf counts. At the other stated twice-odd moduli a matching of size $m-1$ on $H$ suffices. The interval test can work with a smaller matching when its endpoint residues permit it.

The [independent checker](check_internal_matchings.py) compares the interval with explicit enumeration of all possible matching sizes on 3,045 rooted trees. It checks the formula for 664 cores with independent positive leaf populations. It also attaches leaves in 798 whole-tree tests across the seven moduli, verifying both histograms after every added leaf.

~~~sh
python3 -B -m research.check_internal_matchings
~~~
