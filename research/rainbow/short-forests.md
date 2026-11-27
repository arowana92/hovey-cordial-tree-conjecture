# Excluding order residues by checking shorter forests

**Theorem (computer-assisted).** At 26 and 27 labels, a minimum counterexample of order $mk+s$, where $1\le s\le k$, must have $s\ge21$. At 26 labels its order is also at most 598 by the [divisible-cut bound](../divisible-cuts.md).

## The reduction

Fix a potential counterexample of least order at its modulus. For $s\le20$, the case $m=0$ follows from the [integer tree census](../census/README.md). For $m\ge1$, put $t=s-1$. The [leaf deletion lemma](../counterexample-bound.md#removing-leaves) gives $L<t$. Take the size-ordered preorder cut from the [leaf-centroid construction](ordered-cut.md). Its $mk+1$ retained vertices form a smaller cordial tree. Its $t$ exterior vertices have at most $\lfloor2L/3\rfloor$ rooted terminals, and the changes of boundary label obey the sharp run condition. Translating the core sets the single surplus vertex label to zero while preserving uniform edge counts.

With $s\le20$ this exterior can be padded to just 19 vertices by continuing a terminal of a largest component. Padding preserves the number of terminals and all permitted color changes. Since $L\le18$, at most 12 terminals occur. For each allowed boundary assignment it suffices to inject the 19 vertices into the nonzero residues, with all 19 new edge sums distinct, including the edges to the fixed boundary parents. Restriction to the original exterior restores the tree. This proof uses the cardinality of the short suffix directly.

The earlier 18-vertex test at $k=26$ already gives $s\ge20$. At $s\le19$, eleven or more leaves would violate $2s-26\ge14$ in the [odd-batch list theorem](../biased/twice-prime-power-lists.md), taking $r=11$. Thus $L\le10$ and six terminals suffice.

## Certificates

| Modulus | Free vertices | Tip limit | Forest shapes | Witness rows | Boundary assignments |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 26 | 18 | 6 | 489,585 | 2,000,745 | 659,663,160 |
| 26 | 19 | 12 | 12,508,236 | 104,723,103 | 38,364,554,436 |
| 27 | 19 | 12 | 12,508,236 | 85,260,039 | 43,086,511,494 |

The [generator](spine_generate.cpp) uses a parent-before-child search on the free vertices. Its SPN3 stream starts with the four ASCII header bytes followed by the modulus and free order, one byte each. Each record has an eight-byte little-endian forest word, a four-byte row count, and one byte per free vertex in each witness row. A row can cover many boundary assignments. Multiplication by a unit gives the corresponding labeling on every assignment in its orbit.

The [verifier](spine_verify.cpp) checks canonical forest structure, the exact free order and tip limit, uniqueness and the independent bivariate shape count. For every row it checks distinct nonzero labels and distinct internal sums. It reconstructs the boundary colors by assigning unused sums to a distinguished root in each group and verifies the other roots individually. Its run-condition oracle and separate counts establish coverage for the entire required family. The [Python replay](check_short_forests.py) independently grows the small rooted trees by inserting leaves, expands the units, and checks every sum literally on 87,422 small boundary inputs through modulus 40. It also recomputes the large shape and coloring counts by branch-size partitions. [SHA-256 manifest](short-streams.sha256)

## Reproduction

Run in Bash from the repository root with Python 3 and a C++17 compiler.

~~~bash
set -e
src="$PWD/research/rainbow"
out=$(mktemp -d)
c++ -O3 -std=c++17 -c -Drainbow_witness=reference_witness "$src/search.cpp" -o "$out/ref.o"
c++ -O3 -std=c++17 "$src/spine_generate.cpp" "$src/leaf_search.cpp" "$out/ref.o" -o "$out/generate"
c++ -O3 -std=c++17 -pthread "$src/spine_verify.cpp" -o "$out/verify"
python3 -B -m research.rainbow.check_short_forests --binaries "$out/generate" "$out/verify"
while read -r digest name; do
    IFS=- read -r mod mass limit <<< "${name%.spn}"
    k=${mod#s}
    "$out/generate" "$k" 0 1 "$out/$name" --short "$mass" "$limit"
    "$out/verify" "$k" --short "$mass" "$limit" "$out/$name"
done < "$src/short-streams.sha256"
(cd "$out" && shasum -a 256 -c "$src/short-streams.sha256")
python3 -B "$src/check_spine_samples.py" "$out/s26-18-6.spn" --stride 80000
~~~
