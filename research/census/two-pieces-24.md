# Two 24-vertex sides in a 52-vertex tree

**Computer-assisted theorem.** Every tree of order 52 with two disjoint edge sides of order 24 is 27-cordial. Thus a 52-vertex counterexample can have at most one edge cutting off 24 vertices. Two distinct sides of that size cannot contain one another, and their combined size is less than 52. A subsequent proof covers every 52-vertex tree with even one such side. [Single-side theorem](side24-at-52.md)

Remove the two sides. The remaining connected tree $C$ has four vertices. Each removed piece meets $C$ by one edge. Call its endpoint in $C$ a port.

* **Different ports.** An edge on the path between them divides the tree into pieces of orders $24+i$ and $28-i$ for some $1\le i\le3$. Both have order at most 27, so the [affine joining theorem](../prime/four-deficits.md) applies.
* **One port of degree at least two in $C$.** At the port, the other three vertices of $C$ form branches of sizes $1,2$ or $1,1,1$. Keep two vertices in whole branches together with the port and one 24-vertex piece. The resulting 27-vertex tree has a bijective rainbow labeling. The exterior is the other 24-vertex piece and a singleton, both attached to the port. Apply the [divisible-core singleton theorem](../rainbow/divisible-singleton.md).
* **One port of degree one in $C$.** Both pieces attach at the same leaf of $C$. The other three vertices form a rooted path or a root with two children. The interval calculation below covers every pair of rooted 24-vertex trees for either connector. The [integer census](README.md) supplies their interval labelings.

## Interval calculation at the shared leaf

Normalize each piece so that its vertex labels are $0,\ldots,23$ and its 23 internal weights are a cyclic interval. Write $a,b$ for the labels at the two roots and $f,g$ for the two interval starts. All arithmetic is modulo 27. Use color zero at the common port. A row specifies which piece is first, two translations $d,e$, a unit $u$, and the labels $x,y,z$ of the three other connector vertices starting from the neighbor of the port. The first piece uses the map $v\mapsto v+d$, the second $v\mapsto uv+e$. An internal weight changes by twice its piece's translation after scaling. Each bridge weight is its transformed root label.

The new internal connector weights are $x,x+y,y+z$ for the path or $x,x+y,x+z$ for the fork. Recount all four connector labels and all five new edges together with both pieces. Every vertex bin and every edge bin must have frequency one or two. These tests depend only on $a,f,b,g$ and the connector shape, so one row proves the assertion for every pair of piece labelings with those parameters. They also apply to pieces of orders $24\bmod 27$ whose vertex and edge histograms have uniform baselines and, above those baselines, the indicated intervals with the same unit step on each piece. Subtracting the baselines gives exactly the counts checked here.

The [generator](two_pieces_24.cpp) tries both orientations. In normalized coordinates at least one shifted vertex interval must omit zero, since the connector port already uses it. When this is the first interval its translation belongs to $\{1,2,3\}$. The search chooses the second affine map, counts the bridges, and assigns the remaining three vertices in parent-first order.

The [independent verifier](check_two_pieces_24.py) constructs all 24 vertex labels and all 23 internal weights for each affine interval. It sums the literal frequencies in 27 unsigned bytes and adds the actual connector and bridge contributions. It covered **531,441 parameter tuples for each shape**, including all 27 choices at each root. It also rebuilt **10,368 whole trees** from three different 24-vertex caterpillars, trying all marked vertices, and counted their endpoint sums. The ordinary theorem uses no leaf-count assumption. In particular it covers the order-52 centroid profile with one three-vertex terminal path and two 24-vertex branches of eight tips each.

| Connector beyond the port | SHA-256 of all witnesses |
|---|---|
| Path | `0b7745cedc7d75bbb718273eb7ebd0f9aa29a45e29d8d704d601b423f55fef16` |
| Fork | `f930a3428dd6087f767aca2a2cb48dbaef1b2d5f0c3bc598d3b148403072f489` |

The nested order is $a,f,b,g$, each from zero through 26. Each record has seven bytes giving the orientation, $u,d,e,x,y,z$.

~~~bash
set -euo pipefail
out=$(mktemp -d)
c++ -std=c++17 -O3 research/census/two_pieces_24.cpp -o "$out/generate"
for shape in path fork; do
  "$out/generate" "$shape" > "$out/$shape.bin"
  python3 -B -m research.census.check_two_pieces_24 "$shape" "$out/$shape.bin"
done
python3 -B -m research.rainbow.check_divisible_singleton
~~~
