# Reducing sixteen leaves to two orders at 27 labels

**Theorem (computer-assisted).** Every tree with at most sixteen leaves and at most 52 vertices is 27-cordial. If any tree with at most sixteen leaves fails ordinary 27-cordiality, a least-order failure within that class has **53 or 54 vertices**. Within fourteen leaves only order 54 remains. The connected-prefix theorem already covers every tree with at most thirteen leaves. [Leaf profile certificates](leaf-profile-cuts.md)

Write the least order as $27m+1+t$. The [short-forest proof](../rainbow/twenty-one-free.md) leaves $22\le t\le26$. Suppose the order exceeds 54. The [three-group reduction](../rainbow/few-leaves.md) and [seven-tip certificate](../rainbow/seven-tip-27.md) require exactly sixteen leaves. At every vertex, any union of branches with at most seven leaves has mass strictly below $t$, since its last $t$ vertices in size-ordered preorder would otherwise give a certified cut. A connected core has at most as many leaves as the original tree.

## Four groups at a centroid

First suppose no edge splits the leaves eight to eight. Group the branches at a leaf centroid as in the [balanced-path proof](leaf-corridor.md). Three or fewer groups would give $n-1\le3(t-1)$, impossible. There must be four groups of exactly four leaves each. If a group contains two or more original branches, split it into two nonempty subgroups. Each has at most three leaves. Merge them into two of the other groups to obtain three groups of at most seven leaves, again impossible. Thus there are four original branches and $n-1\le4(t-1)$, leaving $n=55+t$. Each branch has four tips and order between 5 and $t-1$. For every sorted quadruple with the required total, the published profile cuts cover its geometry. The checker also allows extending a tip of any largest component to use a published profile of larger mass. All assignments remain valid under this padding. [Profile cut proof](leaf-profile-cuts.md) · [Padding lemma](../rainbow/ordered-cut.md)

## An eight-to-eight path

Otherwise the equally splitting edges form a path with $h<27$ internal degree-two vertices. Its two endpoints have outward branches of eight tips in total, and every proper subset has at most seven tips. If $A$ is the sum of the outward branch orders at one end, then $A-\min s<t$ for its branch sizes $s$. In particular $A\le2(t-1)$. Write $B$ for the mass at the other end. The balanced-path bound gives $n=55+t$ or $82+t$, with $h=n-A-B-2$. The side orders on the path are $A+1,\ldots,A+h+1$. Exclude an order congruent to zero or $n$ modulo 27 using the [divisible-cut theorem](../divisible-cuts.md).

As in the [fourteen-leaf calculation](leaf-corridor.md), test each endpoint for a certified cut of mass $t$. At an outgoing branch $(s,j)$ of order $s$ and $j$ tips, there is also an edge replacement if $i=26-A+s$ satisfies $2\le i\le h$ and $1\le8-j\le6$. It uses the endpoint, the other outgoing branches, and $i$ internal path vertices. The closed cycle has length at least three. Use the [one-leaf replacement](one-leaf-period.md) for one leaf and the [harmonious ring certificates](few-leaf-rings.md) for two through six. Compressing it to an edge creates no new leaves in the smaller tree.

Two further operations finish the calculation.

* **Two 27-vertex pieces.** Among the remaining pairs $A,B\ge27$. Indeed, if $A\le26$, the side orders reach 27 since $A+h+1=n-B-1\ge27$ by $B\le2(t-1)$. On the $A$ side, if a terminal arm contains at least $A-26$ vertices, leave its outermost $A-26$ vertices as a path. All other vertices on this side, including the endpoint, form a connected 27-vertex tree with two ports. A one-tip outward branch is a terminal arm of its full recorded length. Even without one, every leaf gives an arm of length at least one. If the test succeeds at both ends, compress the two trees. The residual path consists of the two terminal paths and the original $h$ internal vertices. It has order $n-54$ and at most two effective edge offsets. When $h=0$ both trees occur in series on the same edge. Both pieces have bijective rainbow labelings by the order-27 census. The [two-offset path and expansion theorem](../biased/sparse-path-offsets.md) restores them and proves cordiality.
* **A cut from opposite ends.** Take an entire branch of size $a$ at one end, and the last $z=t-a$ vertices of a branch of size $s$ at the other, where $0<z\le s$. Require that their two original tip counts sum to at most seven. When $z<s$ and the second branch has $j$ tips, its suffix has at most $\min(j,z)$ boundary runs. Pad the whole first branch by $26-t$ vertices at a tip. If its new size is at least $z+\min(j,z)$, it can follow the suffix as a new boundary run, whatever the two endpoint labels. When $z=s$, there are two whole branches. Pad a larger one. It only needs to become strictly larger than the other for an independent boundary color. In either case the [sharp boundary inequalities](../rainbow/ordered-cut.md#which-colored-forests-actually-occur) hold for the padded forest. The seven-tip theorem labels it, and restricting to the original vertices extends the connected smaller core.

## Finite geometry check

The [checker](check_sixteen_leaf_corridor.py) generates the endpoint profiles both by partitions of the tip count and by a decreasing-size recursion which records all attainable masses for each tip budget. It requires equality of the two complete sets. It uses only the twelve- and thirteen-leaf manifests, plus the fourteen- and fifteen-leaf ones at orders 50 and 51. The separate [manifest checks](leaf-profile-cuts.md#independent-enumeration-and-labeling-checks) verify their shape counts and labeling coverage.

| $t$ | Four-branch profiles | Endpoint profiles | Two-piece path reductions at $55+t$ | Opposite-end cuts at $55+t$ |
|---:|---:|---:|---:|---:|
| 22 | 15 | 17,163 | 0 | 0 |
| 23 | 27 | 22,203 | 0 | 0 |
| 24 | 47 | 28,367 | 1,365 | 850 |
| 25 | 72 | 35,887 | 2,683 | 1,752 |
| 26 | 108 | 44,933 | 8,375 | 3,173 |

The last two columns count the pairs left after the local cuts, ring replacements, and divisible edges. Equal endpoint masses permit both orientations in the count. At $82+t$ the earlier tests remove all pairs for every $t$. This proves the reduction for ordinary cordiality. The path compression can change the order in which vertices become available, so the existing prefix-growth theorem retains its separate hypotheses.

~~~sh
python3 -B -m research.census.check_sixteen_leaf_corridor
~~~


## Orders 50 through 52

The existing proof covers up to fifteen leaves at all three orders. Suppose there are exactly sixteen leaves and let $t=n-28$. A union of branches at a vertex with at most seven tips and mass at least $t$ gives an ordered suffix cut of $t$ vertices. Its connected 28-vertex core is cordial. Also, if the terminal paths at any one joint contain at least $t$ vertices, remove a size-ordered suffix of those paths. Its possible partial arm is uniquely shortest and the [terminal path certificate](../rainbow/terminal-paths.md) reattaches it. At order 50, any union of whole branches at a joint of mass exactly 22 works by the [common-parent theorem](../rainbow/common-site-27.md).

If there is no eight-to-eight leaf split, select a leaf centroid. All its branches have at most seven tips. Record their orders and tip counts, discarding every profile already excluded by a seven-tip union of mass at least $t$. The [geometry checker](check_sixteen_base.py) obtains the complete remaining set in two ways, first ordering by branch size and then by tip count. In the first recursion it tracks every attainable mass for each tip budget. In the second it keeps only the greatest attainable mass. For every profile, it checks a terminal-path cut, a common-parent cut at 50, or a [certified ordered suffix](leaf-profile-cuts.md) using the current manifests, including padding of a largest component.

If an eight-to-eight path exists, keep the earlier notation $A,B,h$. If $A,B\le26$, the sequence of side orders from $A+1$ through $n-1-B$ meets $[n-27,27]$. Both resulting pieces then have at most 27 vertices and the [affine cut theorem](../prime/four-deficits.md) gives ordinary cordiality. Otherwise select an endpoint of outward mass $A\ge27$. Its profile obeys $A\le2(t-1)$ by the seven-tip union bound and $A\le t+18$ since $B\ge8$. For every such endpoint profile, the same checker finds a cut there, regardless of the far endpoint. Two independent recursions agree on all the heavy endpoint profiles.

| Order | Central profiles | Heavy endpoint profiles | Additional certificate profiles | Rooted forests | Witness rows | Literal boundary assignments |
|---:|---:|---:|---:|---:|---:|---:|
| 50 | 9,504 | 969 | 151 | 7,516,917 | 121,303,563 | 49,499,842,527 |
| 51 | 17,351 | 1,778 | 482 | 24,264,177 | 865,895,881 | 223,478,853,795 |
| 52 | 31,370 | 3,386 | 1,118 | 52,602,355 | 1,806,879,253 | 485,545,258,575 |

The witness streams were independently verified for distinct labels, distinct actual weights and complete boundary coverage. The geometry checker recomputes the exact forest and literal input counts of the [order-50](leaf-profile-audits/16-50.txt), [order-51](leaf-profile-audits/16-51.txt) and [order-52](leaf-profile-audits/16-52.txt) manifests. At order 52 a [whole-tree replay](check_order_fifty_samples.py) attached all ten forests of one profile to three different 28-vertex cores under every permitted boundary assignment. Counting actual vertex labels and endpoint sums verified 21,870 joins, including 720 with exactly 16 leaves. These three orders require only ordinary cordiality on a joined pair of small trees. The prefix and marked-leaf results retain the bounds in the [separate induction](leaf-profile-cuts.md).

~~~bash
set -euo pipefail
out=$(mktemp -d)
r=research/rainbow
c=research/census
c++ -O3 -std=c++17 -Drainbow_witness=reference_witness -c "$r/search.cpp" -o "$out/ref.o"
c++ -O3 -std=c++17 "$r/spine_generate.cpp" "$r/leaf_search.cpp" "$out/ref.o" -o "$out/make"
c++ -O3 -std=c++17 -pthread "$r/spine_verify.cpp" -o "$out/check"
for n in 50 51 52; do
  cert="$c/leaf-profile-audits/16-$n.txt"
  awk -F '  ' '{print $3}' "$cert" > "$out/profiles"
  flags=()
  if [[ $n != 51 ]]; then flags+=(--restarts); fi
  python3 -B "$c/stream_leaf_profiles.py" 27 "$out/profiles" "$out/make" "$out/check" "$out/a$n" --workers 2 "${flags[@]}"
  cmp "$out/a$n/manifest.txt" "$cert"
done
"$out/make" 27 0 1 "$out/sample" --typed-restarts 1,1 1,1 5,1 5,2 5,2 7,1
python3 -B -m research.census.check_order_fifty_samples "$out/sample" --order 52
python3 -B -m research.census.check_sixteen_base
~~~
