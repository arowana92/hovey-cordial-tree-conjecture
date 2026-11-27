# Excluding order residue 21 by restoring twenty vertices

**Theorem.** At 26, 27 and 29 labels, a smallest unrestricted counterexample has order $mk+s$ with $22\le s\le k$. The same conclusion holds at every modulus $k\ge33$. In particular every tree on at most **47 vertices** is 26-cordial, and the only possible order residues for a smallest 26-label counterexample are $22,23,24,25,0$. Its order lies between **48 and 546**. Every tree on at most **48 vertices** is 27-cordial. [Upper bound from branching vertices](terminal-paths.md)

## Why twenty free vertices suffice

The [nineteen-vertex theorem](short-forests.md) already gives $s\ge21$ at every modulus. Consider $s=21$. Order 21 itself is covered by the [integer census](../census/README.md). If $m\ge1$, at least 20 original leaves would allow deletion and restoration of 20 leaves by [Hall's prescribed-differences theorem](../counterexample-bound.md#removing-leaves). Thus the minimum tree has at most 19 leaves. Take the [size-ordered cut](ordered-cut.md) leaving a connected core of order $mk+1$. Its exterior has 20 vertices and at most $\lfloor2L/3\rfloor$ terminal vertices, where $L$ is the original leaf count. The parent colors can change only at the positions allowed by the ordered-cut theorem.

Translate the surplus label of the cordially labeled core to zero. Every old edge count is $m$. An injection of the 20 free vertices into the nonzero residues with distinct weights on all 20 entering edges suffices. Restoring the translation preserves the resulting balance. The finite tests below cover every possible exterior and every allowed boundary assignment. At 26 and 27 labels the order-$k$ bases are known. The first possible counterexample orders are consequently 48 and 49, respectively.

The general 19-leaf bound gives a limit of 12 exterior tips at moduli 26 and 27. At 29 labels the [prime leaf bound](../biased/two-star-lists.md) gives $L\le2s-29-3=10$. At 33 labels the [general leaf bound](../biased/six-spare-leaves.md#removing-every-leaf-at-once) gives $L\le2(42-33)-1=17$, hence at most eleven exterior tips. At $34=2\cdot17$, seven leaves would give $2s-34\ge10$ from the [odd-batch theorem](../biased/twice-prime-power-lists.md), whereas the left side is 8. At 35 labels the [leaf count bound](../biased/six-spare-leaves.md#removing-every-leaf-at-once) gives $L\le2(2s-35)-1=13$. At 36 labels the even equality case $2s-k=6$ requires exactly five leaves. At $k=31$ the [prime bound](../biased/pruned-forests.md) also gives $s\ge22$. At every $k\ge37$ the general inequality $2s-k\ge6$ already forces $s\ge22$.

## Exhaustive checks

| Modulus | Exterior tip limit | Forests | Witness rows | Boundary assignments before unit symmetry |
| ---: | ---: | ---: | ---: | ---: |
| 26 | 12 | 33,607,992 | 377,121,275 | 111,769,375,042 |
| 27 | 12 | 33,607,992 | 290,490,978 | 125,489,205,558 |
| 29 | 6 | 1,478,884 | 2,147,694 | 2,733,033,892 |
| 33 | 11 | 30,824,753 | 116,027,756 | 208,304,484,465 |
| 34 | 4 | 41,553 | 81,931 | 42,472,392 |
| 35 | 8 | 10,571,178 | 26,727,643 | 61,074,558,020 |
| 36 | 3 | 3,023 | 16,571 | 1,521,288 |

The [native verifier](spine_verify.cpp) checks the shape of each forest, distinctness of all free labels and internal sums, the exact coverage of permitted boundary assignments and global uniqueness of the forest records. The partition recurrence counts the required shapes and boundary assignments by a different calculation. The [whole-tree replay](check_short_joins.py) attaches sampled forests to actual path or star cores, tries the stored permutations and their unit multiples, and counts every vertex and edge residue of each complete tree. The whole-tree test checked 672 joins across these streams. An independent small-order regression checked 87,422 boundary inputs and rejected four damaged streams. A separate [Python sum checker](check_spine_samples.py) scanned all 8,401,998 records of the first 26-label shard and tested 475,956 color assignments on samples spanning one through four boundary runs.

## Reproduction

Run in Bash from the repository root. The SHA-256 manifest is generated from the full streams, including all four disjoint 26-label shards.

~~~bash
set -euo pipefail
src="$PWD/research/rainbow"
out=$(mktemp -d)
c++ -O3 -std=c++17 -Drainbow_witness=reference_witness -c "$src/search.cpp" -o "$out/ref.o"
c++ -O3 -std=c++17 "$src/spine_generate.cpp" "$src/leaf_search.cpp" "$out/ref.o" -o "$out/make"
c++ -O3 -std=c++17 -pthread "$src/spine_verify.cpp" -o "$out/check"
for j in 0 1 2 3; do
    "$out/make" 26 "$j" 4 "$out/s26-20-12-$j.spn" --short 20 12
done
"$out/check" 26 --short 20 12 "$out"/s26-20-12-*.spn
while read -r k tips; do
    name="s$k-20-$tips.spn"
    "$out/make" "$k" 0 1 "$out/$name" --short 20 "$tips"
    "$out/check" "$k" --short 20 "$tips" "$out/$name"
done <<'CASES'
27 12
29 6
33 11
34 4
35 8
36 3
CASES
python3 -B -m research.rainbow.check_short_joins "$out"/*.spn
python3 -B -m research.rainbow.check_spine_samples "$out/s26-20-12-0.spn" --stride 3000000
(cd "$out" && shasum -a 256 -c "$src/twenty-free.sha256")
~~~
