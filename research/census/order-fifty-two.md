# Through nineteen leaves at order 52

**Theorem (computer-assisted).** Every tree on 52 vertices with at most seventeen leaves is 27-cordial. The [nineteen-leaf proof below](#nineteen-leaves) narrows a possible 52-vertex counterexample to **20 through 23 leaves**. The smaller leaf counts follow from the sixteen-leaf theorem. At least 24 leaves allow 24 of them to be restored on a 28-vertex core by Hall's theorem. All smaller tree orders already admit 27-cordial labelings. [Sixteen-leaf theorem](sixteen-leaf-corridor.md) · [Leaf restoration](../counterexample-bound.md#removing-leaves) · [Through order 51](order-fifty-one.md)

At 23 leaves, every tree whose leaf parents are all different is also 27-cordial. A possible failure at this leaf count has eight through twenty-two distinct parents. [Four-hole matching and restoration](../biased/four-hole-matchings.md)

## The centroid calculation

An edge with sides of orders 24 and 28, 25 and 27, or 26 and 26 already supplies a labeling. A hypothetical failure thus has a unique centroid, with every branch of order at most 23. Record each branch by its order and number of rooted tips. The orders sum to 51 and the tips sum to 17. A union of branches with at most seven tips has at most 23 vertices, since otherwise a size-ordered preorder suffix of 24 vertices would extend on the remaining 28-vertex core. Each branch has at most nine tips. If it had ten, the opposite side would have at most seven rooted tips when rooted at the centroid and could supply that suffix instead. The six largest guaranteed terminal arm lengths sum to at most 23. A one-tip branch guarantees its full length, and an $h$-tip branch guarantees at least $h$ arms of length one. [Single 24-vertex side](side24-at-52.md) · [Seven-tip extension](../rainbow/seven-tip-27.md) · [Six independent terminal paths](ring-order.md)

Two enumerations give the same **146,667** numerical centroid profiles under these restrictions. One assigns tips after partitioning 51 into branch orders. The other enumerates both together, recording which masses are attainable at a given tip count. For each profile at least one of the following restorations succeeds.

* If a singleton and a disjoint union of whole branches of order 24 are available, remove both. The remaining 27-vertex core admits a bijective rainbow labeling. The removed branches all attach to the centroid and include a singleton, so the odd-modulus extension applies. [Divisible-core singleton theorem](../rainbow/divisible-singleton.md)
* Terminal paths with total length at least 24 at the centroid allow a size-ordered suffix of length 24. A whole-branch exterior of size 24 also works when the other centroid branches have at most seven tips. In this case the common-site period construction places the surplus at the centroid and restores the exterior. [Terminal paths](../rainbow/terminal-paths.md) · [Common-site period construction](../rainbow/single-branches-27.md)
* Otherwise use whole branches and, if needed, a suffix of size $z$ of another branch of size $s$ with $h$ tips. Each whole branch must have size at least $\min(s,z+\min(z,h))$ when the suffix is partial. The ordered-cut inequality then applies to the exterior's old parent colors. Test all possible component sizes and tip counts in the suffix. At most seven tips suffice immediately. A rooted star together with singleton components also suffices, because the equal-sized singletons have one common parent color and the 24 vertices are within the short-star bound. The remaining exteriors use verified typed forest labelings, allowing padding at a tip of a largest component. [Suffix inequality](leaf-profile-cuts.md#selecting-a-cut-from-the-numerical-branch-data) · [Short star theorem](../rainbow/pinned-star.md#a-sharp-bound-for-shorter-attachments-at-every-composite-modulus) · [Ordered-cut condition](../rainbow/ordered-cut.md)

The additional 335 profiles cover **90,239,953 rooted forests**, **2,478,004,819 witness rows** and **581,499,116,235 literal boundary assignments**. These profiles supplement the order-51 and sixteen-leaf catalogs. Each row stream was independently checked during generation. A separate build regenerated all 83 streams with at most 40 forests, reproducing their digests and counts for 1,048 forests, 124,388 rows and 15,250,464 assignments. The geometry checker validates the manifest counts against separate shape and boundary recurrences. It requires an actual sufficient cut at every centroid profile. [Manifests](order-52-audits/) · [Geometry checker](check_order_fifty_two.py)

As a whole-tree check, the two forests of types $(1,1)^4,(3,1),(4,2),(13,1)$ were joined to three 28-vertex caterpillars at every admissible parent-color assignment. Recounting all vertex labels and all 51 endpoint sums verified **4,374 trees**, including 666 with seventeen leaves. [Whole-tree checker](check_order_fifty_samples.py)

~~~bash
set -euo pipefail
out=$(mktemp -d)
r=research/rainbow
c++ -O3 -std=c++17 -Drainbow_witness=reference_witness -c "$r/search.cpp" -o "$out/ref.o"
c++ -O3 -std=c++17 "$r/spine_generate.cpp" "$r/leaf_search.cpp" "$out/ref.o" -o "$out/generate"
c++ -O3 -std=c++17 -pthread "$r/spine_verify.cpp" -o "$out/verify"
python3 -B -m research.census.check_order_fifty_two
"$out/generate" 27 0 1 "$out/sample" --typed-restarts 1,1 1,1 1,1 1,1 3,1 4,2 13,1
python3 -B -m research.census.check_order_fifty_samples "$out/sample" --order 52
for cert in research/census/order-52-audits/*.txt; do
    id=$(basename "$cert" .txt)
    sed -E 's/^.*  ([0-9]+,[0-9]+.*)$/\1/' "$cert" > "$out/$id.profiles"
    python3 -B -m research.census.stream_leaf_profiles 27 "$out/$id.profiles" "$out/generate" "$out/verify" "$out/$id" --workers 2 --restarts
    cmp "$out/$id/manifest.txt" "$cert"
done
~~~

## Eighteen leaves

**Theorem (computer-assisted).** Every tree on 52 vertices with eighteen leaves is 27-cordial. This was the starting bound for the nineteen-leaf calculation below.

Use the unique centroid and record the orders and tip counts of its branches. Every branch has size at most 21. No subset of the branch orders may sum to 22 or 24, by the independent-pair and common-parent extensions. Two disjoint edge sides cannot have orders summing to 25, since their common middle would have 27 vertices and could be compressed to one edge on a 25-vertex tree. The seven-tip and six-terminal-path bounds from the preceding proof still apply. In particular, each branch has at most ten tips. The size-partition and branch-multiset enumerations agree on 18,105 numerical possibilities. [Independent pair](../rainbow/common-pair-22.md) · [Common-parent extension](../rainbow/common-site-24.md) · [One-edge offset on 25 vertices](../biased/one-offset-25.md)

The two-cut restriction also applies below the centroid. Each branch of order $s$ contains descendant subtrees of orders 1 and $s$. If the branch has just one tip, it is a path and contains every order through $s$. For any forced order $a$ in a different branch, forbid a descendant subtree of order $25-a$. A multiset recurrence counts possible tip numbers using only the remaining subtree orders. Independently, for each branch type, enumerate the inclusion-minimal sets of descendant orders. At a new root, take the union of the child sets and add the order of the whole tree. Supersets can be discarded because every cross-branch restriction forbids the simultaneous presence of two orders. Select one set per branch, rejecting complementary orders in different branches. These two calculations retain exactly the same **14,689** numerical profiles. Each deletion uses two disjoint actual sides in every tree with the rejected profile.

For the remaining profiles choose exterior mass 24 on a 28-vertex core, as in the preceding proof. If its ordered component sizes prohibit every change of parent color, use the 24-vertex common-parent theorem. If they permit a change only after the first two vertices, those vertices form one two-vertex path or two singleton components with a common parent color. The other 22 vertices have one common parent color. The independent-pair theorem covers both choices. The existing typed catalogs, including the 14-leaf order-54 and 15-leaf order-53 certificates, leave 201 profiles requiring an additional restoration. The [334 new forest types](order-52-audits/eighteen/24-restarts.txt) supply a successful cut in every one of those cases. [Full geometry and manifest checker](check_order_fifty_two_eighteen.py)

These certificates cover **60,880,962** rooted forests, **2,466,494,372** witness rows and **716,742,396,252** literal boundary assignments. All streams were verified during generation. A separate build regenerated all 35 types with at most 128 forests, reproducing the digests and counts for 1,925 forests, 169,801 rows and 39,646,179 assignments. A whole-tree replay reconstructed 42,930 ordinary 52-vertex trees, including 8,500 with exactly eighteen leaves, from ten sampled forests and three actual 28-vertex cores. It recounted all 1,030,320 nonempty restoration prefixes.

Use the same compiled generator and verifier as above. Run the following from the repository root.

~~~bash
python3 -B -m research.census.check_order_fifty_two_eighteen
cert=research/census/order-52-audits/eighteen/24-restarts.txt
awk -F '  ' '{print $3}' "$cert" > "$out/eighteen.profiles"
python3 -B -m research.census.stream_leaf_profiles 27 "$out/eighteen.profiles" \
    "$out/generate" "$out/verify" "$out/eighteen" --workers 2 --restarts
cmp "$out/eighteen/manifest.txt" "$cert"
"$out/generate" 27 0 1 "$out/sample18" --typed-restarts 1,1 3,1 5,1 5,1 5,2 5,2
python3 -B -m research.census.check_order_fifty_samples "$out/sample18" --order 52
~~~

## Nineteen leaves

**Theorem (computer-assisted).** Every tree on 52 vertices with nineteen leaves is 27-cordial. Since 24 or more leaves already suffice for leaf restoration, an order-52 counterexample must have **20, 21, 22 or 23 leaves**.

The two centroid enumerations give 28,781 numerical profiles at nineteen leaves. The descendant-order test retains 23,366. Of these, 246 need a cut outside the eighteen-leaf catalog. The geometry checker verifies that the 335 additional ordered forest profiles cover every one of those 246 profiles. All 335 now have [native verifier receipts](order-52-audits/nineteen/24-restarts.txt). They cover 54,036,955 rooted forests, 2,564,633,294 witness rows and 822,735,416,943 literal boundary assignments. The verifier checks vertex labels, internal sums and entering weights at the actual parent colors. The surviving 28-vertex core has a cordial labeling by the smaller-order theorem. Its forest certificate therefore extends it to the whole tree.

A separate build reproduced 32 stream hashes and verifier counts, covering 2,433 forests and 98,182 witness rows. Recounting all labels and edge sums gave 13,122 complete joins on 52 vertices, including 2,604 with exactly nineteen leaves, and verified all 314,928 nonempty restoration prefixes. The following command checks the nineteen-leaf stage from its published receipts.

~~~sh
python3 -B -m research.census.check_order_fifty_two_frontier --through 19
~~~

## A finite checklist for all remaining leaf counts

**Conditional reduction.** If the [2,568 listed forest profiles](order-52-frontier.profiles.gz) pass the ordered boundary test at 27 labels, every tree on 52 vertices is 27-cordial. The list contains only 24-vertex exteriors. Its profiles cover **360,580,312 distinct rooted forests** and **4,846,812,725,340 literal boundary assignments**. The geometry calculation is complete. The first 575 receipts reduced the list to 1,993 entries. [Alternative choices of cuts and further receipts](#a-shorter-checklist) leave 1,792 outstanding.

For each remaining leaf count $L$, enumerate the branches at the unique centroid by order and number of rooted tips. The restrictions proved above continue to apply. Every branch has at most 21 vertices. No subcollection has total order 22 or 24, and two disjoint descendant subtrees in different branches cannot total 25. A subcollection with at most seven tips has total order at most 23. A single branch has at most $L-8$ tips, since otherwise the other branches could supply a 24-vertex ordered suffix with at most seven tips. The six longest guaranteed terminal paths total at most 23. These conditions are necessary for a counterexample. A profile surviving them may still have every represented tree cordial.

Two enumerations give the same numerical inventories. One first partitions 51 by branch orders. The other grows order-and-tip pairs in descending order and tracks subset sums for each tip budget. It can discard a partial list as soon as it contains a forbidden order sum. Next enumerate the inclusion-minimal sets of descendant orders within each branch, as in the eighteen-leaf calculation. At least one choice of a set per branch must avoid complementary orders summing to 25 in different branches.

| Leaves | Numerical profiles | Survive descendant-order test | Outside earlier cut catalog | Additional forest profiles | Additional forests |
|---:|---:|---:|---:|---:|---:|
| 19 | 28,781 | 23,366 | 246 | 335 | 54,036,955 |
| 20 | 42,714 | 35,046 | 1,478 | 627 | 102,632,172 |
| 21 | 59,150 | 49,124 | 4,563 | 396 | 57,101,507 |
| 22 | 77,866 | 65,496 | 10,166 | 776 | 94,095,197 |
| 23 | 97,391 | 82,864 | 18,901 | 434 | 52,714,481 |

The last two columns are incremental. A row can use all forest types from earlier rows. The [checker](check_order_fifty_two_frontier.py) starts from the published cut catalogs, including the eighteen-leaf certificates. For each profile still outside those catalogs it exhibits the existence of a cut by trying subcollections of whole branches, with an optional size-ordered suffix of one further branch. For that cut it requires coverage of **every** possible exterior order-and-tip profile and of all permitted parent colors. The 28-vertex connected core is already known to be 27-cordial. Verifying the proposed additional rows would therefore complete the proof at this order. The nineteen-leaf stage now has complete receipts.

As a check on the restoration, one forest from each of five proposed profiles was joined to three explicit 28-vertex trees. Recounting all labels and sums directly verified 10,935 52-vertex joins. These examples test the construction on actual trees.

A three-edge cut also gives unconditional labelings when the 27-vertex middle closes to a unicyclic graph with zero or two through six leaves. Explicit examples cover each remaining leaf count and avoid the two-side and whole-branch size tests. [Three-side theorem and original-tree witnesses](three-side-cuts.md)

The [240 additional receipts](order-52-audits/frontier/24-restarts.txt) for the later leaf counts cover 39,200,909 forests and 433,608,260,157 literal boundary assignments. A separate build reproduced 24 of their stream hashes. Together with the nineteen-leaf stage these initially left **1,993 sufficient profiles**, representing **267,342,448 forests** and **3,590,469,048,240 literal boundary assignments**. At that point the incremental counts at 20, 21, 22 and 23 leaves were 555, 327, 736 and 375. These numbers count sufficient tests.

Run the geometry separately from the potentially much longer witness census. The generator and verifier build commands are given above. Each line in the compressed list begins with the leaf count that first uses the profile.

~~~bash
set -euo pipefail
python3 -B -m research.census.check_order_fifty_two_frontier --write-pending "$out/frontier.profiles"
python3 -B research/census/stream_leaf_profiles.py 27 "$out/frontier.profiles" "$out/generate" "$out/verify" "$out/frontier" --restarts --workers 2
python3 -B -m research.census.check_order_fifty_two_frontier --receipts "$out/frontier/manifest.txt"
~~~

To regenerate the three manifests, extract their profiles and use the restart generator and independent verifier described above.

~~~bash
for stage in nineteen frontier twenty; do
    cert="research/census/order-52-audits/$stage/24-restarts.txt"
    awk -F '  ' '{print $3}' "$cert" > "$out/$stage-known.profiles"
    python3 -B -m research.census.stream_leaf_profiles 27 "$out/$stage-known.profiles" "$out/generate" "$out/verify" "$out/$stage-known" --restarts --workers 2
    cmp "$out/$stage-known/manifest.txt" "$cert"
done
~~~

## A shorter checklist

**Conditional reduction.** Verifying the [1,815 indicated profiles](order-52-reduced.profiles.gz) suffices for every tree on 52 vertices to be 27-cordial. The first 289 alone suffice to extend the unconditional result to twenty leaves. The full list covers 263,558,863 rooted forests and 3,536,873,791,551 literal boundary assignments.

Start with the earlier catalog and all 575 public receipts above. For each centroid profile, several selections of whole branches and a partial size-ordered branch can be available. Each choice requires its own set of exterior profiles. A forest test used in a different leaf-count stage of the original list may permit a cheaper selection at this centroid. For example, fifteen of the 289 tests in the new twenty-leaf stage originally appeared at higher leaf counts. Across all four stages the choice of cuts saves 178 tests and 53,595,256,689 literal boundary assignments.

| Leaves | Additional profiles | Cumulative profiles | Additional forests | Additional boundary assignments |
|---:|---:|---:|---:|---:|
| 20 | 289 | 289 | 65,852,198 | 757,255,004,658 |
| 21 | 415 | 704 | 56,177,338 | 732,523,076,424 |
| 22 | 364 | 1,068 | 89,727,804 | 1,264,263,579,108 |
| 23 | 747 | 1,815 | 51,801,523 | 782,832,131,361 |

**Verified portion.** A [further 23 receipts](order-52-audits/twenty/24-restarts.txt) cover 13,801,306 forests, 532,345,037 witness rows and 136,330,653,042 boundary assignments. All fifteen tests borrowed from higher leaf counts for the twenty-leaf stage passed. The receipts cover 22 of the first 289 entries and one of the next 415. This leaves **267 tests for twenty leaves** and **1,792 for all leaf counts**, the latter covering 249,757,557 forests and 3,400,543,138,509 literal boundary assignments. A separate build regenerated eight of the 23 streams, covering 35,496 forests and 2,689,620 witness rows. All eight hashes matched.

The [proof checker](check_order_fifty_two_frontier.py) starts afresh from the two numerical centroid enumerations. At each leaf count it tests every surviving profile with the published receipts and just the conditional entries available through that stage. For each successful cut all eligible exterior shapes and boundary changes are covered. The verification establishes sufficiency without requiring an optimal choice of cuts.

~~~bash
python3 -B -m research.census.check_order_fifty_two_frontier --reduced --through 20
python3 -B -m research.census.check_order_fifty_two_frontier --reduced --write-pending "$out/reduced.profiles"
python3 -B -m research.census.stream_leaf_profiles 27 "$out/reduced.profiles" "$out/generate" "$out/verify" "$out/reduced" --restarts --workers 2
python3 -B -m research.census.check_order_fifty_two_frontier --reduced --receipts "$out/reduced/manifest.txt"
~~~
