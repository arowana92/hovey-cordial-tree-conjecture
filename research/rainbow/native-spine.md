# A certificate for every finite tree at eighteen and nineteen labels

**Theorem.** Every finite tree is 18-cordial and 19-cordial. The [ordered-cut theorem](ordered-cut.md) reduces the claim at all orders to two finite hypotheses. The witness stream verifies both, using the sharp condition on actual runs of boundary colors. For every required colored forest the verifier checks a bijection to the nonzero residues and computes all parent-edge sums, including the prescribed boundary edges.

| Modulus | Rooted base trees | Eligible forests | Base-only shapes | Witness rows | Eligible boundary colorings before unit symmetry |
|---:|---:|---:|---:|---:|---:|
| 18 | 1,721,159 | 1,587,279 | 133,880 | 239,253,064 | 1,276,116,192 |
| 19 | 4,688,676 | 4,479,243 | 209,433 | 266,718,296 | 4,721,012,403 |

## One representation for the two hypotheses

Removing the root from a rooted tree of order $k$ gives a forest of order $k-1$. When every external parent label is zero, a rainbow labeling of that forest is precisely a bijective rainbow labeling of the tree with its root labeled zero. We check the all-zero row on **every** forest, including those above the terminal limit. For an eligible forest this same row also handles its all-zero boundary coloring.

The [generator](spine_generate.cpp) recursively lists multisets of rooted children. It enumerates potential color changes at the size gaps and discards assignments incompatible with the sharp run condition or equivalent to a lexicographically smaller assignment under multiplication by a unit. It obtains witnesses using the [native search](search.cpp).

The [verifier](spine_verify.cpp) parses balanced parentheses and verifies that components and siblings are sorted by size and then code. These comparisons make the representation unique by induction on size. It rejects repeated forest codes across all shards. Independently, the product $\prod_{j\ge1}(1-x^j)^{-R_j}$ counts multisets of rooted trees, where $R_j$ is the number of rooted trees of order $j$. Its coefficient at $x^{s-1}$ is $R_s$. The verifier computes the coefficients by multiset binomial counts. Consequently the final number of distinct valid forests proves complete shape coverage.

For each size profile the verifier enumerates boundary patterns, counts actual color runs on the components, tests the separation inequalities and partitions the valid patterns into unit orbits. The rows for each eligible shape must hit every orbit exactly once. On every row the verifier checks residue ranges, injectivity with zero forbidden, and weight distinctness from the original endpoint labels. The all-zero row must occur even at ineligible shapes.

## Reproduction

From the repository root, use a C++17 compiler. The script below writes the complete witness stream in 24 shards and checks it. Run independent generator shards concurrently if desired. The files need about 4.5 GiB at 18 and 5.3 GiB at 19. Set the shell variable to either modulus. Shard numbers refer to the zero-based index of the shape modulo 24. [SHA-256 hashes at 18](spine18.sha256) · [Hashes at 19](spine19.sha256)

~~~sh
set -e
src="$PWD/research/rainbow"
out=$(mktemp -d)
c++ -O3 -std=c++17 "$src/spine_generate.cpp" "$src/search.cpp" -o "$out/generate"
c++ -O3 -std=c++17 "$src/spine_verify.cpp" -o "$out/verify"
cd "$out"
k=18
mkdir "out$k"
for i in $(seq 0 23); do
  ./generate "$k" "$i" 24 "out$k/$i.spn"
done
shasum -a 256 -c "$src/spine$k.sha256"
./verify "$k" "out$k"/*.spn
~~~

Each file starts with ASCII `SPN1` and one byte for $k$. Each shape has eight little-endian bytes encoding its fixed-length balanced-parentheses forest, with 1 for open, followed by a four-byte little-endian row count. Each row gives one byte per potential color group followed by $k-1$ vertex labels in preorder. A new potential color group starts when the next component is larger than all preceding components combined.
