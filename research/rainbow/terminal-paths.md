# Attaching terminal paths and bounding the number of branching vertices

**Theorem.** For every modulus through 45, a prescribed cordial labeling of any tree of order zero or one modulo $k$ extends across arbitrarily many paths of arbitrary lengths attached by one end at a single chosen vertex. In particular every spider is $k$-cordial throughout this range. For every modulus through 39, every tree with at most two vertices of degree at least three is $k$-cordial, at every order. Degrees and the length of the path between the two branching vertices are unrestricted.

At a modulus in the first range a smallest counterexample with $b$ branching vertices has order at most $(b-1)k$. At 26 labels this lowers the unrestricted upper bound on its order from 598 to **546**. The full conjecture and the unrestricted 26-label case remain open.

The extension may be repeated at different joints, including newly added vertices, whenever the order before each graft is zero or one modulo $k$. In particular, arbitrarily many grafts each adding a multiple of $k$ vertices may precede a final graft of any size.

## Removing ends of paths

Call the chosen core vertex the joint. An arm of length $a$ has $a$ new vertices. Induct on the number of added vertices. Write $n$ for the current total order and let $t$ be the least nonnegative residue of $n-1$ modulo $k$. If $t=0$ and at least one vertex has been added, remove a tip. The remaining tree is divisible and its labeling extends by making the tip edge supply its unique deficient weight.

Suppose $t>0$. The number of added vertices is at least $t$ because the fixed core has order zero or one modulo $k$. Order the arms by nondecreasing length and each arm from the joint toward its tip. Remove the last $t$ vertices. The retained tree still consists of the fixed core and paths attached at the joint. Its order is one modulo $k$. By induction it has a labeling extending the prescribed one. Subtract its surplus vertex residue from all labels for the duration of the construction. Its edge counts are uniform, and it suffices to give the new vertices distinct nonzero labels and their entering edges distinct sums.

The removed components are paths. Every whole removed arm has the joint as parent. If the cut falls inside an arm, its outer piece has a retained parent of its own. That piece is strictly shorter than every whole arm removed with it, since those arms were at least as long as the arm before the cut. Pad one longest component at its tip until the total free order is $k-1$. A lone path can always be padded. With several paths, a distinguished strictly shortest path stays strictly shortest.

It suffices to check the following finite assertion for each partition of $k-1$ into positive lengths. For a common parent label $y$, the free vertices can use all nonzero residues and the $k-1$ sums can be distinct. If the shortest path is unique and there are at least two paths, its parent may independently have any label $x$. Restrict a successful labeling to the original $t$ vertices, translate back, and keep all original core labels. This proves the graft theorem including the case of an arbitrary number of arms. One core vertex gives all spiders.

### Four labels

At $k=4$ the finite assertion itself fails for lengths $(1,2)$ with parent labels $(0,1)$. A different choice of tips proves the graft theorem. For $t=1,2$ every forest of terminal paths works with arbitrary parent colors. For $t=3$, remove one tip from each of three arms if available. Three singleton paths work with arbitrary parents. With at most two arms use one path of length three if possible. The only remaining length lists with enough mass are $(1,2)$ and $(2,2)$. Take the whole of $(1,2)$, whose two parents are the joint. For $(2,2)$ take all four vertices. The remaining tree is divisible. For every joint label and old edge deficit, there is a permutation of the four labels on the two paths which, together with the old counts, leaves exactly one deficient edge bin. The [four-label checker](check_path_grafts.py) tries the at most 24 permutations for each assignment. The case $k=1$ is immediate.

## Bounding a smallest counterexample by its branching vertices

Take a smallest counterexample among trees with at most a fixed number of branching vertices. Both pieces of any edge cut stay in this class, so [divisible cuts](../divisible-cuts.md) are impossible. Write $n=mk+1+t$, $0\le t<k$. Removing one leaf excludes $t=0$. Every branching vertex is the joint of its own terminal arms, the paths running outward to a leaf with no intervening branching vertex. If these arms together have at least $t$ vertices, use the same tip choices as above. The retained tree is smaller and in the class. It has order one modulo $k$, or divisible order in the four-vertex exception. The construction restores the labeling. Thus each branching vertex and its own terminal arms contain at most $t$ vertices.

Contract the skeleton to its $b$ branching vertices joined along their connecting paths. Root it at any branching vertex. A child branch of this skeleton containing $j$ branching vertices, counted together with the degree-two interior of its connector to its parent, has order strictly less than $jk$. Indeed, the child branches below it contain $j-1$ branching vertices in total. Inductively their orders sum to at most $(j-1)k$. Including the current branching vertex and its arms brings the total to at most $(j-1)k+t<jk$. Moving up its connector adds vertices one by one. Reaching $jk$ at any point would give a divisible cut, including at the highest cut immediately below its parent. At the root the same sum gives $n\le(b-1)k+t$. Substituting $n=mk+1+t$ gives $m\le b-2$ and $n\le(b-1)k$.

In particular, for $b\le2$ only orders at most $k$ need testing, and order exactly $k$ suffices. Lengthen a terminal arm to reach $k$. A cordial labeling there is bijective with all edge sums distinct, so restricting it works at the smaller order. Spiders and paths are already covered. For all $b$, write $s=t+1$ and let $L$ be the leaf count. The degree sum gives $b+2\le L$ and the [leaf-deletion theorem](../counterexample-bound.md#removing-leaves) gives $L\le s-2$. Thus $m+4\le L\le s-2$, and $n\le k(k-5)$ for a smallest counterexample in the unrestricted problem at the tested moduli $k\ge5$. [Lean verification of the connector and order inequalities](BranchingBound.lean)

## Certificates and independent tests

The [path generator](terminal_paths.cpp) enumerates sorted partitions and parent-color orbits under multiplication by units. Each row is an explicit permutation of the nonzero residues. The [independent verifier](check_terminal_paths.cpp) reconstructs the internal weights and tests all common-parent colors against an entire row. The remaining holes determine the admissible shortest-parent colors. The verifier expands unit orbits, requires coverage of every requested ordered color assignment, and checks the exact number of distinct partitions by a separate integer partition recurrence.

At order $k$, a tree with exactly two branching vertices has two unordered lists of terminal arm lengths, each with at least two parts, together with a connector of positive length. The total of the arm lengths fixes the connector length. The [base generator](../census/two_centers.cpp) encodes each list by its partial sums as a bit mask. A separate verifier decodes the two lists, reconstructs the tree, counts all actual vertex labels and edge sums, and checks the number of unordered pairs against the partition numbers. For unequal side masses $a<b$ it expects $(p(a)-1)(p(b)-1)$ shapes, and for equal masses it counts unordered pairs with repetition. The [integer census](../census/README.md) supplies every base through order 27.

The [constructive replay](check_path_grafts.py) fixes a path or star core, applies affine changes to its labeling, rebuilds the omitted path batches from the public certificates, and recomputes the two histograms on the entire tree. It also asserts that every core label was preserved. It checked 3,520 complete trees and 20,336 restoration steps through modulus 45. These samples exercise the construction. The exhaustive finite assertions and the induction prove the all-orders results.

## Reproduction

Run from the repository root in Bash. Streams are regenerated locally and their SHA-256 hashes are pinned. The separate checker does not link to the witness search. The [per-modulus counts](terminal-paths.counts) list partitions, witness permutations, tested orbits, individual color assignments and order-$k$ bases.

~~~bash
set -euo pipefail
src="$PWD/research/rainbow"
out=$(mktemp -d)
c++ -O3 -std=c++17 -Drainbow_witness=reference_witness -c "$src/search.cpp" -o "$out/reference.o"
c++ -O3 -std=c++17 -DRAINBOW_WIDE_MASK -c "$src/leaf_search.cpp" -o "$out/leaf.o"
c++ -O3 -std=c++17 "$src/terminal_paths.cpp" "$out/leaf.o" "$out/reference.o" -o "$out/paths"
c++ -O3 -std=c++17 "$src/../census/two_centers.cpp" "$out/leaf.o" "$out/reference.o" -o "$out/bases"
c++ -O3 -std=c++17 "$src/check_terminal_paths.cpp" -o "$out/check"
for k in 2 3 {5..45}; do
    "$out/paths" "$k" > "$out/leg$k"
    "$out/check" paths "$k" < "$out/leg$k"
done
for k in {28..39}; do
    "$out/bases" "$k" > "$out/base$k"
    "$out/check" bases "$k" < "$out/base$k"
done
python3 -B "$src/check_path_grafts.py" "$out" {2..45}
lean "$src/BranchingBound.lean"
(cd "$out" && shasum -a 256 -c "$src/terminal-paths.sha256")
~~~
