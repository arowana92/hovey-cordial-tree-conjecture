# Restoring two leaves and subdividing one edge

**Theorem.** Take any labeled tree, choose an edge with endpoint labels $a,b$, and attach two new leaves at old vertices labeled $p,q$. Insert $k-2$ vertices on the chosen edge. One can keep every old label and increase **every vertex count and every edge count by one** at every odd $k\ge5$ and every even $10\le k\le64$. The parents may coincide with each other or with either endpoint. At six and eight labels this uniform-increment statement has the exceptions below.

In particular, for every such $k$, any $n$-vertex tree becomes $k$-cordial on subdividing any chosen edge by **any** number of vertices at least
$$
(k-2)\left\lfloor (n-2)/2\right\rfloor .
$$
This improves the [one-leaf padding bound](edge-padding.md). In a smallest ordinary counterexample at 26 labels, no connector between branching vertices can have more than **23 internal degree-two vertices**. Such a tree would have at least eleven leaves. Suppressing 24 consecutive internal degree-two vertices and deleting two leaves outside that path gives a smaller tree to which the theorem applies. The earlier [order-dependent bound](cycle-subdivision.md) still applies at the other order residues.

## Turning a cycle into a subdivision

Let $S=\sum_{i\in\mathbb Z_k}i$. If the leaf labels are $x,y$, the inserted vertices must be the complement of $\{x,y\}$. Taking moments of the net edge increment forces $x+y=p+q+S$. Indeed the net path contribution after deleting the old edge is twice the sum of the inserted labels. Find a cycle on that complement whose edge sums are precisely the complement of $\{p+x,q+y\}$. If it contains $a$, walk once around the cycle from $a$, ending at a new copy of $a$. Join this copy to $b$ to recover the deleted edge sum. Two different omitted pairs of the required sum are disjoint; thus two such cycles guarantee that one contains any prescribed $a$.

## Explicit switches at every odd modulus

Write $k=2r+3\ge7$. On the interval $0,\ldots,2r$ take the cyclic order
$$
0,r+1,1,r+2,\ldots,r-1,2r,r .
$$
Its integer sums are exactly $r,\ldots,3r$. Thus its omitted vertex labels are $-2,-1$ and its omitted weights are $r-2,r-1$ modulo $k$. Assigning the two omitted weights to the leaves in either order gives normalized parent differences $0$ and $-2$.

For $1\le t\le\lfloor r/2\rfloor$, set $i=t-1$ and $j=r-t$. Reverse the segment between the cuts at $(i,r+1+i)$ and $(j,r+1+j)$. The new edges join the two lower ends and the two higher ends. Their sums $r-1$ and $3r+1$ fill the old holes. The new missing weights are $A=r-1+2t$ and $B=3r+1-2t$. Assigning them in the two possible orders to the leaves gives parent differences $4t$ and $k-2-4t$.

It remains to choose two different omitted pairs for each actual difference $h=q-p$. A change $z\mapsto uz+d$ on all vertices multiplies a parent difference by the unit $u$, and translation matches the first parent exactly. Every omitted vertex pair of a transformed cycle has difference $\pm u$.

* For $h=0$, use the original equal-parent cycle with scales 1 and 2.
* For $h$ a unit, use the original difference $-2$ and the switched difference 4. The two required scales differ even up to sign, since $k\ge7$.
* Otherwise let $g=\gcd(h,k)>1$ with $h\ne0$. If $g\le\lfloor r/2\rfloor$, use $t=g$, giving difference $4g$ with gcd $g$. Otherwise $k/g=3$: any odd quotient at least five would give $g\le(k-3)/4$ since $g\ge3$. Take $t=(g-1)/2$ so that $k-2-4t=g$. In either case multiplication by units reaches $h$. The number of possible scales is $\varphi(k)/\varphi(k/g)\ge2$, by the prime-power formula for the totient and surjectivity of reduction of units onto the divisor. Two such scales cannot be negatives of one another, since $h\ne-h$.

In each case the omitted pairs differ, and the common moment equation makes them disjoint. At five labels direct enumeration supplies a witness for every one of the 75 normalized choices of $q,a,b$, taking $p=0$ and $a\le b$.

## Even moduli and small exceptions

For each even modulus from 10 through 64, the [cycle certificate](two-leaf-cycles.txt) supplies two cycles with disjoint omitted pairs for parents $0,g$, for every proper positive divisor $g$ and for $g=0$. The verifier checks all vertices and cyclic endpoint sums in every row. Translations and unit multiplications carry these cases to all parental differences. The rows are positive witnesses; no conclusion about unlisted moduli depends on the search.

At six labels the only normalized failures have $q=0$ and $(a,b)=(2,2),(4,4)$. At eight they have $q=4$ and $(a,b)=(0,4),(1,3),(2,2),(5,7),(6,6)$. Here $p=0$ and $a\le b$. The small-case verifier tries every leaf pair of the required sum and every ordering of the remaining vertices on the actual path, including paths that do not come from a cycle. These failures concern uniform increments on prescribed labels; every ordinary tree is cordial at both moduli.

## Peeling in pairs

Retain the chosen edge and repeatedly remove two leaves outside its endpoints. At each step the two parents survive. At termination the rest is a path: a tree with a branching vertex has at least three leaves, and the two endpoints of a retained edge cannot both be leaves in such a tree. With $j$ pairs removed we have $j\le\lfloor(n-2)/2\rfloor$. Place any subdivisions beyond $(k-2)j$ on the chosen edge of the remaining path and label that path cordially. For example, alternate the lower and upper halves of the consecutive integer vertex labels in increasing order within each half. Restore the pairs in reverse order, each time putting $k-2$ subdivisions into one segment of the chosen edge. The net increment is uniform at every step. [Constructor](two_leaf_padding.py)

## Reproduction

Run from the repository root with Python 3 and a C++17 compiler, using Bash.

~~~bash
set -eu
out=$(mktemp -d)
c++ -O3 -std=c++17 research/census/two_leaf_cycles.cpp -o "$out/cycles"
for k in {10..64..2}; do "$out/cycles" "$k"; done > "$out/witnesses"
cmp "$out/witnesses" research/census/two-leaf-cycles.txt
python3 -B -m research.census.check_two_leaf_padding
~~~

The check covers 350 certified cycles, 110,049 actual leaf-and-path assignments, 670 complete subdivided trees and all normalized inputs at five, six and eight. The uniform result for unbounded odd moduli follows from the switch argument. [Independent verifier](check_two_leaf_padding.py)
