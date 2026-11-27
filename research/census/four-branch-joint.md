# Uniform increments with four branching neighbors

**Theorem.** Attach four stars at a joint by joining each of their centers to the joint. Their positive numbers of leaf children $a,b,c,d$ are arbitrary. Also attach $p\ge0$ direct leaves at the joint. With $n=a+b+c+d+p+4$ free vertices, there is a labeling modulo $n$ for which both the free labels and all $n$ new weights are permutations. At **every divisor of $n$** the attachment therefore adds equal numbers of all labels and all weights at any prescribed vertex of any core.

At **every** modulus, including those that do not divide $n$, the attachment extends a prescribed cordial labeling of a core of divisible order. The corresponding assertion for at most three branching neighbors is already known here, including the cases with no uniform increment. [Three branching neighbors](three-branch-joint.md) · [Two branching neighbors](two-branch-joint.md)

Put the joint at zero. Construct a permutation of the $n$ residues that fixes four distinct center labels, including zero. A jump $j$ at $x$ means that a child labeled $x$ attached to center $j$ has weight equal to the image of $x$. Allocate the desired child populations to the nonzero jumps. Use the remaining fixed positions outside the four centers for the children of the zero center and the direct leaves. The center edges weigh their respective center labels.

## A rotation and disjoint pairs

Assign population $D$ to center zero. Name the other populations $R,B,C$ with $C>B$. Let $g=\gcd(R,C-B)$, $s=R/g$, $t=(C-B)/g$, and $H=D+2B+4+p$. The following conditions suffice:
$$
s\ne t,\qquad D+p\ge s,\qquad s+\max(s,t)+1\le H.
$$

Choose centers $t,s,-s,0$ for $R,B,C,D$. All are in $F=[-s,H-s-1]$. Immediately after $F$ put $g$ intervals of length $s+t$. Rotate each by $t$ places: the first $s$ positions jump $t$, the last $t$ jump $-s$. This supplies population $R$ and $C-B$ children of the larger paired population. The intervals together with $F$ have length $n$.

In $F$ join positions differing by $s$. Its step-$s$ chains number at most $s$. Removing $-s,0,s$ deletes the first three positions of a single chain. Removing $t$ can increase the number of remaining chains by at most one. There are $2B+D+p$ positions left. A chain of length $j$ has $\lfloor j/2\rfloor$ disjoint adjacent pairs. The number of odd chains is at most $s+1$ and has the parity of $D+p$. As $D+p\ge s$, at most $D+p$ chains are odd. Thus at least $B$ disjoint pairs are available. For each of $B$ pairs assign the smaller position to a child at $s$ and the larger to a child at $-s$. Their weights exchange the two labels. Exactly $D+p$ positions remain. This proves the construction over the integers on a common interval, hence also modulo $n$.

## Two equal populations and their sum

For sizes $(a,b,b,a+b)$ put $T=a+b$, $u=b+3+p$ and $n=2a+3b+4+p$. Use nonzero centers $b,b+1,-T-1$ with populations $a,b,b$. On $[u,u+T-1]$ the rotation by $b$ uses $a$ jumps $b$ and $b$ jumps $-a$. Split each $-a$ jump into a jump $b+1$ followed by $-T-1$. The intermediate positions occupy exactly $[u+T+1,u+T+b]$. These intervals are disjoint and fit below $n$. The center $-T-1$ is $u+T$ modulo $n$, in the gap. The centers $0,b,b+1$ are below the first interval. The resulting permutation has all the required jumps.

## Two copies of the sum

Suppose the sizes are $(a,b,c,c)$ with $a\le b$ and $c=a+b$. Here $n=3c+4+p$. Start with the rotation on the interval $[a+1,2c+2a]$ of length $2c+a$ having jumps $c+a$ and $-c$. A position in its first $c$ slots has incoming jump $-c$ and outgoing jump $c+a$. Call these positions valleys. The last $c$ positions have the opposite incident jumps. No two valleys are consecutive in a cycle of the rotation.

Skip $a$ pairwise nonconsecutive positions with these opposite incident jumps. Make each skipped position fixed and connect its predecessor directly to its successor. Each skip replaces a pair of jumps by a single jump $a$. The remaining jump counts at centers $c+a,-c,a$ become $b,c,a$, respectively. We must protect the centers. Zero and $a$ are already outside the interval. The position $c+a$ is its last valley, which we require to be skipped. If the center $n-c$ is in the interval, it belongs to the last $c$ positions and must also be skipped. It lies inside only if $2a\ge p+4$, so then $a\ge2$. The two required skips are neighbors precisely if
$$
a=p+4 \quad\text{or}\quad 2a=p+4 .
$$
Indeed the two neighbors of $c+a$ are $2c+a$ and $2c+2a$. Away from these equalities retain both required skips and fill the rest from the valleys. At most two valleys are neighbors of the required peak, leaving at least $c-2\ge a-1$ available valleys including the required one. If the peak is outside, simply take $a$ valleys. [Lean verification of the interval inequalities](FourBranchArithmetic.lean)

The two exceptional equalities have different clockwise constructions. A list of positive jumps summing to $n$ defines one cycle on its partial sums modulo $n$, since its proper partial sums lie strictly between its start and its start plus $n$.

* If $2a=p+4$, use centers $0,4,2,1$ and take $a$ jumps of four, $b$ of two and $c$ of one. Their sum is $n$. Start at $-1$, go to $3$ and then $5$, and take the remaining jumps in any order. The cycle avoids $0,1,2,4$.
* If $a=p+4$, first take a cycle with $a$ jumps of four and $b$ of three; their sum is $n=3c+a$. Start at $-12$ and visit $-9,-6,-2,2,6,10$, then use the remaining jumps. This prefix uses four fours and two threes, available since $b\ge a\ge4$. Its vertex set $W$ avoids $-10,-5,0,3,4,8,9$: the rest of the walk stays between $10$ and $n-12$. Insert $y+5$ immediately before each visited position $y$. The inserted set $W+5$ is disjoint from $W$, since a forward distance of five is neither one gap nor a sum of two or more gaps. Both sets avoid the centers $0,9,8,-5$ by the listed exclusions. Each old jump of four or three becomes a jump of nine or eight followed by $-5$. This supplies exactly $a,b,c$ nonzero jumps.

## Exhausting the populations

Sort $a\le b\le c\le d$. If three counts coincide, use the [integer construction with one exceptional population](regular-joints.md). Otherwise the following choices exhaust the possibilities. Tuples in the rotation-and-pair column give $(R,B,C,D)$. The sufficient inequalities follow already with $g=1$ in their upper bounds.

| Condition | Construction |
| --- | --- |
| $c>b$ and $c-b\ne a$ | $(a,b,c,d)$ |
| $b=c$ and $d=a+b$ | Two equal populations and their sum |
| $b=c$, $d\ne a+b$, $d\ge2b$ | $(b,a,b,d)$ |
| $b=c$, $d\ne a+b$, $d<2b$ | $(a,b,d,b)$ |
| $c=a+b$, $d=c$ | Two copies of the sum |
| $c=a+b$, $c<d\le2c$ | $(a,b,d,c)$ |
| $c=a+b$, $d>2c$, $a<b$ | $(c,a,b,d)$ |
| $c=a+b$, $d>2c$, $a=b$ | Four-position permutation below |

In the row $c<d\le2c$, the bound $a+d-b\le a+2c-b=3a+b\le a+3b=2b+c$ gives room in $F$. In the last row use centers $0,1,3,-2$. Repeat the permutation of four positions with jumps $(3,1,-2,-2)$ on $a$ disjoint intervals beginning at four. There are $d+p$ remaining child or direct positions at shift zero, including the holes among the centers. In residues $0,1,3,n-2$ the moving interval $[4,4a+3]$ avoids all four centers because $d>4a$. This completes the all-orders proof for the full modulus.

## Extending a divisible-order core

Translate a full-modulus permutation to the prescribed joint and reduce modulo any divisor for the uniform assertion. For $n<k$, pad to $k$ with twin leaves at a branch center. If a dummy supplies the deficient weight, swap it with a real twin before restriction. For $8\le k\le n$, take a $k$-edge prefix containing all four centers and one child at each. Fill to size $k$ with any remaining vertices. Apply the uniform theorem, then add the remaining leaves in batches at their labeled parents.

For $4\le k<8$, include the four center edges and any $k-4$ other edges. The prefix has at most three branching neighbors and admits the required full extension by the earlier one-, two- and three-branch results. For $k<4$ add as many complete batches of $k$ centers as possible, with uniform increments. Any remaining centers and enough children of earlier centers make a full batch with labeled parents. Each of these earlier centers has a child available. All remaining vertices are now leaves. At a divisible-order core the first vertex in any such batch can supply its deficient weight and Hall's partial permutation lemma assigns the other at most $k-1$ vertices. [Leaf batches](../counterexample-bound.md#removing-leaves)

The verifier reconstructs the actual tree, checks both histograms and independently checks restrictions and reductions. It tested 52,650 full blocks on all four-count multisets through child count 24 at three choices of $p$, another 7,500 blocks concentrating on the sum families, 1,500 proper divisors and 1,500 short blocks with prescribed deficits. The unconditional parameter ranges follow from the constructions above. [Constructor](four_branch_joint.py) · [Independent checks](check_four_branch_joint.py)

~~~sh
python3 -B -m research.census.check_four_branch_joint
lean research/census/FourBranchArithmetic.lean
~~~
