# Ordinary 27-cordiality at order 50

**Computer-assisted theorem.** Every tree on 50 vertices is 27-cordial. Together with the [short-forest theorem](../rainbow/twenty-one-free.md), this proves 27-cordiality for every tree through order 50. A smallest counterexample would have **51 through 216 vertices** by the [upper bound](ring-order.md). The unrestricted 27-label question remains open.

## Restrictions at a vertex centroid

Let a component at a centroid be described by its order $s$ and its number of tips $h$ when rooted next to the centroid. These tips are leaves of the original tree. The components have total order 49 and each has at most 25 vertices. Suppose that the tree has no cordial labeling. The [sixteen-leaf theorem](sixteen-leaf-corridor.md) gives at least seventeen leaves. If it has at least 22 leaves, delete 22 of them. The remaining tree has order 28 and a cordial labeling. Hall's prescribed-differences theorem reattaches 22 leaves at arbitrary parent labels. Thus at most 21 leaves remain to consider. [Leaf extension](../counterexample-bound.md#removing-leaves)

The following restrictions apply together.

* A component of order 23 through 25 would split the tree into two pieces of order at most 27, which the [affine join theorem](../prime/four-deficits.md) labels. No collection of components can total 22, since the [common-parent theorem](../rainbow/common-site-27.md) would restore it on the 28-vertex core. In particular every component has order at most 21.
* A subcollection with at most seven tips must have order below 22. Otherwise its final 22 vertices in size-ordered preorder give a [certified seven-tip extension](../rainbow/seven-tip-27.md) of a connected core of order 28. This applies at the vertex centroid regardless of how many tips its other components contain.
* Two disjoint components cut off by individual edges cannot total 23. Their connected complement would have 27 vertices and the [one-offset theorem](../biased/one-offset-23.md) would expand it between the two parts. In particular two whole centroid branches cannot total 23. Within one branch $i$, every descendant subtree must avoid the orders $23-s_j$ for all other branches $j$.

For the last test, let $F$ be the forbidden orders in a branch. To minimize its possible tips, assign infinity to a rooted tree of any size in $F$. At an allowed order $s$, minimize the sum of tip counts over multisets of children totaling $s-1$, counting a childless root as one tip. This recurrence follows by deleting or adjoining the root. Discard a branch size and tip count if its recorded number of tips is below this minimum. Only a necessary condition is used.

## Checking all remaining profiles

For each admissible numerical profile, first test whether the one-tip branches have at least 22 vertices between them. These branches are paths starting at the same vertex. Their size-ordered suffix of mass 22 is covered by the [terminal-path extension](../rainbow/terminal-paths.md).

Otherwise select a collection of whole branches and a separate branch of size $s$ with $h$ tips. Let the whole branches have total size $22-z$, with $0<z<s$. Remove them and the last $z$ vertices of the separate branch. The latter suffix has at most $\min(z,h)$ tips. The smallest whole branch must have size at least $\min(s,z+\min(z,h))$. This size bound ensures that the actual boundary colors satisfy the [ordered-cut inequalities](leaf-profile-cuts.md#selecting-a-cut-from-the-numerical-branch-data). The retained core is connected and has order 28.

Enumerate every possible multiset of rooted component sizes and tip counts in this suffix. Each resulting exterior is certified in at least one way. Up to seven tips are already covered. If the ordered-cut inequalities allow only the 27 constant boundary assignments, use the common-parent theorem. For the remaining cases use a published component profile, permitting [padding at a tip of a largest component](../rainbow/ordered-cut.md). Every such certificate supplies distinct new vertex labels avoiding the core's surplus and distinct new weights, including all edges to the core. These properties suffice for ordinary cordiality.

| Number of leaves | Remaining centroid profiles | Profiles with a certified cut |
|---:|---:|---:|
| 17 | 11,172 | 11,172 |
| 18 | 23,538 | 23,538 |
| 19 | 43,716 | 43,716 |
| 20 | 74,698 | 74,698 |
| 21 | 116,022 | 116,022 |

The [Python checker](check_order_fifty.py) enumerates partitions of 49, then assigns their tip counts. The independent [C++ enumeration](order_fifty_centroids.cpp) orders branches by tip count and builds the possible subset masses separately at each tip count. The former calculates the minimum tips with unbounded knapsack over allowed child orders. The latter splits off the first component of a child forest. Their complete sets of centroid profiles agree for each leaf count. Every surviving profile is tested for an actual sufficient cut.

The [additional manifests](order-50-audits/) contain 1,195 component profiles, covering 95,001,506 rooted forests, 1,422,399,948 verified labeling rows and 475,272,311,022 literal boundary assignments. Streams were checked at generation by the independent [labeling verifier](../rainbow/spine_verify.cpp). The geometry checker separately recomputes the number of forests from rooted-tree multisets and the number of allowed boundary assignments. The earlier certificates it uses are the [leaf-profile audits](leaf-profile-audits/) through sixteen leaves at 50 and 51, fifteen at 52, fourteen at 53 and thirteen at 54.

The [whole-tree replay](check_order_fifty_samples.py) joins each of three certified forests to three different 28-vertex caterpillars, with all 729 allowed boundary assignments on each forest. It recounts every bin of all 6,561 resulting trees of order 50. These examples have sixteen through twenty-two leaves.

~~~bash
set -euo pipefail
out=$(mktemp -d)
r=research/rainbow
c=research/census
c++ -O3 -std=c++17 "$c/order_fifty_centroids.cpp" -o "$out/geometry"
python3 -B -m research.census.check_order_fifty "$out/geometry" 21
c++ -O3 -std=c++17 -Drainbow_witness=reference_witness -c "$r/search.cpp" -o "$out/ref.o"
c++ -O3 -std=c++17 "$r/spine_generate.cpp" "$r/leaf_search.cpp" "$out/ref.o" -o "$out/generate"
c++ -O3 -std=c++17 -pthread "$r/spine_verify.cpp" -o "$out/verify"
"$out/generate" 27 0 1 "$out/sample" --typed-restarts 2,1 4,1 4,1 4,1 4,2 4,2
python3 -B -m research.census.check_order_fifty_samples "$out/sample"
for cert in "$c"/order-50-audits/*.txt; do
  id=$(basename "$cert" .txt)
  awk -F '  ' '{print $3}' "$cert" > "$out/$id.profiles"
  flags=()
  if [[ $id = *-restarts ]]; then flags+=(--restarts); fi
  python3 -B "$c/stream_leaf_profiles.py" 27 "$out/$id.profiles" "$out/generate" "$out/verify" "$out/$id" --workers 2 "${flags[@]}"
  cmp "$out/$id/manifest.txt" "$cert"
done
~~~
