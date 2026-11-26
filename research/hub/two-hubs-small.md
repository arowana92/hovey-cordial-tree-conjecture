# Two unrestricted leaf counts on every core through order thirteen

**Theorem.** Take any tree $H$ of order at most thirteen and any two distinct vertices $a,b$. Add any number of leaves at each of $a$ and $b$, including zero. Every resulting tree is cordial at every positive modulus. In particular this holds whenever all but at most five edges of a tree touch one of two specified vertices: after removing their other leaf neighbors, each remaining vertex outside the pair belongs to one of the five edges, except possibly the pair's unique common neighbor.

## Why the data suffice

Absorb any unmarked leaf already attached to a marked vertex into that hub's free leaf count. In the remaining core, if deleting the leaves after adding one new leaf at each mark leaves a path, all distributions give caterpillars. Deleting the extra leaves or adding further ones at the marks keeps those trees in the same family. Hovey's caterpillar theorem applies.

The other marked cores have explicit integer labelings with the two hub labels 0 and 1. In every gap $l<u$ between successive sorted core labels there is exactly one core weight $w$ with $l<w\le u$. Filling the gap needs $w-l-1$ leaves at the first hub and $u-w$ at the second. Sum these quantities to get $A$ and $B$. The [two-hub interval proof](two-hubs.md) gives all moduli and all leaf counts at least $A,B$. [Lean verification of injectivity and exact gap coverage](TwoHubGaps.lean)

If the first hub gets $j<A$ leaves, absorb those leaves into the core. The second hub then has one unrestricted count. Use the [one-hub theorem through order thirteen](README.md) whenever $h+j\le13$. Do the same when the second count is below $B$. Six additional marked one-hub cases are needed across the entire archive. Each contains its own integer witness with the unrestricted hub labeled zero, distinct vertices of span at most 17 and distinct weights in the vertex set. The one-hub periodic extension works at every $k\ge18$. The all-tree proofs through seventeen cover the smaller moduli. This exhausts both unbounded leaf counts.

## Coverage

The 31,820 rows contain parent vectors, the two hub indices, integer labels and any required one-hub strip witnesses. Unordered marked pairs suffice because both counts vary independently.

| Core order | Trimmed caterpillar families | Other marked cores with witnesses |
|---:|---:|---:|
| 2 | 1 | 0 |
| 3 | 1 | 0 |
| 4 | 3 | 0 |
| 5 | 6 | 1 |
| 6 | 15 | 5 |
| 7 | 33 | 19 |
| 8 | 79 | 68 |
| 9 | 178 | 226 |
| 10 | 414 | 731 |
| 11 | 934 | 2,291 |
| 12 | 2,128 | 7,063 |
| 13 | 4,768 | 21,416 |

The generator roots a tree at one hub and marks the other. The verifier independently starts a path of every possible length between the hubs and grows all side branches by single-leaf insertion. Every marked tree that is not a bare marked path has a nonhub leaf to delete. Growing even the untrimmed intermediate shapes preserves this completeness argument. Sorted child codes distinguish rooted isomorphism types, with brackets marking the second hub. Taking the smaller code under exchange of the two hubs gives a complete invariant for unordered hub pairs. The verifier checks the actual labels, all original edge sums, both thresholds and every residual one-hub case.

~~~sh
python3 -B -m research.hub.two_hub_certificate 13 --verify research/hub/two-hubs-through13.jsonl.gz
lean research/hub/TwoHubGaps.lean
~~~

Regeneration uses Python and a C++17 compiler. The independent verifier needs only Python. The uncompressed published certificate has SHA-256 `1628b7c436a8c7310da75eb61ea42fc010859718c34e497600aef7baefc928f2`.

~~~sh
out=$(mktemp -d)
c++ -O3 -std=c++17 -shared -fPIC research/hub/two_hub_search.cpp -o "$out/search.so"
python3 -B -m research.hub.two_hub_certificate 13 --library "$out/search.so" > "$out/data.jsonl"
gzip -dc research/hub/two-hubs-through13.jsonl.gz | cmp - "$out/data.jsonl"
~~~
