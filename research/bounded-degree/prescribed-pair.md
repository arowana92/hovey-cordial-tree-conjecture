# Prescribing two occurrences of the surplus vertex label

Let $T$ be a tree with $n$ edges. At any divisor $k$ of $n$, a $k$-cordial labeling has uniform edge frequencies $t=n/k$ and exactly one surplus vertex residue of frequency $t+1$. Specify distinct vertices $r,y$ and require them **both** to carry a prescribed surplus residue $a$. Edges have ordinary endpoint sums. Write $d$ for their distance, and $q$ for the number of leaves of $T$ outside $\{r,y\}$. Put $S=\sum_{x\in\mathbb Z_k}x$.

**Theorem.** Fix $D\ge3$ and $0<\epsilon<1$. Suppose $\sum_v(\deg_T(v)-D)_+\le n^{1-\epsilon}$. For sufficiently large $n$, the complete list of exceptions is as follows.

| Modulus | Pairs that cannot carry the surplus together |
|---|---|
| Proper divisor $k$ of $n$ | The two ends of a path when $tS\ne0$ |
| $k=n$, distance one | An end of a path and its neighbor when $k$ is odd |
| $k=n$, distance two | Every such pair |
| $k=n$, distance at least three | $q=0$ and $k$ even, or $q=1$ and $k$ odd |

In particular any vertex can carry the prescribed surplus, with complete freedom of the second position at proper divisors apart from the stated parity case. The large-order assertion applies uniformly to the divisors.

**Finite result.** In the last row, the same classification holds for $11\le k=n\le30$ when $q\le3$, and for $k=n\in\{26,27\}$ when $q\le6$. The distance-two exclusion holds at every $k=n$. Consequently any forest of exactly $k$ new vertices and at most four rooted tips can be attached at an arbitrary old vertex with every vertex and edge frequency increasing by one, for $11\le k\le30$. At $k=26,27$ up to **seven tips** are allowed. The old tree can have any size and labeling.

## Identifying the two vertices

Identify $r$ and $y$ to one vertex $s$, retaining all edges with their multiplicities. The resulting connected graph has $n$ vertices and $n$ edges. A uniform vertex and edge labeling on this graph gives the required labeling on splitting $s$. Conversely, a labeling of the required kind descends to this graph. A common translation sets the label of $s$ to the prescribed value while preserving uniformity.

For $d\ge3$ the quotient is a simple unicyclic graph with exactly $q$ leaves. Merging the two degrees increases the total excess above $D$ by at most $D$. Apply the [prescribed edge-frequency theorem](spectrum-projection.md) to the uniform target. With at least two leaves the target difference is zero, so the gcd condition always holds. At a proper divisor a single leaf is also allowed. With no leaf the quotient is a cycle, requiring $tS=0$ by incidence summation. At $k=n$ the one-leaf condition instead requires $S\ne0$. One may anchor a regular cycle vertex and translate afterward to set $s$. The [finite harmonious ring census](../census/few-leaf-rings.md) supplies the corresponding small-modulus positive cases. An odd cycle is harmonious in the natural order.

For $d=1$ the identification produces a loop at $s$. Delete the loop, giving an $n$-vertex tree $U$. Normalize the surplus to zero. Require the label zero at $s$ and the histogram $tG-[0]$ on the tree edges, where $G$ has one entry in each bin. The loop restores the missing zero. The [tree frequency theorem](spectrum-projection.md) has difference $A=0$ and anchor label zero, so its gcd test holds. The only further obstruction is at $k=n$ on an endpoint-rooted path when $S=0$. The merged vertex is an endpoint of a path in $U$ precisely when $T$ was a path and the pair was a leaf and its neighbor. This gives the first distance row at $k=n$.

## Two edges to the same neighbor

When $d=2$, the quotient has two parallel edges joining $s$ and the old middle vertex. At $k=n$ these give equal weights in a required bijection. At a proper divisor we use different lifts of their common weight and then project.

Work in $\mathbb Z_n$. Give one copy offset zero and the other offset $k$. They always have distinct shifted weights upstairs. With at least two leaves give a remote ordinary edge offset $-k$, so the total offset is zero. With one leaf choose the total to be zero if $n$ is even and $k$ if $n$ is odd, using the same remote edge. Then $C'=\sum\mathbb Z_n+\sum\eta'$ is nonzero. A connected graph consisting of a digon with one leaf is a digon with a single pendant path. Its length is $n-2$, greater than two here. When $n>2$ a digon cannot be the entire leafless graph.

The [shifted-ring embedding proof](shifted-rings.md) applies with the following details for the parallel edges. Open the shifted copy and keep the ordinary copy in the spanning tree. Mark both endpoints. Count their degrees with multiplicity in the original graph. All sites chosen outside the marked neighborhoods still have their original degrees. The induced pinned edge forms now include $X_s+X_z$ and $X_s+X_z+k$. Their difference is the nonzero constant $k$ in $\mathbb Z_n$. They cost at most one extra comparison against each other form. With one leaf the only substituted label is the tip label $X_j+C'$ at the end of the long pendant path, and the tip does not neighbor either endpoint of the parallel edges. With two eliminated leaves in the few-leaf case neither belongs to the parallel edges. Thus the same bounded-coefficient pin assignment applies, including the small core and its two moments. The total-offset congruence holds with at least two leaves, and with one leaf the required tip and junction labels differ by $C'$. Completing the core, returning the shifted copy and reducing modulo $k$ gives both uniform histograms. Every offset vanishes on projection. [Implementation with separate parallel-edge offsets](shifted_ring.py)

## Attaching a forest at equal parent labels

Add a dummy root $r$ to the forest, adjoining its component roots. A uniform attachment with any specified new vertex $y$ carrying the old parent color is exactly the prescribed-pair problem. Translate all free labels as needed. Distinct old vertices may serve as parents provided they have the same label. At proper divisors of the forest order, the only asymptotic exception under the excess hypothesis on the augmented tree is a single path attached at one end with its other end specified and $tS\ne0$.

For the finite result let $h$ count rooted tips, which are the leaves of the augmented tree other than $r$. With $h=1$ use the [explicit neutral pendant path](../counterexample-bound.md#shortening-paths). With $h=2$ and $k\ge11$ there is an internal free vertex at depth at least three. Otherwise all tip depths are at most three and the forest has at most $3h$ vertices, by covering it by its root-to-tip paths. Identify such an internal vertex with $r$. The quotient has two leaves. For $3\le h\le4$, or up to seven at 26 and 27, there is a tip at depth at least three since $k>2h$. Identify it with $r$. The quotient has $h-1$ leaves, exactly within the certified finite range. This allows repeated attachment of such forests, at any sites with the required common parent color within each forest.

## Checks

The [parallel-edge checker](check_prescribed_pair.py) independently recounts all induced edge weights, including both copies, and both partial embedding moments. It verified 68 lifted cores, including 17 with a single leaf. A literal enumeration on small paths and forks gave 254 feasible inputs and rejected all 62 inputs in the necessary exclusion classes. Another 38 inputs failed at those small orders outside the asymptotic assertion.

The [common-parent replay](../census/check_common_site_period.py) constructs actual quotients, reads an explicit harmonious labeling, splits the two vertices and checks every vertex and edge count on the original rooted tree. It tested 1,032 rooted trees with 21,588 prescribed colors. The finite theorem uses the exhaustive ring census.

~~~bash
out=$(mktemp -d)
c++ -std=c++17 -O3 research/census/branched_search.cpp -o "$out/solve"
python3 -B -m research.census.check_common_site_period "$out/solve"
python3 -B research/bounded-degree/check_prescribed_pair.py
python3 -B research/bounded-degree/check_shifted_ring.py
~~~
