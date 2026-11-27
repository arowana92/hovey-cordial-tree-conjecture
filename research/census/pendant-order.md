# A smallest 26-label counterexample has at most 286 vertices

The [side-forest substitution](ring-order.md) lowers the ceiling to **208**.

**Theorem (computer-assisted).** Write the order of a smallest counterexample as $26m+s$ with $1\le s\le26$. Only the four residues in the table remain. Testing ordinary trees through order **286** would suffice to settle the unrestricted case at 26. The bounds apply to a counterexample of minimum order over all trees.

| $s$ | Least possible order | Upper bound |
|---:|---:|---:|
| 23 | 49 | 205 |
| 24 | 50 | 232 |
| 25 | 51 | 259 |
| 26 | 52 | 286 |

The lower bounds and residues come from the [21-vertex forest extension](../rainbow/twenty-one-free.md). The argument uses the existing [six-tip certificates](../rainbow/few-leaves.md#six-terminals-at-26-labels) and the [four-terminal-path bound](terminal-order.md). The orders in the table are necessary bounds. The computation supplies no noncordial example.

## Removing a forest with few tips

Put $t=s-1$ and $M=t-1$. A *side* is a component obtained by cutting one edge, rooted at its endpoint on that side. Its tips are its original leaves. More generally, take any union of components of $T-v$ for one retained vertex $v$. If the union has at most six tips, its order is at most $M$.

Indeed, if it has at least $t$ vertices, traverse these branches in preorder from $v$, visiting smaller child subtrees first. Remove the last $t$ vertices. The rest is connected, smaller, and has order one modulo 26. Its labeling has a single surplus residue, which we normalize to zero. Every outside tip was a tip in the selected group. Group the free components by their boundary colors in order of increasing size. Each component of a new run has size at least the total previous size plus the number of previous runs, by the [ordered-cut lemma](../rainbow/ordered-cut.md#which-colored-forests-actually-occur). Pad a largest component at a tip to get 25 free vertices. The six-tip certificates provide distinct nonzero labels and distinct entering weights. Restriction restores the tree, a contradiction.

For **two disjoint sides** $A,B$, each with at most three tips, write $a=|A|$. If $a\ge t-11$, then
$$
                         |B|\le t-a-1 .
$$
Otherwise keep all $a$ vertices of $A$ for deletion and take the final $z=t-a$ vertices in size-ordered preorder of $B$. The one-side bound gives $z\ge1$. The parents of both sides survive: if the two attachment edges coincided the two sides would cover the tree with at most six leaves, already excluded. For distinct edges, disjoint sides with an attachment vertex inside the opposite side would likewise cover the tree. The core is connected. The suffix in $B$ meets the ordered-cut condition and has at most three runs. Extend a tip of $A$ by $25-t$ dummy vertices. The padded size $a+25-t$ is at least $z+3$ since $a\ge t-11$. Thus $A$ can be appended after every run from $B$ with *any* boundary label. Equality of the last two colors merely joins runs. The full forest has at most six tips and the certificate restores all actual vertices. This contradiction proves the inequality.

## Finding the edge at which to join the calculation

Suppose there is no edge with at least seven original leaves on each side. Walk toward any component containing more than six original leaves. The reverse side has at most six, so the walk terminates at a vertex where every component has at most six. The tree has at least eleven leaves by the [few-leaf theorem](../rainbow/few-leaves.md), so the terminal vertex of the walk is internal. Merge groups of components whenever they have at most six leaves in total. Among the remaining $p\ge2$ groups every pair accounts for at least seven leaves. Summing over pairs gives $7p\le2L$, where $L\le M\le24$ is the original leaf count. There are at most six groups and each has order at most $M$. Hence $n\le1+6M$. One remaining group gives the same bound.

Otherwise choose an edge with at least seven leaves on both sides. Its corridor between branching vertices has this property throughout. On either half, every side with at most three leaves points away from the joining corridor. Let $a$ be the largest order of such a side in either half, including terminal arms. If $a<t-11$, both halves have cap $t-12$ on these orders. Otherwise place a maximizing side on the left. Every such side on the right is disjoint from it. The two caps are then $a$ and $t-a-1$. In every case all sides with at most six leaves retain the absolute cap $M$.

## Counting branch orders

Use the branching skeleton and the necessary restrictions in the [previous order calculation](terminal-order.md#counting-possible-orders). A half records its leaf count, parent corridor length, order, and the excess budget from the four longest terminal arms. Add the six-leaf bound at each downward cut. In a half of cap $c$, a side with up to three leaves has order at most $c$, and $j$ terminal arms at a joint have total length at most $jc$. Each half has at least seven leaves, so at most $M-7$ are needed in a branch table. Try every pair of caps above, glue two halves with the same corridor length, and count its internal vertices once. Take the maximum in the indicated residue, also admitting the bound for trees without a joining edge.

The [Python calculation](pendant_order.py) records attainable exact orders as bits for each excess cost. It reuses the local arm recurrence. The [independent C++ program](check_pendant_order.cpp) stores the least cost at each exact order before the parent corridor, with no assumed upper bound on orders. Both implementations give all four maxima above. A separate [cut check](check_pendant_cuts.py) tries every eligible short component-size list and boundary equality pattern from the second side, then appends the padded first side and rechecks every run inequality.

~~~sh
python3 -B -m research.census.pendant_order
python3 -B research/census/check_pendant_cuts.py
out=$(mktemp -d)
c++ -std=c++17 -O3 research/census/check_pendant_order.cpp -o "$out/check"
"$out/check"
~~~
