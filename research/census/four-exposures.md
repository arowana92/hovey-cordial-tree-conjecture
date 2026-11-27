# Three candidate orders for matching deficiency four at 26 labels

**Theorem.** If a finite tree of matching deficiency at most four fails to be 26-cordial, a smallest such tree has order 52, 78 or 104 and deficiency exactly four. At order 104 the subtree joining the four uncovered leaves in the matching quotient must have two distinct branching vertices, and at least seven matched pairs must lie outside that subtree. The theorem reduces this class to three orders. Cordiality at those orders for the entire class remains open.

## Attaching two terminal pieces to a prescribed core

Let the core have order divisible by 26 and fix any cordial labeling of it. At two chosen sites attach disjoint pieces, each consisting of a terminal exposed vertex and a chain of matched pairs leading to it. Each chain may be empty. Attach further paired trees to the chains. Suppose the two pieces together have 12 matched pairs, of which at most six are outside the chains. Then the labeling extends at **any** two sites, including the same vertex.

When there are no side pairs this is the [two-arm theorem](two-exposures.md#blocks-with-zero-off-path-pairs). Otherwise join the exposed vertices by a temporary matching edge and join the two attachment sites **inside the pieces** by a closing edge. The cycle and its decorations are among the [independently counted rings](branched-rings.md#independent-orbit-count) with 13 pairs and $b$ side pairs, $1\le b\le6$. This also works for a one-vertex piece. The temporary edge and closing edge are distinct because at least six ordinary chain pairs remain.

Fix the temporary edge and closing edge. Let $w$ be the former's weight and $a,b'$ the latter's endpoint labels in a bijection with every cycle and pendant edge weight distinct. Deleting the edges leaves the two holes $w,a+b'$. For old parent labels $p,q$ and unique old deficient weight $D$, the [affine joining identities](TwoPortJoin.lean) give two ways to attach. If $p-q$ is a unit multiple of $w-2a$ or $2b'-w$, both bridges fill holes in the pieces. If $p+q-D$ is a unit multiple of $w-a-b'$ or is zero, one bridge fills the old deficit and the other fills a hole in the pieces. The remaining deficit is a single residue in either case. Both constructions use every free vertex residue once.

For every ring and every ordered choice of the two different cycle edges for which the first belongs to a perfect matching, the verifier covers **all 16 combinations** of the unit orbits of $p-q$ and $p+q-D$. The four orbits have representatives 0, 1, 2 and 13. The [search](ring_ports.cpp) stores explicit permutations. The [verifier](check_ring_ports.cpp) reconstructs the graph, checks the two bijections, tests temporary-edge eligibility by greedy matching in a forest, and expands unit multiples of both assignments of the missing weights. The [whole-tree test](check_paired_joins.py) samples connected 52-vertex joins with identical, antipodal and other boundary labels.

| Side pairs | All rings | Rings with an eligible edge | Checked bijections | Edge choices with both orbit assignments |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 4,160 | 4,158 | 126,191 | 6,984,000 |
| 2 | 28,091 | 28,069 | 812,003 | 39,594,224 |
| 3 | 127,725 | 127,573 | 3,477,305 | 148,177,216 |
| 4 | 443,944 | 442,973 | 11,275,556 | 416,076,016 |
| 5 | 1,241,271 | 1,235,863 | 28,934,459 | 914,995,200 |
| 6 | 2,877,385 | 2,853,377 | 60,360,139 | 1,618,624,784 |

The verifier accepted 104,985,653 explicit bijections covering 3,144,451,440 choices. The whole-tree replay checked all 51 edge sums and connectivity on 1,608 attached trees.

## The four uncovered leaves

Choose a smallest counterexample within the class. The [three-exposure theorem](three-exposures.md) forces deficiency four. Put its order equal to $n$. The [prefix matching bound](../near-matching.md) already works unless $(n+4)/2$ is 1, 2 or 3 modulo 13, so $n$ is $-2,0$ or $2$ modulo 26. The three-exposure theorem also covers deficiency four at order $-2$. At order $2$, arrange that all four exposed vertices are leaves and delete two. The resulting divisible tree has deficiency at most two. Restore the first leaf by filling the unique edge deficit, then give the second leaf any vertex label different from the first. This balances both histograms. Hence $n=26q$ with $q\ge2$ by the order-26 base.

Contract each matched pair, keeping the four exposed leaves as singletons. Their minimal connecting subtree has either one degree-four vertex or two degree-three vertices. Call these its branching vertices. Every nonleaf vertex in this subtree is a contracted pair. Let $s$ be the number of pairs outside it. If $s\ge13$, prune 13 outside pairs in child-before-parent order. The remaining tree has a smaller divisible order and a matching missing at most four. The [matched forest theorem](../paired-forest.md) restores the deleted pairs. Thus $s\le12$.

At each of two branching vertices group its two terminal arms together. For a single branching vertex group its four arms into any two pairs. Join the exposed leaves of each group by a temporary matching edge, adding two pairs to the list. Each group now gives a linear list of pair positions running out along one arm, across its temporary pair, and back along the other arm. The branching vertices are excluded from these lists. With two branching vertices include a third list consisting of the interior pairs of their connector. At every position, including the branching vertices, add its entire outside forest to its mass. Thus the mass is one plus the number of outside pairs there. The total is $13q$.

Arrange the positions on a circle in the order *first arm group, first branching vertex, connector interior, second branching vertex, second arm group*. With one branching vertex the order is *first group, branching vertex, second group*. Mark the boundary from the end of the second arm group to the start of the first. Exactly $s<13$ integer boundaries lie strictly inside positions. Choose a residue modulo 13 containing none of them. Cutting at all boundaries of that residue divides the circle into $q$ blocks of mass 13. At most three blocks contain a branching vertex or cross the marked boundary, at most two in the single-branching-vertex case.

Every other block lies in a single list. If it contains a temporary edge and at most six outside pairs, removing the block leaves a connected divisible core with two exposed vertices. The two-piece extension above restores it. If it avoids the temporary edges and has at most six outside pairs, suppress it and use the [two-ended substitution](branched-rings.md). In the exceptional pure-path case the 26 consecutive degree-two vertices give an edge cut with divisible order on one side. The cut splits the four exposures as $1+3$ along an arm or $2+2$ along the connector. At most one endpoint per side loses its mate, so both smaller trees stay in the class. The [divisible-cut theorem](../divisible-cuts.md) rejoins them.

Consequently every block outside the marked boundary and branching vertices consumes at least seven outside pairs. Since $s\le12$, there is at most one such block. This proves $q\le4$, with $q\le3$ when the four arms share one branching vertex. If $q=4$, at least one block requires seven outside pairs.

## Reproduction

Run in Bash from the repository root. The [original catalog replay](branched-rings.md#reproduction) verifies its members against an independent orbit count. The manifest below pins the additional witness streams. No search failure is used as an obstruction.

~~~bash
set -euo pipefail
src="$PWD/research/census"
out=$(mktemp -d)
c++ -O3 -std=c++17 "$src/ring_ports.cpp" -o "$out/ports"
c++ -O3 -std=c++17 "$src/check_ring_ports.cpp" -o "$out/check"
for b in {1..6}; do
    python3 -B "$src/branched_rings.py" 13 "$b" "$out/input"
    "$out/ports" --divisible < "$out/input" > "$out/diverse$b"
    "$out/check" "$out/input" "$out/diverse$b" --divisible
done
lean "$src/TwoPortJoin.lean"
python3 -B -m research.census.check_paired_joins "$out" --divisible
(cd "$out" && shasum -a 256 -c "$src/four-exposures.sha256")
~~~
