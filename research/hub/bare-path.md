# A long bare path rules out a one-hub rational obstruction

Fix a finite tree $H$ and a vertex $o$. Root the tree at $o$. Suppose a downward path of seven edges starts at positive even depth, and each of its six interior vertices has degree two. Then, for every sufficiently large modulus $k$, adding any number of leaves at $o$ gives a $k$-cordial tree. The threshold depends only on $H$. There is no condition on the components beyond the ends of the path.

In particular, a bare path of seventeen edges anywhere in $H$ suffices for **every choice of the hub**. If the hub is on the path, one side has length at least nine. Start at depth two on that side. If the hub is off the path, the route from the hub reaches an endpoint first, since all internal vertices have degree two. Start at that endpoint or one step beyond it to achieve positive even depth.

## Two components with two unused weights

Call the near endpoint $P$ and the far endpoint $Q$. Remove the six interior vertices, leaving components rooted at $o$ and $Q$. Let $d$ be the degree of $o$. Give $o$ label zero, its neighbors distinct negative labels $-2,-5,\ldots,-(3d-1)$, and $Q$ label $q=3d+1$. Initially the hub edges use their neighbors' labels. The two unused weights are $N=0$ and $M=q$.

Grow the forest one vertex at a time from a labeled nonzero parent $x$.

- If $x>0$, assign $N-x$ to its child and replace $N$ by $N-x$.
- If $x<0$, assign $M-x$ and replace $M$ by $M-x$.

The new edge consumes the old unused weight. Positive labels increase strictly from $q$. Each new negative label is at most $-q$ and the sequence decreases strictly. Thus all vertex labels are distinct and exactly $N,M$ remain unused. In particular $M$ is the maximum vertex label.

Grow the stem from the first hub neighbor to $P$ **before** the rest of the forest. At depth two the positive label is $q+u$, where $u$ is the magnitude of the first neighbor label, so it is zero modulo three. At this point both moving weights are zero modulo three. Along the rest of the stem they stay so, with negative labels at odd depths and positive labels at even depths. The label $p$ at $P$ therefore satisfies $p>q>0$ and $p\not\equiv q\pmod3$. Now finish the remaining vertices in any parent-before-child order.

## Reconnecting the endpoints

Take $w=M$, so $w\ge p$. Multiply all forest labels by six. From $P$ to $Q$, put the following six integer labels on the internal vertices:
$$
(a,b,c,d',e,f)=
(-4p-2q,\ 2(p-q),\ q-p+3w,\ p-q+3w,\ 2(q-p),\ -2p-4q).
$$
Direct addition gives the seven edge weights, in order,
$$
b,\ f,\ d',\ 6w,\ c,\ a,\ e.
$$
All six new labels are nonzero modulo three. All the scaled forest labels are zero modulo three. Within the path the strict order is $a<f<e<0<b<c<d'$, using $w\ge p>q>0$. The completed tree therefore has distinct integer vertex labels, hub zero, and its edge sums use all its labels except $6N$. Reduction at every modulus exceeding its span preserves the labeling. The periodic list of leaf labels at zero then works for every population. [Leaf-extension proof](README.md) · [Equivalence with the one-hub rational test](rational.md)

The [Lean proof](BarePath.lean) checks the seven equations, the six congruences and the strict order. The [constructor](bare_path.py) also checks the actual sums of 1,156 whole-tree labelings, with arbitrary rooted attachments at both ends up to order five and four different stem depths. The example checks two complete periods of extra hub leaves at each of two consecutive moduli.

~~~sh
lean research/hub/BarePath.lean
python3 -B -m research.hub.bare_path
~~~

## A finite decision with a bound on the number of tips

Remove all leaf neighbors of $o$, which can be restored with fresh labels equal to their own edge weights. Count the terminal vertices of each remaining branch, rooting it away from $o$. For every fixed bound $b$ on this count **per branch**, there is a finite decision whether all such rooted cores satisfy the rational criterion. The original orders, degrees of the hub, and lengths of degree-two paths can be unbounded.

Three or more nonsingleton branches are covered by the [cyclic construction](cyclic-transfer.md). If a branch root has at least one child and at most one nonleaf child, the [anchor construction](branches.md) handles all other branches. In the remaining cases there are at most two branches, each starting at a fork. Suppress chains of unary vertices below each fork. A reduced branch with $j$ tips has at most $j-1$ forks and $2j-2$ edges. If a reduced edge expands to length at least eight, its upper endpoint is at depth at least one. Starting there or one step farther gives the seven-edge path at positive even depth. Thus only lengths one through seven need testing on the finitely many remaining skeletons. Apply the [exact rational test](rational.md) on each full residual core. Extra singleton neighbors cannot repair a failed test, since their labels are already used by their incident edges.

**The test is affirmative through four tips per branch.** For the short residual branches we check the stronger property that each admits a coprime parent-before-child order. By the [branch lemma](branches.md), one can attach the branches successively to the zero hub. The checker enumerates reduced forks by unordered multisets of child arms, each carrying a length in $[1,7]$ and a child subtree. It treats a terminal vertex as the single type with one tip. Independently, if $R_i$ is the number of shapes with $i$ tips, the number with $j>1$ is the coefficient of $x^j$ in $\prod_{i<j}(1-x^i)^{-7R_i}$. Only multisets of at least two arms contribute. The checker requires this count of distinct canonical shapes, reproduces a coprime order for each, and directly checks its integer labels and edge sums.

| Tips | Short branches rooted at a fork |
|---:|---:|
| 2 | 28 |
| 3 | 1,456 |
| 4 | 96,348 |

Consequently a failed one-hub rational test would require a branch with at least five terminal vertices as well as the absence of the long paths above. This result gives a threshold for each **fixed** rooted core, uniform over further leaves at the hub. It leaves open the small moduli for that core and the full conjecture.

~~~sh
python3 -B -m research.hub.few_tip_branches
~~~
