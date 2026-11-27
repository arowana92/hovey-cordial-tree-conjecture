# All trees with at most seven nonleaf vertices

**Theorem.** Every finite tree with at most seven nonleaf vertices is super edge-magic. One integer labeling works for all positive moduli, including the harmonious labeling at one less than the order for nontrivial trees. The tree order and the individual leaf counts are unrestricted. This includes every diameter-five tree having at most five nonleaf neighbors in total off the two centers, regardless of how they are split. It also includes every tree of matching number at most four, since a tree of matching number $d$ has at most $2d-1$ nonleaf vertices. [Matching bound and results through five nonleaf vertices](five-nonleaf.md) · [Youssef's interval implication](https://ajc.maths.uq.edu.au/pdf/43/ajc_v43_p031.pdf)

Delete the leaves once and call the resulting tree $H$. The previous theorem covers $|H|\le5$. For $h=|H|\in\{6,7\}$, a path core gives a caterpillar, and a star core gives diameter at most four. Both have consecutive-sums labelings. [Diameter-four and caterpillar proofs](all-radius-two.md)

For every remaining core reserve one leaf at each terminal vertex of $H$ and rank its $h$ vertices by their remaining leaf counts, highest first. Let $e_r$ be the difference between the counts at ranks $r$ and $r+1$, with zero after the final rank. Thus the unrestricted vector $e$ specifies extra leaves through layers, each rank-$r$ layer attaching one leaf to each of the first $r$ vertices.

For each ranked core the certificate partitions all vectors $e$ into cells. A cell specifies $e_r=b_r+d_rt_r$ with $t_r\ge0$ independently. At step zero only $b_r$ occurs. A labeling of the seed at $e=b$ uses vertex interval $[L,U]$ and edge-sum interval $[L+1,U]$. For each positive step the certificate exhibits a lower and upper band of new leaves with exactly $d_r$ copies of every required parent. Direct addition checks that their sums fill the corresponding new ends of the edge interval. The bands can be repeated in any order. This gives the mathematical induction from each checked seed to all trees in its cell. [Band identities and proof of finite coverage](five-nonleaf.md#ranking-the-excess-leaf-counts)

| Core order | Ranked cores | Certified cells | Cells using a double layer | Largest seed order | Coverage representatives |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 6 | 930 | 1,775 | 43 | 31 | 98,620 |
| 7 | 14,280 | 43,335 | 6,125 | 45 | 6,201,958 |

The verifier checks that each core is a connected simple tree on the stated ranks, excludes paths and stars, and rejects any repeated group. Cayley's formula gives exactly $h^{h-2}-h!/2-h$ such trees because there are $h!/2$ distinct paths and $h$ stars. This count verifies completeness independently of the generator's rooted-shape and permutation enumeration. For each core the verifier checks exact coverage of the finite periodic box, direct integer sums on every seed, endpoint sums after actual layer insertions, and each parent's final number of leaves. [Verifier](check_ranked_core_cover.py) · [Six-vertex certificate](ranked-cores-6.jsonl.gz) · [Seven-vertex certificate](ranked-cores-7.jsonl.gz)

Run from the repository root with Python 3.

~~~sh
python3 -B -m research.hub.check_ranked_core_cover 6
python3 -B -m research.hub.check_ranked_core_cover 7
~~~

The generator first tries a seed for an entire cell. On failure it splits a coordinate into its first value and the remaining progression, or splits the progression into its even and odd positions. It favors splits for which both children already have witnesses. A search failure has no obstruction meaning. The decompressed SHA-256 digests are `a00d4b0bc76bc28ab0e527f8ebc8d423a5efe6219dbb9bdded45deff4725da7d` at six and `b62a24c0968868f2e56136fd0a2422a915d2a4e96dbb3fa4a7c73ff33f958c1d` at seven. [Generator](ranked_core_cover.py) · [Native seed search](ranked_core_search.cpp)

~~~sh
out=$(mktemp -d)
c++ -O3 -std=c++17 -shared -fPIC research/hub/ranked_core_search.cpp -o "$out/search.so"
for h in 6 7; do
    python3 -B -m research.hub.ranked_core_cover "$h" "$out/search.so" > "$out/$h.jsonl" || exit 1
    gzip -dc "research/hub/ranked-cores-$h.jsonl.gz" | cmp - "$out/$h.jsonl" || exit 1
done
~~~
