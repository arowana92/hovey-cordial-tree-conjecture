# A prescribed leaf in a most-frequent class

**Theorem.** For every modulus $1\le m\le25$, every finite tree and any one of its leaves, there is an $m$-cordial labeling in which the leaf belongs to a most-frequent vertex residue. The same holds for $m=26,27$ on trees with at most ten leaves, and for $28\le m\le30$ on trees with at most eight leaves. Translation allows any particular residue to be chosen for that most-frequent class.

**Matching consequence.** Every finite tree with a perfect matching or a matching missing just one vertex is $2m$-cordial at **every odd $m\le25$**. This includes $26,30,34,38,42,46,50$ labels at arbitrary tree orders and with arbitrarily many leaves. The same conclusion holds at 54 labels with at most ten leaves and at 58 labels with at most eight leaves.

## Keeping the leaf in a high bin across a cut

If the order is divisible by $m$, all vertex frequencies are equal in any cordial labeling. At orders at most $m$, injectivity makes every used label a most-frequent one. At order $qm+1$, remove the specified leaf, cordially label the remainder, and return the leaf with the label which fills the edge deficit. Its own label is now the unique surplus. The singleton causes no difficulty.

Otherwise take the usual cut at order $qm+1$, with $1\le t<m$ exterior vertices. If the tree has at least $t$ leaves one can use a batch of $t$ original leaves. Hall's prescribed-differences lemma handles their parent labels. With fewer leaves, the leaf-centroid cut gives a size-ordered exterior with at most $\lfloor2L/3\rfloor$ terminals, where $L$ is the number of original leaves. The finite forest tests supply distinct new vertex residues avoiding the one surplus of the core, and distinct new edge sums, for every permitted assignment of parent labels. The cut depends only on the tree shape. [Leaf-batch argument](counterexample-bound.md#removing-leaves) · [Size-ordered cut and padding](rainbow/ordered-cut.md)

If the marked leaf is **outside** the core, its new label increases a previously low count. It is a most-frequent residue at the end. If it is **inside**, it is still a leaf of the core. Use the preceding order-$qm+1$ construction to make its label the core surplus. Every exterior label then avoids that bin, which stays a most-frequent bin. This is the only extra prescription needed. Smaller connected subtrees have at most as many leaves as the original tree, as can also be seen by pruning single leaves. The same argument consequently works with leaf-bounded ordinary bases and forest certificates.

For moduli 2, 3, 5 and 7 the [prescribed-prefix theorem](near-matching.md#every-connected-prefix) suffices. Modulus one is immediate. At modulus four the only case where the leaf batch is unavailable has two leaves and hence is a path. Starting from the marked endpoint, rank its two alternating classes by first appearance and put the marked class first. The consecutive integer vertex labels begin at zero at the mark, and the consecutive edge sums give cordiality. At six and eight the small ordered-cut tests below supply the hypothesis. For nine through twenty-five use the [forest catalog](rainbow/README.md), [ordered certificates](rainbow/ordered-cut.md), [eighteen through twenty-one](rainbow/native-spine.md), [twenty-two](rainbow/twenty-two.md), [twenty-three](rainbow/twenty-three.md), [twenty-four](rainbow/twenty-four.md) and [twenty-five](rainbow/twenty-five.md). The [leaf-limited certificates](rainbow/few-leaves.md) give the remaining claims.

## Returning to the original matching tree

In the near-perfect case move the exposure to an original leaf, add a temporary leaf there and include its edge in the perfect matching. The contracted quotient has a specified leaf representing this last pair. Give it a most-frequent residue by the theorem. Apply the [odd-modulus matching lift](matching-expansion.md). Removing the temporary vertex reduces a most-frequent vertex bin, and removing the odd matching weight reduces a most-frequent edge bin. Both resulting histograms are balanced, exactly as in the [matching deletion calculation](near-matching.md#completing-and-lifting-a-maximum-matching). The perfect case uses the lift without deletion. Extending a terminal arm by one edge preserves the leaf count, and contraction of matching edges does not increase it. The leaf-limited statements therefore apply to the quotient as claimed. The singleton is immediate.

## Reproduction

The [constructor](marked_leaf.py) records an actual cut, labels the core with the required surplus when the mark survives, and restores the exterior. The [checker](check_marked_leaf.py) computes the two histograms on the original edges. It tests 6,939 marked small trees, 200 additional marked trees, path cuts placing the mark on both sides, and 90 matching lifts through 58 labels. The [matching constructor](near_matching.py) starts from the original tree.

At modulus six the native verifier accepted 20 rooted bases, seven eligible forests, 38 rows and 102 boundary assignments. At eight it accepted 115 rooted bases, 87 eligible forests, 548 rows and 3,216 assignments. To regenerate these small sufficient tests and the marked-leaf checks, run the following from the repository root in Bash.

~~~bash
set -e
src="$PWD/research/rainbow"
out=$(mktemp -d)
c++ -O3 -std=c++17 "$src/spine_generate.cpp" "$src/search.cpp" -o "$out/generate"
c++ -O3 -std=c++17 -pthread "$src/spine_verify.cpp" -o "$out/verify"
for m in 6 8; do
    "$out/generate" "$m" 0 1 "$out/$m.spn" --cover
    "$out/verify" "$m" "$out/$m.spn"
done
python3 -B -m research.check_marked_leaf
python3 -B -m research.check_near_matching
~~~
