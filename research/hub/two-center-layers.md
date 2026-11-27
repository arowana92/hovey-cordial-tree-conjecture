# Independent branch sizes on the two sides of a diameter-five tree

**Theorem.** Join two centers by an edge. Give each center $h$ branch parents. Give every branch parent a positive number of leaf children. These $2h$ numbers can all differ. The resulting tree is super edge-magic and is cordial at every positive modulus.

The theorem permits further leaves directly at either center. On each side their number must be strictly smaller than the least branch child count on that side. When $h=0$ any two direct leaf counts work. For example, one center can have branch child counts $(11,5,2)$ and one direct leaf, and the other counts $(21,7,4)$ and three direct leaves. The number of centers' neighbors with children is the only equality in the statement. The integer intervals give the result for all moduli by [Youssef's theorem](https://ajc.maths.uq.edu.au/pdf/43/ajc_v43_p031.pdf).

## Two independently extensible lists of parents

Start with one leaf per branch parent and put $m=2h+1$. Use the [matched-arm construction](matched-arms.md) with center labels $h,h+m$, integer vertex interval $[0,2m-1]$, and edge interval $[m,3m-2]$. At distance $j$ from the central index, always use the upper endpoint of pair $h-j$ as its arm parent and the lower endpoint of pair $h+j$ as its arm parent. For even $j$ the first belongs to the upper center and the second to the lower center. For odd $j$ those assignments reverse. This gives the required joining sums in the matched-arm table. Each center receives one branch at every distance.

Rank each side's branches by decreasing child count. Assign rank $t$ to distance $j=h+1-t$ for $1\le t\le h$. The two parent labels at rank $t$ are
$$
m-t,\qquad m+t-1.
$$
The parent on the lower-center side has parity $h$ and the other has opposite parity. This follows for even $j$ from the lower-center parent $h+j$, and for odd $j$ from its parent $m+h-j$. Rank $h+1$ has the same description if we take the lower and upper centers themselves as the two parents. Consequently the first $r$ parents on each side consist of a single parity class of the interval $[m-r,m+r-1]$.

Suppose the current vertex interval is $[L,U]$ and the edge interval is $[L+m,U+m-1]$. To add a leaf to each of the first $r$ parents on just one side, use the row of the following table with their parity. Here $0\le i<r$.

| End extended | Leaf label | Parent label | Edge weight |
| --- | --- | --- | --- |
| lower | $L-r+i$ | $m+r-1-2i$ | $L+m-1-i$ |
| upper | $U+1+i$ | $m+r-2-2i$ | $U+m+r-1-i$ |

The parent columns are the two parity classes of the required interval. In the lower row both intervals extend down by $r$. In the upper row both extend up by $r$. Thus the relation between the two intervals persists, as do all existing parent labels. Layers on opposite sides can be chosen independently.

On one side let $c_1\ge\cdots\ge c_h\ge1$ be the child counts and let $d$ be its direct leaf count. The desired additional counts in rank order are $c_1-1,\ldots,c_h-1,d$. These are weakly decreasing by hypothesis. For any decreasing list of nonnegative integers $e_1,\ldots,e_s$, adding $e_r-e_{r+1}$ layers of rank $r$, with $e_{s+1}=0$, realizes precisely that list. Apply this separately on the two sides. At $h=0$ start from the central edge and give the two centers their rank-one layers.

## Unequal numbers of branches

Let $a,b$ be the numbers of branch parents, where $a+b=2h$ and $d=|a-h|\ge1$. Set $r=h-2d+1$. Suppose $r\ge0$, every branch has at least one child, and on each side at most $r$ branches have more than one child. With no direct center leaves, the tree is again super edge-magic.

Use the preceding rank assignment for the first $r$ distances in descending order. It consumes $r$ branch parents on each side. The remaining distances are $1,\ldots,2d-1$. The $d-1$ even distances give one arm to each center. At the $d$ odd distances give both arms to the more populated center, using the flexibility of the matched-arm table. The final numbers are $r+d-1=h-d$ and $r+d-1+2d=h+d$. Only the first $r$ ranks need further children. Their parity classes remain available for the two independent interval extensions. For instance if $a=b+2$, all $b$ branches on the smaller side can have arbitrary populations, as can all but two on the larger side.

## Checks

The Python checker reads the finished ordinary edge list from the two centers outward. It independently recovers both multisets of branch child counts and both direct leaf counts, verifies that it has visited the entire tree, and tests both integer intervals by sorting. It checks 5,027 equal-count and 3,900 unequal-count trees. Lean verifies the parity classes, the endpoint-sum identities and the interval reversal used in a layer. [Constructor](two_center_layers.py) · [Independent checker](check_two_center_layers.py) · [Lean verification](TwoCenterLayers.lean)

~~~sh
python3 -B -m research.hub.check_two_center_layers
lean research/hub/TwoCenterLayers.lean
~~~
