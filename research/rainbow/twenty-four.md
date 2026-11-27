# Every finite tree is 24-cordial

**Theorem (computer-assisted).** Every finite tree, with unrestricted order or degrees, has a 24-cordial labeling. The labels are residues modulo 24 and the edge weight is the sum of its endpoint labels. Both histograms have pairwise differences at most one, including bins with count zero.

The [ordered-cut theorem](ordered-cut.md) reduces arbitrary orders to two finite statements. At order 24 every tree needs a bijection with 23 distinct edge sums. At larger orders a labeled core of order one modulo 24 has a unique surplus vertex label. Translate it to zero. The 23 free vertices in an attachment forest must use the nonzero residues and have distinct new weights, including those of their edges back to the prescribed core labels. The forest test needs at most 14 terminal vertices. Order components by size. A change of incoming label is possible only if the new component has size at least the preceding total order plus the number of preceding color runs. Induction and the restriction of a padded final block give the all-orders conclusion. [Cut and induction](ordered-cut.md) · [Ranked rooted-forest enumeration](twenty-three.md#generating-a-shard-without-storing-every-rooted-branch)

| Rooted bases | Eligible forests | Base-only shapes | Witness rows | Eligible boundary assignments before unit symmetry |
| ---: | ---: | ---: | ---: | ---: |
| 743,724,984 | 723,584,510 | 20,140,474 | 70,137,407,884 | 2,446,537,872,000 |

## What was checked

The all-zero input on each forest gives its rooted base by reinstating a root labeled zero. For each witness the independent native verifier checks all vertex values and internal edge sums. It assigns still-unused weights to distinguished component roots, deduces their boundary labels, and tests the remaining root edges by addition. The union of covered inputs must contain every required boundary assignment up to multiplication by a unit. It checks canonical parenthesis words inside each shard and sorts the complete set across all 1,024 shards to exclude duplicates. It checks the final count against the rooted-tree generating function. A second count from integer partitions gives the same totals for bases, eligible forests and boundary assignments. The separate integer census also covers the order-24 base. [Native verifier](spine_verify.cpp) · [Partition count](spine_counts.py) · [Integer census](../census/README.md)

A third checker enumerates actual subsets of component positions at which the incoming color changes. For each permitted coloring it excludes collisions between internal and incoming weights and between pairs of incoming groups. On shards 413, 982 and 993 it checked 57 sampled forests spanning the three files and all possible maximum run counts, including the base-only case. It checked 15,319 witness rows against 1,213,491 boundary inputs on those forests. At modulus nine the same checker tested all 286 shapes, 911 witnesses and 10,478 inputs including base-only cases. Independent regenerations of shards 413 and 982 from an SSH checkout reproduced their digests. Six deliberate input faults were rejected by the native verifier, including an invalid vertex value, truncation, a duplicate forest, an incomplete catalog, an empty record and a partial boundary cover. [Independent sample checker](check_spine_samples.py) · [SHA-256 manifest](spine24.sha256)

## Reproduction with bounded disk space

Use Python 3, a C++17 compiler and a system with POSIX named pipes. The streams contain 1,622,085,086,260 uncompressed bytes in total. The runner stores up to one shard per generation worker at a time, hashes the bytes it delivers to the native verifier, and removes that shard after delivery. The global shape keys alone require about 6 GB of verifier memory. The arguments below request twelve workers. Fewer workers reduce the simultaneous scratch footprint. The output directory must be new.

~~~sh
set -e
src="$PWD/research/rainbow"
out=$(mktemp -d)
c++ -O3 -std=c++17 -c -Drainbow_witness=reference_witness "$src/search.cpp" -o "$out/reference.o"
c++ -O3 -std=c++17 "$src/spine_generate.cpp" "$src/leaf_search.cpp" "$out/reference.o" -o "$out/generate"
c++ -O3 -std=c++17 -pthread "$src/spine_verify.cpp" -o "$out/verify"
python3 -B "$src/stream_spine.py" 24 1024 12 "$out/generate" "$out/verify" "$out/audit"
cmp "$out/audit/spine24.sha256" "$src/spine24.sha256"
cat "$out/audit/verified.txt"
python3 -B "$src/spine_counts.py" 24
~~~

For a smaller replay, use the same binaries and generate the sampled shard alone.

~~~sh
cd "$out"
mkdir spine24
./generate 24 413 1024 spine24/413.spn --ranked-cover
awk '$2 == "spine24/413.spn"' "$src/spine24.sha256" | shasum -a 256 -c -
python3 -B "$src/check_spine_samples.py" spine24/413.spn
~~~

The repository publishes the reproducible generator, verifiers and manifest. The all-orders proof here covers ordinary endpoint sums at one additional modulus. Hovey's all-moduli conjecture remains open.
