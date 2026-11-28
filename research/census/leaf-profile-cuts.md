# Cordial growth for trees with at most fifteen leaves at 27 labels

**Theorem (computer-assisted).** Every finite tree with at most fifteen leaves has one labeling that is 27-cordial on every prefix of a connected vertex order. Any specified leaf can be placed in the last block of 27 vertices (or the final shorter block) and receive a most-frequent vertex residue.

The earlier results cover [every tree through 49 vertices](../rainbow/twenty-one-free.md) and [at most eleven leaves at every order](eleven-leaves.md). The [three-group reduction](../rainbow/few-leaves.md#a-finite-reduction-for-eleven-leaves) puts the least counterexample within thirteen leaves at order at most 54 using six tips. The [seven-tip certificate](../rainbow/seven-tip-27.md) gives the same bound within fifteen leaves. This leaves five orders to verify for an all-orders theorem.

## Selecting a cut from the numerical branch data

Fix $50\le n\le54$, $t=n-28$, and $11\le L\le15$. Put $q=6$ for $L\le13$ and $q=7$ otherwise. At a leaf centroid $v$, each branch of $T-v$ has at most $\lfloor L/2\rfloor\le q$ original leaves. Such a vertex exists by walking toward any side containing more than half the leaves. With $L>2$ it is an internal vertex. Describe a whole branch by its order $s$ and number $h$ of rooted tips. Its tips are precisely its original leaves. We have $h\le\max(1,s-1)$, with equality possible at $s=1$.

If some selection of whole branches has at most $q$ tips and total order at least $t$, retain $v$ and the other branches. Traverse the selected branches in size-ordered preorder from $v$, stopping when exactly $t$ vertices remain. The resulting forest has at most $q$ tips. Its actual boundary colors satisfy the ordered-cut inequalities. Pad a largest component at a tip to reach total order 26 and apply the [six-terminal](../rainbow/few-leaves.md) or [seven-terminal](../rainbow/seven-tip-27.md) certificate. The retained core has order 28. Translate its unique surplus label to zero. Injective nonzero labels and distinct new weights on the exterior then maintain cordiality.

In every remaining numerical case each branch has order less than $t$. Choose a set $W$ of entire branches to delete, all with common parent $v$, and write $z=t-\sum_{A\in W}|A|$. For $z=0$ this is the entire cut. Otherwise choose a separate branch $B$ of order $s_B>z>0$ with $h_B$ tips. In $B$, delete the final $z$ vertices of its size-ordered preorder. The core remains connected. This suffix consists of complete rooted subtrees with at most $h_B$ tips in total. Accept the proposed cut only if at least one of the following holds.

* Every member of $W$ is at least as large as $B$. After the retained whole branches at $v$ have been included, traverse $B$ before every member of $W$. This is a size-ordered traversal of the exterior and its starting vertex $v$.
* Every member of $W$ has size at least $z+\min(z,h_B)$. The suffix in $B$ has at most $\min(z,h_B)$ boundary runs, since each run uses at least one component and each component has a tip. Append all of $W$ at the one color on $v$. At a change of color the first new component must have order at least the previous mass plus the previous number of runs. The assumed lower bound gives exactly this. The appended components are all larger than any suffix component.

Thus in either case the actual assignment satisfies the [sharp ordered-cut conditions](../rainbow/ordered-cut.md#which-colored-forests-actually-occur). These conditions use the canonically sorted list of component sizes. Tied sizes cannot change color. Whole branches with equal size may therefore be sorted by their canonical bracket words.

Enumerate every possible multiset of pairs $(s,h)$ for the suffix within $B$, with total order $z$ and at most $h_B$ tips. Adjoin the fixed pairs of $W$. For every resulting profile, either there are at most $q$ tips, or the exact profile must occur in the verified dictionary for this order. This condition proves the cut works without choosing a labeling of the core in advance. For a mark in the core, give its leaf the surplus by deleting it before labeling the remaining 27-vertex tree and then filling the deficient edge weight. A mark outside the core receives an incremented label. The marked base through order 49 for these leaf counts uses the 21-vertex exterior certificate with at most thirteen tips. [Marked cut and order-one argument](marked-ring.md)

## One labeling for all connected prefixes

Use the existing [prefix induction](../rainbow/cut-growth.md) for at most ten leaves. For eleven through fifteen leaves, the integer base gives distinct labels and edge weights through order 27. At order one modulo 27, delete the marked leaf, or any leaf if unmarked, apply induction, then append it with the label that fills the deficient edge bin. For the remaining orders through 49 use the [21-vertex exterior certificate](../rainbow/twenty-one-free.md) on the size-ordered cut, which has at most thirteen tips. At orders 50 through 54, each completed row below certifies a cut to a 28-vertex core. For exactly eleven leaves they accept all 64, 81, 100, 120 and 140 exceptional numerical cases, respectively, using the twelve-leaf manifests. Above 54 the [three-group argument](../rainbow/few-leaves.md#a-finite-reduction-for-eleven-leaves) supplies a cut with at most $q$ tips.

Each core is connected, has order one modulo 27 and has at most as many leaves as the original tree. Apply induction to the core, retaining the mark if it lies there. Its final block is a singleton, so a retained mark has the unique surplus color. The exterior receives distinct colors avoiding this surplus, with distinct new edge weights. Append its vertices in any parent-first order. Every prefix increments only distinct low vertex bins and distinct initially equal edge bins. The final block consists of the last core vertex and the exterior. Its residues are all most frequent. The certificates in the table cover all five finite orders through fifteen leaves. This closes the induction at every order.

The [matching lift and marked-leaf deletion](marked-ring.md#matching-consequence-and-verification) give 54-cordiality for any tree with at most fifteen leaves and a perfect or near-perfect matching. Matching contraction and the temporary-leaf construction in that argument preserve the required leaf bound. Direct checks expanded 24 fourteen-leaf quotient trees of order 54 using both ports at every nonleaf. All 24 perfect expansions of order 108 and all 24 near-perfect examples of order 107 retained fourteen leaves and had balanced 54-bin histograms. The same calculation passed on 24 fifteen-leaf quotients at each of orders 53 and 54 for both matching types.

## Independent enumeration and labeling checks

The [C++ checker](check_leaf_profile_cover.cpp) orders branches by tip count and keeps the maximum selectable mass for tip budgets zero through $q$. It enumerates the remaining cases and tests all choices of $W$ and $B$, including the zero-suffix case. An [independent Python implementation](leaf_profile_geometry.py) orders branches by decreasing size, records the sets of exact attainable masses with bit masks, and independently chooses a cut. It constructs suffixes from integer partitions and the possible tip counts of actual rooted trees of each order. The check compares the complete numerical case sets of the two implementations, then requires both to accept every case.

A certificate profile lists the order and tip count of every component. The [generator](../rainbow/spine_generate.cpp) selects a multiset of rooted bracket words of each requested type. The [native verifier](../rainbow/spine_verify.cpp) reconstructs each rooted forest from its stream, checks canonical ordering and the actual profile, and rejects repeated shapes. It independently computes the required number of shapes by the bivariate multiset product on order and tip count. For every row it checks label distinctness and edge sums. It tests every permitted boundary assignment under multiplication by units. A missing witness, shape or boundary orbit fails verification.

The [manifest checker](check_leaf_profile_manifests.py) uses integer partitions to count rooted components independently. If a type has $N$ rooted trees and occurs $c$ times, its factor in the shape count is $\binom{N+c-1}{c}$. A separate recurrence counts literal boundary assignments by whether the next component starts a new run. The [small-modulus regression](check_typed_leaf_streams.py) compares whole component-type dictionaries against full catalogs at eight labels and directly checks their literal boundary inputs. It also injects 184 truncated, repeated, empty or invalid-label streams.

At each order the profile dictionaries are cumulative in leaf count. Each manifest records the additional profiles first used at that leaf count. The twelve- and thirteen-leaf table entries give cumulative certificate totals. At fourteen and fifteen leaves the table counts the additional profiles, and the seven-tip theorem supplies the freely permitted shapes.

| Leaves | Order | Numerical cases requiring a cut | Profiles | Rooted forests | Witness rows | Boundary assignments |
|---:|---:|---:|---:|---:|---:|---:|
| 12 | 50 | 388 | 81 | 941,848 | 24,453,837 | 7,557,356,376 |
| 12 | 51 | 559 | 168 | 1,872,577 | 70,755,366 | 17,300,096,559 |
| 12 | 52 | 778 | 223 | 4,360,159 | 248,375,882 | 43,615,436,499 |
| 12 | 53 | 1,058 | 244 | 8,482,500 | 462,878,824 | 81,174,030,444 |
| 12 | 54 | 1,389 | 321 | 16,670,448 | 1,688,748,176 | 189,852,628,734 |
| 13 | 50 | 1,394 | 180 | 4,547,618 | 77,339,210 | 18,767,082,942 |
| 13 | 51 | 2,355 | 335 | 9,020,220 | 225,561,628 | 55,271,031,804 |
| 13 | 52 | 3,921 | 460 | 16,539,837 | 634,532,366 | 108,112,875,093 |
| 13 | 53 | 6,787 | 601 | 31,775,049 | 1,339,646,446 | 232,189,280,811 |
| 13 | 54 | 11,655 | 822 | 60,001,367 | 4,824,484,964 | 496,958,855,715 |
| 14 | 50 | 780 | 237 | 7,233,287 | 144,783,375 | 37,597,824,351 |
| 14 | 51 | 1,186 | 388 | 15,878,970 | 459,395,255 | 103,700,019,582 |
| 14 | 52 | 1,732 | 183 | 16,028,313 | 877,505,837 | 172,313,857,575 |
| 14 | 53 | 2,505 | 249 | 32,960,118 | 1,794,713,468 | 344,948,036,130 |
| 14 | 54 | 3,451 | 293 | 66,743,558 | 6,336,041,656 | 666,995,883,318 |
| 15 | 50 | 2,186 | 329 | 16,019,357 | 274,022,699 | 71,146,816,965 |
| 15 | 51 | 3,768 | 554 | 35,862,672 | 930,592,083 | 209,257,110,180 |
| 15 | 52 | 6,446 | 240 | 42,112,876 | 1,536,568,447 | 249,950,696,346 |
| 15 | 53 | 11,305 | 442 | 82,619,236 | 3,403,891,094 | 575,972,140,716 |
| 15 | 54 | 19,989 | 705 | 172,011,702 | 13,985,725,802 | 1,488,412,955,736 |

The last fourteen-leaf order and the first four fifteen-leaf orders have complete cut coverage in both geometry implementations. Every generated stream received independent witness verification. A second build regenerated all 79 new streams with at most 100 forests, matching each digest for a total of 3,499 forests, 651,902 witness rows and 71,827,641 boundary assignments. A [whole-tree replay](check_order_fifty_samples.py) recounted every prefix of the restoration on 8,748 trees of order 54, including 2,104 with fourteen leaves, and 2,187 trees of order 53, including 287 with fifteen leaves. [Fourteen leaves at 54](leaf-profile-audits/14-54.txt) · [Fifteen leaves at 53](leaf-profile-audits/15-53.txt)

The final [fifteen-leaf manifest at order 54](leaf-profile-audits/15-54.txt) completes the all-orders proof. Both geometry implementations cover all 19,989 necessary branch profiles. Every witness stream passed independent verification, and a fresh build reproduced all 74 new streams containing at most 100 forests. Their hashes cover 2,740 forests, 700,386 witness rows and 30,940,218 literal boundary assignments. A separate replay on 2,187 actual trees of order 54 checked all 26 restoration prefixes, including 287 trees with exactly fifteen leaves. It lifted 24 fifteen-leaf trees to both perfect and near-perfect matching examples at 54 labels.

## Reproduction

Run in Bash from the repository root. Python 3.8 or later and a C++17 compiler suffice. Each stream is generated, checked and hashed in a pipeline. Only its small manifest is kept.

~~~bash
set -euo pipefail
out=$(mktemp -d)
r=research/rainbow
c=research/census
c++ -O3 -std=c++17 -Drainbow_witness=reference_witness -c "$r/search.cpp" -o "$out/reference.o"
c++ -O3 -std=c++17 "$r/spine_generate.cpp" "$r/leaf_search.cpp" "$out/reference.o" -o "$out/generate"
c++ -O3 -std=c++17 -pthread "$r/spine_verify.cpp" -o "$out/verify"
c++ -O3 -std=c++17 "$c/check_leaf_profile_cover.cpp" -o "$out/geometry"
python3 -B -m research.census.check_typed_leaf_streams "$out/generate" "$out/verify"
for manifest in "$c"/leaf-profile-audits/1[2-5]-*.txt; do
  name=$(basename "$manifest" .txt)
  leaves=${name%-*}
  n=${name#*-}
  awk -F '  ' '{print $3}' "$manifest" > "$out/$name.profiles"
  flags=()
  if [[ $n == 53 ]]; then flags+=(--restarts); fi
  python3 -B "$c/stream_leaf_profiles.py" 27 "$out/$name.profiles" "$out/generate" "$out/verify" "$out/$name" --workers 4 "${flags[@]}"
  cmp "$manifest" "$out/$name/manifest.txt"
  if [[ $leaves == 12 ]]; then
    python3 -B -m research.census.check_leaf_profile_manifests "$n" 11 "$out/geometry" "$manifest"
  fi
  proof=()
  for ((i=12; i<=leaves; i++)); do proof+=("$c/leaf-profile-audits/$i-$n.txt"); done
  python3 -B -m research.census.check_leaf_profile_manifests "$n" "$leaves" "$out/geometry" "${proof[@]}"
done
"$out/generate" 27 0 1 "$out/sample54" --typed 1,1 1,1 1,1 1,1 1,1 4,1 17,2
python3 -B -m research.census.check_order_fifty_samples "$out/sample54" --order 54 --sample 4
"$out/generate" 27 0 1 "$out/sample53" --typed-restarts 1,1 1,1 1,1 1,1 1,1 1,1 1,1 18,1
python3 -B -m research.census.check_order_fifty_samples "$out/sample53" --order 53
"$out/generate" 27 0 1 "$out/sample15at54" --typed 1,1 1,1 1,1 1,1 1,1 1,1 1,1 19,1
python3 -B -m research.census.check_order_fifty_samples "$out/sample15at54" --order 54 --lift-leaves 15
~~~
