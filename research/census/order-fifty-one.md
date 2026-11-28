# Ordinary 27-cordiality at order 51

**Computer-assisted theorem.** Every tree on 51 vertices is 27-cordial. Together with the [order-50 theorem](order-fifty.md), this proves 27-cordiality for every tree through order 51. A smallest counterexample, if one exists, has **52 through 216 vertices**. At order 52 the minimum is now 21 leaves. [Twenty-leaf proof](order-fifty-two.md#twenty-leaves) [Order bounds](ring-order.md) · [Sixteen-leaf theorem](sixteen-leaf-corridor.md)

For order 51, the sixteen-leaf theorem supplies the lower leaf counts. If a tree has at least 23 leaves, delete 23 of its original leaves and use the Hall extension on the resulting 28-vertex core. The proof below covers the six intermediate leaf counts, 17 through 22.

## Necessary centroid data

Suppose a 51-vertex tree has $17\le L\le22$ leaves and no 27-cordial labeling. Choose a vertex centroid. Write $(s,h)$ for the order and rooted tip count of a branch there. The orders sum to 50 and the tip counts sum to $L$. Each branch has at most 25 vertices. The [two-vertex attachment theorem](../rainbow/common-pair-21.md) excludes every edge side of order 21 through 27 and every union of branches at the centroid of order 21 or 22. Consequently the branch orders are at most 20.

A collection of centroid branches with at most seven tips must have fewer than 23 vertices. Otherwise its size-ordered suffix of 23 vertices gives a [seven-tip extension](../rainbow/seven-tip-27.md). No single branch can have more than $L-8$ tips, since the opposite edge side has order at least 31 and at most seven original leaves and admits the same suffix cut, rooted toward that branch. The centroid has degree at least three under the size bound.

Finally a branch with one tip is a terminal path of its full length $s$. Each of the $h$ original leaves in any other branch supplies at least one terminal vertex. If the six longest of these guaranteed lengths total at least 23, delete path suffixes totaling exactly 23. The [six-path theorem](ring-order.md#terminal-paths-with-independently-prescribed-parents) restores them with arbitrary old parent colors. These restrictions leave **5,125** numerical profiles at seventeen leaves, **11,289** at eighteen, **21,426** at nineteen, **36,683** at twenty, **56,586** at twenty-one and **80,606** at twenty-two.

For 22 leaves, let $r_1,r_2$ be the two largest counts of leaves at individual parents. The [independent-parent theorem](../rainbow/pinned-star.md#an-independently-chosen-leaf-parent) gives $2r_1+r_2\le19$, hence $r_1+r_2\le12$. The numerical profiles alone can violate this condition. Every order-one branch contributes a leaf at the centroid. For each other branch of order $s$ and tip count $h$, distribute its $h$ leaves as evenly as possible over its $s-h$ nonleaf vertices. This minimizes the sum of the largest count and the sum of the two largest counts: transferring one unit from a larger entry to a smaller one differing by at least two can only decrease each of these two quantities. Independently, the checker tests whether all leaf counts can fit under a common capacity with just one larger capacity. These tests agree and exclude **991 of the 80,606** necessary 22-leaf profiles. If four centroid branches have order greater than one, they contain four distinct leaves of the stripped tree. At least one of these avoids the three busiest parents. The same theorem gives $2r_1+r_2+r_3\le20$ in this case. Comparing the balanced distributions against a separate test with two exceptional capacities excludes 36 further profiles, leaving **79,579** after both restrictions. The sufficient-cut calculation below also covers the entire set of 80,606 independently of these restrictions.

## Sufficient cuts

If all one-tip branches at the centroid have total order at least 23, take their size-ordered suffix and apply the [terminal-path theorem](../rainbow/terminal-paths.md). Otherwise the checker tries a collection of whole branches and, if necessary, a suffix of one other branch, with 23 deleted vertices in total. For a partial branch of size $s$ and $h$ tips, require that its suffix size $z$ satisfy $0<z<s$ and each whole branch have size at least $\min(s,z+\min(z,h))$. This is the established [ordered-cut criterion](leaf-profile-cuts.md#selecting-a-cut-from-the-numerical-branch-data). For a whole-branch cut whose complement has at most seven tips among the 27 other branch vertices, the [common-site period construction](../rainbow/single-branches-27.md) can place the surplus at the centroid and restore every whole branch.

For the other cuts, enumerate all possible rooted component sizes and tip counts in the suffix. An exterior with at most seven tips is already covered. There is also a direct test using the two independent parent colors. Sort the component sizes. Require the first size to be one or two and, whenever the accumulated preceding mass is greater than two, require the next component to be at most that preceding mass. The cut inequality permits a change of old parent color only when the next size exceeds the preceding mass. Hence every change occurs after a prefix of mass one or two. Two changes are impossible, since the first change after a mass of at least one leads immediately to mass at least three. If there is one change, take the entire first group as the extra attachment. If there is none, take the first component. An extra vertex leaves a main forest of 22, and either shape of mass two leaves a main forest of 21. The [one-leaf](../rainbow/common-leaf-22.md) and [two-vertex](../rainbow/common-pair-21.md) certificates apply.

For the remaining exteriors use typed witness streams, allowing padding at a tip of a largest component as in the [order-50 proof](order-fifty.md). The [2,147 additional profiles](order-51-audits/) cover **153,587,535** rooted forests, **4,308,744,933** verified labeling rows and **1,694,227,867,641** literal boundary assignments. Each stream was independently checked during generation. Some mass-24 streams are also used in the separate [order-52 calculation for sixteen leaves](sixteen-leaf-corridor.md). For every profile the rooted-tree recurrence and the exact count of permitted runs give independent totals. The [geometry checker](check_order_fifty_one.py) enumerates branch sizes first and assigns tips while tracking the maximum attainable mass for each tip budget. A second enumeration interleaves branch size and tips and keeps all attainable masses for each exact tip count. The two candidate sets agree, and each profile has a sufficient cut.

The [whole-tree replay](check_order_fifty_samples.py) joins each of the 36 forests of component types $(2,1),(2,1),(2,1),(4,3),(13,2)$ to three 28-vertex cores at all 729 allowed parent assignments. Direct enumeration of every vertex and edge bin verified **78,732** trees of order 51, including 11,988 with exactly seventeen leaves. Repeating the check on the 40 forests of types $(3,1),(3,1),(7,1),(10,7)$ verified a further **87,480** joins, including 14,520 with exactly twenty-one leaves. At the types $(3,1),(10,1),(10,8)$, independent reconstruction verified 17,496 joins, including 3,296 with exactly twenty-two leaves. A separate build reproduced the digests of all 47 newly required streams containing at most 40 forests each, covering 1,066 forests and 46,022,418 literal boundary inputs.

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
"$out/generate" 27 0 1 "$out/sample21" --typed-restarts 3,1 3,1 7,1 10,7
python3 -B -m research.census.check_order_fifty_samples "$out/sample21" --order 51
"$out/generate" 27 0 1 "$out/sample22" --typed-restarts 3,1 10,1 10,8
python3 -B -m research.census.check_order_fifty_samples "$out/sample22" --order 51
for cert in "$c"/order-51-audits/*-restarts.txt; do
  id=$(basename "$cert" .txt)
  awk -F '  ' '{print $3}' "$cert" > "$out/$id.profiles"
  python3 -B "$c/stream_leaf_profiles.py" 27 "$out/$id.profiles" "$out/generate" "$out/verify" "$out/$id" --workers 2 --restarts
  cmp "$out/$id/manifest.txt" "$cert"
done
~~~
