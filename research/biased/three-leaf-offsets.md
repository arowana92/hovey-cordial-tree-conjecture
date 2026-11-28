# Two prescribed edge offsets on trees with at most three leaves

**Theorem (computer-assisted at 27 labels).** Every finite tree with at most three leaves admits a 27-cordial labeling with up to two exceptional edge offsets. The exceptional edges can be anywhere and have independently prescribed offsets. All remaining edges have one common offset. An adjusted edge $uv$ has weight $f(u)+f(v)+\delta_{uv}$.

In particular, start with a tree of any order having at most three leaves. Replace each of up to two edges by a chain of ordinary trees of orders divisible by 27, each with a known cordial labeling. Choose arbitrary entry and exit vertices in each inserted tree, allowing them to coincide. The resulting ordinary tree is 27-cordial. Every tree of order exactly 27 is available as an insertion by the [integer census](../census/README.md). [Expansion formula](sparse-path-offsets.md#compressing-a-tree-between-two-ports)

## Reduction to one order

Let $G$ be any finite abelian group of order $k\ge2$ and let $q\ge1$. **The arbitrary-order statement for at most three leaves and at most $q$ exceptional offsets is equivalent to its restriction to trees on exactly $k$ vertices.** At that order the requirement is a permutation of $G$ giving $k-1$ distinct adjusted edge weights. Subtract the common offset from every edge to normalize it to zero.

A path of order at most $k$ can be padded by ordinary edges and its bijective labeling restricted. A longer path splits into a nonempty first block of at most $k$ vertices and subsequent blocks of $k$ vertices. Given an edge from an old label $a$ into a block at label $p$, with joining offset $b$, translate the block by $d=a+p+b-h$ where $h$ is its missing weight. The joining edge fills $h+2d$. The block contributes one copy to each vertex and each edge bin. This also permits removing a terminal segment of $k$ vertices from any arm and restoring it afterward.

A tree with exactly three leaves has one vertex of degree three. Regard its three arms as paths out of that vertex. Remove terminal segments of $k$ vertices until every remaining arm has length at most $k-1$. If an arm disappears, use the path result. Write $n$ for the remaining order. For $n\le k$, pad a longest arm and restrict. For $n=k+1$, remove a leaf, label the $k$-vertex tree, and assign the removed leaf the unique label that fills the missing weight on its joining edge. The vertex counts are then balanced as well.

Suppose $n\ge k+2$. Select an arm $A$ containing an exceptional edge if one remains. Include all of $A$ and the center in a connected $k$-vertex piece $U$. Complete $U$ using initial segments of the other arms $B,C$, leaving at least one vertex on each. This is possible because $|A|\le k-1$ and $(|B|-1)+(|C|-1)\ge k-1-|A|$, where arm lengths exclude the center. The piece has at most three leaves and at most $q$ exceptions. Choose a bijective rainbow labeling on it with missing edge weight $h$.

The vertices outside $U$ form two paths. Join their inner endpoints by a temporary edge. If the two ports of $U$ have labels $p,r$ and their joining edges have offsets $b,c$, assign the temporary edge offset $p+r-h+b+c$. At least one original exception was absorbed whenever any was present. The residual path therefore has at most $q$ exceptions, including the temporary edge. Label the path, then expand this edge using the translation $d=a+p+b-h$ at its first endpoint $a$. The second joining edge has exactly the temporary edge's adjusted weight. The piece and the first joining edge contribute one to every bin. This works also when the two ports coincide. Finally restore the removed terminal blocks. The reverse implication follows by specializing to order $k$.

## Verification at 27

The order-27 [path stream](sparse-path-offsets.md) handles trees with at most two leaves. The remaining shapes have arm lengths $1\le a\le b\le c$ with $a+b+c=26$. For all **56 shapes** the [generator](sparse_path_offsets.cpp) supplies one permutation for each pair of exceptional positions and simultaneous unit orbit of their offsets, including separate rows for one or zero exceptions. The [independent verifier](check_three_leaf_offsets.py) reconstructs the edges arm by arm, checks the permutation and actual adjusted sums, expands each orbit at the specified positions, and requires disjointness and the full literal count. Per shape this count is $1+26^2+\binom{26}{2}26^2=220{,}377$. The [manifest](three-leaf-offsets-27.sha256) covers **841,624 permutations** and **12,341,112 literal inputs** for branching trees. The extended generator also reproduces the original path digest.

A separate [whole-tree replay](replay_three_leaf_offsets.py) reconstructs 1,560 complete trees, including 984 reductions to two ports, 64 reductions with coincident ports, and 6,264 restored terminal periods. It checks both histograms from the original endpoints and offsets. It also replaces two edges in each of 120 actual three-leaf trees by chains containing 360 independently labeled period trees in total, and checks the expanded trees with ordinary endpoint sums.

~~~bash
set -euo pipefail
out=$(mktemp -d)
r=research/biased
c++ -std=c++17 -O3 "$r/sparse_path_offsets.cpp" -o "$out/generate"
python3 -B -m research.biased.check_three_leaf_offsets "$out/generate" --keep "$out/rows" --manifest "$r/three-leaf-offsets-27.sha256"
"$out/generate" 27 > "$out/rows/path.txt"
python3 -B -m research.biased.replay_three_leaf_offsets "$out/rows"
~~~
