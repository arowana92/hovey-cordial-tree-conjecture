# Subdividing an edge while keeping the old tree labeled

**Theorem.** Fix $k\ge5$ and any cordial labeling of a tree of order one modulo $k$. Write $y$ for its surplus vertex label. Replace a chosen edge with a path by inserting $t$ new vertices. The old labels extend for every $t\ge0$, with precisely the following exceptions.

- $t=1$ and both old endpoints have label $y$.
- $k\equiv2\pmod4$ and $t$ is an odd multiple of $k$.

From a prescribed **divisible** core, every $t=jk+r\ge k$, $0\le r<k$, also works, except when $k$ is even, $r=1$, and the old deficient edge weight $D$ satisfies $D+jk/2$ odd. This exception is necessary. A pendant path of any length extends a prescribed core of either order residue at **every** positive modulus.

**Consequence.** If a smallest counterexample has order $mk+s$, then every terminal path has length at most $s-2$, and a connector between branching vertices has at most $s-2$ internal degree-two vertices. At 26 and 27 labels, subdividing one edge of **any tree of order at most 27** by any number of vertices gives a cordial tree at every resulting order.

## A short cycle inserted at an endpoint

Put $S=\sum_{x\in\mathbb Z_k}x$, which is zero for odd $k$ and $k/2$ otherwise. For $3\le h<k$, every interval of $h$ consecutive residues has a cyclic ordering with all $h$ adjacent sums distinct. The same holds for $h=k$ odd. We use Mosahab's constructive interval theorem. For the special length $k-1$, related group results give a cyclic near transversal at even $k$ and a harmonious ordering of the nonzero residues at odd $k>3$. [Mosahab, Theorem 1.1, preprint](https://doi.org/10.2139/ssrn.7166164) · [de Wolf and Javaheri, Theorems 4.2–4.3](https://escholarship.org/content/qt5489614t/qt5489614t.pdf) · [Beals, Gallian, Headley and Jungreis](https://deepblue.lib.umich.edu/bitstream/handle/2027.42/29431/0000512.pdf)

First suppose $3\le t<k$. Translate the surplus label to zero. If one endpoint has nonzero label $a$, choose an interval of $t$ nonzero residues containing $a$. Starting at that endpoint, traverse the cycle beginning immediately after $a$ and ending at a **new copy of $a$**. The edge from the copy to the far endpoint retains the old edge weight. Thus all incremental weights are distinct and all new vertices avoid the surplus.

If both endpoints are zero, take a cycle of length $t+1$ on $[0,t]$. This applies also at $t+1=k$ odd. Some adjacent pair has even integer sum $2j$: there are only $t$ odd integers between 1 and $2t-1$, and the $t+1$ cyclic sums are distinct integers. The midpoint $j$ is a vertex of the interval. Subtract $j$ from all labels, start the cycle at zero and return to zero. Its $t$ internal vertices are distinct and avoid zero. The edge weights are distinct and include zero, so one of them replaces the deleted old weight. At $t+1=k$ even, the repeated-zero cycle below gives the same conclusion after subtracting the deleted zero weight.

For $t=2$ with old endpoints $a,b$, use new labels $x,z=a+b-x$ to reproduce the deleted weight on the middle edge. Avoid $x=0$, $z=0$, $2x=a+b$ and $2x=2b$. The latter two conditions exclude at most two residues each. A choice exists for $k\ge7$. At five and six the constructor tries the ordered pairs of distinct nonzero labels and the independent verifier checks all endpoint assignments. For $t=1$ the new label must equal an old endpoint to reproduce the deleted weight, and it must avoid the surplus. These two conditions suffice.

For a pendant path reduce its length modulo $k$ using the [neutral pendant-path block](../counterexample-bound.md#shortening-paths). With a nonzero parent, the same short cycle works for $3\le t<k$ without a far endpoint. With parent zero, label even positions $2i$ by $i$ and odd positions $2i+1$ by $\lceil(t+1)/2\rceil+i$. Including the root at position zero gives exactly $[0,t]$ and the path weights are consecutive. For two vertices choose distinct nonzero labels and avoid the parent on the tip. One vertex needs only avoid the surplus. To grow from a divisible core, first add one vertex to fill its edge deficit and continue from the new endpoint.

## An even Hamilton cycle with prescribed repeated weight

At even $k=2r\ge6$, there is a cyclic ordering of **all** residues whose adjacent sums repeat any specified $D$ twice and omit just $D+r$. It suffices to obtain an odd and an even repeated weight, since a uniform translation of vertices moves weights by twice the translation. The alternating order $0,r,1,r+1,\ldots,r-1,2r-1$ repeats the odd weight $2r-1$. For $r$ odd, Mosahab's even interval construction has integer sums $[r-1,3r-1]\setminus\{2r-1\}$ and consequently repeats $r-1$, which is even.

For $r$ even we give a modification of the low- and high-path construction in that paper. At $2r=8$ the cycle $0,1,4,2,6,5,3,7$ repeats zero. For even $r\ge6$, take the same low path $L_r$ from $2r-2$ to its other endpoint. Its vertices after the first are $(i-1)/2$ for odd indices $i$ and $r-2+i/2$ for even indices $i$, with $1\le i\le r$. Its sums are $[r-1,2r-2]$. Join its endpoints by a high path using the complementary vertices. Require the mixed edges of the high path, with one endpoint below $r$, to give
$$
[2r-1,3r-3]\setminus\{2r\}.
$$
The two edges with both endpoints at least $r$ must give $3r-2$ and $3r$. The following base paths meet these conditions by substitution.

| $r$ | High path from the end of $L_r$ back to its start |
| ---: | --- |
| 6 | $7,9,4,11,3,8,10$ |
| 8 | $10,12,5,13,11,4,15,6,14$ |

To increase $r$ by four, move each old high-path vertex below $r$ up by two and each other vertex up by six. Append $r+2,2r+7,r+1,2r+6$ after the moved endpoint $2r+4$. The vertex sets and endpoints obey exactly the recurrence of Mosahab's Lemma 4.2, since the base sets match and only the ordering changed. Old mixed sums grow by eight and the two high-high sums grow by twelve. The four appended mixed edges give $3r+6$ through $3r+9$. These are exactly the additional mixed sums required. [Lean verification of the sum profiles](CycleSubdivision.lean)

Reducing the combined low and high paths modulo $2r$ now gives every bin except zero, with $r$ repeated. Indeed the low sums occupy $[r-1,2r-2]$, the mixed high-path sums yield $2r-1$ and $[1,r-3]$, and the two high-high sums yield $r-2,r$. Since $r$ is even, translation gives every requested even repeat. When $D=0$, rotate the resulting cycle to start and end at zero. After canceling the old zero edge, the remaining $k-1$ weights are distinct as required in the short proof.

## Long subdivisions and the obstructions

On a divisible core, insert a period of $k$ new vertices by following a full cycle from an endpoint back to its copy. For odd $k$ the natural order is harmonious, so the deficit $D$ stays fixed. For even $k$ use the cycle repeating $D$. The low edge bin moves to $D+S$ and all vertex bins gain one. This works on the chosen edge for any number of periods. The new chain now contains every label.

For a tail of $3\le r<k$ vertices, take a short interval cycle whose weights include the current deficit after translation. Its integer sums contain both parities: an even sum exists by the interval count, and connectivity across even and odd vertices gives an odd sum. Thus a translation hitting the deficit exists even at even modulus. Choose a vertex of the chain in this interval and insert the cycle beside it, finishing at a copy of that vertex. The net increments are distinct and fill the deficit.

For a two-vertex tail choose an edge $uv$ of the chain with $2u\ne2v$. Any three consecutive distinct labels contain such an edge. With current deficit $D'$, take $x=D'-u$, $z=u+v-x$. If $x=z$, force $z=D'-v$ instead. Both failures would imply $2u=2v$. This reproduces the old weight $u+v$ and fills $D'$. A one-vertex tail is possible if $2x=D'$ for some $x$, since an occurrence of $x$ on the chain can be duplicated. Necessity follows by summing the changes on the subdivided edge. The net weight sum equals twice the sum of the inserted labels. For $jk+1$ new vertices from a divisible core those sums require $2x=D+jS$, where $x$ is the unique new surplus label. This proves the divisible-core classification for $t\ge k$.

From an order-one core and $t\ge k+1$ not divisible by $k$, first insert $k-1$ vertices by the short theorem. The resulting core is divisible and the new chain contains all residues except the old surplus. Insert as many full periods as required. The remaining tail has size zero or between two and $k-1$. The preceding proof still works: a translated cycle of at least three vertices intersects the chain, and its first $k-1$ inserted vertices are consecutive distinct labels before any full periods. Each full period supplies another such run.

Finally suppose the original order is one modulo $k$ and $t=jk$. The old surplus $y$ may change to $z$. The new edge counts must be uniform and the sum of the inserted vertex labels is $jS+z-y$. Thus
$$
2(z-y)=jS.
$$
If $k$ is two modulo four and $j$ is odd, the right side is odd and no $z$ works. At odd $k$ insert full natural cycles, which add one to every bin. At even $k$, pairs of periods always work: on a replacement edge with endpoints $a,b$ assign its new positions $2i$ the label $a+i$ and $2i+1$ the label $b+i$. After $2k$ positions the next edge retains the original weight. Both histograms gain two in every bin.

It remains to insert a single period when four divides $k$. Insert $k-1$ vertices first. Their labels are precisely the residues other than $y$, and their net weights are all residues except the new deficit $D'$. Summing gives $S-D'=2(S-y)$, so $D'=2y-S$. Both $y-k/4$ and $y+k/4$ double to $D'$. Each occurs on the new chain since neither equals $y$. Duplicate one of them next to itself. The added edge of weight $D'$ restores uniform edge counts, and the duplicated label is the new surplus. Further pairs of periods are neutral. This proves all cases.

## Implications for a smallest counterexample

The [short-forest bound](../rainbow/short-forests.md) gives $s\ge21$ at any unresolved modulus. If a connector has $s-1$ consecutive degree-two vertices, suppress that many. The smaller tree has order one modulo $k$ and its labeling extends by the short theorem. If a terminal path has length at least $s-1$, remove that many vertices from its end and use the pendant-path extension. Both arguments contradict minimality.

For the stated 26- and 27-label family, the [integer census](README.md) covers every order through 27. Suppose there were a smallest exception obtained by subdividing an edge of a core of order at most 27. This class stays closed under deleting leaves: if a deleted leaf was an endpoint of the long segment, its new endpoint gives the same type of representation. Orders one and two modulo $k$ above the base are excluded by deleting one leaf and restoring it. At residue one the leaf fills the old edge deficit. At residue two it avoids the old vertex surplus while the old edges are uniform. Every remaining order above 27 has the form $mk+1+t$, $2\le t<k$, with $mk+1\ge27$. Thus at least $t$ internal vertices of the designated subdivision can be removed. Its smaller instance has order one modulo $k$ and extends by the short theorem. No such exception exists.

The [constructor](cycle_subdivision.py) returns all inserted labels. The [independent checker](check_cycle_subdivision.py) tests the full vertex and weight histograms of interval cycles and the prescribed-repeat cycles. It also compares the actual replacement edges with the deleted edge and replays the constructions on complete trees. The replay checked 3,062 cycle arrays, 106,295 endpoint assignments with insertion lengths, and 6,411 whole trees. It independently ruled out every possible shifted surplus and vertex ordering for a six-vertex insertion at modulus six across all 21 unordered endpoint assignments, giving 52,920 negative checks. The Lean file checks the mixed- and high-edge recurrences, the two-vertex orientation argument, and the parity obstruction.

~~~bash
python3 -B -m research.census.check_cycle_subdivision
lean research/census/CycleSubdivision.lean
~~~
