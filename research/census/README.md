# Every tree through 26 vertices has consecutive integer edge sums

**Theorem.** Every tree on $2\le n\le26$ vertices admits a bijection $f$ onto $0,\ldots,n-1$ such that the $n-1$ ordinary sums $f(v)+f(w)$ on its edges are consecutive. Consequently every tree on at most 26 vertices is $k$-cordial for **every positive integer** $k$. Reduction of an integer interval modulo $k$ gives counts differing by at most one, even when some counts are zero. The one-vertex tree is immediate. Shifting the vertex labels by one and assigning the unused edge labels in reverse sum order gives the standard super edge-magic labeling. [Youssef, Theorem 4](https://ajc.maths.uq.edu.au/pdf/43/ajc_v43_p031.pdf)

An independent research project reports checking the super edge-magic property through order 23 and describes its result as awaiting expert review. The calculations here generate their own trees and witnesses. [Jared Vogler’s research report](https://www.jaredvogler.com/side-quests/agentic-solvers)

| Order | Trees checked | One centroid | Two centroids |
| ---: | ---: | ---: | ---: |
| 22 | 5,623,756 | 3,926,353 | 1,697,403 |
| 23 | 14,828,074 | 14,828,074 | 0 |
| 24 | 39,299,897 | 27,940,136 | 11,359,761 |
| 25 | 104,636,890 | 104,636,890 | 0 |
| 26 | 279,793,450 | 201,837,109 | 77,956,341 |

The full census covers 447,672,595 unrooted shapes of orders 2 through 26. The uncompressed witness streams occupy 14,950,989,300 bytes. [Counts at every order](counts.txt) · [SHA-256 manifest](streams.sha256)

## Construction and completeness

Root a tree at a centroid. Each child branch has at most half the total order. For a unique centroid all child branches have strictly less than half. Two centroids determine an unordered pair of rooted trees of the same size, joined at their roots. A rooted tree in turn is determined by the multiset of branches below its root. The generator encodes each tree with opening and closing bits in preorder, sorting child branches by order and then by encoding. It outputs one record per shape in this order, followed by the two-centroid cases ordered by the pair of halves.

If the least desired edge sum is $h$, then
$$
\sum_v (\deg(v)-1)f(v)=(n-1)(h-1).
$$
This follows by subtracting the sum of the vertex labels from the sum of the edge sums. Leaves have zero coefficient, so choosing internal labels determines the last internal label whenever its coefficient is nonzero. The solver then pairs unused leaf labels and unused edge sums with their available parents. A record consists of an eight-byte little-endian tree word followed by $n$ bytes of vertex labels in preorder. Exhaustiveness of the search strategy is unnecessary because every shape has a positive witness. [Generator](generate.cpp) · [Label search](interval.cpp)

The separate checker parses every word, checks the centroid and the ordering of all child branches, canonicalizes the half-pair, and requires strictly increasing unrooted keys. It verifies the vertex permutation and computes every endpoint sum from the parsed tree, requiring $n-1$ distinct sums spanning an interval of length $n-1$. For completeness it computes the number $R_n$ of rooted trees from the rooted-tree multiset product and obtains the number $U_n$ of unrooted trees by dissymmetry:
$$
R_1=1,\quad (n-1)R_n=\sum_{j=1}^{n-1}R_{n-j}\sum_{d\mid j} dR_d,\qquad
U_n=R_n-\frac{1}{2}\left(\sum_{j=1}^{n-1}R_jR_{n-j}-[2\mid n]R_{n/2}\right).
$$
Here the correction term is zero for odd $n$. Equivalently, vertex-rooted plus unoriented-edge-rooted trees minus oriented-edge-rooted trees count unrooted trees. For each underlying tree, its center (a vertex or an edge) supplies the unrooted term. Each other vertex specifies an oriented edge toward the center, and each other edge specifies its orientation away from the center. If the center is an edge, its two orientations come from its two endpoints. The correspondence commutes with isomorphisms. The verifier checks exactly $U_n$ records and then checks end of file. As negative controls at order seven, duplicating a vertex label and exchanging the first two records each caused the expected rejection. [Independent verifier](verify.cpp)

## An unbounded-order consequence

For $2\le k\le26$, every tree with at most $k$ nonleaf vertices is $k$-cordial, at any order. If its order exceeds $k$, its nonleaf vertices form a connected subtree. Retain all of them and enough leaves to obtain order $k$. The census gives a cordial labeling there. When the current order is a multiple of $k$, add one leaf to obtain the unique deficient edge weight. Starting from order $1\bmod k$, add up to $k-1$ further leaves with distinct labels avoiding the unique surplus and with distinct new weights. Hall’s prescribed-differences theorem gives exactly this extension for any list of parent labels. Iterating restores every original leaf. [Leaf extension proof](../counterexample-bound.md#removing-leaves)

In particular this holds whenever the matching number $\nu$ is at most $\lfloor(k+1)/2\rfloor$. To see that the nonleaf count is at most $2\nu-1$ for a tree of order at least two with $L$ leaves, root at a leaf and let every vertex with children keep exactly one outgoing edge. The resulting disjoint paths end at the $L-1$ other leaves and cover every vertex. A matching on these paths leaves at most $L-1$ vertices unmatched. Therefore $2\nu\ge n-L+1$.

## Reproduction

Run in Bash from the repository root with a C++17 compiler. The verifier interleaves shards in numerical order. Each record belongs to shard (zero-based record position modulo the shard count). Independent generators can run concurrently.

~~~bash
set -e
src="$PWD/research/census"
out=$(mktemp -d)
c++ -O3 -std=c++17 "$src/generate.cpp" "$src/interval.cpp" -o "$out/generate"
c++ -O3 -std=c++17 "$src/verify.cpp" -o "$out/verify"
cd "$out"
mkdir small
for n in {2..21}; do
    ./generate "$n" 0 1 "small/$n.bin"
    ./verify "$n" "small/$n.bin" >> counts.txt
done
for n in {22..26}; do
    mkdir "o$n"
    for i in {0..11}; do ./generate "$n" "$i" 12 "o$n/$i.bin"; done
    ./verify "$n" "o$n"/{0..11}.bin >> counts.txt
done
diff "$src/counts.txt" counts.txt
shasum -a 256 -c "$src/streams.sha256"
~~~
