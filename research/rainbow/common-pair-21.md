# A second attachment of two vertices at 27 labels

**Theorem (computer-assisted).** Fix any 27-cordial labeling of a core of order one modulo 27. Add a rooted forest of at most 21 vertices whose parents in the core all have color $a$. At an independently prescribed color $b$, also attach either a path on two new vertices by one end or two new leaves. The two leaves may have different old parents of color $b$. One extension works on every parent-first prefix.

**Consequence.** In a smallest counterexample of order $27m+24$, no union of branches at any single vertex can have order 21 or 22. In particular, no edge side can have any of the orders **21 through 27**.

For order 21, remove the union and root the retained tree at its joint. This rooted tree has at least three vertices. Choose a deepest vertex with children. If it has two or more children, remove two of its leaf children. If it has one child, remove that vertex and its child. In the latter case the vertex has a parent since the retained tree has at least three vertices. Either deletion preserves the joint and gives a connected core of order one modulo 27. Label the smaller core and apply the theorem. The [independent-leaf result](common-leaf-22.md) treats 22 and 23. Orders 24 through 27 follow from the [affine and divisible joins](../prime/four-deficits.md).

## What a witness certifies

Translate the old surplus residue to zero. The old edge frequencies are equal. Add a temporary root to the main forest with 21 free vertices, joining it to each component root. A witness row labels the resulting 22-vertex tree injectively with distinct edge weights modulo 27. Mark its temporary root, with label $r$. Write $V$ and $E$ for the unused vertex labels and edge weights.

Choose $z$ in $V\cup\{r\}$ and a unit $u$. Transform the augmented labels by $t\mapsto u(t-z)$ and substitute the old color $a=u(r-z)$ for the temporary root. The 21 retained labels are distinct and avoid zero. Their edges, including the edges to the old parents, have distinct weights. The unused weights are $u(E-2z)$.

Choose two distinct values $x,y$ in $(V\cup\{r\})\setminus\{z\}$. Use labels $u(x-z)$ and $u(y-z)$ on the extra vertices. Put $c=u^{-1}b+z$ modulo 27.

* For two leaves, require $x+c,y+c\in E$. These weights are different since $x\ne y$.
* For a path with $x$ at its entering end, require $x+c,x+y\in E$ and $x+c\ne x+y$. Also try the reverse orientation.

These conditions preserve distinct edge weights after the transformation. Each parent-first prefix inherits distinct new weights and distinct nonzero new labels. Padding a smaller main forest to 21 vertices and restricting the result gives the same conclusion at all smaller orders. The empty main forest can be padded with a separate component. The extension also lifts to any multiple of 27 on a core of order one modulo the larger modulus. Normalize its surplus first, reduce the two prescribed colors modulo 27, then use any lifts of the free labels. Distinctness and avoidance of the normalized surplus follow by reduction modulo 27.

## Exhaustion and reproduction

The [generator](common_site_generate.cpp) covers the 53 simultaneous unit orbits of $(a,b)$ separately for each shape of the extra attachment and each marked vertex. At even order the [ranker](marked_tree_ranks.hpp) enumerates trees with a unique centroid by multisets of strictly smaller branches. For two centroids it enumerates unordered pairs of rooted half-trees. The [verifier](common_site_verify.cpp) checks the parenthesis word, the child order, the centroid conditions and the expected rank. It checks every label and edge weight directly. It then works in transformed coordinates, fixing $a$ in $\{0,1,3,9\}$, applying all units, and testing all 27 values of $b$ for each attachment. Scaling covers all literal color pairs. Rooted-tree multisets and dissymmetry give an independent count of the unrooted shapes.

The [192-shard manifest](common-pair-21.sha256) covers **5,623,756** unrooted 22-vertex trees, **135,481,675** witness rows and **180,387,597,456** literal choices of marked vertex, two colors and attachment shape. Independently forgetting the root and minimizing the rooted encoding over every possible root found exactly 2, 6, 23, 106, 551 and 3,159 distinct shapes at orders 4, 6, 8, 10, 12 and 14.

The [whole-tree replay](check_common_site.py) fits each attachment to a cordial path of order 28, builds every edge by its actual endpoints and recounts both frequency lists. At four sampled main trees it checked **128,304** trees on 51 vertices, including both shapes, every marked vertex and all 729 color pairs. A separate replay of the final rank, a tree with two centroids, gave 32,076 further whole trees. The native checker rejected a duplicate label, a missing witness family and a truncated stream.

~~~bash
set -euo pipefail
out=$(mktemp -d)
r=research/rainbow
c++ -O3 -std=c++17 "$r/common_site_generate.cpp" -o "$out/generate"
c++ -O3 -std=c++17 "$r/common_site_verify.cpp" -o "$out/verify"
python3 -B -m research.rainbow.check_common_site 22 --pair --manifest "$r/common-pair-21.sha256"
python3 -B -m research.rainbow.check_common_site 22 --pair --run "$out/shards" --generator "$out/generate" --verifier "$out/verify" --shards 192 --workers 2
cmp "$out/shards/manifest.txt" "$r/common-pair-21.sha256"
"$out/generate" 22 0 1024 --pair > "$out/sample"
python3 -B -m research.rainbow.check_common_site 22 --pair --replay "$out/sample"
~~~
