# Every finite tree is 26-cordial

**Theorem (computer-assisted).** Every finite tree admits a vertex labeling in $\mathbb Z/26\mathbb Z$ with all vertex frequencies differing by at most one and all edge frequencies differing by at most one. Each edge receives the sum of its endpoints modulo 26. Both comparisons include residues of frequency zero.

## Why a finite computation proves the all-orders theorem

On 26 vertices, a bijection with 25 different edge weights suffices. Deleting a root leaves a forest of order 25 with external parent color zero after translating the labels. Testing this boundary for every forest proves the base. Trees of smaller order extend to order 26 by adding leaves and inherit the conclusion by restriction.

For a larger tree, write its order as $26q+1+t$ with $0\le t\le25$. At $t=0$, delete a leaf and use induction. The remaining tree has uniform vertex counts and one deficient edge weight. Restoring the leaf with the label that produces this weight works. At $t>0$, if the tree has at least $t$ leaves, delete that many leaves and apply Hall's prescribed-differences construction. Otherwise the ordered-cut lemma gives a connected core of order $26q+1$ and an attached rooted forest with at most 16 terminal vertices. Sort the components by size. A change of boundary color requires the next component to have at least as many vertices as the total order of earlier components plus the number of earlier color runs. Extending a largest component by a path pads this forest to order 25 and preserves that condition. [Leaf deletion and Hall's argument](../counterexample-bound.md#removing-leaves) · [Ordered cut, exact run condition and padding](ordered-cut.md)

By induction the core has a cordial labeling, with one surplus vertex residue that we translate to zero and uniform edge counts. The certified forest permutation uses each nonzero residue once and gives 25 distinct weights on its internal and attachment edges. Restrict it to the actual exterior. It adds only to low vertex bins and at most once to each edge bin. This completes the induction.

## Certificate

| Rooted bases | Eligible forests | Base-only shapes | Witness permutations | Eligible boundary assignments before unit symmetry |
| ---: | ---: | ---: | ---: | ---: |
| 5,759,636,510 | 5,711,066,633 | 48,569,877 | 370,983,467,355 | 28,546,749,606,908 |

The certificate consists of 4,096 deterministic streams. The verifier reads each forest and permutation, checks the nonzero vertex labels and internal sums, and reconstructs all possible parent labels by assigning unused edge weights at distinguished component roots. It verifies the remaining attachment edges and checks coverage modulo multiplication by units. It tests the all-zero boundary even when only the rooted base is required. The verifier rejects a repeated shape by ranking the actual parent array and setting the corresponding bit. Every expected rank occurred. [Generator](spine_generate.cpp) · [Native verifier](spine_verify.cpp) · [Ranking proof](shape-rank.md) · [Stream digests](spine26.sha256)

Three independent checks cover different claims.

- A partition recurrence counted the rooted bases, eligible forests and ordered boundary assignments. A separate exhaustive topology run found 5,759,636,510 distinct ranks in range. The integer-labeling census independently supplies the ordinary base on all 279,793,450 unrooted trees of order 26. [Integer-labeling census](../census/README.md) The generator totals for all 4,096 shards and the independently computed partition totals agree with the native verifier's report. [Partition recurrence](spine_counts.py) · [Report checker](check_spine_report.py)
- Shards 53, 311 and 2027 regenerated from a separate SSH checkout and matched their published SHA-256 digests and byte lengths. On those files a Python checker examined 135 sampled forests, all 14,448 of their permutations and 1,850,710 boundary inputs. It enumerates the positions of color changes and tests pairwise sum collisions. A separate pilot at stride 524,288 received the same Python check on **every** record, totaling 10,986 forests, 709,471 rows and 55,865,961 inputs. [Python checker](check_spine_samples.py) · [Pilot digest and commands](twenty-five.md#a-finite-pilot-for-26)
- At modulus 26 both native catalog modes rejected seven deliberate faults, including invalid residues, missing coverage, truncated data and duplicated shapes within or across files. [Fault tests](check_spine_faults.py)

## Reproduction

Use Python 3, a C++17 compiler and POSIX named pipes. The uncompressed streams total 9,343,702,342,475 bytes. Piping avoids storing that volume on disk. The rank array uses approximately 686.6 MiB in addition to worker memory. Choose the worker count to suit the machine and keep the shard count at 4,096 to reproduce the manifest.

~~~sh
set -e
src="$PWD/research/rainbow"
out=$(mktemp -d)
c++ -O3 -std=c++17 -c -Drainbow_witness=reference_witness "$src/search.cpp" -o "$out/reference.o"
c++ -O3 -std=c++17 "$src/spine_generate.cpp" "$src/leaf_search.cpp" "$out/reference.o" -o "$out/generate"
c++ -O3 -std=c++17 -pthread "$src/spine_verify.cpp" -o "$out/verify"
python3 -B "$src/stream_spine.py" 26 4096 12 "$out/generate" "$out/verify" "$out/audit" --pipe-witnesses --rank-bits
cmp "$out/audit/spine26.sha256" "$src/spine26.sha256"
python3 -B "$src/check_spine_report.py" 26 4096 "$out/audit"
~~~

A one-shard check takes about 2.28 GB of disk. After building the same binaries, run the following from the same shell.

~~~sh
cd "$out"
mkdir spine26
./generate 26 311 4096 spine26/311.spn --ranked-cover
awk '$2 == "spine26/311.spn"' "$src/spine26.sha256" | shasum -a 256 -c -
python3 -B "$src/check_spine_samples.py" spine26/311.spn --stride 30000
python3 -B "$src/check_spine_faults.py" "$out/verify" spine26/311.spn --rank-bits
~~~

The same certificate also yields a connected growth order with a single cordial labeling on every prefix, and a most-frequent label at a specified leaf. A forest of any order with at most 16 tips attached at one old vertex can grow from a fixed cordial core of order zero or one modulo 26. In particular, in a tree with at most 17 leaves any specified leaf can start a connected cordial growth order. The full conjecture remains open. [Growth proof](cut-growth.md) · [Marked-leaf proof](../marked-leaves.md) · [27-label inventory and finite pilot](shape-rank.md#a-27-label-pilot)
