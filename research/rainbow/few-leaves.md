# Trees with few leaves beyond 25 labels

**Theorem (computer-assisted).** Every tree with at most five leaves is $k$-cordial for each $26\le k\le30$, at every tree order. At 26 and 27 labels this holds for every tree with at most seven leaves. Together with the earlier modulus proofs, the five-leaf result applies at every $k\le30$.

**Corollary at 26.** A smallest counterexample would have at least eight leaves and order $26m+s$ with $18\le s\le26$. At $s=18$ it must have exactly eight leaves. Indeed, the [parity list theorem](../biased/twice-prime-power-lists.md) permits deleting seven leaves, giving $2s-26\ge10$, and nine leaves would give $2s-26\ge12$.

## The cut with a bound on terminal vertices

Fix $k\ge5$ and a limit $q$. Suppose every size-ordered forest on $k-1$ vertices with at most $q$ terminals passes the [ordered-cut extension test](ordered-cut.md#which-colored-forests-actually-occur). This gives a bijection onto the nonzero residues with all $k-1$ new edge sums distinct, for every boundary assignment allowed by that test. All edges to the prescribed boundary vertices count.

Take a tree with at most $L$ leaves, where $\lfloor2L/3\rfloor\le q$. Assume first that the trees of order $k$ in this class admit a bijection with distinct edge sums. Trees of smaller order follow by extending a terminal path to order $k$ and restricting the labeling. Singletons are immediate. Every connected subtree has at most as many leaves as the original tree, apart from conventions for a singleton. Indeed, each new leaf with an edge outside the subtree can be extended outward to a distinct original leaf.

Thus the minimum-counterexample argument applies within the class. Write its order as $mk+1+t>k$. As in the ordered cut, $1\le t<k$. Split at a leaf centroid to retain a connected seed of at most $(n+1)/2\le mk+1$ vertices containing at least $\lceil L'/3\rceil$ of the tree's $L'\le L$ original leaves. Grow it to order $mk+1$ in size-ordered preorder. The exterior has at most $\lfloor2L'/3\rfloor\le q$ terminals. Padding an exterior terminal by a path to reach order $k-1$ preserves the tip count and the allowed boundary runs. The smaller core is cordial, so the extension test restores the original tree.

When $L-1\le q$, the same forest audit supplies the order-$k$ base. Root any such tree at an original leaf and remove that leaf. The single remaining rooted component has $L'-1$ terminals. Its all-zero boundary witness labels the missing leaf zero and supplies the required bijection. At $k=26,27$ the independent [integer census](../census/README.md) supplies every order-$k$ base, so only $\lfloor2L/3\rfloor\le q$ is needed. Taking $q=4$ proves the assertions.

## Four-terminal certificates

| Modulus | Forests | Witness rows | Boundary assignments before unit symmetry |
| ---: | ---: | ---: | ---: |
| 26 | 165,424 | 1,600,711 | 62,618,374 |
| 27 | 210,874 | 1,866,639 | 85,214,754 |
| 28 | 266,312 | 3,820,962 | 111,400,688 |
| 29 | 333,476 | 1,374,847 | 148,761,532 |
| 30 | 414,228 | 8,504,239 | 189,886,830 |

The [generator](tip_forests.hpp) enumerates multisets of rooted branches by order, canonical word and number of terminals. The [native verifier](spine_verify.cpp) parses every tree, rejects duplicate words, checks its tip count and each label permutation, recomputes the edge sums and verifies coverage of the permitted boundary assignments. It computes the exact number of eligible forests using a separate bivariate multiset product indexed by order and terminal count. A [Python partition count and cross-check](check_tip_forests.py) reproduces both outer columns, compares every selected witness record with the unrestricted generator at moduli 5 through 11, and tests rejection of an omission, duplication and extraneous shape.

At 26 and 30, a further [Python check](check_spine_samples.py) sampled 26 forests across all four possible run counts, verified 7,903 witness rows, and directly checked 1,316,086 boundary assignments. The exhaustive native checks supply the theorem. The unrestricted 26-label audit is a separate calculation. [Deterministic stream digests](tip-streams.sha256)

## Reproduction

From the repository root, run the following in Bash with Python 3 and a C++17 compiler. The five four-terminal streams occupy about 471 MiB combined.

~~~bash
set -e
src="$PWD/research/rainbow"
out=$(mktemp -d)
c++ -O3 -std=c++17 -c -Drainbow_witness=reference_witness "$src/search.cpp" -o "$out/reference.o"
c++ -O3 -std=c++17 "$src/spine_generate.cpp" "$src/leaf_search.cpp" "$out/reference.o" -o "$out/generate"
c++ -O3 -std=c++17 -pthread "$src/spine_verify.cpp" -o "$out/verify"
python3 -B -m research.rainbow.check_tip_forests --binaries "$out/generate" "$out/verify"
for k in 26 27 28 29 30; do
    "$out/generate" "$k" 0 1 "$out/k$k-t4.spn" --tips 4
    "$out/verify" "$k" --tips 4 "$out/k$k-t4.spn"
done
python3 -B "$src/check_spine_samples.py" "$out/k26-t4.spn" --stride 21000
python3 -B "$src/check_spine_samples.py" "$out/k30-t4.spn" --stride 35000
(cd "$out" && shasum -a 256 -c "$src/tip-streams.sha256")
~~~
