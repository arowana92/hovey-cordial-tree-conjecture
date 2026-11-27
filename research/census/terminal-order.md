# Four terminal paths and the order bound at 26 labels

The [two-side reduction](pendant-order.md) improves the ceiling to **286**.

**Theorem (computer-assisted).** If a smallest 26-label counterexample has order $n=26m+s$, $1\le s\le26$, it satisfies the following bounds. In particular, testing orders through **364** would suffice to settle the unrestricted 26-label case. The repository's proofs for eight through twenty-five labels cover every tree order.

| $s$ | Minimum possible order | Maximum possible order |
|---:|---:|---:|
| 23 | 49 | 309 |
| 24 | 50 | 336 |
| 25 | 51 | 337 |
| 26 | 52 | 364 |

The residue restriction and lower bounds follow from the [21-vertex extension](../rainbow/twenty-one-free.md). Two local constructions sharpen the previous upper bound of 546.

## Four paths at arbitrary vertices

Start with a fixed cordial labeling of a tree of order zero or one modulo 26. Attach at most four paths, of arbitrary lengths, by one end at any prescribed old vertices. Their parents may coincide. All the old labels extend. In fact, for any prescribed interleaving that grows each path outwards, one can keep the tree cordial after **every single new vertex**.

For a core of order one modulo 26, translate its unique surplus vertex label to zero. The edge histogram is uniform. On any one through four nonempty path segments with a total of 25 new vertices, the following certificate supplies the nonzero residues once each and distinct weights on all 25 actual entering edges. For a shorter batch, pad any one segment at its tip and restrict. Consequently every prefix of the chosen interleaving within this batch stays cordial. After 25 steps the vertex counts are uniform and just one edge weight is deficient. Give the next path vertex the label that fills it. This returns to order one modulo 26. The same one-vertex rule starts the process on a divisible core. A segment crossing a batch boundary simply uses its current tip as its next prescribed parent.

| Paths | Unordered length lists | Verified permutations | Ordered parent assignments over all lists |
|---:|---:|---:|---:|
| 1 | 1 | 3 | 26 |
| 2 | 12 | 269 | 8,112 |
| 3 | 52 | 10,936 | 913,952 |
| 4 | 120 | 190,776 | 54,837,120 |

For each permutation the independent verifier computes the internal sums and assigns distinct unused sums to the entering edges. Subtracting the corresponding first vertex labels reconstructs all accepted parent tuples. Multiplication by units preserves zero, distinctness and the endpoint sums. The verifier enumerates all unit orbits from the full ordered tuple space and requires all of them to be covered for every partition. [Generator](../rainbow/independent_paths.cpp) · [Independent verifier](../rainbow/check_independent_paths.py)

A terminal arm runs from a branching vertex to a leaf with no intervening branching vertex. Its length excludes the branching vertex. In a minimum counterexample the **four longest terminal arms together have length at most $s-2$**. Otherwise take terminal segments with a total of $s-1$ vertices on at most four arms. The remaining connected tree has order one modulo 26 and is smaller. The construction restores the removed vertices. There are at least eleven leaves by the [few-leaf theorem](../rainbow/few-leaves.md).

## Replacing an edge by three arms

Replace an edge with old labels $a,b$ by a new three-way joint. Between that joint and the old endpoints put $l,r\ge0$ internal vertices, respectively. Add a third path from the joint to a new leaf with $m\ge1$ further vertices, where $1+l+r+m=26$. For **every** such shape and every old labeling, the 26 new labels and the net 26 new weights can each use all residues precisely once.

The [explicit certificate](through-arm-26.txt) gives 676 rows with $l\le r$, old endpoints $0,h$ and $h\in\{0,1,2,13\}$. Each row lists the joint label followed by the three arms in outward order. These four differences represent all residues under multiplication by units. Swap the old endpoints if needed, multiply all labels by a unit and then translate them to realize the actual pair. The [second implementation](check_through_arms.py) checks all **219,700** oriented shape and endpoint assignments directly. It counts the 27 new sums and subtracts the deleted weight $a+b$. The search uses the necessary relation that the tip differs from the joint by 13, obtained by summing the weights and using the degree of each vertex. [Certificate generator](through_arms.cpp)

In a smallest counterexample each corridor between consecutive branching vertices or leaves has at most 19 internal degree-two vertices, by the [six-vertex forest theorem](dense-cycles.md). Suppose a trivalent joint has a terminal arm. The sum of the numbers of internal degree-two vertices on its three incident corridors is at most **23**. Otherwise take one whole terminal arm and the joint. This gives at most 21 vertices. Taking further internal vertices from the other two corridors allows every total up to at least 26. Choose 26, retain the two outside endpoints and suppress the removed piece to one edge. The preceding certificate restores it on the smaller tree.

## Counting possible orders

Suppress the degree-two vertices and regard the branching vertices as a tree joined by corridors, with terminal arms attached. Paths and spiders are already cordial. Put $M=s-2$. There are at most $M$ leaves, by [leaf deletion](../counterexample-bound.md#removing-leaves). At each joint the sum of its terminal arm lengths is at most $M$ by the [single-joint path theorem](../rainbow/terminal-paths.md#bounding-a-smallest-counterexample-by-its-branching-vertices). Neither side of any edge may have order divisible by 26. Thus if a rooted branch has order $b$ before the internal vertices of its parent corridor, and the corridor has $e$ such vertices, every integer from $b$ to $b+e$ avoids residues $0,s$ modulo 26. [Divisible-cut theorem](../divisible-cuts.md)

Let $z$ be the fourth largest arm length. Then $1\le z\le\lfloor M/4\rfloor$, and the total of $(a-z)_+$ over all terminal arm lengths $a$ is at most $M-4z$. A joint with $t$ arms of total length $w$ consumes at least $\max(0,w-tz)$ of this budget. The order calculations use this necessary lower bound.

The [Python enumeration](arm_order_bounds.py) roots the branching skeleton at an endpoint. A table records leaf count, parent corridor length, excess budget used and the possible orders as bits. At each new joint, choose its terminal arms and zero, one, or at least two child branches. Form the last class by repeated binary addition of child orders. Enforce degree at least three and the trivalent bound whenever a terminal arm is present. Test every cut along the parent corridor. At the root, attach at least two terminal arms and exactly one child. Induction over the leaf count includes every eligible branch, since any nonroot joint contributes at least two descendant directions. The earlier order bound of 546 suffices for the bit table.

The [independent C++ calculation](check_arm_order.cpp) instead closes the skeleton across an arbitrary internal connector. It keeps only the largest open branch order for each residue and resource state. All later cut tests depend only on the residue, so a larger representative can replace a smaller one. It combines two branches with compatible connector lengths and counts the intervening vertices once. This calculation has no a priori cap on the order. Both algorithms give the four maxima in the table. They enumerate necessary conditions for a minimum counterexample. No tree at any of those upper endpoints is asserted to be noncordial.

## Reproduction

Run in Bash from the repository root. The four path streams occupy about 5 MiB.

~~~bash
set -eu
out=$(mktemp -d)
r="$PWD/research/rainbow"
c="$PWD/research/census"
c++ -O3 -std=c++17 -fPIC -Drainbow_witness=reference_witness -c "$r/search.cpp" -o "$out/ref.o"
c++ -O3 -std=c++17 -fPIC -DRAINBOW_WIDE_MASK -c "$r/leaf_search.cpp" -o "$out/leaf.o"
c++ -O3 -std=c++17 "$r/independent_paths.cpp" "$out/ref.o" "$out/leaf.o" -o "$out/paths"
for j in 1 2 3 4; do
    "$out/paths" 26 "$j" > "$out/multipath-26-$j"
    python3 -B -m research.rainbow.check_independent_paths 26 "$j" "$out/multipath-26-$j"
done
(cd "$out" && shasum -a 256 -c "$r/independent-paths.sha256")
c++ -O3 -std=c++17 "$c/through_arms.cpp" -o "$out/through"
"$out/through" > "$out/through.txt"
cmp "$out/through.txt" "$c/through-arm-26.txt"
python3 -B -m research.census.check_through_arms "$c/through-arm-26.txt"
python3 -B -m research.census.arm_order_bounds
c++ -O3 -std=c++17 "$c/check_arm_order.cpp" -o "$out/bound"
"$out/bound"
~~~
