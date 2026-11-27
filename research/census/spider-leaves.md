# Spiders with at most four legs longer than one

**Theorem.** A spider with at most four legs longer than one has an integer labeling whose vertex set and edge sums are consecutive intervals. Its degree and the lengths of the four legs are unrestricted. The same labeling gives cordiality at every positive modulus.

For example, one may add any number of leaves to the center of the spider with legs $2,2,2,14$. This family includes trees of arbitrarily large order, maximum degree and diameter as the leg lengths and leaf population vary. Panpa and Poomsa-ard studied graceful labelings with the same restriction on long legs. The construction here gives consecutive ordinary edge sums. [Panpa and Poomsa-ard, *On Graceful Spider Graphs with at Most Four Legs of Lengths Greater than One*](https://doi.org/10.1155/2016/5327026) · [Four-leaf construction and path lemmas](four-leaves.md)

## Adding leaves at a specified vertex

Use the bipartition ranks and the two joining rules from the four-leaf proof. If a vertex has rank zero in its class, add $m$ leaves there. Increase every old rank on the opposite side by $m$ and give the leaves the ranks $0,\ldots,m-1$. The new weights fill the first $m$ sums, and every old edge sum increases by $m$. In particular the attachment vertex retains rank zero.

There is also an ordinary integer version. Suppose the vertex labels are $0,\ldots,n-1$, the center label is $x$ and the edge sums are $x+1,\ldots,x+n-1$. Giving the next $m$ leaves the labels $n,\ldots,n+m-1$ extends both intervals at their upper ends.

## Proof for spiders

Set aside the $m$ one-edge legs. With at most two longer legs, the remaining vertices lie on a path. Use one star block at each path vertex, including the set-aside leaves at the central block. Every star center has rank and deficiency zero in its singleton bipartition class. Joining these blocks in path order gives the required labeling.

With three or four longer legs, apply the marked-path pairing from the four-leaf proof. When there are three, choose two lengths different from the pair $(2,2)$. When there are four, choose two pairs neither of which is $(2,2)$. Place all $m$ leaves at rank zero on the first path before reflecting it and identifying the centers. All cases with at most two legs of length two are covered. With three longer legs all of length two, the center label 3 and the arm rows $(6,0),(5,2),(1,4)$ have least sum 4, so the ordinary extension works for all $m$.

It remains to treat four long legs of lengths $2,2,2,t$, where $t\ge2$. When $t=2,3,4,6$, four certified rows on the tree with no direct leaves have least sum equal to the center label plus one. When $t=5$ or $t\ge7$, first label $S(2,2,t)$ with rank zero at its center. Add the $m$ leaves at this zero, reflect, and identify the center with the rank-zero end of a path of length two. This establishes the theorem. [Four ordinary rows and constructor](spider_leaves.py)

The required center-zero statement for $S(2,2,t)$ is Lemma 3.6 of Panpa, Imnang and Wasuanankul. There is also a short replay using the endpoint lemma. At $t=5$, the rank row $0,0,1,2,2,3,3,4,4,1$ has center zero and long-tip deficiency three. Direct rows give center zero for $7\le t\le11$. For $t\ge12$ append $t-5$ vertices starting at rank three, preserving every original rank. The only exception is $t=18$. There use the row for $t=7$, which also has tip deficiency three, and append eleven vertices. [Panpa, Imnang and Wasuanankul (2025)](https://doi.org/10.1155/jama/5826777)

## Leaves along a path between two branching vertices

Take a path with distinct endpoints $u,v$. At each endpoint attach two terminal paths of arbitrary positive lengths, with neither pair of lengths equal to $(2,2)$. Attach any number of additional leaves at **each** vertex of the original path, including both endpoints. The resulting tree is also super edge-magic and cordial at every positive modulus.

Indeed, at $u$ and $v$ the two terminal paths have rank zero at their common vertex by the marked-path theorem. Include each endpoint's extra leaves by the zero-rank construction and reflect the block at $u$. The interior connector vertices, together with their own direct leaves, are individual stars. Join the left block, these stars in path order, and the right block. Every bridge connects local deficiency zero to local rank zero. This covers an empty connector interior as well.

## Reproduction

From the repository root run

~~~sh
python3 -B -m research.census.check_spider_leaves
~~~

The checker verifies the nine new finite rows and directly recomputes the vertex labels and edge sums of 3,639 spiders and 2,304 trees with leaves along their connectors. The proof covers every nonnegative number of direct leaves. [Independent checker](check_spider_leaves.py)
