# Uniform increments with arbitrarily many unequal branch populations

Consider a joint with $m\ge3$ branching neighbors, each with a positive number of leaf children, and $P\ge0$ direct leaves. Let $n$ count the free vertices, excluding the joint.

**Theorem.** Choose a center with largest child population $D$, and partition the other centers into pairs and, if necessary, one triple. If the gcd of the child counts **within each group** is at least $4m^2$, the attachment has a uniform increment at every modulus dividing $n$. At every modulus it extends any prescribed cordial labeling of a core of divisible order. The distinct groups may have unrelated gcds. There is no bound on the degree or on the ratios of the counts.

In particular, on **every ray of positive integer child populations** the conclusions hold for every common multiplier $t\ge4m^2$, with any number of direct leaves. The full construction gives an integer labeling at joint zero for which all free labels and all new weights fill exactly the same consecutive interval of length $n$. Smaller multipliers can work. With three or four branching neighbors the divisor and divisible-core conclusions already hold at **every** multiplier by the [three-center](three-branch-joint.md) and [four-center](four-branch-joint.md) theorems.

## Packing a pair or triple

Give the distinguished center zero. For each group divide the counts by their gcd $g$, giving prototype counts of total $L$. Construct displacements on a prototype interval, with each displacement representing a different center.

* For a pair with counts $a,b$, place blocks of lengths $a,b$ in that order and exchange the two blocks keeping their internal orders. The first block has jump $b$, the second $-a$.
* For a triple of normalized counts $a\le b\le c$ with $a<c$, reverse the order of the three blocks, keeping each internal order. Their jumps are $b+c,c-a,-a-b$, all nonzero and distinct.
* For an equal triple the normalized counts are $1,1,1$. Use jumps $1,2,-3$. One layer uses the cycle $0,1,3,0$, leaving position two fixed. Two and three layers fit their entire intervals: the respective permutations in source order are $(1,3,4,0,5,2)$ and $(2,3,4,0,1,6,7,8,5)$. Every layer count at least two is a sum of twos and threes. Thus any number of equal triples requires at most **one** extra fixed position.

Take the triple first if present, at scale one. For each successive pair choose the least positive integer $s$ for which its two jumps multiplied by $s$ avoid all previous centers. Each nonzero previous center can forbid at most one positive scale since the pair has opposite signs. In particular $s\le m$. Use the resulting jumps as the group's center labels. Write $I$ for the smallest interval containing all centers, including zero. Reserve this whole interval. The incoming edge at each center weighs its assigned label.

For a group with an ordinary interval permutation $\pi$ of length $L$, take $g$ copies at scale $s$. To place $s$ copies use positions $sx+i$, for $0\le i<s$, $0\le x<L$. Map each to $s\pi(x)+i$. This uses a full interval of length $sL$. For a last incomplete set use the same interval, omitting its unused residue classes. The total number of extra fixed positions needed for this group is at most $(s-1)L$, independent of $g$. The same bound applies to every retained number of copies from zero to $g$.

Place all these intervals consecutively after $I$. Let $B$ be $|I|-m$ plus the sum of these fixed-position bounds, counting one for an equal triple instead. Write $L_{\max}$ for the largest normalized group size. The actual sufficient condition for the full integer labeling is $D+P\ge B$. Indeed the moving positions supply the requested child labels at their respective displacement centers. Their weights permute those positions. All untouched positions except the centers themselves are available for the children of the zero center and the direct leaves, whose weights equal their labels. Extend the upper interval as necessary for the remaining fixed positions. Reduction modulo any divisor and translation to any prescribed joint give the uniform assertions.

## Prefixes and the numerical bound

Assume $D+P\ge B+L_{\max}$. For every $m\le K\le n$ one can retain all centers and exactly $K-m$ children or direct leaves with the same interval property. Put $Z=D+P$. If $K-m\le Z$, use only zero-shift children and direct leaves, and choose the centers to fill $[0,m-1]$ starting with the distinguished center zero. Otherwise retain group prototypes, counting each available copy separately, until their total first reaches $K-m-Z$. Enough copies exist. The overshoot is less than $L_{\max}$. Hence at least $Z-L_{\max}$ and at most $Z$ zero-shift leaves are needed. The same positions and scales work when any groups retain fewer copies, even zero. Every excluded vertex is now a leaf at an already retained parent.

To verify the simpler gcd hypothesis, put $T=4m^2$, $d=D/T$. At least one group exists, so $d\ge1$. Each normalized entry is at most $d$ and $L_{\max}\le3d$. Every unscaled jump has magnitude at most $3d$, also for an equal triple. Hence $|I|\le6md+1$. The sum of all normalized sizes is at most $(m-1)d$. All ordinary group scales are at most $m$. The extra position for an equal triple costs at most one. Consequently
$$
B+L_{\max}\le \big(6m+(m-1)^2+3\big)d+2-m
\le4m^2d=D.
$$
This calculation also gives the explicit slack test when the gcd hypothesis fails.

For a modulus $k>n$, pad to $k$ with direct leaves and take the integer interval construction. A missing core weight occurring on a dummy leaf can be retained by exchanging its label with a real child of the zero center: the two incoming parent labels agree. Restriction thus gives distinct new labels, distinct new weights and a hit on the required deficit. For $m\le k\le n$, take the $K=k$ prefix. It adds uniform counts. At a core of divisible order, any subsequent batch of at most $k$ leaves at already labeled parents can be attached cordially. Label one to supply the deficient weight and use Hall's partial permutation theorem on the rest. Full batches restore the divisible order. [Leaf extension](../counterexample-bound.md#removing-leaves)

For $k<m$, first take full batches of $k$ centers, each the children of the joint. If $r$ centers remain with $0<r<k$, add them and $k-r$ children of earlier centers in one ordinary leaf batch. There are at least $k$ earlier centers, each with a child. All other additions are now leaves. This finishes the unrestricted modulus assertion.

The checker independently recomputes actual edge sums and the common integer interval, including prefixes with inactive groups, independent group multiplicities and exceptional equal triples. It tests 1,470 prefixes, 3,328 divisor histograms after translation and 1,437 restrictions with a deficit initially supplied by padding. [Constructor](scaled_joints.py) · [Checks](check_scaled_joints.py)

~~~sh
python3 -B -m research.census.check_scaled_joints
~~~
