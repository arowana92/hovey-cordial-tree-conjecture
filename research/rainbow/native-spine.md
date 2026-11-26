# Certificates for every finite tree at eighteen through twenty labels

**Theorem.** Every finite tree is 18-cordial, 19-cordial and 20-cordial. The [ordered-cut theorem](ordered-cut.md) reduces the claim at all orders to two finite hypotheses. The witness stream verifies both, using the sharp condition on actual runs of boundary colors. For every required colored forest the verifier checks a bijection to the nonzero residues and computes all parent-edge sums, including the prescribed boundary edges.

| Modulus | Rooted base trees | Eligible forests | Base-only shapes | Witness rows | Eligible boundary colorings before unit symmetry |
|---:|---:|---:|---:|---:|---:|
| 18 | 1,721,159 | 1,587,279 | 133,880 | 239,253,064 | 1,276,116,192 |
| 19 | 4,688,676 | 4,479,243 | 209,433 | 266,718,296 | 4,721,012,403 |
| 20 | 12,826,228 | 12,508,236 | 317,992 | 638,068,501 | 17,333,648,400 |

## One representation for the two hypotheses

Removing the root from a rooted tree of order $k$ gives a forest of order $k-1$. When every external parent label is zero, a rainbow labeling of that forest is precisely a bijective rainbow labeling of the tree with its root labeled zero. We check the all-zero row on **every** forest, including those above the terminal limit. For an eligible forest this same row also handles its all-zero boundary coloring.

The [generator](spine_generate.cpp) recursively lists multisets of rooted children. It enumerates potential color changes at the size gaps and discards assignments incompatible with the sharp run condition or equivalent to a lexicographically smaller assignment under multiplication by a unit. It obtains witnesses using the [native search](search.cpp).

The [verifier](spine_verify.cpp) parses balanced parentheses and verifies that components and siblings are sorted by size and then code. These comparisons make the representation unique by induction on size. It rejects repeated forest codes across all shards. Independently, the product $\prod_{j\ge1}(1-x^j)^{-R_j}$ counts multisets of rooted trees, where $R_j$ is the number of rooted trees of order $j$. Its coefficient at $x^{s-1}$ is $R_s$. The verifier computes the coefficients by multiset binomial counts. Consequently the final number of distinct valid forests proves complete shape coverage.

For each size profile the verifier enumerates boundary patterns, counts actual color runs on the components, tests the separation inequalities and partitions the valid patterns into unit orbits. At 18 and 19 the rows for each eligible shape must hit every orbit exactly once. At 20 the verifier checks the shared-witness coverage described below. On every row the verifier checks residue ranges, injectivity with zero forbidden, and weight distinctness from the original endpoint labels. The all-zero row must occur even at ineligible shapes.

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

## Sharing a witness across boundary colorings

The optional generator argument `--cover` writes the version `SPN2`. Each record has the same shape and row-count fields as above. A row now stores just the $k-1$ vertex labels. With these labels fixed, one can evaluate the boundary assignments for which all weights are distinct. Multiplying all labels by a unit then covers the whole orbit of each such assignment.

The generator finds the possible sets of weights at each group of roots by cyclically shifting the set of their labels. The verifier takes a different route. It gives the first root of a group an unused weight, subtracts its label to determine the parent color, and checks every other root in that group by direct addition. A completed recursion marks only the orbit of that concrete assignment. Before advancing to another shape it checks every required orbit, including the zero boundary for the rooted base. Ineligible shapes require only the zero boundary.

A small comparison can be reproduced after building the two executables above.

~~~sh
./generate 10 0 1 plain.spn
./generate 10 0 1 shared.spn --cover
./verify 10 plain.spn
./verify 10 shared.spn
~~~

Both streams certify 719 rooted bases and 46,630 boundary colorings on 550 eligible forests. The first uses 13,157 witness rows and the second uses 4,901.

## Reproducing the twenty-label proof

Use the same compiler commands and working directory as above. The twenty-label certificate uses 32 independently generated shards, approximately 11.4 GiB total. The two programs share no orbit-checking or tree-enumeration code. The complete verified stream covers all 12,826,228 rooted shapes. The [SHA-256 manifest](spine20.sha256) identifies every shard.

~~~sh
k=20
mkdir "out$k"
for i in $(seq 0 31); do
  ./generate "$k" "$i" 32 "out$k/$i.spn" --cover
done
shasum -a 256 -c "$src/spine20.sha256"
./verify "$k" "out$k"/*.spn
~~~

Alternatively pass `--files-stdin` to the verifier and write one completed shard path per line to its standard input. It checks shapes across all inputs and requires the full rooted-tree count at end of file in both modes.

## Counting the required cases from integer partitions

A third program reproduces the rooted-base, eligible-forest and boundary-assignment columns without reading witnesses or listing individual trees. For each partition of $k-1$, group components of the same order $s$. If there are $R$ available rooted shapes of order $s$ with a given leaf count, taking $a$ of them with repetitions gives $\binom{R+a-1}{a}$ choices. Convolve these counts by the number of leaves; summing over partitions at smaller orders supplies the initial rooted-shape counts. For a fixed sorted size list, count colorings by their current number $r$ of runs. The next color can stay the same, or change in $k-1$ ways when the next size is at least the preceding mass plus $r$. Multiplying by the terminal-limited count of forests of each profile recovers exactly 17,333,648,400 colorings at 20. The explicit witness verifier establishes the labelings for these cases. [Partition count](spine_counts.py)

~~~sh
python3 -B research/rainbow/spine_counts.py 18 19 20
~~~
