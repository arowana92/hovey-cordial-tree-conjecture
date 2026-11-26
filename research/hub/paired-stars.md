# Two pendant stars per vertex at many different vertices

**Theorem.** Fix $D\ge3$ and $s\ge1$. There is a constant $N(D,s)$ such that the following suffices for cordiality at every modulus. At most $s$ vertices of the tree have degree greater than $D$, and at least $N(D,s)$ distinct vertices each support two pendant stars. A pendant star at $v$ consists of a neighbor of $v$ with at least one leaf child and no other vertices beyond it. The two stars can have different arities. The distances between the supporting vertices are unrestricted.

Consequently, in any counterexample of this degree class, delete all original leaves and call the result $H$. For $|H|\ge3$, the total number of leaf neighbors of vertices of $H$ with at least two such neighbors is bounded in terms of $D,s$. Indeed there are boundedly many such supporting vertices by the theorem. At one supporting vertex there are at most $s$ star roots above degree $D$ and boundedly many of each other arity by the [single-vertex theorem](pendant-stars.md). This conclusion does not require a bound on the diameter of $H$.

## Five stars with four distinct boundary labels

Use stars at boundary labels $a,q,c,h,q$, in this order. The two stars at $q$ share a parent. Put the following labels on their roots and on one child of four of the roots.

| Boundary | Root | Child |
|---|---|---|
| $a$ | $d$ | open |
| $q$ | $d+a$ | $-2d-2a-h-q$ |
| $c$ | $d-c$ | $d+a+q$ |
| $h$ | $-d-a-h-q$ | $-d-a$ |
| $q$ | $-d-a-q$ | $2d+a+q-c$ |

The five boundary and four internal edges give exactly the nine assigned labels with multiplicity. This integral identity holds before reduction modulo $k$. [Lean proof](PairedStarRoots.lean)

At order $k$ the assigned boundary labels are distinct residues. For one repair let $[t]-[b]$ be its surplus and deficit and $g$ the current omission. Here $t\ne0$ is free as a vertex label. In a group the offsets at slope $+1$ in $d$ are $0,a,-c,a+q$ and those at slope $-1$ are $-a-h-q,-a,-a-q$. Choose four boundary vertices one at a time, omitting the following residues in addition to previously chosen vertices.

| Choice | Exclude |
|---|---|
| $a$ | $0,t,-b,-g$ |
| $q$ | $0,-a,t-a,-a-b,-a-g$ |
| $c$ | $0,-a,-a-q,-t$ |
| $h$ | $0,-q,-a-q-b,-a-q-g$ |

Each repeated-slope list now has distinct offsets. The positive list avoids $t$ and the negative list avoids $b,g$. At most five residues are excluded at a time. Six disjoint groups can be chosen from 32 available vertices even if their labels are adversarial. Each selected vertex supplies two stars of a common profile $(m,n)$ with $1\le m\le n$. Within the displayed group use the larger stars at the first three roots and the smaller stars at the last two. This uses all of the pair at $q$ and leaves one further star at each of $a,c,h$.

## Completing one repair and all unused stars

Write $P$ for the sum of the boundary jumps at the additional star roots, including the unused partners and any final unused pairs. Give the six groups parameters
$$
A,\quad B,\quad F,\quad b-t-P-A-B-F,\quad U,\quad V .
$$
At the four distinguished open children in the first four groups start a walk at $t$ using their parent labels as jumps. Between its second and third jumps insert **all additional root jumps**. The walk ends at $b$. For the additional roots walk from offset zero with jumps equal to their exterior labels, giving terminal $P$. Erase simple cycles upon repetitions and translate their offsets separately to avoid one another and the residual tails and terminal. This takes boundedly many exclusions for a bounded number of roots. Assign each such root $t+A+B$ plus its offset. Its edge goes to the translated head. The net discrepancy from this part is $[t+A+B+P]-[t+A+B]$. The four primary leaf labels are $t,t+A,t+A+B+P,b-d_4$, where $d_4=b-t-P-A-B-F$. They and the additional roots together contribute $[b]-[t]$. The additional root offsets all avoid $P$, so they miss the same-slope third primary leaf.

All remaining vertices are leaves with known parent jumps. From the old gap $g$ work backwards, subtracting each jump. Start with the distinguished open child of the fifth and then the sixth group. In each of these groups process the positive-coefficient parents before the negative ones, maintaining the relative order of its own list. After both first steps one may complete the fifth list, then the sixth, then process all other jumps. Each guard group has $n+2(n-1)$ positive and $2(m-1)$ negative jumps, and its signed count stays positive after its first step. Thus every tail after the first two steps has nonzero coefficients of both $U,V$, including the new gap $g'$. Erase and translate cycles as in the [single-supplier repair](pendant-stars.md#one-repair-with-a-moving-omitted-weight). The total change on actual weights minus vertex labels is $[b]-[t]+[g]-[g']$.

For clarity, group slope directions are the six listed directions in the five independent parameters, with nonzero scalar coefficients. No two groups' directions are proportional. Main leaves at slopes $A$ and $-d_4$ (in their moving parts) meet only the equal-slope tests on $t$ and $b$ already imposed. The slope $A+B$ of the extra roots and their terminal differs from every group direction. The first backward tail $g-U$ meets the test on $g$. All later backward tails use both guard coordinates and hence miss every group direction, every extra root and every primary leaf. Repetitions within the backward walk are handled by erasure. For specialization take the five parameters as $z,Rz,\ldots,R^4z$ with $R$ larger than twice the maximum possible coordinate difference plus two. The number of vertices in a single placement and this radix are bounded in terms of $D$ when $n<D$ and at most eight extra pairs are included. Distinct slope vectors remain distinct integer slopes. The [common palette lemma](bounded-error.md#a-common-set-of-intervals-for-the-direct-leaves) places all moving forms outside the large leaf palette on a positive proportion of parameters. Unequal-slope comparisons against sparse occupied and reserved values and within the packet exclude $O_D(h+1)$ parameters for ordinary order $h$, up to an additive constant depending on the preparation. Translating each erased cycle uses the same lemma with slope one.

## From the local identity to the theorem

Discard candidates whose selected pair meets a star root above degree $D$. A star root has only one nonleaf neighbor, so at most $s$ candidates are lost. Distinct suppliers of two stars cannot occur inside one another's selected stars. There are at most $\binom D2$ possible unordered positive arity profiles up to $D-1$. By pigeonholing choose sufficiently many pairs at distinct vertices with the same profile $(m,n)$.

For large $k$ remove direct leaves at the original high sites, obtaining ordinary order $h$. If there are no high sites use the [bounded-degree theorem](../bounded-degree/README.md). If $h\ge\delta k$ use the [positive-density theorem](concentrated-leaves.md). In the sparse case first take total order $k$. Withhold the two stars at exactly $24(C+1)+8$ selected vertices and leave those vertices in the ordinary tree. Apply the [sparse core preparation](bare-path-repair.md#keeping-the-surplus-weights-available) with the original high sites. It permits an ordinary leaf at a supplier that has lost all its children. If a supplier was a site, the site remains marked. The preparation bounds depend on $D,s$ and its palette, independently of the number of withheld stars. We obtain $E-V=-[0]+\sum_{i=1}^e([t_i]-[b_i])$, with $e\le C$ and all surplus labels reserved. The common palette is chosen for the bounded placements above before fixing $C$ and then $\delta$.

Use one six-group repair on 24 pairs for each error. Fill spare jobs with $b=t$ fresh, and include the final eight unused pairs among the additional roots of the last job. There are at least 32 choices at the start of every job. Withhold the new gap from all previous occupied and reserved values. This restores every branch and gives $E=V-[g']$. The direct leaves at zero take the complement. For $n<k$ pad and restrict. For $n>k$ reduce and restore only direct leaves at the original high sites, preserving all withheld stars, as in the [all-orders reduction](bare-path-repair.md#repairing-the-actual-weights). The finitely many smaller moduli are covered by increasing the required number of suppliers past their [order thresholds](../large-order/linear.md).

## Reproduction

The independent checker recalculates 61,775 nine-edge histograms, tests 14,400 group selections, and reconstructs 18 whole trees with 2,948,982 actual edge sums. The selection checks include pools of only 32 residues. The whole trees include far-apart parents, different arities, prime moduli and composite moduli sharing factors with the arities. [Construction](paired_stars.py) · [Checker](check_paired_stars.py)

~~~sh
python3 -B -m research.hub.check_paired_stars
lean research/hub/PairedStarRoots.lean
~~~
