# Trees of order 51 with at most 19 leaves at 27 labels

**Computer-assisted theorem.** Every tree of order 51 with at most nineteen leaves is 27-cordial. A counterexample of this order would have **20 through 22 leaves**. The [order-50 theorem](order-fifty.md) labels every smaller tree, the [sixteen-leaf theorem](sixteen-leaf-corridor.md) covers the smaller leaf counts at 51, and deleting 23 original leaves when available gives a Hall extension on a 28-vertex core. With exactly 22 leaves a counterexample would need at least five different leaf parents. [Short star theorem](../rainbow/pinned-star.md#several-singleton-parent-colors)

## Necessary centroid data

Suppose a 51-vertex tree has $17\le L\le19$ leaves and no 27-cordial labeling. Choose a vertex centroid. Write $(s,h)$ for the order and rooted tip count of a branch there. The orders sum to 50 and the tip counts sum to $L$. Each branch has at most 25 vertices. The [two-vertex attachment theorem](../rainbow/common-pair-21.md) excludes every edge side of order 21 through 27 and every union of branches at the centroid of order 21 or 22. Consequently the branch orders are at most 20.

A collection of centroid branches with at most seven tips must have fewer than 23 vertices. Otherwise its size-ordered suffix of 23 vertices gives a [seven-tip extension](../rainbow/seven-tip-27.md). No single branch can have more than $L-8$ tips, since the opposite edge side has order at least 31 and at most seven original leaves and admits the same suffix cut, rooted toward that branch. The centroid has degree at least three under the size bound.

Finally a branch with one tip is a terminal path of its full length $s$. Each of the $h$ original leaves in any other branch supplies at least one terminal vertex. If the six longest of these guaranteed lengths total at least 23, delete path suffixes totaling exactly 23. The [six-path theorem](ring-order.md#terminal-paths-with-independently-prescribed-parents) restores them with arbitrary old parent colors. These restrictions leave **5,125** numerical profiles at seventeen leaves, **11,289** at eighteen and **21,426** at nineteen.

## Sufficient cuts

If all one-tip branches at the centroid have total order at least 23, take their size-ordered suffix and apply the [terminal-path theorem](../rainbow/terminal-paths.md). Otherwise the checker tries a collection of whole branches and, if necessary, a suffix of one other branch, with 23 deleted vertices in total. For a partial branch of size $s$ and $h$ tips, require that its suffix size $z$ satisfy $0<z<s$ and each whole branch have size at least $\min(s,z+\min(z,h))$. This is the established [ordered-cut criterion](leaf-profile-cuts.md#selecting-a-cut-from-the-numerical-branch-data). For a whole-branch cut whose complement has at most seven tips among the 27 other branch vertices, the [common-site period construction](../rainbow/single-branches-27.md) can place the surplus at the centroid and restore every whole branch.

For the other cuts, enumerate all possible rooted component sizes and tip counts in the suffix. An exterior with at most seven tips is already covered. There is also a direct test using the two independent parent colors. Sort the component sizes. Require the first size to be one or two and, whenever the accumulated preceding mass is greater than two, require the next component to be at most that preceding mass. The cut inequality permits a change of old parent color only when the next size exceeds the preceding mass. Hence every change occurs after a prefix of mass one or two. Two changes are impossible, since the first change after a mass of at least one leads immediately to mass at least three. If there is one change, take the entire first group as the extra attachment. If there is none, take the first component. An extra vertex leaves a main forest of 22, and either shape of mass two leaves a main forest of 21. The [one-leaf](../rainbow/common-leaf-22.md) and [two-vertex](../rainbow/common-pair-21.md) certificates apply.

For the remaining exteriors use typed witness streams, allowing padding at a tip of a largest component as in the [order-50 proof](order-fifty.md). The [811 additional profiles](order-51-audits/) cover **70,460,595** rooted forests, **2,022,158,716** verified labeling rows and **775,399,508,127** literal boundary assignments. Each stream was independently checked during generation. For every profile the rooted-tree recurrence and the exact count of permitted runs give independent totals. The [geometry checker](check_order_fifty_one.py) enumerates branch sizes first and assigns tips while tracking the maximum attainable mass for each tip budget. A second enumeration interleaves branch size and tips and keeps all attainable masses for each exact tip count. The two candidate sets agree, and each profile has a sufficient cut.

The [whole-tree replay](check_order_fifty_samples.py) joins each of the 36 forests of component types $(2,1),(2,1),(2,1),(4,3),(13,2)$ to three 28-vertex cores at all 729 allowed parent assignments. Direct enumeration of every vertex and edge bin verified **78,732** trees of order 51, including 11,988 with exactly seventeen leaves.

~~~bash
set -euo pipefail
out=$(mktemp -d)
r=research/rainbow
c=research/census
python3 -B -m research.census.check_order_fifty_one
c++ -O3 -std=c++17 -Drainbow_witness=reference_witness -c "$r/search.cpp" -o "$out/ref.o"
c++ -O3 -std=c++17 "$r/spine_generate.cpp" "$r/leaf_search.cpp" "$out/ref.o" -o "$out/generate"
c++ -O3 -std=c++17 -pthread "$r/spine_verify.cpp" -o "$out/verify"
"$out/generate" 27 0 1 "$out/sample" --typed-restarts 2,1 2,1 2,1 4,3 13,2
python3 -B -m research.census.check_order_fifty_samples "$out/sample" --order 51
for cert in "$c"/order-51-audits/*-restarts.txt; do
  id=$(basename "$cert" .txt)
  awk -F '  ' '{print $3}' "$cert" > "$out/$id.profiles"
  python3 -B "$c/stream_leaf_profiles.py" 27 "$out/$id.profiles" "$out/generate" "$out/verify" "$out/$id" --workers 2 --restarts
  cmp "$out/$id/manifest.txt" "$cert"
done
~~~
