# Substituting trees with prescribed joining vertices

An $\alpha$-labeling in sum form assigns each of the two vertex classes its own ranks, from zero up to the class size minus one. Each class uses every one of its ranks once, and the sums across edges are exactly $0,\ldots,n-2$ on a tree of order $n$. Adding the size of the first class to all ranks in the second makes both the vertex labels and the edge sums consecutive integer intervals. Reducing these labels modulo any $k$ gives a cordial labeling, including when some frequencies are zero.

Call a vertex fully attainable if each rank of its own class can be assigned there in some such labeling. The choice of labeling may depend on the vertex and the rank. This requirement is strictly stronger than existence of an $\alpha$-labeling.

## Equal even orders and arbitrary joining vertices

**Theorem.** Let a quotient tree $Q$ have equally large vertex classes and let all its vertices be fully attainable. Replace each of its $q$ vertices by a tree of order $2s$, with two classes of size $s$ and all vertices fully attainable. For each quotient edge join any prescribed pair of vertices in the corresponding pieces. The resulting tree has two equal classes and every vertex is fully attainable. Piece shapes may differ, and several joins may use the same vertex.

To assign rank $R$ to a given vertex, root $Q$ at its piece $u$. Write $R=s i+j$, $0\le j<s$, $0\le i<q$. Choose within-class quotient ranks $r$ with $r(u)=\lfloor i/2\rfloor$. Give one quotient class the even slots $2r$ and the other the odd slots $2r+1$, choosing the parity of $u$ to be $i\bmod2$. All slots occur once, and their sums across edges are the odd numbers $1,3,\ldots,2q-3$.

Choose a piece labeling at $u$ giving the target vertex rank $j$. Visit its descendants from parent to child. If the parent’s actual joining vertex has local rank $x$, assign local rank $s-1-x$ to the child’s actual joining vertex. Each child receives only one instruction before its labeling is chosen. In particular the proof requires no simultaneous choices at several vertices of one piece.

Use whole-tree rank $s\,i'+y$ at a vertex with local rank $y$ in slot $i'$. The joined tree is bipartite. Each piece supplies each rank of its interval exactly once on each global side, whichever way that piece is oriented. The internal rank sums in slot $i'$ fill $2s i'+[0,2s-2]$. A bridge between slots summing to $2d+1$ has rank sum $s(2d+1)+(s-1)=2sd+2s-1$. These are exactly the single gaps between the $q$ intervals. The target has rank $R$, as required.

In the two-vertex-piece case, Luiz, Campos and Richter characterize when a tree with a perfect matching has a strongly $\alpha$-labeling in terms of its contracted tree. The theorem above keeps track of a requested vertex rank and allows larger, nonisomorphic pieces. Substitution constructions for graceful trees and prescribed labels on paths have an extensive literature. [Luiz, Campos and Richter, Theorem 14](https://ic.unicamp.br/~reltech/2017/17-14.pdf) · [The substitution theorem for graceful trees](https://www.cs.ucy.ac.cy/~mavronic/pdf/GRACEFUL.pdf) · [Cattell, *Graceful labellings of paths*](https://doi.org/10.1016/j.disc.2007.03.046)

## Unequal class sizes

Suppose $Q$ has an $\alpha$-labeling and its two class sizes differ by at most one. Again give its vertices slots $2r$ and $2r+1$ from their within-class ranks, using even slots on the larger class at odd order. At each slot use an $\alpha$-labeled tree with the same ordered pair of class sizes $(a,b)$, writing $n=a+b$. Each joining edge must use like classes at its two ends. It can join two first-class vertices or two second-class vertices, independently at each edge. Assume every vertex used as an incoming port can attain every rank in its class. At the root use any labeling, or prescribe an attainable rank there.

**Theorem.** All these joined trees admit an $\alpha$-labeling. In particular one may place equal stars on any such quotient, joining any specified leaves to leaves or centers to centers.

Choose complementary port ranks along each join by the same rooted traversal, replacing $s$ by the size of the port class. Let $A=\lceil q/2\rceil a+\lfloor q/2\rfloor b$. The whole-tree integer label for local rank $y$ is given below.

| Quotient slot | First local class | Second local class |
| --- | --- | --- |
| $2r$ | $rn+y$ | $A+rn+y$ |
| $2r+1$ | $A+rn+b+y$ | $rn+a+y$ |

Even and following odd slots together fill a block of length $n$ in each whole-tree class. At odd $q$ the final even slot adds $a$ ranks on the first side and $b$ on the second. Internal sums at slot $i$ cover $A+in+[0,n-2]$. For a join between slots $2r,2t+1$, a first-class pair gives $A+(r+t)n+b+(a-1)$, and a second-class pair gives $A+(r+t)n+a+(b-1)$. These coincide and fill the missing entries because the quotient edge ranks $r+t$ use $0,\ldots,q-2$.

If $q$ is even and every quotient vertex is fully attainable, a fully attainable vertex in the larger local class can attain **every** whole-tree class rank. For instance, suppose it belongs to the first class of size $a\ge b$. In either slot parity choose its quotient rank $r$ freely. Its offsets in the $n$-block of class ranks are $[0,a-1]$ for an even slot and $[b,n-1]$ for an odd one. Their union is the full block. The second-class case follows by renaming the local classes. For equal sizes, the first theorem also permits arbitrary cross-class ports because the class names may be exchanged independently in each piece.

## Direct checks

The checker enumerates all within-class permutations when classifying the unrooted shapes at each order below. The three fully attainable shapes of order eight are available as distinct substitution factors. The path of order six illustrates the extra force of prescribing a rank.

| Order | Unrooted trees | Two equal classes | All vertices fully attainable |
| ---: | ---: | ---: | ---: |
| 2 | 1 | 1 | 1 |
| 4 | 2 | 1 | 1 |
| 6 | 6 | 3 | 0 |
| 8 | 23 | 9 | 3 |
| 10 | 106 | 37 | 1 |

The independent verifier reconstructs all original edges at their specified vertices, computes the global bipartition and checks the integer labels and sums. It verifies 104,816 demands on equal-class products, including iterated products, and 5,726 products of stars with fixed attachments, including pins in the larger class. [Constructor](flexible_products.py) · [Verifier](check_flexible_products.py)

~~~sh
python3 -B -m research.census.check_flexible_products
~~~
