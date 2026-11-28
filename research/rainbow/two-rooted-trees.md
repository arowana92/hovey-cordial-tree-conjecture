# Growing across two independently attached rooted trees

**Theorem (computer-assisted).** Fix any 27-cordial labeling of a nonempty tree of order zero or one modulo 27. Attach two rooted trees by one edge each, at any two old vertices, possibly the same. If the rooted trees have at most seven tips between them, their orders are unrestricted. Either root may be chosen as the first new vertex. There is a parent-first order starting there and a single extension of the old labels that is cordial on every prefix. One may independently prescribe an additive offset on each of the two entering edges. A tip is a vertex with no children, including a singleton root.

For example, any tree with at most seven leaves can start at a specified degree-two vertex even with arbitrary offsets on both incident edges. Take that vertex as a singleton core and root each of the two sides at its neighbor. In an ordinary smallest 27-label counterexample of order $n$, two disjoint pendant subtrees with at most seven rooted tips in total cannot leave a nonempty connected complement of order zero or one modulo 27. In particular the two sides cannot total 24 at order 52, 26 at order 53, or 27 at order 54. The unrestricted 27-label conjecture remains open.

## The first block

Write $E$ for the number of new vertices. A bridge offset can always be added to its old parent label when computing its weight. Call the result the effective parent color.

**Core of order one modulo 27, $E\le26$.** Translate the surplus label to zero. It suffices to find distinct nonzero labels and distinct new edge sums. Their restrictions work in every parent-first order. With one component, or two of different sizes, the [seven-tip forest theorem](seven-tip-27.md) applies with arbitrary effective parent colors. Indeed, the larger of two unequal sizes is at least the smaller plus one, precisely the [two-run condition](ordered-cut.md#which-colored-forests-actually-occur). For equal sizes with $E<26$, lengthen one tree at a tip by one vertex. The sizes are now different, and the new total is at most 26. Restrict its labeling.

This leaves exactly two trees of order 13. The [twelve certificate streams](two-thirteen-27.sha256) cover all 736,645 unordered pairs of rooted shapes with at most seven tips combined. Their 15,938,206 witness rows cover **537,014,205 literal inputs**, all $27^2$ ordered parent-color pairs on every shape. This also covers identical trees and coincident attachment vertices.

**Core of order zero modulo 27, $E\le27$.** The old vertex bins are uniform and there is one deficient edge weight $D$. For the chosen first root at effective parent color $a$, assign $x=D-a$. This fills the edge deficit and makes $x$ the unique vertex surplus. When both components are present, temporarily join their roots by an edge, retaining all their internal edges. This tree on $E$ vertices has exactly as many leaves as the two rooted trees have tips. If the second effective parent color is $b$, put offset $b-x$ on the temporary edge. The [one-offset rainbow theorem](../biased/period-ports-27.md#a-certificate-on-27-vertices) gives an injective labeling with distinct adjusted edge sums, by padding to order 27 when necessary. Translate the labeling so the chosen root has label $x$. All adjusted weights shift together. The temporary edge incident to the second root of label $y$ now weighs $x+y+(b-x)=b+y$, precisely its actual entering weight. All remaining labels avoid $x$ and all remaining weights are distinct. Any parent-first continuation works. With one component the [fixed-site theorem](cut-growth.md#growing-from-a-fixed-site) applies. A common offset on the entering edge is absorbed in its effective parent color, or one may label the component injectively using the [integer census](../census/README.md) and translate its root to $x$.

## Arbitrary orders

Keep the initial core and the designated first root fixed. Induct on $E$, allowing one component to be absent. Write $t=(n-1)\bmod 27$ for the final order $n$. Outside the first-block cases, if $t=0$, delete a new tip other than the designated first root. There is such a tip, since $E>1$. Induct, then label the deleted vertex to fill the unique edge deficit of the divisible-order intermediate tree.

If $t>0$, then $E\ge27+t$ for an initial one-surplus core, and $E\ge28+t$ for an initial divisible core. Thus $E>2t$ and one component has **more** than $t$ vertices. Visit that component in preorder with children sorted by nondecreasing subtree size. Remove its last $t$ vertices, retaining both original roots whenever present. The retained forest has at most the original number of tips, since each of its tips extends to a different original tip. Apply induction. The intermediate tree has order one modulo 27. The removed suffix obeys the ordered boundary inequalities, has at most seven tips, and now meets its parents at their actual prescribed colors. The seven-tip theorem restores it in any parent-first order. This completes the induction and preserves the first-root choice.

## A reduction for other moduli and more sites

Suppose the ordered forest test at modulus $k\ge3$ holds through $q$ tips. From a fixed **one-surplus** core, the same two-tree induction for $q$ combined tips uses only that test, except for two components each of size $(k-1)/2$ when $k$ is odd. In particular at **every even modulus** with such a test, the two-tree conclusion from a one-surplus core needs no equal-size census. This gives 16 tips at 26 labels, 14 at 24, and five at both 28 and 30. [26-label certificate](twenty-six.md) · [24-label certificate](twenty-four.md) · [28- and 30-label certificates](few-leaves.md)

More generally, attach a forest with at most $q$ tips at at most $d\ge2$ old sites, with ordinary entering edges. For a fixed initial phase (zero or one), unbounded-order existence of a prefix-cordial extension reduces to testing the cases with $t>0$ in which **every site's attached mass is less than $t$**. Indeed, if some site carries at least $t$ vertices, size-order the entire forest at that site as the children of its old parent, remove its last $t$, and use induction followed by the ordered test. The same argument handles a suffix equal to the entire site's forest. When $t=0$ a terminal deletion works. No order below the fixed core is needed. The total mass of a remaining test is at most $d(k-2)$. At $k=27$ and three sites the maximum test masses are 53 from a one-surplus core and 54 from a divisible core. To see the sharper bounds, write $E=27j+t$ or $27j+t+1$, respectively. The inequality $E\le3(t-1)$ forces $j\le1$, since $t\le26$. This last reduction supplies finite tests. Their success at three sites is open here.

## Independent verification

The generator gives each root its own unrestricted color group. The [native verifier](spine_verify.cpp) reads the actual vertex labels, checks internal sums, reconstructs the two entering weights, and checks all parent-color assignments up to simultaneous multiplication by units. It accepts each canonical forest exactly once and independently checks the number with the specified tip counts. A [Python checker](check_two_rooted_trees.py) counts the unordered shape pairs by integer partitions, directly constructs 2,187 whole trees from sampled rows and recounts all 56,862 new prefixes. It also checks that the weaker equal-color stream for two paths is rejected. A separate growth replay on fixed path cores of orders 1, 27, 28, 54 and 55 checks 280 growth orders and 14,720 prefixes with independently chosen bridge offsets, including both choices of first root. These sample replays exercise the construction. The exhaustive certificate closes the equal-halves case in the induction.

Run from the repository root in Bash. The full audit streams the rows directly into the verifier.

~~~bash
set -euo pipefail
out=$(mktemp -d)
r=research/rainbow
c++ -O3 -std=c++17 -fPIC -Drainbow_witness=reference_witness -c "$r/search.cpp" -o "$out/ref.o"
c++ -O3 -std=c++17 "$r/spine_generate.cpp" "$r/leaf_search.cpp" "$out/ref.o" -o "$out/generate"
c++ -O3 -std=c++17 -pthread "$r/spine_verify.cpp" -o "$out/verify"
c++ -O3 -std=c++17 -fPIC -shared "$r/leaf_search.cpp" "$out/ref.o" -o "$out/search.so"
awk -F '  ' '{print $3}' "$r/two-thirteen-27.sha256" > "$out/profiles"
python3 -B research/census/stream_leaf_profiles.py 27 "$out/profiles" "$out/generate" "$out/verify" "$out/accepted" --two-roots --workers 2
cmp "$r/two-thirteen-27.sha256" "$out/accepted/manifest.txt"
python3 -B -m research.rainbow.check_two_rooted_trees "$r/two-thirteen-27.sha256" --samples "$out/generate" "$out/verify" --growth "$out/search.so"
~~~
