# A quadratic bound for every counterexample

**Theorem.** For $k\ge2$, every tree of order $n\ge(2^{34}+4)k^2$ is $k$-cordial. This bounds the order of **every** possible counterexample, assuming nothing about smaller trees. The constants below allow substantial slack.

Let $M$ be the largest number of leaf neighbors at one vertex $u$, and $h=n-M$. We will prove $k$-cordiality whenever $h\ge2^{34}k^2$. If $h$ is smaller under the displayed order hypothesis, then $M\ge4k^2$, and the [high-degree theorem](high-degree.md) applies. The argument for large $h$ strengthens the [first large-order bound](README.md) in two ways. The relabelings can be distributed over translated types of sites. Their supply can be arranged deterministically while keeping the initial prefix discrepancies small.

## Distributing the corrections

Write $\tau$ for cyclic translation by one on histogram vectors. Take $r$ disjoint groups of sites with no edge between any two sites, including across groups. A group with base label $j$ has degree-$d$ sites of type A with all neighbors labeled $j$, and type B with one neighbor labeled $j+1$ and $d-1$ labeled $j$, with $d\in\{1,2\}$ fixed. In each type in each group suppose every initial vertex label is available at least 32 times. Different groups may use the same base.

Let $a,b$ be the required vertex and edge histogram changes. They have coordinate sum zero, all prefixes have absolute sum at most $P$, and their moments obey $s(b-da)=0$ modulo $k$. **If $r\ge P$ and $r\ge1$, these changes can be realized.**

For any zero-mass integer vector $f$ let $F_i$ be its prefixes, putting $F_{-1}=0$. Split $f$ into $r$ zero-mass vectors by assigning to part $\ell=0,\ldots,r-1$ the differences of the prefixes $\lfloor(F_i+\ell)/r\rfloor$. These prefixes sum to $F_i$. On every cyclic interval the contribution of one part differs from $1/r$ of the original interval sum by less than one. This also holds for a wrapped interval by zero total mass.

Apply the split to $a$. If group $\ell$ of base $j_\ell$ used its part $a^\ell$ entirely at type A, the remaining edge change would be
$$
z=b-d\sum_\ell\tau^{j_\ell}a^\ell .
$$
Its moment vanishes since translating a zero-mass vector preserves its moment. Every prefix of $z$ has absolute sum at most $P+d(2P+r)\le5P+2r$. The [integer correction formula](README.md#correcting-two-histograms-by-local-changes) gives a zero-mass vector $H$ with $(\tau-I)H=z$ and $\|H\|_\infty\le2(5P+2r)\le14r$.

Split $H$ by the same rule. In group $\ell$ put $v^\ell=\tau^{-j_\ell}H^\ell$ at type B and $a^\ell-v^\ell$ at type A. The vertex changes sum to $a$. The extra edge change relative to using A alone is $\sum_\ell\tau^{j_\ell}(\tau-I)v^\ell=z$. Each entry of $v^\ell$ has magnitude at most 15, and each entry of $a^\ell$ has magnitude at most $2P/r+1\le3$. Thus the 32 available sites per bin suffice by moving labels from negative to positive entries.

## Controlling all prefixes

For $m$ independent uniform residues, the expected maximum absolute discrepancy over all prefixes from $0$ through $j$ is at most $4\sqrt m$. Here is a short proof. Replace the expected count by that of an independent copy, using convexity of the maximum absolute value to bound the original expectation from above. Independently swap each paired observation or keep it, with equal probabilities. The triangle inequality now bounds the result by twice the expected maximum of signed prefix counts of a single sample with independent fair signs. Sorting the observations makes the signed counts a subset of the partial sums of $m$ fair signs. The chance that the maximum absolute partial sum reaches $t$ is at most $m/t^2$: after the first crossing, the remaining increments are independent and centered, so the conditional expected final square is at least $t^2$. The final square has mean $m$. Integrating $\min(1,m/t^2)$ gives $2\sqrt m$ and proves the estimate.

At one parent residue, a list of $F$ leaves can be given counts $\lfloor(i+1)F/k\rfloor-\lfloor iF/k\rfloor$ at label $i$. On every cyclic interval their counts differ from the uniform benchmark by less than one, including after shifting to edge weights. We use this observation even for very large leaf sets.

## Many leaves away from the largest parent

Write $L'=L-M$, where $L$ counts all leaves. Suppose $L'\ge h/32$. Pair the two heaviest leaf parents first, placing weights $M,w_2$ together. In each bipartition class separately, sort the remaining parents by decreasing weight and pair consecutive entries, discarding an unpaired last entry. For a pair retain equal numbers of matched leaves at both ends, namely the smaller multiplicity. Write $F$ for the sum of the retained multiplicities counting just one side of each pair. Within a sorted list the sum of even-position entries is at least half the total excluding the first entry. Thus
$$
F\ge \max\big(w_2,\ w_2+(L'-3w_2)/2\big)\ge L'/3 .
$$
Only the first pair can be adjacent in the tree.

Assign the parents of each oriented pair labels $X,X+1$ using an independent uniform base $X$ per pair. Unpaired nonleaves get independent uniform labels. In each base $j$ the two sides of its matched pairs both have $F_j$ leaves. Give each side low-discrepancy counts by the preceding list rule, pooled across parents of that base. Do the same separately on the unmatched leaves grouped by their actual parent residue. The at most $3k$ lists give at most $3k$ prefix error in either histogram. For each base we can form $\lfloor F_j/(32k)\rfloor$ groups with 32 sites in every bin of each type. All sites are leaves. Thus
$$
r\ge F/(32k)-k\ge h/(3072k)-k.
$$

There are at most $h$ nonleaves. Their vertex indicators partition into two lists of independent uniform observations, by taking at most one vertex from each variable in each list. For the edges between nonleaves, identify each parent pair, keeping track of the additive offset on every incidence. There is at most one loop. The loop-free multigraph on these variables is a union of three forests. Indeed a set of $m$ variables contains at most $2m$ original vertices and spans at most $2m-1$ edges by acyclicity of the original tree. Repeatedly remove a vertex of degree at most three, counting parallel edges. Put its remaining edges into different ones of three classes. A cycle in a class, including a parallel pair, would have an earliest removed vertex with two edges in that class. For each forest, sums of its endpoint variables are mutually independent and uniform by propagation from its roots. Fixed incidence offsets preserve this. A loop can contribute at most one to the prefix error. Applying the prefix estimate to the two vertex lists and three edge lists gives some realization with both full discrepancies at most $20\sqrt h+3k+1$.

## Few leaves away from the largest parent

Suppose $L'<h/32$. Remove the $M$ leaves at $u$ to get a tree $R$ on $h$ vertices with at most $l=L'+1$ leaves. As in the [degree-two run count](README.md#finding-enough-local-changes), excluding $u$ gives at least $h-2l-1$ usable degree-two vertices in at most $2l+1$ runs. Divide each run into disjoint blocks of five consecutive vertices, discarding its remainder. There are at least $(h-10l-5)/5\ge h/10$ blocks under the hypothesis on $h$.

Use batches of $2k^2$ blocks, leaving surplus blocks alone. In the middle three positions of a batch put each triple $(j,x,j)$ and $(j,x,j+1)$ once for every $j,x\in\mathbb Z_k$. The two end positions of each block are unassigned buffers. In a complete batch, the planted vertices have exactly uniform counts: each position in each triple family runs equally over all residues. The same holds for the two planted internal edges by summing $x+j$ or $x+j+1$. For each base $j$ we can take one group of 32 sites of every label in both types per 32 batches. Centers are nonadjacent. Hence $r\ge h/(640k)-k$.

Pin $u$ at zero and give the $M$ removed leaves low-discrepancy counts. Give the remaining unpinned and unplanted vertices independent uniform labels. Edges from planted triples to the rest have different free buffer vertices, so their weights are independent uniform observations. Edges with both endpoints outside the planted triples form a forest in $R$ and also have independent uniform weights, with at most one pinned root. The free vertex labels give a third independent list. The prefix estimate gives a labeling with both full discrepancies at most $12\sqrt h+2$. Every center has degree two and two degree-two neighbors. Changing one original leaf therefore leaves the supplies intact.

## Finishing the proof

In the leaf case choose balanced targets with the required moment. In the degree-two case use balanced targets and change one leaf to achieve the required moment, as in the [target lemma](README.md#choosing-the-balanced-targets). In both cases the changes have prefix bound $P=20\sqrt h+4k+3$. Since $\sqrt h\ge2^{17}k$, we have $h/(3072k)-k\ge P$. The distributed corrections apply, proving the theorem.

The checker tests the split on cyclic intervals, executes both reservoir constructions and verifies the vertex and edge histograms on the original trees. [Executable construction](../large_order_quadratic.py)

~~~sh
python3 -B -m research.large_order_quadratic
~~~
