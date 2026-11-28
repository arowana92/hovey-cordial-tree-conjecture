# Cutting three subtrees from a 52-vertex tree

**Theorem.** Let three edges separate a tree on 52 vertices into a connected middle tree $U$ of order 27 and three exterior components. Write $u,v,w$ for the vertices of $U$ incident to the three cut edges. Suppose two of them, say $u,v$, are distinct and nonadjacent, and adding $uv$ to $U$ gives a graph with zero or two through six leaves. The original tree is 27-cordial. The third edge may meet either of the first two vertices. There is no restriction on the shapes of the exterior components.

## Compressing the middle to two edges

Write $a,b,t$ for the exterior endpoints opposite $u,v,w$, respectively. Closing $U$ by $uv$ gives a simple connected unicyclic graph. On 27 vertices the [unicyclic census](few-leaf-rings.md) supplies a bijection $g$ whose edge sums are a bijection when there are two through six leaves. With no leaves, label the cycle in cyclic order by consecutive residues. Its sums are distinct since 27 is odd.

Join the three exterior trees by the two edges $ab,at$. Use ordinary weight on $ab$ and offset $g(w)-g(v)$ on $at$. This is a tree on 25 vertices, so the [one-offset theorem](../biased/one-offset-25.md) supplies an injective labeling $f$ with 24 distinct adjusted weights. Translate all of $g$ by $f(a)-g(v)$, obtaining $g'$ with $g'(v)=f(a)$. In the restored tree the three joining edges have the following weights.

| Physical edge | Weight it supplies |
|---|---|
| $au$ | The closing weight $g'(u)+g'(v)$ |
| $bv$ | The ordinary weight $f(a)+f(b)$ |
| $tw$ | The adjusted weight $f(a)+f(t)+g(w)-g(v)$ |

Thus the 27 new vertices contribute one of each label. The internal middle edges and $au$ contribute one of each weight. The other two joining edges replace the weights counted on the compressed tree. Every final bin is balanced.

The same calculation works for any modulus whenever the closed graph contributes the same positive number of copies to every vertex and edge bin and the compressed tree is cordial with that one offset. At 27 the compressed tree may have **any order** if it has at most seven leaves. [One offset on trees with at most seven leaves](../biased/period-ports-27.md)

## Recognizing cuts

* If the three ports are distinct and $U$ has four through six leaves, some port pair is nonadjacent since $U$ is a tree. Closing it removes at most two leaves and leaves between two and six.
* Suppose the three ports are distinct and $U$ contains two through five leaves of the original tree. Any additional leaf of $U$ is a port. With at least two such leaves, close two of them. With one such leaf, at least one other port is nonadjacent to it. With none, take any nonadjacent pair. At most one additional leaf survives. Every original leaf inside $U$ survives because it is distinct from the ports.
* If there are just two distinct ports, closing them leaves precisely the original leaves inside $U$. More generally, let any number of exterior components attach at $v$ and one further component at $u$. If closing $uv$ has a labeling uniform on vertices and weights, use the root $a$ of the single component as the common exterior endpoint of all the compressed edges. Translating $g(v)$ to $f(a)$ restores them all with ordinary weights. Any cordial labeling of this compressed tree works, at every order.

The [five examples](three-side-examples.jsonl) have 19, 20, 21, 22 and 23 leaves. Their centroid profiles lie outside the earlier cut catalog used to prepare the [order-52 checklist](order-fifty-two.md#a-finite-checklist-for-all-remaining-leaf-counts). In each actual tree, no two disjoint single-edge sides total 25 and no union of branches at any vertex totals 22 or 24. Each supplied labeling can be checked on the original 51 edges. These five cases leave the general order-52 question open.

The [checker](check_three_side_cuts.py) reconstructs both directions of every edge cut, the closed graph, the adjusted exterior tree and the final frequency lists from the supplied parents and residues.

~~~sh
python3 -B -m research.census.check_three_side_cuts
~~~
