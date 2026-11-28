# A single 24-vertex side at order 52

**Theorem (computer-assisted).** Every 52-vertex tree with an edge separating 24 vertices from 28 is 27-cordial. Together with the known joins for splits of 25 and 27 or 26 and 26, this covers every tree of order 52 admitting an edge whose two sides differ by at most four vertices. Any counterexample of this order has a unique centroid, and every component after deleting that centroid has at most 23 vertices. Two centroids would give an edge with equal sides. [Joins for the other splits](../prime/four-deficits.md)

Let $A$ be the 24-vertex side, and root the 28-vertex side at its endpoint of the joining edge. At a deepest vertex with children, either remove two leaf children, or remove this vertex and its only child. In the second case this vertex has a parent, since otherwise the entire side would have only two vertices. In both cases a connected tree $B$ of order 26 retains the joining endpoint. The two removed vertices form two leaves at a single site of $B$, or a path entering at a site of $B$.

**Small-leaf case.** If $B$ has at most three leaves, the 28-vertex side has at most five leaves after the two vertices are restored. Traverse that side in preorder, visiting children in nondecreasing order of subtree size. Keep the first four vertices and all of $A$. The resulting 28-vertex tree has a 27-cordial labeling. The remaining 24 vertices form a suffix of the traversal on the 28-vertex side. Every rooted tip in the suffix was a tip of that side, so there are at most five. Its actual boundary colors obey the ordered-cut inequalities for every labeling of the prefix, including the labeling inherited from the core containing $A$. The seven-tip theorem extends this core of order one modulo 27. [Order-28 base](order-fifty-one.md) · [Ordered suffixes](../rainbow/ordered-cut.md) · [Seven-tip extension](../rainbow/seven-tip-27.md)

**Interval calculation.** The integer census gives labels $0,\ldots,23$ on $A$ and $0,\ldots,25$ on $B$, with consecutive integer edge sums on each. Write $f,g$ for their starting sums. Distinct endpoints in a tree labeled $0,\ldots,n-1$ have sums between 1 and $2n-3$, hence each start belongs to $1,\ldots,n-1$. Let $a,b$ be the joining labels in $A,B$, and let $p$ be the site of the two removed vertices in $B$. The case $p=b$ is included. [Integer census](README.md)

A direct witness applies $v\mapsto uv+d$ to $A$, keeps the labels on $B$, and gives the two removed vertices labels $x,y$. The joining edge weighs $ua+d+b$. The other two edges weigh $p+x,p+y$ for two leaves or $p+x,x+y$ for a path. All these expressions are reduced modulo 27. The generator keeps each histogram entry between one and two in the completed tree.

There are $24\cdot23\cdot26\cdot25\cdot2\cdot26=18{,}657{,}600$ inputs. Direct rows cover 18,657,460. For each of the remaining 140, choose a leaf of $B$ with original label $z$ and neighbor label $t$. A repair changes that leaf to $v$, replaces one internal weight $z+t$ by $v+t$, and uses the new label at the joining or attachment site if it coincides with the leaf. The possible ordered pairs satisfy $0\le z,t<26, z\ne t, g\le z+t<g+25$ over the integers.

For **each** exceptional input, at most three values of $z$ lack a repair for some permitted $t$. When $B$ has at least four leaves, their labels are distinct, so one leaf has a repair for every permitted neighbor label. This completes the proof.

## Independent verification

The verifier reads each row and counts all 27 vertex and edge bins. For a direct row it constructs two concrete double stars realizing the specified intervals. At order $n$ and start $f$, use the edges from $f$ to $0,\ldots,f-1$ and from $f-1$ to $f+1,\ldots,n-1$. The resulting weights run once through $f,\ldots,f+n-2$. The counts therefore apply to any two pieces with the specified intervals and ports.

For repaired rows the verifier removes the specified integer sum from the right interval and recomputes every new edge. It checked 59,864 repairs and the three-label bound after accounting for all 144 omitted incidences. Whenever the specified leaf incidence also occurs in the representative double star, it separately reconstructs all 51 edges by endpoints. This gave 3,360 repaired whole trees, including 164 repairs that changed the label of a port. The earlier two-24-side theorem has a separate proof. [Generator](side24_at_52.cpp) · [Independent verifier](check_side24_at_52.cpp) · [Two disjoint sides](two-pieces-24.md)

~~~bash
set -euo pipefail
out=$(mktemp -d)
r=research/census
c++ -O3 -std=c++17 "$r/side24_at_52.cpp" -o "$out/generate"
c++ -O3 -std=c++17 "$r/check_side24_at_52.cpp" -o "$out/verify"
"$out/generate" | tee "$out/witnesses" | "$out/verify"
shasum -a 256 "$out/witnesses"
~~~

The witness stream has SHA-256 `29226b94d7a2b54d7421ec80c374fe49445f76ab845d417c2defd36238a6e5f2`. The 27-label conjecture remains open.
