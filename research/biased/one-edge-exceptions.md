# All failures with one prescribed edge offset at eight, nine and ten

Fix one edge of a finite tree and add $d$ to its endpoint sum modulo $k$. All other edges have the ordinary endpoint sum. The following list classifies every failure of cordiality at $k=8,9,10$. In every successful case at eight and nine, one labeling works on every prefix of a connected order starting at either chosen endpoint of the marked edge.

* **At each of eight, nine and ten**, take a double star on exactly $k$ vertices with the joining edge marked. Let $s$ be the number of vertices on one side of that edge. It fails exactly when $\gcd(s,k)\nmid d$. This is the entire list at eight and nine.
* **At ten, on ten vertices**, there are two further marked trees, both failing only for $d=5$. In the first, attach six leaves and a path of length three to one hub. Mark the first edge of the path from that hub. In the second, join a hub with five pendant leaves to a hub with two pendant leaves by a path of length two. Mark the edge of this path next to the five-leaf hub. The [connector criterion](connector-offsets.md) explains both obstructions at all even moduli.
* **At ten, on eleven vertices**, join two hubs with four and five pendant leaves respectively. Mark their joining edge. It fails exactly when $d$ is a unit modulo ten.

In particular, at eight a chain of arbitrary cordially labeled eight-divisible pieces with any prescribed ports can be inserted on a single edge of any tree whose order differs from eight. The same holds at nine with nine-divisible pieces away from order nine, and at ten with ten-divisible pieces away from orders ten and eleven. At the exceptional orders, test the effective offset from the chosen piece labelings against the list. [Expansion formula](period-chains.md)

## Allowing independent offsets on all edges at one vertex

These classifications follow from a more general equivalence. Suppose all adjusted edges meet one vertex $u$. Normalize $f(u)=0$ by translation. In each component of $T-u$, use the offset on the edge from $u$ as that component's prescribed parent color. This turns every adjusted edge into an ordinary boundary sum and leaves every internal sum unchanged. Every successful labeling of this forest over the singleton surplus core yields the required tree labeling, and every cordial tree labeling yields a solution of the forest problem.

To apply a fixed-core theorem stated for actual parent vertices, take a surrogate star on $k+1$ vertices with center zero and leaves carrying all residues. Attach each forest root to a leaf with its prescribed color. Replacing this star by the single vertex $u$ and restoring the offsets removes exactly one from every vertex and edge bin. The same identity holds at each restoration prefix. Translating all labels back permits prescribing any label at $u$.

Consequently **every** assignment of offsets on the edges at $u$ works at eight and nine at all orders except possibly $k$. At order $k$ the complete exceptions are exactly the 42 boundary-colored forests at eight and the 12 at nine. At ten, only orders ten and eleven admit exceptions, with 34 and eight boundary-colored forests respectively when the hub label is normalized. At eight and nine the fixed-core prefix theorem lets growth start at $u$ for every successful input. [Eight-label exceptions](../eight/surplus.md) · [Nine-label exceptions](../rainbow/surplus-nine.md) · [Fixed-core prefix theorem](../eight/growth-orders.md) · [Ten-label exceptions](../rainbow/ten-prescribed.md)

An ordinary consequence holds for **any number of edges meeting one vertex**. Replace each selected edge by a chain of cordially labeled trees of positive orders divisible by $k$, with arbitrary ports. Prescribe the sum of each chain's effective offsets at the corresponding edge of the core. At eight and nine every core order other than $k$ works, and at ten every core order other than ten and eleven works. At the remaining orders the preceding boundary-colored lists decide whether the chosen effective offsets work. The expanded tree may have many vertices of high degree.

For one marked edge only one component boundary color can be nonzero. At eight and nine the only possible failing shape is a double star with a central mark. The gcd criterion follows by the pinned-star theorem. At ten the nine-vertex exceptional forest list also has the two connector shapes displayed above after identifying the two orientations of the mark. The ten-vertex exceptional forest list gives the eleven-vertex double star and its unit offsets. [Pinned-star criterion](../rainbow/pinned-star.md) · [Ten-label obstruction representatives](../rainbow/ten-surplus-obstructions.json)

## Independent enumeration on the original trees

The [enumerator](check_one_edge_small.py) builds each edge-marked tree as an unordered pair of rooted trees joined at their roots. A separate recurrence for rooted counts checks completeness. For each such tree and every literal offset, the [native search](check_one_edge_small.cpp) normalizes one vertex label to zero and searches the entire tree without using the prescribed-core classification. It discards repeated edge weights because the orders tested are $k$ and $k+1$. At order $k+1$ it allows one repeated vertex residue. It reconstructs both histograms before accepting a witness and exhausts all remaining assignments before declaring failure.

| Modulus | Order | Edge-marked shapes | Literal inputs | Failures |
| ---: | ---: | ---: | ---: | ---: |
| 8 | 8 | 96 | 768 | 10 |
| 9 | 9 | 239 | 2,151 | 6 |
| 10 | 10 | 622 | 6,220 | 20 |
| 10 | 11 | 1,607 | 16,070 | 4 |

The same checker applied the surrogate-star construction and recounted 22,260 actual connected prefixes in 1,020 trees with independent offsets at one vertex. It then replaced the incident edges by 3,437 ordinary star pieces and checked both final histograms on all 1,020 expanded trees. All failures above require a nonzero assigned offset. The ordinary cases of Hovey's conjecture at these three moduli already follow from their all-tree proofs.

~~~bash
out=$(mktemp -d)
c++ -O3 -std=c++17 research/biased/check_one_edge_small.cpp -o "$out/check"
python3 -B -m research.biased.check_one_edge_small "$out/check"
~~~
