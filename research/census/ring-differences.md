# Prescribing two vertex labels on a 27-vertex unicyclic graph

**Finite theorem.** Let a simple connected unicyclic graph on 27 vertices have zero, two or three leaves. At **any two distinct vertices**, prescribe any two distinct residues modulo 27. The graph has a bijective labeling meeting the prescription in which all 27 edge sums are distinct. The vertices may lie anywhere in the attached trees or on the cycle.

For every graph and vertex pair it suffices to find ordinary harmonious labelings in which the difference of the endpoint labels has gcd $1,3,9$, respectively, with 27. Multiplying by a unit gives every nonzero difference in its class. Translation sets the first label, preserving both permutations. In total the certificates cover **625,067,118** choices of graph, unordered vertex pair and nonzero difference for a fixed orientation. At a prime modulus the two-vertex prescription follows directly from a single harmonious bijection by scaling and translating.

| Leaves | Graphs | Bijections in stream | Vertex-pair and nonzero-difference inputs |
|---:|---:|---:|---:|
| 0 | 1 | 49 | 9,126 |
| 2 | 1,938 | 95,269 | 17,686,188 |
| 3 | 66,554 | 3,273,483 | 607,371,804 |

## Moving branches to a third vertex

In any 27-cordial tree with an edge $ab$ joining unequal labels, take a graph from the theorem, a cycle edge $uv$ and a vertex $w\ne v$. Prescribe $g(v)=f(a)$ and $g(w)=f(b)$. Remove $ab,uv$ and add $au,bv$. Move any selection of the remaining branches at $a$ to $v$ and any selection at $b$ to $w$. The choice $w=u$ moves branches to both endpoints of the opened edge. Other choices can put branches on an arbitrary third vertex.

The old tree splits into two components linked by the opened graph. Every transferred branch retains its single attachment. The link $au$ supplies the removed cycle weight $g(v)+g(u)$, and $bv$ supplies the removed core weight $f(b)+f(a)$. Each other moved edge retains the labels at its ends. The resulting tree gains one of every vertex and edge residue, with all old labels preserved. A proper labeling stays proper. Starting from a properly and cordially labeled tree allows the operation to be repeated on any edge.

**Consequence through 54 vertices.** Suppose a 27-vertex middle tree $U$ meets the exterior at vertices $u,v,w$, with one exterior component attached at $u$, one or more at $v$, and the others at $w$. Assume $u,v$ are distinct and nonadjacent, and closing $uv$ gives a graph with zero, two or three leaves. The exterior may be any forest on two through 27 vertices in total. The original tree is 27-cordial.

Indeed let $a$ be the root opposite $u$ and let $b$ be the root of any one component opposite $v$. Join $a$ to $b$ in the compressed tree. Attach all remaining roots from $v$ to $a$ and all those from $w$ to $b$. The [integer census](README.md) gives an injective rainbow labeling of this tree, so $f(a)\ne f(b)$. Use the preceding transfer. If $w=v$, all roots other than the one at $u$ can attach to $a$ and translating $g(v)$ to $f(a)$ suffices. If $w=u$, arbitrarily many components may meet **both** ports, with one at $u$ distinguished to supply $a$.

In particular this covers three single-edge exterior sides totaling 26 in order 53 or 27 in order 54 whenever two of the middle ports permit the stated closure. If the exterior totals at most 25, an independent theorem also permits four through six leaves in the closure. [Three-side proof and explicit 52-vertex examples](three-side-cuts.md)

On a connected odd $D$-sheeted cover of any graph in this theorem, two vertices over distinct base vertices can receive any prescribed labels modulo $27D$ whose reductions modulo 27 differ. Prescribe their low labels and choose the two fiber translations independently. [Odd-cover construction](cycle-progressions.md#odd-covers-and-odd-abelian-groups)

## Reproduction

The [generator](ring_differences.cpp) stores a complete permutation when it adds a difference class at any vertex pair. The [independent checker](check_ring_differences.py) reconstructs each graph, tests both permutations, rejects duplicate canonical graphs and compares counts at each girth with the rooted-forest and Burnside recurrence. It partitions the vertices of each row by label modulo 3 and 9 and checks that every other vertex occurs in each of the three required classes relative to each mark. It separately expands the unit orbits to all 26 literal differences.

On one graph at each nonempty girth it constructs actual two-site and three-site branch transfers and odd covers. It checks both histograms and connectivity on 33,592 transfers of order 82 and another 156 of order 53 or 54.

Run from the repository root in Bash. The three uncompressed witness streams are reproducible from their [hashes](ring-differences.sha256).

~~~bash
set -euo pipefail
out=$(mktemp -d)
c++ -std=c++17 -O3 research/census/ring_differences.cpp -o "$out/generate"
python3 -c "print('.'.join(['()']*27))" | "$out/generate" > "$out/ring-all-pairs-0.txt"
for q in 2 3; do
    python3 -B -m research.census.few_leaf_rings 27 "$q" | "$out/generate" > "$out/ring-all-pairs-$q.txt"
done
for q in 0 2 3; do
    python3 -B -m research.census.check_ring_differences "$q" "$out/ring-all-pairs-$q.txt"
done
manifest="$PWD/research/census/ring-differences.sha256"
(cd "$out" && shasum -a 256 -c "$manifest")
~~~
