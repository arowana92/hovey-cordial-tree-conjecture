# Four possible least orders within seventeen leaves

**Theorem (computer-assisted).** If any tree with at most seventeen leaves fails ordinary 27-cordiality, the smallest order of a failure in that class belongs to **53, 54, 80, 81**. Thus checking just those orders suffices for the whole class. The [order-52 theorem](order-fifty-two.md) covers all smaller orders. Within sixteen leaves the existing reduction leaves only 53 and 54. [Sixteen-leaf proof](sixteen-leaf-corridor.md)

Suppose the least order in the class exceeds 54. It must then occur at exactly seventeen leaves. Write the order as $27m+1+t$. The short-forest and leaf-deletion reductions give $22\le t\le26$. Every smaller tree needed for these reductions is a connected subtree or results from compressing a piece between two ports. Both operations preserve the bound on leaves. [Short-forest reduction](../rainbow/twenty-one-free.md) · [Least-order reductions in a leaf class](sixteen-leaf-corridor.md)

At any joint, a union of branches with at most seven original leaves has order at most $t-1$. Otherwise its size-ordered preorder has a suffix of $t$ vertices with at most seven tips, which can extend a labeling of the remaining tree. The sum of the six longest terminal arm lengths is at most $t-1$ by the independent-path theorem. Terminal arms at one joint also have total length at most $t-1$, even if more than six meet there. No edge side has order congruent to zero or to the total order modulo 27. For $t=22,23,24,25,26$ the forbidden intervals of exact side orders start respectively at $22,21,22,26,27$ and all end at 27. At $t=22,23,24$ the forbidden branch-union orders at a joint include respectively $\{22\},\{21,22\},\{22\}$. These cuts use smaller connected trees. [Seven tips](../rainbow/seven-tip-27.md) · [Terminal paths](../rainbow/terminal-paths.md) · [Independent paths](ring-order.md) · [Side and union restrictions](../rainbow/common-pair-22.md) · [Residue 23](../rainbow/common-site-27.md) · [Residue 24](../rainbow/common-pair-21.md) · [Affine and divisible cuts](../prime/four-deficits.md)

## The central path

Mark each edge with at least eight original leaves on each side. If there are no such edges, a leaf centroid has at most seven leaves in every branch. Three groups of at most seven leaves would give order at most $1+3(t-1)<55+t$, the first possible order above 54 at this residue. Among all partitions of 17 into parts at most seven, the only branch-tip multisets that cannot be packed into three such groups are $(4,4,4,5)$ and $(1,4,4,4,4)$. Both fit four groups, so only order $55+t$ needs checking. The certified local suffix cuts cover every remaining profile there. [Local cut criterion](leaf-profile-cuts.md#selecting-a-cut-from-the-numerical-branch-data)

If there is a marked edge, all marked edges form a path. The edges between any two marked edges are marked, and three directions with eight leaves each are impossible. At each end of this path, the outward branches have at least eight leaves altogether, and each has at most seven. There are just two possibilities. The ends have eight and nine leaves with only degree-two vertices between them, or each has eight leaves and a single intervening joint has one off-path terminal arm. This follows by counting the original leaves outside the two ends. Every bare corridor has at most 20 interior degree-two vertices. [Bare-path bound](dense-cycles.md#consequences-for-tree-order)

Record an end by the order and tip count $(s,j)$ of each outward branch. Write $A$ for their total order, excluding the joint, and $H$ for their total tip count. They split into two groups with at most seven tips each. For $H=8$, separate any one branch. For $H=9$, separate a branch with at least two tips, or choose two singleton-tip branches when all counts are one. Hence $A\le2(t-1)$. Test all seven-tip subcollections, the terminal lengths, forbidden sides and unions, and established suffix cuts from the published forest catalogs. If the next corridor has $e$ interior vertices, also exclude an end whenever $i=26-A+s$ satisfies $2\le i\le e$ and $1\le H-j\le6$. The joint, the other branches and $i$ corridor vertices give a removable 27-vertex piece. Closing its two ports produces a cycle of length at least three with $H-j$ leaves. [One side leaf](one-leaf-period.md) · [Two through six side leaves](few-leaf-rings.md)

For the plain path the order is $A+B+2+e\le4t+18$, with $B$ the other outward mass. All side orders $A+1,\ldots,A+e+1$ and their complements must be allowed. The end and corridor tests exclude all orders above 54 other than 80 and 81.

For the intervening joint write $e,f$ for the two corridor interiors and $d$ for its terminal arm length. The order is $A+B+3+e+f+d\le5t+33$, since $d+5\le t-1$ by the six-arm bound. Check the side intervals at both ends. If $1+d+e+f\ge27$ and $27-d\ge3$, the center joint, its arm, and initial corridor segments give the one-leaf replacement. Also test the arm of type $(d,1)$ against each end branch, taking one whole branch and a suffix of the other under the seven-tip inequality. [Opposite-end suffix proof](sixteen-leaf-corridor.md#an-eight-to-eight-path)

## The two pieces left by the last test

The two ends can sometimes each supply a connected piece of order 27 while leaving a terminal path on the outside. At an end of mass $A$, let $l$ be a guaranteed terminal length, the largest order of a one-tip branch or at least one. Take
$$
                z=\max(1,A-26),\qquad i=\max(0,27-A).
$$
If $z\le l$ and $i\le e$, retain the outermost $z$ terminal vertices. The rest of this end, its joint and $i$ corridor vertices give exactly $A+1-z+i=27$ vertices. They are connected and have just two edges to the outside. Apply this at both ends, preserving the center joint and its third arm. Compress both pieces to edges. The residual tree has three leaves and at most two effective edge offsets. Its order is unrestricted by the [three-leaf offset theorem](../biased/three-leaf-offsets.md). Expanding the two pieces restores an ordinary cordial labeling of the original tree. Their isolated bijective rainbow labelings exist by the [integer census](README.md).

| $t$ | Central profiles checked | Eight-tip end profiles | Nine-tip end profiles | Pairs requiring the two-piece join |
|---:|---:|---:|---:|---:|
| 22 | 49 | 17,163 | 37,520 | 0 |
| 23 | 8 | 22,203 | 49,147 | 0 |
| 24 | 36 | 28,367 | 63,578 | 0 |
| 25 | 334 | 35,887 | 81,394 | 39 at order 107 |
| 26 | 526 | 44,933 | 103,134 | 386 at order 108 |

The [checker](check_seventeen_leaf_corridor.py) constructs each end inventory twice, once partitioning the tip count and tracking maximum attainable masses, and once enumerating masses with a separate subset calculation. It checks every attainable order in the proved ranges except 80 and 81. The last column counts profile pairs with their corridor and arm lengths, allowing both orientations at equal outward mass. A [whole-tree geometry check](check_seventeen_leaf_shapes.py) classified 900 trees by directly counting leaves on both sides of each edge. It found 408 with no marked edge, 155 plain marked paths and 337 with an intervening arm. In 180 cases it independently trimmed the two connected pieces, found their actual boundary edges, and verified that their compression left exactly three leaves.

~~~sh
python3 -B -m research.census.check_seventeen_leaf_corridor
python3 -B -m research.census.check_seventeen_leaf_shapes
~~~
