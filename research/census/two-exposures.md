# Every tree with a matching missing at most two vertices is 26-cordial

**Theorem.** Let $T$ be any finite tree. If some matching of $T$ covers all but at most two vertices, then $T$ has a 26-cordial labeling. There is no restriction on order, degree, or the distance between the uncovered vertices. In particular, every even-order 26-label counterexample would have matching deficiency at least four. The unrestricted conjecture remains open.

The [near-perfect theorem](../near-matching.md) settles deficiency zero and one, as well as deficiency two at orders not divisible by 26. The [branched block reduction](branched-rings.md) shows that a least counterexample in this class would have order 52. Here we construct the labeling at that order.

## Two full blocks

Use the circular partition from the reduction. The total number of off-path pairs is at most 12. Each of the two blocks has 13 pairs. Call the block containing the temporary edge between the two exposures $C$, and the other block $B$. If $B$ has at most six off-path pairs, the [branched and unbranched substitutions](branched-rings.md) already settle the tree, including the pure-subdivision case by a divisible cut. Hence suppose $B$ has at least seven off-path pairs. Then $C$ has some number $b\le5$ of off-path pairs.

Keep $B$ as an ordinary tree on 26 vertices. Close $C$ into its own ring by joining its two boundary sites. The temporary matching edge lies on the cycle, since one of its ends is on each side of the path between the original exposures. The closing edge and the temporary edge are distinct. Deleting both gives the two components which actually attach to $B$, one at each closing-edge endpoint.

If $b>0$, there are at most eleven off-path pairs in $B$. At least two central pairs remain, so its two attachment sites lie in different pairs. Contract all pairs of $B$. The resulting 13-vertex tree has a bijective 13-cordial labeling. The [matching lift](../matching-expansion.md) gives $B$ a bijective 26-cordial labeling in which vertices from different pairs have different residues modulo 13. Thus its two parent labels $p,q$ satisfy $p-q\not\equiv0\pmod{13}$. For $b=0$ we only require a bijective cordial labeling of $B$ and impose no condition on its parents, which may be the same vertex.

## Joining at two labeled parents

Take any forest on 26 vertices with two rooted components. Suppose its labels biject onto the residues and its 24 internal edge weights are distinct. Let $a,b'$ be the two root labels and $u,v$ the two missing weights. Multiplying the forest labels by a unit $s$ modulo 26 and then adding $t$ moves the missing weights to $su+2t,sv+2t$. The new bridges have weights $p+sa+t,q+sb'+t$.

There are two sufficient constructions. All equations below are modulo 26.

1. If $p-q=s(u-v-a+b')$, take $t=p+s(a-u)$. The bridges supply the two missing weights. Interchanging $u,v$ is also allowed. The forest then adds one to every vertex and edge bin.
2. If the old core has divisible order and deficient edge weight $D$, it suffices that $p+q-D=s(v-a-b')$. Take $t=D-p-sa$. The first bridge fills the old deficit and the second supplies the translated hole $sv+2t$. The only final deficit is at the other translated hole. Either of $u,v$ may be used as $v$.

Both conclusions follow by substitution, including coincidences between an old and a new deficit. There are four unit orbits in the additive group, distinguished by the gcd with 26. [Lean checks the two congruences at any modulus and the per-residue histogram accounting](TwoPortJoin.lean).

### Blocks with one to five off-path pairs

Start from a harmonious bijection of the closed ring of $C$. Write $w$ for the weight of the temporary edge, and $a,b'$ for the labels of the closing edge. On deleting both edges the missing weights are $w,a+b'$. In construction 1 the two possible right-hand differences before scaling become $w-2a$ and $2b'-w$. It is enough that one belongs to the unit orbit of $p-q$. Here the two possible orbits have representatives 1 and 2.

The certificate supplies this condition for **every** cycle edge belonging to a perfect matching, **every other** cycle edge as the closure, and **both** representatives. The eligible temporary edge thus includes the actual one, regardless of which perfect matching was chosen on the closed block. Bijections may differ between choices.

| Off-path pairs | All rings | Rings with an eligible edge | Checked bijections | Edge choices including both parent orbits |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 4,160 | 4,158 | 17,048 | 873,000 |
| 2 | 28,091 | 28,069 | 110,857 | 4,949,278 |
| 3 | 127,725 | 127,573 | 484,382 | 18,522,152 |
| 4 | 443,944 | 442,973 | 1,615,515 | 52,009,502 |
| 5 | 1,241,271 | 1,235,863 | 4,301,493 | 114,374,400 |

The [ring generator](ring_ports.cpp) retains bijections covering new cases. A separate [verifier](check_ring_ports.cpp) decides edge eligibility by deleting its endpoints and greedily matching leaves of the remaining forest. It checks every vertex and edge residue and tries both assignments of the two holes for the actual boundary sites. Coverage of the underlying catalog is certified by the [independent bracelet count](branched-rings.md#independent-orbit-count). In total the verifier checks 190,728,332 combinations.

### Blocks with zero off-path pairs

Deleting the two edges now gives two arms. Each starts at its boundary site, runs through a chain of matched pairs and ends at one of the original exposed vertices. An arm with no pairs consists of the exposed vertex alone. There are twelve ordinary pairs in total. Exchange the arms to give the first between zero and six pairs. The incoming and outgoing sites of each pair either agree or differ, and exchanging its two vertices removes any other port choice. This gives $7\cdot 2^{12}=28{,}672$ ordered descriptions, allowing repetitions under arm exchange.

For each description the [arm search](paired_arms.cpp) gives one or more forest bijections with 24 distinct internal weights. For each bijection the checker expands the two possible differences in construction 1 under all units, and does the same for the two expressions in construction 2. For every description either the first union covers all 26 parent differences or the second covers all 26 values of $p+q-D$. Thus the arms attach to **any fixed cordial core of divisible order**, at any two sites. This includes coinciding parents. The checker accepts 122,523 bijections and performs a literal join with independently chosen parents and deficit in every one of the 28,672 descriptions.

All cases at order 52 are now covered. Together with the least-counterexample reduction, this proves the all-orders theorem. The [whole-tree checker](check_paired_joins.py) also reconstructs and labels 1,020 full trees on 52 vertices, checking all 51 original edge sums in each.

## Reproduction

Run in Bash from the repository root. The earlier [branched catalog replay](branched-rings.md#reproduction) provides the separate checks on the underlying shapes and on the ordinary block substitution.

~~~bash
set -euo pipefail
src="$PWD/research/census"
lean "$src/TwoPortJoin.lean"
out=$(mktemp -d)
c++ -O3 -std=c++17 "$src/paired_arms.cpp" -o "$out/arms"
c++ -O3 -std=c++17 "$src/ring_ports.cpp" -o "$out/ports"
c++ -O3 -std=c++17 "$src/check_ring_ports.cpp" -o "$out/check"
"$out/arms" > "$out/arms.out"
for b in {1..5}; do
    python3 -B "$src/branched_rings.py" 13 "$b" "$out/input"
    "$out/ports" < "$out/input" > "$out/socket$b.txt"
    "$out/check" "$out/input" "$out/socket$b.txt"
done
python3 -B -m research.census.check_paired_joins "$out"
(cd "$out" && shasum -a 256 -c "$src/paired-joins.sha256")
~~~
