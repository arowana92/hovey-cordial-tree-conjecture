# Independently attached paths and order bounds at 26 and 27 labels

**Theorem (computer-assisted).** If a counterexample exists at 26 labels, one of least order has **49 through 208 vertices**. At 27 labels the corresponding interval is **50 through 243 vertices**. At both 26 and 27 labels, any five paths attached by their endpoints at arbitrary vertices of a prescribed cordial core of order zero or one modulo $k$ can grow in any prescribed interleaving. One labeling works on every prefix. At 26 labels this also holds for six independently attached paths.

Write the minimum order as $km+s$, $1\le s\le k$. The possible order lies in the interval in the corresponding cell and is congruent to its column heading modulo $k$.

| $k$ | $s=23$ | $s=24$ | $s=25$ | $s=26$ | $s=27$ |
|---:|---:|---:|---:|---:|---:|
| 26 | 49–153 | 50–180 | 51–181 | 52–208 | |
| 27 | 50–158 | 51–159 | 52–187 | 53–215 | 54–243 |

The lower endpoints and residue exclusions follow from the [21-vertex extension](../rainbow/twenty-one-free.md). The maxima are upper bounds from necessary conditions. For 26 the previous ceiling was [286 vertices](pendant-order.md). At 27 the one-side-leaf replacement reduces the previous ceiling of 351. [Edge replacements for all old frequency profiles](one-leaf-period.md)

## Terminal paths with independently prescribed parents

On a core of order one modulo $k$, translate the sole surplus vertex residue to zero. For every partition of $k-1$ into the certified number of positive path lengths, the certificate works for every tuple of parent labels. A witness uses every nonzero residue once on the paths and gives $k-1$ distinct sums including the entering edges. Every parent-first prefix uses a subset of these vertices and a subset of these edges. Consequently both frequency distributions stay balanced. Pad a last short batch at a tip and restrict. From order zero modulo $k$, give the next vertex the unique label filling the deficient weight, then start another batch. A path that continues through this boundary uses its present endpoint as its next parent.

| Modulus | Paths | Length lists | Witnesses | Ordered parent tuples across all lists |
|---:|---:|---:|---:|---:|
| 26 | 5 | 192 | 1,816,020 | 2,281,224,192 |
| 26 | 6 | 235 | 10,727,429 | 72,595,207,360 |
| 27 | 1 | 1 | 3 | 27 |
| 27 | 2 | 13 | 281 | 9,477 |
| 27 | 3 | 56 | 10,376 | 1,102,248 |
| 27 | 4 | 136 | 184,128 | 72,275,976 |
| 27 | 5 | 221 | 1,789,693 | 3,171,108,447 |

The [one- through four-path certificates at 26](terminal-order.md) complete the lower path counts. For each larger path count, a [separate checker](../rainbow/check_path_permutations.cpp) enumerates all ordered compositions to obtain the expected sorted lists. It checks every permutation and actual internal sum, recursively assigns distinct unused weights to the entering edges, and reconstructs the parent labels from these sums. It computes the least unit multiple of every ordered input tuple by a base-$k$ digit recurrence, then requires every representative to have a witness. Multiplication by any unit fixes zero and scales every sum. The Python and native checkers also agreed on all four smaller path counts at 27. A separate SSH checkout regenerated all ten streams for one through five paths at both moduli and reproduced every digest and verifier total. A [whole-tree replay](../rainbow/check_path_growth.py) assembled the witnesses on star cores at both allowed order residues, with coincident and different parents. Recounting both histograms after each step verified 1,240 actual prefixes at 26 and 1,280 at 27. [Generator](../rainbow/independent_paths.cpp) · [SHA-256 manifest](../rainbow/five-paths.sha256)

At 26 the same full native verification covered six paths. The whole-tree replay with one through six paths recounted 1,500 actual prefixes. [Six-path digest](../rainbow/six-paths.sha256)

In a minimum counterexample the five longest terminal arms together have length at most $M=s-2$. Otherwise remove $s-1$ terminal vertices on at most five paths. Minimality labels the connected remainder of order one modulo $k$, and the certificate restores the removed paths. Let $z$ be the fifth largest length. Then $5z\le M$ and the sum of $(a-z)_+$ over all arm lengths $a$ is at most $M-5z$. Each joint with $j$ terminal arms of total length $w$ uses at least $(w-jz)_+$ of this budget. The six-path certificate gives the same statement at 26 for the six longest arms, with $z$ the sixth largest length and budget $M-6z$.

## Cuts at small sides and at a branching vertex

The [six-tip certificates](../rainbow/few-leaves.md) hold at both moduli. As in the [two-side proof](pendant-order.md#removing-a-forest-with-few-tips), a union of branches at one vertex with at most six original leaves has order at most $M$. Write $t=s-1$. For disjoint sides $A,B$ with at most three leaves each, put $a=|A|$. If $a\ge J=s+1-\lfloor k/2\rfloor$, then $|B|\le M-a$. Indeed, otherwise delete $A$ together with a size-ordered suffix of $t-a$ vertices of $B$. Pad $A$ at a tip by $k-1-t$ vertices. The inequality $a+k-1-t\ge(t-a)+3$ permits the padded component to follow all boundary runs of the suffix. There are at most three such runs and at most six tips overall. The six-tip certificate restores the deleted forest on the smaller core.

If every edge has a side of at most six leaves, walk toward a side of more than six leaves until every side at a vertex is small. Merge any two groups there with at most six leaves in total. At termination every two distinct groups have at least seven leaves between them. Seven such groups would have at least 27 leaves. Indeed, if the smallest group has at most three, all others have at least seven minus its size, and otherwise every group has at least four. The [leaf bound](../counterexample-bound.md#removing-leaves) gives at most $M\le25$ leaves. Thus at most six groups remain and the order is at most $1+6M$.

Otherwise join two rooted halves across a corridor with at least seven leaves on either side. If every small side of at most three leaves has order below $J$, both halves have cap $J-1$. Otherwise orient a maximizing small side of order $a$ into the left half. Such sides point away from the joining corridor. The two caps become $a$ and $M-a$. In every half a side with at most six leaves has absolute cap $M$.

The total length of terminal arms at one joint is at most $M$ by the [single-joint path theorem](../rainbow/terminal-paths.md#bounding-a-smallest-counterexample-by-its-branching-vertices). Each corridor has at most $k-7$ interior degree-two vertices by the [six-vertex reduction](dense-cycles.md#consequences-for-tree-order). At a joint with a parent direction, select a downward direction containing the most original leaves. Break ties arbitrarily, except that when all directions are terminal arms, select a longest arm. The other downward directions form a forest at the joint. Denote its vertex count by $w$ and its original leaf count by $q$. When $q\le6$ the preceding pruning argument gives $w\le M$, even when this forest contains other branching vertices.

Let $e$ and $g$ be the numbers of degree-two vertices on the incoming corridor and the chosen downward corridor. The joint, its entire side forest, and any initial portions of those two corridors make a piece of every order from $1+w$ through $1+w+e+g$. If the interval contains $k$ and $k-w\ge3$, closing the piece gives a unicyclic graph of girth $k-w$ with precisely $q$ leaves. The [ring census](few-leaf-rings.md) excludes this configuration for $q=2,3,4$. The [one-leaf period theorem](one-leaf-period.md) also excludes $q=1$ at both moduli. Since $w\le M\le k-2$ in all these cases, it suffices to test the upper endpoint of the interval. At an end joint with selected arm length $d$, retain its leaf and put $g=d-1$.

The same reduction applies across two consecutive joints in the selected direction. Suppose their side forests have $q,r$ leaves and orders $w,f$. Let $g$ be the interior of the joining corridor and $e,h$ the exterior corridor interiors. Taking both side forests and the entire joining corridor gives minimum piece size $b=2+w+g+f$. The largest size is $b+e+h$. Whenever $q+r\le4$, the piece is forbidden if $b\le k\le b+e+h$ and $k-w-f\ge3$. There are always at least two side leaves in this test. The two forests may themselves branch.

## Reproducing the bounds

Build branch tables in increasing leaf count. A branch records the length $e$ of its incoming corridor, total order including that corridor, number of leaves, and arm excess. To build a joint with $T$ leaves, try every largest child leaf count $l=1,\ldots,T-1$. The side forest has $T-l$ leaves. It contains any number of terminal arms and a multiset of branching children having at most $l$ leaves each. If $l=1$, try a longest terminal arm of length $d$ and all possible total lengths of the other arms. If $l\ge2$, attach the side forest to the chosen branching child with its recorded corridor length. Enforce the small-side, local substitution, and terminal arm bounds. A side of base order $b$ before the parent corridor gives cut sizes $b,b+1,\ldots,b+e$. Discard it if any size is congruent to zero or $s$ modulo $k$ by the [divisible-cut theorem](../divisible-cuts.md).

Every true branch appears by induction, taking its chosen direction and the actual remaining components as its side forest. A side forest made from terminal arms uses the lower bound $(w-jz)_+$ for $j$ arms of total length $w$. Other children contribute their separately computed costs. At the joining corridor the two halves share its $e$ internal vertices, counted only once. Take the largest order of the required residue, also allowing $1+6M$ without a joining corridor. The enumeration relaxes some restrictions, for example when several different downward choices could expose a removable piece. This preserves the upper bound.

The [Python calculation](ring_order.py) stores all exact orders and excess costs as bits. A recursive multiset formula builds each side forest by omitting its largest allowed branch type or taking one more branch of that leaf count. The [C++ calculation](check_ring_order.cpp) instead adds allowed leaf counts to a table incrementally and keeps the minimum cost at each exact order, with no prespecified maximum order. In C++ the corridor cuts are checked one edge at a time. Python uses masks of admissible intervals. For a two-joint test put $t=k-2-g-w$. Among children of a compatible leaf count it suffices to keep the union with $f>\min(t,k-3-w)$ or $f+h<t-e$. Python tabulates the two cumulative unions. C++ stores the actual child triples $(r,f,h)$ and directly tests the interval. Lean 4.36.0 also checks that every intermediate corridor size can be realized, that the cumulative test is equivalent to the interval exclusion, and that the padded-side threshold works for both parities. [Lean arithmetic](SideForestOrder.lean)

Both calculations give the table above. A [separate geometric check](check_ring_cuts.py) removed pairs of actual edges in 3,245 trees and compared 187,661 single-joint and 123,337 two-joint middle components with the interval formulas. It encountered 1,395 eligible size-26 pieces and 1,439 eligible size-27 pieces with two through four side leaves.

~~~bash
set -euo pipefail
out=$(mktemp -d)
r="$PWD/research/rainbow"
c="$PWD/research/census"
c++ -O3 -std=c++17 -Drainbow_witness=reference_witness -c "$r/search.cpp" -o "$out/ref.o"
c++ -O3 -std=c++17 -DRAINBOW_WIDE_MASK -c "$r/leaf_search.cpp" -o "$out/leaf.o"
c++ -O3 -std=c++17 "$r/independent_paths.cpp" "$out/ref.o" "$out/leaf.o" -o "$out/paths"
c++ -O3 -std=c++17 "$r/check_path_permutations.cpp" -o "$out/check-paths"
for k in 26 27; do
    for j in 1 2 3 4 5; do
        "$out/paths" "$k" "$j" > "$out/multipath-$k-$j"
        "$out/check-paths" "$k" "$j" "$out/multipath-$k-$j"
    done
done
(cd "$out" && shasum -a 256 -c "$r/independent-paths.sha256" && shasum -a 256 -c "$r/five-paths.sha256")
"$out/paths" 26 6 > "$out/multipath-26-6"
"$out/check-paths" 26 6 "$out/multipath-26-6"
(cd "$out" && shasum -a 256 -c "$r/six-paths.sha256")
python3 -B -m research.rainbow.check_path_growth "$out" 26 6
python3 -B -m research.rainbow.check_path_growth "$out"
python3 -B -m research.census.check_ring_cuts
lean "$c/SideForestOrder.lean"
python3 -B "$c/ring_order.py"
c++ -std=c++17 -O3 "$c/check_ring_order.cpp" -o "$out/bounds"
"$out/bounds"
~~~
