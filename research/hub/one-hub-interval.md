# A prescribed leaf-attachment vertex on every core through order twenty

**Theorem.** For any tree $H$ on at most twenty vertices, choose any vertex $o$ and attach any number $m\ge0$ of leaves there. The resulting tree is super edge-magic and is $k$-cordial for every positive modulus $k$.

**Corollary.** The conclusion holds at any tree order if some vertex $o$ is incident to all but at most ten edges. Consequently any counterexample to Hovey's conjecture must have at least eleven edges avoiding **each** of its vertices.

To see the corollary, remove all leaf neighbors of $o$. Let $e\le10$ be the number of edges avoiding $o$ and $r$ the number of remaining branches at $o$. Each branch has at least one internal edge, so $r\le e$. The trimmed tree has $1+e+r$ vertices. If that exceeds twenty, then $e=r=10$ and all ten branches have two vertices. Adding the removed leaves back gives a tree of diameter at most four. The case with no remaining branches is a star. [Diameter-four theorem](all-radius-two.md)

## How one labeling covers every population

Root $H$ at $o$ and write $n=|H|$. For the main certificate the raw labels $a_v$ are a permutation of $[0,n-1]$, with $a_o=c$. The verifier requires
$$
\{a_u+a_v-c:uv\in E(H)\}=[1,n-1].
$$
Subtract $c$ from all vertex labels. The root now has label zero, the vertices fill $[-c,n-1-c]$, and the edge sums fill $[1-c,n-1-c]$. Give the added leaves consecutive labels starting at $n-c$. Each contributes its own label as edge sum. Both intervals therefore stay consecutive for every $m$. Their residue counts are balanced modulo any $k$. [Youssef, Theorem 4](https://ajc.maths.uq.edu.au/pdf/43/ajc_v43_p031.pdf)

The other records invoke one of these reductions.

- When $H$ has a leaf neighbor of its root, delete that neighbor and apply the theorem at order $n-1$ with $m+1$ free leaves.
- Form $H^+$ by attaching one leaf at the root. If $H^+$ has at most five nonleaf vertices, has a path as its nonleaf core, or has diameter at most four, the corresponding theorem applies for all $m$. For $m\ge1$ the nonleaf core stays the same. For $m=0$, deleting a leaf preserves each applicable classification. The singleton is immediate. [Five-nonleaf theorem](five-nonleaf.md) · [Caterpillars and diameter four](all-radius-two.md)

Thus the conclusion follows by induction once all the rooted shapes at every order through twenty have been verified. The earlier one-hub certificate through order thirteen allowed a missing weight anywhere in the interval and used a modular extension. The contained integer intervals above give a super edge-magic labeling of the whole extended tree. [Earlier one-hub construction](README.md)

The verifier accepted 20,247,374 distinct rooted shapes across the twenty orders. Of these, 12,064,816 have direct root-zero witnesses and 8,182,558 use the reductions. At order twenty alone the respective counts are 7,742,501 direct witnesses and 5,083,727 reductions.

## Generation and independent verification

The generator represents a rooted tree by its preorder depths with siblings arranged in decreasing lexicographic subtree order. It starts at the path. To advance, find the last depth greater than one and copy a periodically repeated suffix starting at the preceding ancestor one level higher. The verifier does not assume this successor rule is exhaustive.

The search assigns each new vertex a free slot $a_i$ with free edge slot $a_i+a_{\rm parent}-c$. It tries positions close to the middle for $c$ first. The degree sum identity
$$
\sum_v(\deg_H(v)-1)a_v=(n-1)c
$$
follows by summing the required edge slots and vertex slots. It prunes impossible partial assignments. Leaf siblings can use increasing slots in their assignment order. These choices affect search time only. [Generator](one_hub_interval_generate.cpp)

A stream is for one specified order. A record gives the $n-1$ nonroot preorder depths as bytes followed by a kind byte. Zero requests a structural reduction. One is followed by $n$ raw label bytes in vertex order. The independent verifier reconstructs the tree, checks all edge slots and the raw vertex permutation, or validates the reduction on the actual tree. For the diameter test it computes distances after adding the extra root leaf.

For shape coverage, consecutive depths cannot jump upwards by more than one, and positive nonroot depths and preorder determine the parent. The verifier compares the complete depth strings of adjacent sibling subtrees. Siblings start at the same depth, so their absolute depth strings give the same lexicographic comparison as their relative strings. Sorting these strings gives a unique representation by induction. Requiring strict decrease of entire tree codes across records excludes every duplicate.

Finally compute the independent number $t_n$ of rooted unordered trees from
$$
T(x)=x\prod_{j\ge1}(1-x^j)^{-t_j},\qquad T(x)=\sum_{n\ge1}t_nx^n .
$$
The product enumerates multisets of children. Logarithmic differentiation gives $(n-1)t_n=\sum_{j=1}^{n-1}(\sum_{d\mid j}dt_d)t_{n-j}$ with $t_1=1$. The verified number of distinct records must equal $t_n$ at every order. [Independent verifier](one_hub_interval_verify.cpp) · [Per-order counts and digests](one-hub-interval-counts.txt)

## Reproduction

Use a C++17 compiler and a shell with pipeline status checking. The manifest gives order, rooted shapes, structural reductions, root-zero witnesses and SHA-256 of the uncompressed stream. Regenerating one order at a time bounds temporary disk space by the largest single stream.

~~~sh
set -e
set -o pipefail
src="$PWD/research/hub"
out=$(mktemp -d)
c++ -O3 -std=c++17 "$src/one_hub_interval_generate.cpp" -o "$out/generate"
c++ -O3 -std=c++17 "$src/one_hub_interval_verify.cpp" -o "$out/verify"
for n in $(seq 1 20); do
    "$out/generate" "$n" > "$out/current.bin"
    counts=$("$out/verify" "$n" < "$out/current.bin")
    digest=$(shasum -a 256 "$out/current.bin" | cut -d' ' -f1)
    echo "$counts $digest"
done > "$out/counts.txt"
diff "$src/one-hub-interval-counts.txt" "$out/counts.txt"
~~~
