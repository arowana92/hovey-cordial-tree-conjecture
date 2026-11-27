# Every finite tree is 22-cordial

**Theorem.** For every finite tree there is a vertex labeling modulo 22 for which every two vertex frequencies differ by at most one and every two endpoint-sum frequencies differ by at most one. This is a computer-assisted proof for all tree orders.

The [ordered-cut theorem](ordered-cut.md) reduces the assertion to a bijective rainbow labeling on every 22-vertex tree and a list of prescribed boundary problems on forests of order 21. In the sharp version, consecutive runs of boundary colors can change only when each component in the new run has at least the preceding mass plus the number of preceding runs. At most 13 terminals are needed. The base is the zero boundary coloring on a forest obtained by removing a root. Thus every rooted base is checked, including the shapes above the terminal bound.

| Rooted bases | Eligible forests | Base-only shapes | Witness rows | Required boundary assignments before unit symmetry |
| ---: | ---: | ---: | ---: | ---: |
| 97,055,181 | 94,524,403 | 2,530,778 | 3,933,409,170 | 205,254,702,136 |

Each witness is an actual permutation of the 21 nonzero residues. The independent verifier checks its original internal edge sums and tests boundary weights by direct addition. It checks completeness of the coloring orbits for each eligible shape. Valid canonical rooted shapes are globally distinct and their total is checked against the independent rooted-tree recurrence. A separate calculation from integer partitions gives the same numbers of bases, eligible forests and required boundary assignments. These finite checks verify the two hypotheses of the induction. [Stream format and orbit coverage](native-spine.md) · [Verifier](spine_verify.cpp) · [Partition count](spine_counts.py)

## Finding the missing weight before labeling the leaves

When the internal free vertices have labels, the sum $P$ of the parents' labels over all 21 edges is fixed. It includes the prescribed boundary labels with multiplicity and each internal free label once for every child. The free vertex labels use all nonzero residues. If the 21 edge weights are distinct, their missing residue is $-P$ modulo 22, by summing all edge weights. Thus exactly as many weight slots as vertex slots remain for the leaves.

The search takes a remaining label or weight with the fewest possible parent residues. A choice consumes one vertex slot, one sum slot and one leaf at the chosen parent residue. It tries a deterministic sequence of internal placements and uses the earlier exhaustive search as a fallback. The independent verifier only receives the resulting labels. [Leaf search](leaf_search.cpp) · [Fallback](search.cpp) · [Generator](spine_generate.cpp)

## Reproduction

Use a C++17 compiler. The 96 shards occupy 83,766,255,222 bytes in total. The hashes identify the uncompressed streams. Each shard has a five-byte header, twelve bytes per shape and 21 bytes per witness, giving a separate check on the row totals. The parallel verifier rejects a repeated shape across files. Negative controls at ten labels also confirm rejection of a forbidden zero vertex label and a duplicated shard.

~~~sh
set -e
src="$PWD/research/rainbow"
out=$(mktemp -d)
c++ -O3 -std=c++17 -c -Drainbow_witness=reference_witness "$src/search.cpp" -o "$out/reference.o"
c++ -O3 -std=c++17 "$src/spine_generate.cpp" "$src/leaf_search.cpp" "$out/reference.o" -o "$out/generate"
c++ -O3 -std=c++17 -pthread "$src/spine_verify.cpp" -o "$out/verify"
cd "$out"
mkdir spine22
for i in $(seq 0 95); do
    ./generate 22 "$i" 96 "spine22/$i.spn" --cover
done
shasum -a 256 -c "$src/spine22.sha256"
./verify 22 --parallel 8 spine22/*.spn
python3 -B "$src/spine_counts.py" 22
~~~

The generator shards may run concurrently. Verification accepts the files in any order. [SHA-256 manifest](spine22.sha256)
