# Centroid cuts for twelve and thirteen leaves at 27 labels

**Verified orders.** Every tree with at most twelve leaves and at most 52 vertices is 27-cordial. For at most thirteen leaves the verified range reaches 51 vertices. A designated leaf may receive a most-frequent vertex residue in both statements. Orders 53 and 54 for twelve leaves, and orders 52 through 54 for thirteen leaves, are under audit.

The earlier results cover [every tree through 49 vertices](../rainbow/twenty-one-free.md) and [at most eleven leaves at every order](eleven-leaves.md). By the [six-terminal theorem](../rainbow/few-leaves.md#a-finite-reduction-for-eleven-leaves), a smallest counterexample within either new class must have order at most 54. This leaves five orders to verify for an all-orders theorem.

## Selecting a cut from the numerical branch data

Fix $50\le n\le54$, $t=n-28$, and $L=12$ or $13$. At a leaf centroid $v$, each branch of $T-v$ has at most $\lfloor L/2\rfloor=6$ original leaves. Such a vertex exists by walking toward any side containing more than half the leaves. With $L>2$ it is an internal vertex. Describe a whole branch by its order $s$ and number $h$ of rooted tips. Its tips are precisely its original leaves. We have $h\le\max(1,s-1)$, with equality possible at $s=1$.

If some selection of whole branches has at most six tips and total order at least $t$, retain $v$ and the other branches. Traverse the selected branches in size-ordered preorder from $v$, stopping when exactly $t$ vertices remain. The resulting forest has at most six tips. Its actual boundary colors satisfy the ordered-cut inequalities. Pad a largest component at a tip to reach total order 26 and use the existing [six-terminal certificate](../rainbow/few-leaves.md). The retained core has order 28. Translate its unique surplus label to zero. Injective nonzero labels and distinct new weights on the exterior then maintain cordiality.

In every remaining numerical case each branch has order less than $t$. Choose a set $W$ of entire branches to delete, all with common parent $v$, and write $z=t-\sum_{A\in W}|A|$. For $z=0$ this is the entire cut. Otherwise choose a separate branch $B$ of order $s_B>z>0$ with $h_B$ tips. In $B$, delete the final $z$ vertices of its size-ordered preorder. The core remains connected. This suffix consists of complete rooted subtrees with at most $h_B$ tips in total. Accept the proposed cut only if at least one of the following holds.

* Every member of $W$ is at least as large as $B$. After the retained whole branches at $v$ have been included, traverse $B$ before every member of $W$. This is a size-ordered traversal of the exterior and its starting vertex $v$.
* Every member of $W$ has size at least $z+\min(z,h_B)$. The suffix in $B$ has at most $\min(z,h_B)$ boundary runs, since each run uses at least one component and each component has a tip. Append all of $W$ at the one color on $v$. At a change of color the first new component must have order at least the previous mass plus the previous number of runs. The assumed lower bound gives exactly this. The appended components are all larger than any suffix component.

Thus in either case the actual assignment satisfies the [sharp ordered-cut conditions](../rainbow/ordered-cut.md#which-colored-forests-actually-occur). These conditions use the canonically sorted list of component sizes. Tied sizes cannot change color. Whole branches with equal size may therefore be sorted by their canonical bracket words.

Enumerate every possible multiset of pairs $(s,h)$ for the suffix within $B$, with total order $z$ and at most $h_B$ tips. Adjoin the fixed pairs of $W$. For every resulting profile, either there are at most six tips, or the exact profile must occur in the verified dictionary for this order. This condition proves the cut works without choosing a labeling of the core in advance. For a mark in the core, give its leaf the surplus by deleting it before labeling the remaining 27-vertex tree and then filling the deficient edge weight. A mark outside the core receives an incremented label. The marked base through order 49 for these leaf counts uses the 21-vertex exterior certificate with at most thirteen tips. [Marked cut and order-one argument](marked-ring.md)

## Independent enumeration and labeling checks

The [C++ checker](check_leaf_profile_cover.cpp) orders branches by tip count and keeps the maximum selectable mass for tip budgets zero through six. It enumerates the remaining cases and tests all choices of $W$ and $B$, including the zero-suffix case. An [independent Python implementation](leaf_profile_geometry.py) orders branches by decreasing size, records the sets of exact attainable masses with bit masks, and independently chooses a cut. It constructs suffixes from integer partitions and the possible tip counts of actual rooted trees of each order. The check compares the complete numerical case sets of the two implementations, then requires both to accept every case.

A certificate profile lists the order and tip count of every component. The [generator](../rainbow/spine_generate.cpp) selects a multiset of rooted bracket words of each requested type. The [native verifier](../rainbow/spine_verify.cpp) reconstructs each rooted forest from its stream, checks canonical ordering and the actual profile, and rejects repeated shapes. It independently computes the required number of shapes by the bivariate multiset product on order and tip count. For every row it checks label distinctness and edge sums. It tests every permitted boundary assignment under multiplication by units. A missing witness, shape or boundary orbit fails verification.

The [manifest checker](check_leaf_profile_manifests.py) uses integer partitions to count rooted components independently. If a type has $N$ rooted trees and occurs $c$ times, its factor in the shape count is $\binom{N+c-1}{c}$. A separate recurrence counts literal boundary assignments by whether the next component starts a new run. The [small-modulus regression](check_typed_leaf_streams.py) compares whole component-type dictionaries against full catalogs at eight labels and directly checks their literal boundary inputs. It also injects 184 truncated, repeated, empty or invalid-label streams.

Each **13** row below includes the corresponding twelve-leaf streams. A thirteen-leaf manifest records only the extra profiles, so each stream is published once.

| Leaves | Order | Numerical cases requiring a cut | Profiles | Rooted forests | Witness rows | Boundary assignments |
|---:|---:|---:|---:|---:|---:|---:|
| 12 | 50 | 388 | 81 | 941,848 | 24,453,837 | 7,557,356,376 |
| 12 | 51 | 559 | 168 | 1,872,577 | 70,755,366 | 17,300,096,559 |
| 12 | 52 | 778 | 223 | 4,360,159 | 248,375,882 | 43,615,436,499 |
| 13 | 50 | 1,394 | 180 | 4,547,618 | 77,339,210 | 18,767,082,942 |
| 13 | 51 | 2,355 | 335 | 9,020,220 | 225,561,628 | 55,271,031,804 |

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
for manifest in "$c"/leaf-profile-audits/*.txt; do
  name=$(basename "$manifest" .txt)
  leaves=${name%-*}
  n=${name#*-}
  awk -F '  ' '{print $3}' "$manifest" > "$out/$name.profiles"
  flags=()
  if [[ $n == 53 ]]; then flags+=(--restarts); fi
  python3 -B "$c/stream_leaf_profiles.py" 27 "$out/$name.profiles" "$out/generate" "$out/verify" "$out/$name" --workers 4 "${flags[@]}"
  cmp "$manifest" "$out/$name/manifest.txt"
  proof=("$manifest")
  if [[ $leaves == 13 ]]; then proof+=("$c/leaf-profile-audits/12-$n.txt"); fi
  python3 -B -m research.census.check_leaf_profile_manifests "$n" "$leaves" "$out/geometry" "${proof[@]}"
done
~~~
