# Extending a fixed labeling across a bridge to any caterpillar

**Theorem.** Fix a $k$-cordial labeling of a tree whose order is zero or one modulo $k$. Join it by a single edge to a caterpillar of any order. Both ends of the joining edge can be chosen arbitrarily. The labeling extends with all old vertex labels preserved, for every positive integer $k$. The joining edge can carry an arbitrary additive offset.

Hovey proved that caterpillars themselves are $k$-cordial. The additional constraint here is to accommodate a specified core labeling and attachment vertex. Throughout, include the bridge offset in the old parent's label. Modulus one is immediate. [Hovey, *A-cordial graphs*](https://doi.org/10.1016/0012-365X(91)90254-Y)

## A bridge with one vertex residue forbidden

Start with a core of order one modulo $k$. Work in coordinates in which its surplus vertex residue is zero. This subtracts the same constant from all vertex labels and twice that constant from edge weights. Write $c$ for the effective parent label in these coordinates. The old edge counts are uniform. For a piece on $k-1$ vertices it suffices to use all nonzero vertex labels and obtain $k-1$ distinct new edge weights, including the bridge.

In each bipartition class number the vertices by first appearance along the spine, visiting each spine vertex's pendant edges before its outgoing spine edge. The successive edge rank pairs are coordinatewise nondecreasing, with rank sums $0,1,\ldots,k-3$. Each step keeps one endpoint and visits the next vertex in the other class. Let the marked vertex have rank $r$ in class $A$, and write $a=|A|$, $b=|B|$, so $a+b=k-1$.

Put $A$ first. Choose $0\le t\le a$, give its vertices provisional labels $i+[i\ge t]$, and give the vertices of $B$ labels $a+1+j$. Subtract $t$ from all free labels modulo $k$. The only unoccupied provisional label was $t$, so the final labels use exactly the nonzero residues. Before subtraction the internal edge sums are strictly increasing in $[a+1,a+k-1]$. They avoid $a$ modulo $k$. The bridge fills this hole (in the final coordinates, $a-2t$) when
$$
c=a-r-t-[r\ge t]\pmod k.
$$
As $t$ runs from zero to $a$, this covers $[-r,a-r-1]$. At $t=r,r+1$ the two values coincide. Alternatively put $B$ first, skipping $0\le t\le b$ in that class. The marked provisional label is $b+1+r$, and the hole at $b$ is filled when $c=-1-r-t$. This covers $[-b-r-1,-r-1]$. The two intervals adjoin and contain a whole period. For a singleton the bridge is the only weight, so any nonzero vertex label works.

Any shorter nonempty caterpillar can be padded at a spine end to order $k-1$. Restrict the labels to the original vertices and bridge. The new vertex residues still avoid the surplus and are distinct, and the new weights are distinct. For a core of order zero modulo $k$ a shorter bridge is simpler. Stack the two rank classes consecutively to obtain distinct vertex labels and distinct internal weights. Translate the free labels so the bridge fills the unique deficient old weight. The internal edges then increment distinct bins of a uniform histogram.

## A shared spine endpoint

A second short construction handles an old joint which is the first vertex of the new caterpillar's spine. Suppose there are $k-1$ new vertices. With the joint included, write its class as $A$, so now $a+b=k$. The joint has rank zero. Its $d$ neighbors have ranks $0,\dots,d-1$ in $B$ and its incident edges start the staircase. Delete the joint from class $A$ and write $i'$ for the old rank minus one on its remaining vertices. The internal edges in the free part have $i'+j$ running from $d-1$ to $k-3$, with $j\ge d-1$. If every edge meets the joint there are no internal edges.

Again normalize the old surplus to zero. Let $c$ be the joint label. Use the same gap labeling on the free classes of sizes $a-1,b$. Compare all edge weights after adding $2t$ to cancel the common internal translation. A boundary edge in this comparison has weight $c+t$ plus its free neighbor's provisional label.

- Put the free part of $A$ first and choose $c=-1-t$, $0\le t\le a-1$. The boundary weights are $a-1+j$ for $0\le j<d$. The internal weights are $a+i'+j+[i'\ge t]$. They increase strictly and lie in $[a+d-1,a+k-2]$. All weights fit between $a-1$ and $a+k-2$.
- Put $B$ first and choose $c=b-t$, $0\le t\le b$. The boundary weights are $b+j+[j\ge t]$ for $0\le j<d$. The internal weights are $b+1+i'+j+[j\ge t]$. When $t\ge d$ the boundary weights end at $b+d-1$ and the internal weights start at or above $b+d$. When $t<d$ the last boundary weight is $b+d$ and every internal column is bumped, giving a lower bound of $b+d+1$. All weights fit in $[b,b+k-1]$.

The choices for $c$ cover $[-a,-1]$ and $[0,b]$, hence every residue. Within each list the sums are distinct, and the two lists are disjoint modulo $k$. For fewer than $k-1$ free vertices pad at the far end of the spine and restrict. For a core of order zero the [shared-vertex lemma](caterpillar-joints.md) already handles every short caterpillar.

## Pieces adding a full period

A caterpillar on $k$ vertices can be added by a bridge at any mark to any labeled core, increasing every vertex and edge count by one. The stacked rank classes give all vertex residues and all but one edge residue $w$. If the marked label is $z$ and the old parent is $c$, translate the piece by $c+z-w$. The joining edge now fills the translated hole. The same argument adds a caterpillar on any positive multiple of $k$ vertices with uniform increments. [Divisible-cut lemma](../divisible-cuts.md)

Another uniform addition consists of $k$ free vertices sharing one old joint at the start of a spine. In the augmented caterpillar, stack the joint's class first. The integer labels are $0,\ldots,k$, with zero at the joint. The $k$ sums are consecutive. Translate to the old joint label. The free vertices and the edges each give one full period. This is the extreme-rank construction used in Proposition 2.1 of the six-label paper and Proposition 2.7 of the seven-label paper. [Driscoll, Krop and Nguyen](https://www.clayton.edu/cstem/docs/six-cordial-trees-ejta.pdf) · [Driscoll](https://arxiv.org/pdf/1909.12351)

These operations let us set aside $k$ vertices at a time from a spine end. Visit the end vertex's pendant leaves first, then the vertex, and repeat at the next spine position. A cut after a complete group removes a caterpillar joined to the remainder by a bridge. A cut among the leaves retains their parent, which is a spine endpoint of the removed part with the parent included. These two cases give precisely the uniform additions above. In particular a caterpillar attached at a shared spine endpoint, with any number of free vertices, can be shortened from its far end until fewer than $k$ remain. Each set-aside piece can be restored in reverse order.

## An arbitrary mark and length

Let the center be the mark itself if it is on the spine, and its spine neighbor otherwise. From each end remove full periods contained strictly on that side of the center. The remaining two arms have fewer than $k$ vertices each, excluding the center and its pendant leaves. Keep the mark in place. A reduced piece of order below $k$ is covered by the short bridge lemma. A reduced piece of order divisible by $k$ is a uniform addition.

Otherwise its order is greater than $k$. Traverse from the shorter arm, visiting each spine vertex **before** its leaves. Visit the marked leaf first at the center when applicable. The first $k$ vertices contain the mark unless the mark is a leaf and both arms have $k-1$ vertices. In that exceptional case there must be another central leaf, since with just the mark the order is $2k$. Set aside one whole arm and one unmarked central leaf. They form a uniform addition at the shared center, and traversal can now start there.

The first $k$ visited vertices form a caterpillar containing the mark and joined by the specified bridge to the original core. Add it uniformly. All still unvisited vertices, together with the last visited spine vertex, form a caterpillar sharing that one vertex at a spine endpoint. The enlarged core still has its original order residue and special bin. Apply the shared-endpoint construction there, then restore all set-aside pieces. This proves the theorem.

## Consequences for a smallest counterexample

Write $n=mk+s$, $1\le s\le k$. At a given modulus, any smaller tree than a smallest counterexample is cordial. Consequently no edge of such a counterexample can cut off a caterpillar of order $n$ or $n-1$ modulo $k$. The complement would have order zero or one and its labeling would extend. At $k=26$ and $26\mid n$ this rules out every marked caterpillar branch of order $25\bmod 26$. The other possible total-order residues at 26 labels are $21$ through $25$. There the [large-factor cut theorem](../prime/large-factor-cut.md#the-twenty-six-label-cut) already excludes pieces of order $25\bmod26$ with consecutive integer labels and edge sums. The stacked rank classes give these consecutive intervals on every caterpillar. Thus at 26 labels a caterpillar branch of order $25\bmod26$ is excluded at every total order.

There is also a size restriction independent of the order residue of the branch. Write $L,R$ for the two arm sizes at its center, $p$ for the number of central pendant leaves, and $e=1$ for a marked leaf off the spine, $e=0$ otherwise. One can remove any positive number of vertices up to $L+p-e$ by visiting the left arm in the leaf-first order and then unmarked central leaves. One either cuts a bridge or retains a shared spine endpoint. The same holds from the right. Removing exactly $s-1$ would leave an order-one core, and either short construction would restore the piece. Since $s=1$ is [already excluded](../counterexample-bound.md#removing-leaves), both $L+p-e$ and $R+p-e$ are at most $s-2$. Thus the entire branch has at most $2s-2$ vertices, improving to $2s-3$ when its mark is on the spine.

## Verification

The Python verifier reconstructs the initial edge list independently of the labeling algorithm and counts every residue, including empty bins. It checks 106,748 marked extensions using every ordered spine population through order nine at moduli $n+1$ and $\max(2,\lfloor n/2\rfloor)$, all marks and all normalized parent labels. It also checks 9,400 instances at the two-arm boundary and 3,000 whole trees with explicitly labeled cores and varying offsets. The Lean file proves the bridge coverage, the separation of the two weight lists and the exceptional arm arithmetic. The mathematical argument above supplies the reduction for arbitrary orders. [Constructor](surplus_caterpillar.py) · [Independent histogram checker](check_surplus_caterpillar.py) · [Lean arithmetic](CaterpillarGap.lean)

~~~sh
python3 -B -m research.census.check_surplus_caterpillar
lean research/census/CaterpillarGap.lean
~~~
