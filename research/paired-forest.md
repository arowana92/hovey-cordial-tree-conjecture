# Adding a perfectly matched forest at arbitrary sites

**Theorem.** Fix a cordial labeling of a tree of order divisible by $2m$, where $m\in\{3,5,7,11,13\}$. Attach any forest having a perfect matching, joining each component by one edge to any chosen old vertex. The labeling extends, preserving every old vertex label. The sizes, number of components and attachment sites are unrestricted. Each edge outside the forest matching may carry its own additive offset, including edges in the old tree when its labeling is cordial with those offsets.

At **26 labels**, every tree containing a connected subtree of positive even order at most 26 whose deletion leaves a perfect matching is consequently cordial. For a tree of order below 26 this already follows from the integer census. Otherwise adjoin entire matching pairs to that subtree in parent-before-child order until it has exactly 26 vertices. The [order-26 base](census/README.md) labels this seed, and the theorem restores the entire remaining forest. The same argument applies at the other listed moduli using their order-$2m$ bases.

For example, let a matching leave exactly two vertices exposed. Take their connecting path and include the partner of every matched vertex on that path. If it meets $h$ distinct matched pairs, this connected subtree has exactly $2+2h$ vertices and the remainder is perfectly matched. Thus **any such matching with $h\le12$ proves 26-cordiality**, regardless of the rest of the tree. In particular the exposed vertices may have distance up to 13 with no further hypothesis. In a 26-label counterexample with matching deficiency two, the path between the two exposures must meet at least 13 pairs in *every* maximum matching. The [previous deficiency bound](near-matching.md) also requires its order to be divisible by 26.

## Filling the old deficit one batch at a time

Use coordinates consisting of the residue modulo $m$ and the parity. Since $m$ is odd, this specifies a unique residue modulo $2m$. Contract the matched pairs and order them with every parent preceding its children, including across the edges to the old tree. Process at most $m$ pairs at a time, taking $m$ in every nonfinal batch. If the old order is divisible by $2m$, all old vertex counts are uniform and the edge counts have just one deficient weight $D$.

Give the two endpoints of each new pair the same low residue $x$ and opposite parities. For the first pair, assign its entering endpoint the precise label needed to make its joining edge weigh $D$. This fixes its low residue $x_0$ and its orientation. For the remaining $t-1$ pairs in the batch, use distinct low residues different from $x_0$ and require their $t-1$ entering edges to have distinct low weights. The outside low labels and edge offsets are arbitrary. This is the [order-$m$ offset theorem](biased/README.md#reduction-to-one-order): normalize $x_0$ to zero, fold all already labeled parents into one dummy vertex of label zero, and absorb their labels into its joining offsets. Pad to order $m$, apply the bijective rainbow theorem and restrict. A parent in the first pair is already labeled at this point.

Orient these remaining pairs as they arrive so that each entering edge has even weight after including its offset. Its parent's parity is already known. The $t$ matching edges have odd weights with distinct low residues $2x$, and the $t-1$ entering edges after the first give distinct even weights. The first entering edge has filled the old deficit. All other edge increments are on distinct residues, and all $2t$ free vertex labels are distinct. When $t=m$ every vertex residue has increased once, and the unique new edge deficit is the even residue missed by the $m-1$ later entering edges. This proves both the partial and repeated full batches.

## Replacing an edge by a chain of pairs

There is a complementary construction at **every** modulus $2m$ with $m$ odd. Replace an edge by a chain of $jm$ pairs. At each pair choose where the incoming and outgoing edges meet it. When the two sites differ, the endpoint-to-endpoint path traverses the matching edge. If the number of traversed pairs is even, the operation preserves both old endpoint labels and adds exactly $j$ copies of each vertex residue and each edge residue, after the removed edge is subtracted. This holds for every old labeling and every choice of its two endpoint labels.

Let the left endpoint have low residue $a$. In order along the chain use $a+1,\ldots,a+jm$ modulo $m$ for the pair lows, with opposite parities within each pair. Orient the incoming endpoint to match the preceding outgoing parity, starting from the old left endpoint. The matching weights cover each odd residue $j$ times. The entering edges all have even parity and their lows $2a+2i-1$ for $1\le i\le jm$ cover every low residue $j$ times. At the final outgoing site the low residue is again $a$. Each traversed pair changed the running parity once, so the full outgoing label equals the old left label. The last edge exactly reproduces the removed weight. If all pairs are traversed and $j$ is odd, a uniform replacement really is impossible: this is the [even-modulus path sum obstruction](counterexample-bound.md#shortening-paths).

## Verification

The [constructor](paired_forest.py) outputs the actual two endpoint labels per pair. The [independent checker](check_paired_forest.py) rebuilds every original and added edge, varies both ports and offsets on all entering edges, and counts all residue bins. It verified 1,170 complete trees with one to three batches, covering both parities of the old deficit. Another 3,548 replacements checked the exact increments after subtracting the original edge.

~~~sh
python3 -B -m research.check_paired_forest
~~~
