# Placing divisible pieces on several different edges

**Prime packing bound.** Suppose $T$ is a smallest ordinary counterexample at a prime $p$ and has order $n$. If it contains $m\ge1$ vertex-disjoint connected pieces, each of positive order divisible by $p$ and each incident to exactly two edges to its outside, then
$$
                   3m+1 < 2\left\lceil\frac{n-1}{p}\right\rceil .
$$
In particular, a least counterexample of order at most $3p+1$ cannot have two such disjoint pieces. Through order $5p+1$ it cannot have three. This also holds within a class of trees with a given upper bound on their number of leaves.

To see the mechanism, label each piece $P$ of order $qk$ cordially in isolation. If its port labels are $a,b$ and its deficient weight is $h$, its effective offset is $c=a+b-h$. Scaling by a unit and translating permit replacing an edge of weight $w$ by this piece so that its outgoing edge has weight $w+uc$, with $q$ copies added to all bins apart from the replacement. A chain of pieces on one edge has the sum of the individually chosen offsets. [Expansion and cancellation formula](period-chains.md)

In a smallest counterexample every chosen piece has a cordial labeling, and none can give $c=0$, since such a piece could be removed by itself. At a prime, each nonzero $c$ can be scaled to any nonzero value. Two adjacent chosen pieces could therefore cancel on their common chain, so all chosen pieces must suppress to distinct edges. Suppress them and label the resulting smaller tree of order $n'$ by minimality. Each bin contains at most $M=\lceil(n'-1)/p\rceil$ edge weights. If no weight occurs on more than half the marks, order the marked edges in blocks of equal weight. Rotate their target weights by the largest block length. Every marked edge receives a different weight and the multiset stays the same.

In fact $m\ge2M-1$ suffices. The only new case with a strict majority is $m=2M-1$ with all $M$ edges of one bin marked. A smallest failure cannot have order one modulo $p$, since a leaf could be restored at its deficient weight. The compressed order has the same residue, so the bin of size $M$ is high and a low bin exists. Move one mark from the majority bin to that low bin. Pair its remaining $M-1$ marks with the $M-1$ original marks outside and swap the original weights within each pair. Each change is nonzero and the new histogram is balanced. If the pieces have total order $Qp$, it follows that
$$
              m+2Q+1 < 2\left\lceil\frac{n-1}{p}\right\rceil .
$$
Indeed $m<2M-1$ and $M=\lceil(n-1)/p\rceil-Q$. Taking $Q\ge m$ gives the displayed packing bound.

The argument applies at any modulus $k$ when every chosen piece can give effective offset zero or can realize every nonzero offset. In a smallest failure the zero alternative is impossible, and any two adjacent chosen pieces could cancel. In particular the same inequality holds at 27 for the order-27 trees in the [two-port certificate](period-ports-27.md).

The threshold $2M-1$ is sharp as a guarantee with a fixed core labeling. For $M=q+1\ge2$, label a star's center zero and its leaves by $q$ copies of every residue and one additional copy of 1. Mark all $q+1$ edges of weight 1 and $q-1$ others. If every mark must move, at most $q-1$ weights can reenter bin 1, yet it requires at least $q$. Adjacent ports of an inserted $k$-vertex star permit exactly the nonzero changes, giving actual pieces with this constraint. This example concerns restoring that fixed core labeling.

**Small core at any modulus.** Start with any injectively rainbow-labeled tree on $n'\le k$ vertices. At each chosen edge insert a chain of cordially labeled trees of orders divisible by $k$, with any choice of ports. If each chain can realize zero or at least $n'-1$ different offsets under independent unit scalings, the resulting ordinary tree is $k$-cordial. Retain every old vertex label. First keep the old weights at untouched edges and edges permitting zero. Assign distinct destinations to the remaining edges one by one. Fewer than $n'-1$ weights have been used at every assignment. In particular this works for arbitrary chains if $n'$ is at most the least prime divisor of $k$. A chain containing a nonzero coefficient has at least as many possible sums as that coefficient's unit orbit, which has size $\varphi(k/\gcd(k,c))$. This is at least one less than the least prime divisor of $k$. At a prime $p$ the result permits arbitrary chains on every edge of any such core through order $p$.

## Exact criterion for unit offsets at a prime power

Let $k=p^a$. Fix a cordial labeling of a core of any order. Mark $m$ of its edges, each carrying a piece whose given effective offset is a unit. Its new weight can therefore be any residue in a different class modulo $p$ from its old weight. Unmarked edges keep their weights. Write $q$ for the floor of the number of core edges divided by $k$. An old bin is high if it contains $q+1$ edges and low if it contains $q$.

Count the marked edges by the residue modulo $p$ of their original weights. If no class contains more than half the marks, expansion always works with unchanged core labels. If a class $C$ contains a strict majority $m_C$, put $e=2m_C-m$. Expansion by unit scalings of the given pieces works **if and only if** both conditions hold.

* At least $e$ distinct high bins in $C$ contain a mark.
* At least $e$ low bins lie outside $C$.

For necessity, at least $e$ units of edge frequency must leave $C$. Only its marked high bins can lose one while staying balanced. Only low bins outside $C$ can gain one. For sufficiency, move one mark from each of $e$ distinct marked high bins in $C$ to different low bins outside. Equal numbers of marks remain inside and outside $C$. Pair them across the boundary and exchange their original weights. In the no-majority case, use the rotation from the packing proof, grouping by class modulo $p$. Each changed edge has a unit difference. If all old counts are equal the same argument preserves them exactly via the rotation whenever feasible.

**Consequence at 53 vertices.** Suppose two disjoint edge sides in a 53-vertex tree total 26 vertices and their 27-vertex middle piece has a bijective rainbow labeling with effective offset zero or a unit modulo 27. Then the whole tree is 27-cordial. Compress the middle to one marked edge on 26 vertices. The [integer census](../census/README.md) labels this smaller tree with 25 consecutive edge weights modulo 27. Its two unoccupied bins are consecutive, so at least one is outside the marked weight's class modulo three. The criterion supplies the unit difference if needed. Consequently, in a counterexample with this cut, *every* bijective rainbow labeling of the middle must give effective offset in $\{3,6,9,12,15,18,21,24\}$.

The [checker](check_period_edges.py) compared the criterion with a separate bipartite matching that enforces lower and upper bin capacities. They agreed on 6,640 histogram and marking cases, including 767 infeasible with the given choices. The checker also built 387 ordinary trees by replacing different edges with 4,175 pieces of one or two full periods, then recounted the vertices and all endpoint sums. At the improved threshold it rebuilt 525 more ordinary trees and checked 44 sharp examples by independent bin matching.

~~~sh
python3 -B -m research.biased.check_period_edges
~~~
