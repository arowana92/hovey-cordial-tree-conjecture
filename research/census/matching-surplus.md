# A uniform attachment from a matching that leaves the joint exposed

**Theorem (computer-assisted).** Let $k\in\{2,6,10,14,18,22,26,30\}$. Take a rooted tree with $k$ free vertices besides the root. Suppose deleting the root leaves a forest with a perfect matching. For **any** prescribed root label in $\mathbb Z_k$, the free vertices can use each residue exactly once and the $k$ edges can use each weight exactly once.

Consequently such a piece attaches at its root to **any** cordially labeled tree, preserving its labeling for every old order. Its individual vertex and edge increments are uniform. In particular no smallest 26-label counterexample can have an edge cutting off a 27-vertex component whose exposed port can be left unmatched by a matching covering its other 26 vertices. Keep the port as a leaf of the smaller tree and use the theorem there. The conclusion also applies to any number of successive attachments at already labeled vertices. At 26 labels the rooted family has 42,187,148 isomorphism classes, and at 30 labels it has 1,091,711,076.

## Contracting the pairs

Write $k=2m$ with $m$ odd. Set the root label to zero and add the desired constant to all labels at the end. Contract the $m$ matched edges, keeping the root as a singleton, to get a rooted tree $Q$ of order $m+1$. Try to use all $m$ residues once among its nonroot vertices and once among its edge weights, with root zero. Such a quotient labeling $f$ includes its root label once among the free labels. This extra constraint accounts for the exceptional quotients below.

When the labeling exists, give the members of pair $i$ the labels $2f(i)$ and $2f(i)+m$ modulo $2m$. Choose which endpoint gets which value recursively so that ends of every **nonmatching** edge have the same parity. This is possible starting at the singleton root because the contraction is a tree. The free labels are exactly the even and odd lifts of the modulus-$m$ permutation. The matching weights $4f(i)+m$ run through the odd residues. The nonmatching edges weigh twice their corresponding quotient weights and so run through the even residues. This adapts the [perfect-matching lift](../matching-expansion.md) to the prescribed singleton and proves the theorem on every expansion of each successful quotient. Modulus two is the single two-edge path rooted at an endpoint and also follows by the same construction with $m=1$.

## Exceptional quotients and their expansions

| Modulus $2m$ | Rooted quotients | Quotients without the uniform labeling | Expanded rooted trees checked directly | Rooted trees covered |
| ---: | ---: | ---: | ---: | ---: |
| 6 | 4 | 0 | 0 | 10 |
| 10 | 20 | 1 | 6 | 160 |
| 14 | 115 | 4 | 46 | 3,177 |
| 18 | 719 | 5 | 99 | 70,678 |
| 22 | 4,766 | 13 | 329 | 1,686,486 |
| 26 | 32,973 | 18 | 614 | 42,187,148 |
| 30 | 235,381 | 4 | 267 | 1,091,711,076 |

For an exceptional quotient, orient each pair by calling the endpoint incident to its incoming quotient edge the first endpoint. For each outgoing edge choose which endpoint it meets. Deduplicate the resulting rooted trees and solve them directly modulo $2m$. All the resulting trees have positive witnesses. For example at $m=13$ the quotient consisting of a root with two children having five and six leaf children has no uniform root labeling. All 42 rooted expansions of this quotient nevertheless have one at 26. The quotient obstruction here also follows from the [numerical semigroup criterion](prime-neutral.md), since $11-2=9=5+2+2$.

The generator records every quotient shape. Its backtracking assigns the nonroot internal vertices first. The difference between the sum of the free edge weights and the sum of the free vertex residues equals $\sum_{v\ne r}c_v f(v)$ modulo $k$, where $c_v$ is the number of children. This must vanish. Sibling leaves may be assigned increasing labels. Exhausting the search certifies failures only on the small quotients. The larger direct searches need only produce verifiable witnesses.

The separate verifier reads the original parent lists, checks the root-zero vertex and edge permutations, and tests the lift on actual expansion edges. For each indicated quotient exception it independently tries every injection on its internal vertices, then assigns the remaining labels to leaf-parent shifts with their prescribed multiplicities. It constructs all required exceptional expansions recursively by distributing child shapes over both ends of the paired vertex. Their isomorphism types must agree exactly with the direct witness records.

Completeness of the quotient catalog follows by canonicalizing each unordered rooted tree, rejecting repeats, and comparing the total to the rooted-tree multiset count. There is also a count directly on the expanded trees. A tree has at most one perfect matching since the symmetric difference of two would contain a cycle. The root is specified, so any perfect matching of the forest after root deletion is unique. For a paired vertex with its incoming endpoint specified, each endpoint supports an unordered forest of paired child branches. If $B(x)$ counts such paired branches by pairs and $R(x)$ counts unordered forests of them, then
$$
B(x)=xR(x)^2,\qquad R(x)=\prod_{i\ge1}(1-x^i)^{-[x^i]B(x)}.
$$
The desired tree consists of the singleton root and such a forest. The verifier compares $[x^m]R(x)$ with an independent sum over quotient shapes. For a child shape occurring $d$ times with $b$ possible paired expansions, the factor is $\binom{2b+d-1}{d}$ at a paired parent and $\binom{b+d-1}{d}$ at the singleton root.

## Reproduction

From the repository root, run in Bash with C++17 and Python 3.9 or later. The generated text streams contain all quotient permutations and all direct witnesses. [Generator](matching_surplus.cpp) · [Independent verifier](check_matching_surplus.py) · [SHA-256 manifest](matching-surplus.sha256)

~~~bash
set -e
src="$PWD/research/census"
out=$(mktemp -d)
c++ -O3 -std=c++17 "$src/matching_surplus.cpp" -o "$out/generate"
for m in 3 5 7 9 11 13 15; do
    "$out/generate" "$m" > "$out/match-$m.txt"
    python3 -B -m research.census.check_matching_surplus "$m" "$out/match-$m.txt"
done
(cd "$out" && shasum -a 256 -c "$src/matching-surplus.sha256")
~~~
