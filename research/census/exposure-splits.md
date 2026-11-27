# Separating groups of uncovered leaves at 26 labels

Let $T$ be a smallest unrestricted 26-label counterexample, if one exists. At orders congruent to 23, 22 and 21 modulo 26 its order is at most **413, 334 and 203**, respectively. More detailed bounds below retain the matching deficiency. The proof uses the fact that deleting any prescribed group of $H$ exposed leaves from the spanning requirement can free only a small number of matched pairs.

Use $n=26q-H$, $1\le H\le5$. As in the [exposure bound](exposure-bounds.md#discarding-a-chosen-set-of-tips), fix a maximum matching missing $d$ original leaves. Contract its pairs and span the exposed leaves by a subtree. Let $h$ count the pairs outside this subtree. Then $h\le12-H$. If a collection of branches in the spanning subtree can all be removed while retaining $d-H$ exposed leaves, those branches together contain at most $C=12-H-h$ pair positions. This part of the argument also holds for minimality within any fixed matching-deficiency bound.

## Edges with more than H tips on each side

Retain every edge of the spanning subtree with at least $H+1$ exposed leaves on each side. If there are any, they form a connected subtree $J$. Indeed, an edge between two retained edges has at least one outer side of a retained edge in each direction. Every branch outward from $J$ contains at most $H$ tips. If there is no retained edge, take $J$ to consist of a single centroid for the tip weights. Its branches also have at most $H$ tips, since otherwise the centroid property would make the edge into that branch eligible.

Write $w_1,\ldots,w_m$ for the numbers of tips in the outward branches. These positive integers sum to $d$. Group the branches into $g$ collections each of total weight at most $H$. Removing their tips frees all the pair positions in each collection, even if its branches attach at different vertices of $J$. Thus at most $gC$ pair positions of the spanning subtree lie outside $J$.

In $J$ count the leaves, the vertices of degree at least three and the degree-two vertices that carry an outward branch. Let $K$ count these sites, taking $K=1$ for the singleton case. If $J$ has $l\ge2$ leaves, each leaf supports at least $H+1$ tips in at least two outward branches. There are at most $l-2$ vertices of degree at least three. The number of counted degree-two sites is at most $d-l(H+1)$ by counting tips, and at most $m-2l$ by counting branches. Consequently
$$
 K\le\max\{1,\min(d-2H,m-2)\}.
$$
All other positions of $J$ lie on its $K-1$ connectors. No tip-bearing branch attaches along their interiors.

For even $n$, the [thirteen-position bound](exposure-bounds.md#paths-between-uncovered-leaves) puts at most $12(K-1)+13\lfloor h/7\rfloor$ pair positions in these connectors. For odd $n$, one side of every cut between positions is even. Along each connector its successive even component orders change by twice the successive position masses, with either a positive or a negative sign. Hence one prefix residue modulo 13 is forbidden. Every 12 consecutive positions require at least seven side pairs, by the repeated-residue argument in the [five-exposure proof](exposure-bounds.md#five-exposures-at-order-one-short-of-a-multiple). The corresponding bound is $11(K-1)+12\lfloor h/7\rfloor$.

Set $a=11$ for odd $n$ and $a=12$ otherwise. A nonsingleton $J$ has $d\ge2H+2$, so $g\ge3$. Thus $(a+1)\lfloor h/7\rfloor\le(g-1)h$. For a singleton there are no connector costs. Adding all the pairs now gives
$$
 \nu(T)\le g(12-H)+K+a(K-1).
$$

## Numerical bounds

If the tree has $L$ leaves then $d\le L-1$. Root at any leaf and choose one child at every vertex with children. The chosen edges partition all vertices into $L-1$ paths, each ending at a distinct nonroot leaf. Matching along each path leaves at most one exposure on it. For unrestricted minimality the [leaf extension](../counterexample-bound.md#removing-leaves) gives $L\le24-H$. Since $d\equiv H\pmod 2$, we have $d\le22-H$. The earlier theorem gives $d\ge H+4$.

The [finite arithmetic check](check_exposure_splits.py) iterates over all partitions of each admissible $d$ into parts of size at most $H$. It puts the parts in nonincreasing order and places each part in the first group where it fits, opening a new group when necessary. This constructs an admissible $g$ for every actual tree. The checker substitutes this count and the upper bound on $K$ into the inequality above, then uses $26q=2\nu+d+H$. The entries are upper bounds on $q$ in order of increasing $d$. They can be combined with the [closer bounds at $d=H+4$](exposure-bounds.md).

| $H$ | Deficiencies $d$ | Upper bounds on $q$ |
| ---: | --- | --- |
| 2 | 6, 8, 10, 12, 14, 16, 18, 20 | 3, 6, 9, 12, 15, 17, 20, 23 |
| 3 | 7, 9, 11, 13, 15, 17, 19 | 2, 5, 7, 9, 11, 14, 16 |
| 4 | 8, 10, 12, 14, 16, 18 | 2, 3, 5, 8, 10, 13 |
| 5 | 9, 11, 13, 15, 17 | 2, 2, 4, 6, 8 |

There are 813 tested tip partitions across $1\le H\le5$. A separate structural check cuts each edge in 2,100 explicit spanning trees, reconstructs $J$ and checks its site and tip counts.

~~~bash
python3 -B research/census/check_exposure_splits.py
~~~
