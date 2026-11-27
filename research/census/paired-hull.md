# Pairing exposed arms at both parities of the tree order

Let $T$ be a smallest 26-label counterexample among trees of matching deficiency at most any fixed bound. Let $d$ be its actual deficiency and $n$ its order. Then
$$
 n\le \begin{cases}38d-26,&n\text{ even},\\38d-15,&n\text{ odd}.\end{cases}
$$
These restrictions also apply under unrestricted minimality. For example a smallest counterexample at the current upper bound of 546 vertices would require every matching to miss at least 16 vertices.

## Uniform joins at every pair of boundary labels

Consider two terminal components with twelve matched pairs in total and one exposed tip each, as in the [four-exposure theorem](four-exposures.md#attaching-two-terminal-pieces-to-a-prescribed-core). If one through five of the pairs hang off their terminal chains, the pieces can be joined at **any two vertices of any labeled core** while increasing every vertex and edge count by exactly one. The core need not be cordial for this identity.

Close the pieces into a ring with one temporary matching edge across the tips and one closing edge across the ports. For each eligible temporary edge and each different closing edge, the new certificates realize all four unit orbits of the difference of the old parent labels, using the uniform-increment joining identity. The [generator](ring_ports.cpp) and [separate verifier](check_ring_ports.cpp) use the neutral mode. The verifier checks the two permutations on the ring and tests the actual missing weights and endpoint labels. Multiplying the ring labels by a unit and translating gives the required original join. The [Lean identities](TwoPortJoin.lean) verify the shifts and histogram change. The [ring census](branched-rings.md) certifies the shape set independently.

| Side pairs | Rings | Rings with an eligible edge | Bijections | Edge choices with parent orbit |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 4,160 | 4,158 | 170,268 | 1,746,000 |
| 2 | 28,091 | 28,069 | 1,083,565 | 9,898,556 |
| 3 | 127,725 | 127,573 | 4,580,557 | 37,044,304 |
| 4 | 443,944 | 442,973 | 14,594,539 | 104,019,004 |
| 5 | 1,241,271 | 1,235,863 | 36,656,939 | 228,748,800 |

## Pairing the paths

Work in the quotient of a maximum matching with its $d$ exposures at leaves. Let $r$ be the number of branching sites in the subtree spanning them, and $h$ the number of pairs outside that subtree. We have $r\le d-2$, $h\le12$ at divisible orders and $h\le11$ at every nondivisible order. Residue one is impossible. These are consequences of [pruning whole pairs and possibly one leaf](exposure-bounds.md#paths-between-uncovered-leaves).

Set $u=d\bmod2$. Pair the terminal arms in any way, leaving one ordinary terminal arm when $u=1$. In each paired group add one temporary matching edge between its singleton tips. The list runs along one chain, through this temporary pair, and back along the other chain. Its two branching sites may coincide. For the remaining single arm exclude its exposed tip. Add a separate list for the interior of each connector between branching sites. In all there are
$$
 N=(d+u)/2+r-1
$$
lists. Write $P$ for their total number of positions before adding side pairs. The branching sites, lists and side pairs together account for $n=2(P+r+h)+u$ original vertices.

Divide each list into disjoint runs of 13 consecutive positions with a remainder of at most twelve. The fourteen prefix masses in a run give a window of mass 13 as in the earlier proof. A window avoiding temporary edges is reducible with at most six side pairs. If it includes a temporary edge, its removal leaves a connected smaller core with at most $d-2$ exposures. At divisible orders the [two-site certificates](four-exposures.md) restore the window with zero through six side pairs. At other orders one through five side pairs work by the uniform joins above. With zero side pairs use the [unbranched theorem](three-exposures.md#two-arms-on-a-prescribed-core). Its condition on a nonuniform core edge histogram holds because the original order is not one modulo 26 and removal preserves its order residue.

At a divisible order every run therefore needs at least seven side pairs, and $h\le12$. At a nondivisible order it needs at least six and $h\le11$. In both cases at most one complete run occurs across all lists, giving $P\le12N+13$. Substitution in $n=2(P+r+h)+u$ and $r\le d-2$ proves the two stated bounds. [Lean arithmetic](ExposureHull.lean)

## Reproduction

Run in Bash from the repository root. The two manifests cover the five files. The sampling check builds 248 entire trees on path cores with both uniform and nonuniform edge histograms, preserving the increments separately at every residue.

~~~bash
set -euo pipefail
src="$PWD/research/census"
out=$(mktemp -d)
c++ -O3 -std=c++17 "$src/ring_ports.cpp" -o "$out/ports"
c++ -O3 -std=c++17 "$src/check_ring_ports.cpp" -o "$out/check"
for b in {1..5}; do
    python3 -B "$src/branched_rings.py" 13 "$b" "$out/input"
    "$out/ports" --neutral < "$out/input" > "$out/allneutral$b"
    "$out/check" "$out/input" "$out/allneutral$b" --neutral
done
(cd "$out" && shasum -a 256 -c "$src/exposure-bounds.sha256" && shasum -a 256 -c "$src/paired-hull.sha256")
python3 -B -m research.census.check_exposure_bounds --directory "$out" --sides 5
lean "$src/TwoPortJoin.lean"
lean "$src/ExposureHull.lean"
~~~
