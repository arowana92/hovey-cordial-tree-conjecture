# Bounding 26-label counterexamples by their matching deficiency

**Theorem.** Take a smallest 26-label counterexample among trees of matching deficiency at most a fixed bound, assuming one exists. Write $n$ for its order and $d$ for its actual deficiency. Then $n\le51d-26$. In particular the bound applies to a smallest unrestricted counterexample. A sharper restriction holds one step beyond the [known positive range](three-exposures.md). At $n=26q-H$, the following are the only possible orders when $d=H+4$.

| $H$ | Uncovered vertices $d$ | Candidate orders |
| ---: | ---: | --- |
| 0 | 4 | 52, 78, 104 |
| 1 | 5 | 51, 77, 103 |
| 2 | 6 | 50, 76 |
| 3 | 7 | 49 |
| 4 | 8 | 48 |
| 5 | 9 | 47 |

Moreover $d\ge2H+2$ whenever $q\ge3$ and $1\le H\le13$. For example, at orders 73, 99 and every higher order congruent to 21 modulo 26, a smallest counterexample would require **at least thirteen uncovered vertices** in every matching. The parity of $n$ strengthens the lower bound there. Counting the edges with more than $H$ tips on each side gives additional [order bounds for each deficiency](exposure-splits.md). The entries in the table are necessary conditions. No tree at those orders has been shown to fail.

A finite test for the entire class of deficiency at most five now consists of the six orders in the first two rows. Indeed, the [matching-prefix theorem](../near-matching.md) for $d=5$ only leaves orders $-3,-1,1,3$ modulo 26. The [three-exposure theorem](three-exposures.md) also treats $-3$. At residues 1 and 3 remove that many exposed leaves to obtain a smaller divisible tree in the class. Fill its old deficit with the first leaf, then [restore the other leaves](../counterexample-bound.md#removing-leaves) with distinct weights and distinct labels avoiding the first. The first row is the [four-exposure theorem](four-exposures.md).

## Paths between uncovered leaves

Choose a maximum matching with all $d$ exposures at original leaves, and contract its pairs. The minimal subtree spanning the exposures has $r\le d-2$ branching vertices, called its branching sites. The other pair positions on this subtree lie on $d$ terminal arms and $r-1$ connecting paths between sites. Arm lengths and connector lengths below count **pair positions**, omitting the sites and exposed leaves. Write $h$ for all pairs outside this subtree. At each position include its outside branches in its mass, so its mass is one plus the number of side pairs attached there.

Use $s\in\{1,\ldots,26\}$ for the representative of $n$ modulo 26. Then $h<\lfloor s/2\rfloor$. Otherwise prune $\lfloor s/2\rfloor$ outside pairs in child-before-parent order, also removing one exposed leaf when $s$ is odd. The retained core has positive divisible order, since $n>26$, and stays in the class. The pruned forest has at most 13 pairs after giving its possible single exposure a temporary mate. The [forest extension](three-exposures.md#deleting-temporary-mates-from-a-forest) restores it. In particular $h\le12$.

In any run of 13 consecutive positions on one arm or connector, the 14 prefix masses run from zero to at most 25. Two agree modulo 13 and their difference is exactly 13. The intervening full subtree can be suppressed if it has at most six side pairs, using the [branched ring theorem](branched-rings.md). For a pure traversed path the successive cuts include one with divisible order on one side. Each side contains at least one exposure, and even a cut through a mate leaves each side with at most $d$ exposures. Both smaller trees belong to the class and the [divisible-cut theorem](../divisible-cuts.md) joins them. Thus each disjoint group of 13 positions requires seven side pairs. There is room for at most one such group across all $d+r-1$ lists. The total number of positions on those lists is at most $12(d+r-1)+13$. Adding $r$ sites, $h$ outside pairs and the singleton exposures gives
$$
 n\le d+2[12(d+r-1)+13+r+h]\le51d-26 .
$$
At divisible orders, pairing terminal arms as in the [four-exposure construction](four-exposures.md) gives $d/2+r-1$ lists. Each pair of arms includes one extra temporary pair. The same group bound applies within these lists, including a block through a temporary pair by the two-piece theorem. Here $n/2$ counts all ordinary and temporary pairs, so $n\le12d+26r+26$.

## Discarding a chosen set of tips

Take $1\le H\le13$ and $n=26q-H$. In a minimum counterexample $d\ge H+4$ by the earlier deficiency bound. Keep any $d-H$ exposed leaves and their connecting subtree in the quotient. At most $12-H$ pairs can lie outside that subtree. Otherwise grow the connected core through ordinary pairs, without taking the other $H$ exposed leaves, until exactly $13-H$ pairs are outside. The exterior then has $13-H$ pairs and $H$ unpaired vertices. Completing its matching gives 13 pairs, while the retained core has order $26(q-1)$ and stays in the class. The forest theorem applies as before. For $H=13$ the same construction needs zero exterior pairs and rules out such a minimum directly.

It follows that $h\le12-H$, and there are at most $C=12-H-h$ **on-subtree** pair positions which can be discarded by removing any chosen $H$ exposure leaves from the spanning requirement. It suffices to choose at most $H$ leaves since the set can be enlarged. In particular the sum of the lengths of any $H$ terminal arms is at most $C$.

If $d\le2H+1$, take a centroid for the weight which assigns one unit to each exposure. Moving toward a component containing over half the weight finds such a vertex. The centroid is a pair position and every incident branch of the spanning subtree contains at most $H$ tips. Group the branches into at most three collections with at most $H$ tips in each. To see this, merge any two groups whose total is at most $H$. Four surviving groups would have total at least $2H+2$ by taking two disjoint pairs. All positions in a group can be discarded by removing its tips. Thus the number of matched pairs satisfies $\nu\le3C+1+h$, with one extra position for the centroid. Since $n=2\nu+d$, this gives $q\le2$. This proves the general lower bound on $d$ for $q\ge3$ and the last three table rows after the small-order census.

## Six exposures at order two short of a multiple

Here $C=10-h$. If no hull edge splits the six tips evenly, at a weighted centroid each branch has one or two tips. Pack the six tips into three groups of size two, keeping each incident branch whole. This gives $\nu\le3C+1+h$.

Otherwise all edges with a $3+3$ split form one connecting path between two branching sites. Indeed a third direction containing a tip at an internal vertex would prevent both adjacent edges from splitting evenly. At each end, the three outward tips lie in groups of sizes $1+2$ or $1+1+1$. Reserve one singleton branch from each end. The two reserved branches together can be discarded using their two tips. All other outward branches on the left form a second discardable group and their counterparts on the right form a third. This accounts for every hull position except the two end sites and their connector interior. A connector has at most $12+13\lfloor h/7\rfloor$ positions by the run argument. Consequently
$$
 \nu\le3(10-h)+2+12+13\lfloor h/7\rfloor+h\le44 .
$$
Since $n=2\nu+6=26q-2$, this requires $q\le3$.

## Five exposures at order one short of a multiple

Every arm has length at most $11-h$. Its full mass is therefore at most 11. Take two arms of lengths $a_i,a_j$, with $c_i,c_j$ side pairs at positions along them. Their tip prefixes have attainable masses between zero and $A_i=a_i+c_i$ and $A_j=a_j+c_j$, with exactly $c_i,c_j$ omitted integers respectively. If $a_i+a_j\ge12$, there are $A_i+A_j-11>c_i+c_j$ candidate splits of 12. A feasible split removes the two tips and exactly 12 pairs, and leaves a smaller connected core of the same order residue with a matching missing at most three.

For $c_i+c_j\le2$ the two removed pieces attach to **any prescribed** cordial core of this residue. With zero side pairs use the [arbitrary-parent arm theorem](three-exposures.md#two-arms-on-a-prescribed-core), since the core's edge histogram is nonuniform. With one or two side pairs, the new certificate supplies uniformly one of every vertex and edge weight for every pair of parent labels, even when the parents coincide. This last construction works for a core of any order. Given the two distinguished cycle edges of the closed block, its checked permutations cover each of the four unit orbits of the parent difference using the first [affine joining identity](TwoPortJoin.lean). The [independent verifier](check_ring_ports.cpp) accepts 170,268 and 1,083,565 permutations in the two catalogs. It checks 1,746,000 and 9,898,556 choices of edges and parent orbit, respectively.

Each of at most two connectors splits the five exposures as two and three. Look at the side with two tips. Every boundary along the connector, including each end, cuts off $2+2P$ vertices for some $P$. Successive values of $P$ increase by the mass of the next position. Thus its prefix masses avoid one whole residue modulo 13, by the divisible-cut theorem. In 12 consecutive positions the 13 boundaries occupy at most 12 residues. The positive repeated-residue difference is 13 because the mass is at most $12+h\le23$. As before this window requires at least seven side pairs. A connector with at most six side pairs has at most 11 positions, and every connector here has at most 23.

With exactly seven side pairs a connector has at most 17 positions. If it had 18 or more, its first and last 12 positions would both contain all seven side pairs. All seven would then occur in at most six consecutive positions. These positions have mass at most 13, so all omitted prefix integers lie strictly within an interval of length at most 13. Yet the full mass is at least 25. The integers from zero through that mass include two members of the forbidden residue 13 apart, both of which must be omitted. This is impossible.

The [arithmetic checker](check_exposure_bounds.py) enumerates the five arm lengths with $a_i\le11-h$ and every allocation of at most $h$ side pairs among them. It rejects $a_i+a_j\ge12$ whenever $c_i+c_j\le2$. Its independent connector calculation keeps the last 13 unit boundaries and rejects a mass-13 interval containing at least seven positions. The following bounds add the arm lengths, connector lengths, at most three branching sites and $h$ outside pairs.

| Outside pairs $h$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Maximum sum of the five arm lengths | 26 | 26 | 26 | 29 | 28 | 28 | 25 | 20 | 15 | 10 | 5 | 0 |
| Upper bound on matching size | 51 | 52 | 53 | 57 | 57 | 58 | 56 | 58 | 60 | 56 | 52 | 48 |

Order $26q-1$ with $q\ge5$ would require at least 62 matched pairs. This proves the second table row.

## Reproduction

Run from the repository root in Bash. The [underlying ring catalog](branched-rings.md#reproduction) has an independent isomorphism count. The Lean file verifies the order inequalities, and the integer checker directly checks a pair of boundaries at distance 13 in all 5,200,300 thirteen-position mass profiles with at most twelve extra units. It also rebuilds 116 complete joins on cores of four different orders and checks that every vertex and edge count increases by one.

~~~bash
set -euo pipefail
src="$PWD/research/census"
out=$(mktemp -d)
c++ -O3 -std=c++17 "$src/ring_ports.cpp" -o "$out/ports"
c++ -O3 -std=c++17 "$src/check_ring_ports.cpp" -o "$out/check"
for b in 1 2; do
    python3 -B "$src/branched_rings.py" 13 "$b" "$out/input"
    "$out/ports" --neutral < "$out/input" > "$out/allneutral$b"
    "$out/check" "$out/input" "$out/allneutral$b" --neutral
done
(cd "$out" && shasum -a 256 -c "$src/exposure-bounds.sha256")
python3 -B -m research.census.check_exposure_bounds --directory "$out"
lean "$src/ExposureHull.lean"
~~~
