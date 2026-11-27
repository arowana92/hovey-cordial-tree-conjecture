# Partial subdivisions of double stars at every modulus

**Theorem.** Join two centers by an edge, attach any number of leaves to either center, and subdivide any subset of those pendant edges once. The resulting tree is super edge-magic and $k$-cordial for every positive integer $k$. In particular, among diameter-five trees this allows arbitrary numbers of two-edge branches and direct leaves on both sides. There is no ratio or parity restriction.

Write $a,b$ for the numbers of two-edge branches. If either is zero the diameter is at most four and the [diameter-four theorem](all-radius-two.md) applies. For $a,b\ge1$ we prove a stronger statement. The centers can carry labels 0 and 1, the vertex labels fill an integer interval $[L,U]$, and the distinct edge sums fill $[L+1,U]$. Indeed we may begin with no direct leaves. Each new direct leaf at 0 takes the next upper label, which is also its weight. Each new direct leaf at 1 takes the next lower label, whose weight is one higher. This preserves both intervals. Reducing the intervals modulo $k$ gives cordiality. [Youssef's Theorem 4](https://ajc.maths.uq.edu.au/pdf/43/ajc_v43_p031.pdf)

Krisnawati and coauthors study super edge-magic deficiency for subdivisions of double stars with an odd number of vertices inserted in the link between the centers. The centers here are adjacent throughout. [Primary paper](https://doi.org/10.1155/2020/4285238)

## Placing new branches in groups of three

For an even cutoff $D=2d\ge4$, put $v(x)=-1,0,1$ according as $x+(x\bmod2)$ is at most $-D$, lies strictly between $-D,D$, or is at least $D$. Thus $v(0)=v(1)=0$. A starting labeling qualifies for enlargement when both old intervals contain $[1-D,D-2]$ and $v(p)+v(x)=v(p+x)$ on every edge. Choose $s\ge2d-1$, put $\Delta=6s$, and map old vertex and weight labels by $x\mapsto x+\Delta v(x)$. Old edges retain their endpoint sums by the speed equation.

In each old interval the even labels have origin zero and the odd labels have origin $-1$. In coordinates $(x-c)/2$ for origin $c$, the central segment $[1-d,d-1]$ stays fixed, with the two outer segments moved apart by $3s$ at either end. Consequently the enlarged interval extends by $\Delta$ at both ends. Its unfilled entries on the two parities are exactly
$$
2S,\qquad -1+2S,\qquad S=\pm[d,d+3s-1].
$$
This is the same statement for vertices and weights, even when an old outer segment was empty. [Interval image proof in Lean](RadiusTwoIntervals.lean)

The signed Langford theorem partitions $S$ into $2s$ triples $(u,v,w)$ of sum zero. For clarity, its permutation on $B=[d+s,d+3s-1]$ has displacement set $\pm[d,d+s-1]$. For each $x\in B$ take $(x,-\pi(x),\pi(x)-x)$, using every member of $S$ once. [Jordon and Mitchell, *Signed Langford sequences*](https://doi.org/10.1016/j.disc.2021.112719) · [Brown and Jordon's triple construction](https://ajc.maths.uq.edu.au/pdf/79/ajc_v79_p234.pdf)

Choose a center $c\in\{0,1\}$ independently for each triple. Place three arms there using the three cyclic rotations of the following row.

| Parent | Tip | Weight to center | Weight to tip |
| --- | --- | --- | --- |
| $2w-c$ | $2u-1+c$ | $2w$ | $-1-2v$ |

At center zero, the parents use the even slots of the triple and the tips the odd slots. At center one they exchange these roles. The six vertex slots for a triple therefore stay the same under either choice of center. Its six weights also stay the same. Across all triples, the new even weights run through $2S$ and the odd ones through $-1-2S=-1+2S$. This fills all vertex and weight slots. In particular any nonnegative increments to the two branch counts are possible if both are multiples of three and their sum is $6s$. [Lean check of the change of center](DoubleArmFrame.lean)

## All splits and all orders

Name the sides so $a\ge b\ge1$. There are 18 expandable starting labelings, one for each $4\le x\le9$, $1\le y\le3$, with at most cutoff six. When $a+b\ge42$, choose $y$ in this range congruent to $b$ modulo three, then choose $x$ in its range so $x+y\equiv a+b\pmod6$. We have $a\ge21\ge x$, $b\ge y$, both increments are multiples of three, and $a+b-x-y\ge30$. Hence $s=(a+b-x-y)/6\ge5\ge D-1$ and the construction applies.

Below 42 total branches the verifier tests every pair. For each it checks the arithmetic of an eligible enlargement or an explicit integer labeling with pinned centers. The archive contains 203 labelings including the 18 expandable ones. The verifier reconstructs the actual branches, checks both intervals, and verifies the speed and central-interval hypotheses. Independently it constructs the signed triples at the smallest allowed order for each expandable seed, places every subset of those triples at the second center, adds direct leaves to both centers and checks 7,872 whole labeled trees. The infinite step uses the signed Langford theorem and the argument above. [Certificate](double-arm-seeds.jsonl) · [Verifier](check_double_arm_frames.py) · [Expansion code](double_arm_frames.py)

~~~sh
python3 -B -m research.hub.check_double_arm_frames
lean research/hub/RadiusTwoIntervals.lean
lean research/hub/DoubleArmFrame.lean
~~~

The finite generator uses exact cover. A possible arm consumes two distinct vertex slots and two distinct weight slots, plus one branch from its selected center. Each finite result records the actual labeling. Reproduce it from the repository root.

~~~sh
out=$(mktemp -d)
c++ -O3 -std=c++17 -shared -fPIC research/hub/double_arm_search.cpp -o "$out/search.so"
python3 -B -m research.hub.double_arm_generate "$out/search.so" > "$out/seeds.jsonl"
cmp "$out/seeds.jsonl" research/hub/double-arm-seeds.jsonl
~~~
