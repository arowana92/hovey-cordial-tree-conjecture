# Every tree through order 48 is 26-cordial and through order 49 is 27-cordial

**Theorem.** The order of a smallest unrestricted 26-label counterexample must be between **49 and 546** and congruent to **23, 24, 25 or 0** modulo 26. In particular every tree through order 48 has a 26-cordial labeling. With eleven through thirteen leaves, only orders 49 through 52 remain in the [few-leaf reduction](few-leaves.md). The unrestricted all-orders problem at 26 remains open.

The [twenty-vertex extension](twenty-free.md) already excludes the lower positive residues and covers every order through 47. Consider order $26m+22$. The integer census covers $m=0$. For $m\ge1$, a minimum counterexample would have at most 20 leaves, since otherwise one could remove 21 leaves, label the smaller tree and restore them by [Hall's theorem](../counterexample-bound.md#removing-leaves). The [ordered cut](ordered-cut.md) leaves a core of order $26m+1$ and 21 exterior vertices, with at most $\lfloor2\cdot20/3\rfloor=13$ exterior tips. The core has a cordial labeling by minimality. Translate its unique surplus to zero. Distinct nonzero free labels and distinct weights including all incoming edges suffice. The boundary colors in nondecreasing component-size order obey the run constraints of the ordered cut.

The independent native verifier counted **94,524,403** exterior forests, **1,422,256,412** witness rows, and **346,619,289,328** boundary assignments before unit symmetry. For each row it checked the actual vertex residues, internal sums, and allowed incoming weights. It checked coverage for each permitted assignment and uniqueness and completeness of the forest catalog. An independent partition calculation recovered the exact forest and assignment totals. This proves that the core always extends in this residue class. The known order-26 base, exclusion of order one modulo 26, and [branching-vertex upper bound](terminal-paths.md) give the stated interval.

The whole-tree checker replayed 300 joins to explicit path and star cores. A separate Python checker parsed all 23,631,101 records of shard zero and tested 475,956 boundary inputs on sampled records, including every run count from one through four. These are implementation checks alongside the exhaustive verification. The [stream hashes](twenty-one-free.sha256) pin the reproducible certificate.

## Twenty-one exterior vertices at 27 labels

At modulus 27 the same cut and certificate argument excludes order $27m+22$ for a smallest counterexample. The order-27 base is known and the previous residue bounds exclude residues 1 through 21. Consequently this argument gives 27-cordiality through order **49**. The subsequent [order-50 theorem](../census/order-fifty.md) covers the next order as well. A smallest counterexample would have order at least **51**, with residue 23 through 26 or zero. The separate [leaf-profile induction](../census/leaf-profile-cuts.md) covers every order through thirteen leaves.

The native checker verified **94,524,403** exterior forests, **1,048,158,293** witness rows and **390,696,056,451** boundary assignments. The partition recurrence independently recovered the forest and boundary totals, and the whole-tree checker replayed 150 joins to explicit cores from the two streams.

~~~bash
set -euo pipefail
src="$PWD/research/rainbow"
out=$(mktemp -d)
c++ -O3 -std=c++17 -Drainbow_witness=reference_witness -c "$src/search.cpp" -o "$out/ref.o"
c++ -O3 -std=c++17 "$src/spine_generate.cpp" "$src/leaf_search.cpp" "$out/ref.o" -o "$out/make"
c++ -O3 -std=c++17 -pthread "$src/spine_verify.cpp" -o "$out/check"
for j in 0 1 2 3; do
    "$out/make" 26 "$j" 4 "$out/s26-21-13-$j.spn" --short 21 13
done
"$out/check" 26 --short 21 13 "$out"/s26-21-13-*.spn
python3 -B -c 'from research.rainbow.check_tip_forests import totals; assert totals(26,13,21)==(94524403,346619289328)'
for j in 0 1; do
    "$out/make" 27 "$j" 2 "$out/s27-21-13-$j.spn" --short 21 13
done
"$out/check" 27 --short 21 13 "$out"/s27-21-13-*.spn
python3 -B -c 'from research.rainbow.check_tip_forests import totals; assert totals(27,13,21)==(94524403,390696056451)'
python3 -B -m research.rainbow.check_short_joins "$out"/*.spn
python3 -B -m research.rainbow.check_spine_samples "$out/s26-21-13-0.spn" --stride 8000000
(cd "$out" && shasum -a 256 -c "$src/twenty-one-free.sha256")
~~~
