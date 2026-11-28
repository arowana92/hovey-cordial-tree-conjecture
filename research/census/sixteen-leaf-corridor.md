# Reducing sixteen leaves to five orders at 27 labels

**Theorem (computer-assisted).** If a tree with at most sixteen leaves fails ordinary 27-cordiality, a least-order failure within that class has 50, 51, 52, 53 or 54 vertices. In particular, verifying just these five orders would prove ordinary 27-cordiality for the class at every order. With at most fifteen leaves the candidate orders are 52 through 54, and with at most fourteen leaves they are 53 and 54. The connected-prefix theorem already covers every tree with at most thirteen leaves. [Leaf profile certificates](leaf-profile-cuts.md)

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
