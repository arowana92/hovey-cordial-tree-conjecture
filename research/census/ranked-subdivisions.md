# Edge rankings and subdivisions at prescribed orders

Let $\operatorname{er}(T)$ be the minimum height of an edge ranking of a nontrivial finite tree $T$. In an edge ranking, any two edges with the same positive rank are separated on their connecting path by an edge of higher rank. Write $\operatorname{er}(K_1)=0$. The parameter can be computed in linear time by Lam and Yue. The small verifier below uses the elementary separator recurrence instead. [Lam and Yue, *Optimal edge ranking of trees in linear time*](https://hub.hku.hk/handle/10722/152303)

**Subdivision theorem.** For every $N\ge 2^{\operatorname{er}(T)}$, there exists a subdivision of $T$ on exactly $N$ vertices with an $\alpha$-labeling. A single integer labeling of that subdivision is cordial after reduction at every positive modulus. At a power of two in this range, every vertex can attain every rank in its own class, with the labeling chosen for the request.

**Original-tree theorem.** Suppose $|T|=2^h$ or $2^h-1$ and $\operatorname{er}(T)\le h$. Then $T$ itself has an $\alpha$-labeling and is cordial at every modulus. At order $2^h$ it also has the full rank property. The condition on the ranks is essential to the construction. The subdivision assertion applies to arbitrary input trees.

## Completing the bisections

Start with a singleton at height zero. At height $h$ allow any tree obtained by joining two trees of height $h-1$ by a single edge between arbitrary vertices. Such a tree has $2^h$ vertices. At height one it is a single edge. At every positive height it has two equal bipartition classes and full rank attainability, by the [substitution theorem](flexible-products.md) with quotient a single edge. Paths on $2^h$ vertices belong to this family at each height.

The largest rank in a connected edge-ranked tree occurs on a unique edge. Removing it leaves two parts of smaller ranking height. Conversely two ranked parts can be connected by an edge of strictly higher rank. In particular an $h$-ranked tree has at most $2^h$ vertices.

For a tree of positive order in edges with ranking height at most $h$, construct a subdivision in the bisection family of height $h$. The base $h=1$ is a single edge. Remove a largest-ranked edge $uv$. On each nonsingleton side, use induction to subdivide the side to order $2^{h-1}$, retaining the image of its original endpoint. On a singleton side take a path on $2^{h-1}$ vertices. Attach the bridge at one end and let the far end represent the original singleton. The extra path vertices on that side subdivide $uv$. Join the two parts at the specified ports. All original edges are represented by internally disjoint paths with their original endpoints, and the construction accounts for every new edge.

This threshold is **exact within the bisection family**. Give the last joining edge rank $h$ and use the lower rankings recursively in the two halves. This is an $h$-edge-ranking. If a subdivision of $T$ has such a ranking, assign each original edge the largest rank on its replacing path. For equal-ranked original edges, their two witnesses of that rank are separated by a strictly higher rank. It must belong to an intermediate original edge, since neither end path contains any higher rank. Hence $\operatorname{er}(T)\le h$. For a $d$-leaf star the minimum height in this family is $d$, since its incident edges require distinct ranks.

## Filling arbitrary orders and labeling the original tree

Here is a two-piece construction. Let $F$ have equal classes of size $s$ and all ranks attainable at the specified port $u$. Let $B$ be any tree with a fixed $\alpha$-labeling in within-class ranks and with rank $y<s$ at its joining vertex $v$. This includes a singleton, whose rank is zero. Choose rank $s-1-y$ at $u$. Orient the local bipartitions so the new edge crosses global classes. Keep the ranks of $F$, and add $s$ to every rank in $B$. Each global class uses a full initial interval. The internal rank sums on $F$ are $[0,2s-2]$, the joining sum is $2s-1$, and the internal sums on $B$ are $2s+[0,|B|-2]$, empty for a singleton. Thus the joined tree has an $\alpha$-labeling.

Given a subdivision $F$ on $2^{\operatorname{er}(T)}$ vertices from the bisection construction, extend any of its leaves by a path on $N-|F|$ new vertices, moving the original leaf to the far end. For a nonempty added path, the consecutive within-class ranks along it are $0,0,1,1,2,2,\ldots$, truncated at its order. The incoming rank is zero, so the two-piece construction applies regardless of the path length. This proves the first theorem at every prescribed order.

For the second theorem, at order $2^h$ equality in the edge-ranking capacity bound forces both sides of a maximum edge to have order $2^{h-1}$. Recurse to obtain bisections throughout. At order $2^h-1$, the two sides have orders $M=2^{h-1}$ and $M-1$, each of ranking height at most $h-1$. When $M\ge2$, the full side is in the bisection family. The smaller side has by induction an $\alpha$-labeling and bipartition sizes $M/2$ and $M/2-1$, with the singleton included. Joining uses its actual port rank, which is less than $M/2$. The two-piece construction gives the required labeling. The class sizes differ by one, since the full side contributes equally to the two global classes. A singleton supplies the base.

For maximum degree $\Delta\ge2$ the universal subdivision threshold above is polynomial in $n=|T|$ at fixed $\Delta$. At a centroid the largest branch has order between $(n-1)/\Delta$ and $n/2$. Cut its edge. Each resulting part has at most $(n-1)(1-1/\Delta)$ edges. Repeating on each part gives $\operatorname{er}(T)\le1+\lfloor\log_{\Delta/(\Delta-1)}(n-1)\rfloor$.

## Verification

For all 200 unrooted trees of orders 2 through 10, the checker constructs a ranking, checks each rank threshold by connected components and verifies explicit subdivisions at the minimum bisection height and one greater. It suppresses the new degree-two vertices to recover every original edge, and checks actual integer vertex and edge histograms. It also checks 1,000 subdivisions at other prescribed orders. A second enumeration joins all possible equal halves through order 16 and suppresses degree-two vertices in all possible ways. Across its 1,768 distinct resulting shapes it checks the computed minimum heights and verifies every one of the 358 near-power original trees. [Construction](ranked_subdivisions.py) · [Independent checks](check_ranked_subdivisions.py)

~~~sh
python3 -B -m research.census.check_ranked_subdivisions
~~~
