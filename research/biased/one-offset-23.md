# A prescribed edge offset on every tree through order 23 modulo 27

**Theorem (computer-assisted).** In any tree on at most 23 vertices, mark any edge and add any prescribed residue modulo 27 to its endpoint sum. There is a labeling with distinct vertex labels and distinct edge weights, including the shifted weight. Thus it is cordial with the given offset.

**Order-50 consequence.** Every 50-vertex tree with two edges whose removal leaves a middle component of exactly 27 vertices is 27-cordial. Equivalently, it suffices that two disjoint sides totaling 23 vertices can be removed along single edges with connected remainder. This criterion permits arbitrary branching in all three components. More generally, a least counterexample of order $27m+23$ with $m\ge1$ cannot have two disjoint edge sides totaling 23. Their middle component has order $27m$ and is cordial by minimality, so the same expansion applies. The [order-50 proof](../census/order-fifty.md) uses it to exclude complementary subtree sizes in different centroid branches.

To prove the finite theorem at 23 vertices, start with any injective rainbow labeling $f$. Let $w$ be the weight of a marked edge and let $z$ be a missing weight. Multiplying the labels by a unit $u$ permits offset $u(z-w)$ on the mark, since its new weight becomes $uz$. For every unrooted shape, the [certificate](one-offset-23.sha256) gives a family attaining all three nonzero unit orbits at **every** marked edge. Zero works from any row. Pad smaller trees by leaves or a path to order 23 and restrict. The result concerns one arbitrary offset on an arbitrary tree. The [sparse-offset path theorem](sparse-path-offsets.md) handles two offsets in each block on paths of any order.

For the consequence, let $P$ be the middle component. Give it a 27-residue bijection with distinct edge sums by the [integer census](../census/README.md). Write $h$ for its missing weight and $p,r$ for the labels of its two ports, which may coincide. Replace $P$ by an edge of offset $p+r-h$ between its two old neighbors. The remaining tree has order 23 and the finite theorem labels it. If the two neighbors receive $a,b$, translate the labels of $P$ by $d=a+p-h$. Its internal deficit moves to $h+2d$ and the entering edge has exactly that weight. The other joining edge has weight $b+r+d=a+b+p+r-h$, as required. Each vertex and edge bin gains one on expansion. More generally, an arbitrary chain of cordially labeled pieces of order divisible by 27 can replace one edge of any tree through order 23. Their effective offsets add along the chain.

The extended census proves the same one-edge theorem through order 25, including the two-cut exclusion at every order congruent to 24 or 25 modulo 27. [Order-25 theorem](one-offset-25.md)

## Verification

The [generator](../rainbow/common_site_generate.cpp) lists all **14,828,074** unrooted trees of order 23 at their unique centroids. In edge mode it emitted **97,374,096** witness rows. There are **8,807,875,956** inputs when counting every marked edge position and every offset before symmetry. The [independent verifier](../rainbow/common_site_verify.cpp) checks the canonical tree and rank, then recomputes every vertex label and edge weight. It multiplies each difference from the marked weight to an unused weight by every unit and requires all literal offsets to be covered. Negation is a unit, so either orientation of the differences gives the same orbits. A separate recurrence recovers the total unrooted count.

The [whole-tree check](../rainbow/check_common_site.py) inserts an ordinary 27-vertex path at each marked edge. It chooses the exit port to realize each offset, then checks the two complete histograms before and after expansion. Four sampled trees give 2,376 such joins. The 128 stream hashes accompany the proof.

~~~bash
set -euo pipefail
out=$(mktemp -d)
r=research/rainbow
c++ -O3 -std=c++17 "$r/common_site_generate.cpp" -o "$out/generate"
c++ -O3 -std=c++17 "$r/common_site_verify.cpp" -o "$out/verify"
python3 -B -m research.rainbow.check_common_site 23 --edge --manifest research/biased/one-offset-23.sha256
python3 -B -m research.rainbow.check_common_site 23 --edge --run "$out/shards" --generator "$out/generate" --verifier "$out/verify" --workers 2
cmp "$out/shards/manifest.txt" research/biased/one-offset-23.sha256
"$out/generate" 23 0 1024 --edge > "$out/sample"
python3 -B -m research.rainbow.check_common_site 23 --edge --replay "$out/sample"
~~~
