# Seventeen leaves at order 52

**Theorem (computer-assisted).** Every tree on 52 vertices with at most seventeen leaves is 27-cordial. A 52-vertex counterexample would therefore have **18 through 23 leaves**. The smaller leaf counts follow from the sixteen-leaf theorem. At least 24 leaves allow 24 of them to be restored on a 28-vertex core by Hall's theorem. All smaller tree orders already admit 27-cordial labelings. [Sixteen-leaf theorem](sixteen-leaf-corridor.md) · [Leaf restoration](../counterexample-bound.md#removing-leaves) · [Through order 51](order-fifty-one.md)

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
