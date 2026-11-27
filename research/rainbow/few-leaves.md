# Trees with few leaves beyond 25 labels

**Theorem (computer-assisted).** Every finite tree with at most eight leaves is $k$-cordial for every $1\le k\le30$. The proof covers arbitrary tree orders. At $26\le k\le30$, it combines five-terminal extension certificates with a separate order-$k$ base. The [unrestricted modulus proofs](../../README.md) supply the smaller moduli.

At 26 and 27 labels every finite tree with at most ten leaves is cordial, by the six-terminal certificates below. A smallest ordinary counterexample would have at least eleven leaves at either modulus, and at least nine at 28 through 30. At every modulus its order residue $s$ also satisfies $s\ge21$. [Short-forest proof](short-forests.md)

## The cut with a bound on terminal vertices

Fix $k\ge5$ and a limit $q$. Suppose every size-ordered forest on $k-1$ vertices with at most $q$ terminals passes the [ordered-cut extension test](ordered-cut.md#which-colored-forests-actually-occur). This gives a bijection onto the nonzero residues with all $k-1$ new edge sums distinct, for every boundary assignment allowed by that test. All edges to the prescribed boundary vertices count.

Take a tree with at most $L$ leaves, where $\lfloor2L/3\rfloor\le q$. Assume first that the trees of order $k$ in this class admit a bijection with distinct edge sums. Trees of smaller order follow by extending a terminal path to order $k$ and restricting the labeling. Singletons are immediate. Every connected subtree has at most as many leaves as the original tree, apart from conventions for a singleton. Indeed, each new leaf with an edge outside the subtree can be extended outward to a distinct original leaf.

Thus the minimum-counterexample argument applies within the class. Write its order as $mk+1+t>k$. As in the ordered cut, $1\le t<k$. Split at a leaf centroid to retain a connected seed of at most $(n+1)/2\le mk+1$ vertices containing at least $\lceil L'/3\rceil$ of the tree's $L'\le L$ original leaves. Grow it to order $mk+1$ in size-ordered preorder. The exterior has at most $\lfloor2L'/3\rfloor\le q$ terminals. Padding an exterior terminal by a path to reach order $k-1$ preserves the tip count and the allowed boundary runs. The smaller core is cordial, so the extension test restores the original tree.

When $L-1\le q$, the same forest audit supplies the order-$k$ base. Root any such tree at an original leaf and remove that leaf. The single remaining rooted component has $L'-1$ terminals. Its all-zero boundary witness labels the missing leaf zero and supplies the required bijection. At $k=26,27$ the independent [integer census](../census/README.md) supplies every order-$k$ base, so only $\lfloor2L/3\rfloor\le q$ is needed. At 28, 29 and 30 labels the [leaf-bounded modular census](../census/leaf-bases.md) verifies every order-$k$ tree with at most eight leaves. Now $\lfloor2\cdot8/3\rfloor=5$, which proves the theorem.

## A finite reduction for eleven leaves

For each $26\le k\le30$, checking all orders up to $2k$ would suffice for every tree with at most eleven leaves. More generally suppose the $q$-terminal extension test at order $k-1$ holds. A least counterexample among trees with at most $2q+1$ leaves would have order at most $2k$.

Indeed, at a leaf centroid each component contains at most $q$ original leaves. Merge parts whenever their combined leaf count is at most $q$. If four or more parts remained, two disjoint pairs of them would account for at least $2(q+1)$ leaves, a contradiction. If $n=mk+1+t$ with $m\ge2$ and $1\le t<k$, the largest of the at most three groups contains at least $t$ vertices because $n-1=mk+t>3(t-1)$. Keep the centroid and all the other groups as a connected seed. Preorder the chosen group from the centroid, in nondecreasing child-subtree size, growing the seed to $mk+1$ vertices. The exterior has at most $q$ terminals and passes the same extension test. Order $1\bmod k$ is covered by deleting one leaf. This excludes every larger least counterexample in the class.

## Six terminals at 26 labels

The verifier accepted 15,627,230 forests with 293,707,294 witness rows covering 17,299,915,880 boundary assignments. Since $\lfloor2\cdot10/3\rfloor=6$ and the complete order-26 base is available, this proves the ten-leaf result. The three-group argument above also reduces the class with at most thirteen leaves to checking the first $2k$ orders. Thus an ordinary smallest 26-label counterexample with eleven, twelve or thirteen leaves would have between 47 and 52 vertices.

A separate build replayed all witness rows. Regenerating shard 11 with stride 65,537 produced exactly the corresponding 239 records of the full stream, byte for byte. A Python reader scanned the complete stream and checked 13 selected forests across all four possible run counts, covering 2,431 rows and 494,338 boundary assignments.

## Six terminals at 27 labels

The full stream covers 23,665,913 forests, 394,996,404 witness rows and 28,035,301,149 boundary assignments. A separately built native verifier replayed the entire stream. An independent generator reproduced all 362 records from shard 11 at stride 65,537 byte for byte. A Python scan checked 13 selected forests across all four run counts, 1,933 rows and 554,229 literal boundary assignments.

Together with the complete order-27 base, the six-terminal reduction proves every tree with at most ten leaves is 27-cordial. The three-group argument reduces the class with at most thirteen leaves to checking orders through 54. A smallest 27-label counterexample in that class would have eleven through thirteen leaves and order between 48 and 54. [Order restrictions](short-forests.md)

## Five-terminal certificates

| Modulus | Forests | Witness rows | Boundary assignments before unit symmetry |
| ---: | ---: | ---: | ---: |
| 26 | 2,039,320 | 28,003,625 | 1,396,177,120 |
| 27 | 2,831,426 | 34,972,240 | 2,073,156,930 |
| 28 | 3,882,235 | 77,989,441 | 3,008,016,256 |
| 29 | 5,261,441 | 32,237,599 | 4,340,505,081 |
| 30 | 7,053,721 | 205,966,485 | 6,071,873,340 |

## Four-terminal certificates

| Modulus | Forests | Witness rows | Boundary assignments before unit symmetry |
| ---: | ---: | ---: | ---: |
| 26 | 165,424 | 1,600,711 | 62,618,374 |
| 27 | 210,874 | 1,866,639 | 85,214,754 |
| 28 | 266,312 | 3,820,962 | 111,400,688 |
| 29 | 333,476 | 1,374,847 | 148,761,532 |
| 30 | 414,228 | 8,504,239 | 189,886,830 |

The [generator](tip_forests.hpp) enumerates multisets of rooted branches by order, canonical word and number of terminals. The [native verifier](spine_verify.cpp) parses every tree, rejects duplicate words, checks its tip count and each label permutation, recomputes the edge sums and verifies coverage of the permitted boundary assignments. It computes the exact number of eligible forests using a separate bivariate multiset product indexed by order and terminal count. A [Python partition count and cross-check](check_tip_forests.py) reproduces both outer columns, compares every selected witness record with the unrestricted generator at moduli 5 through 11, and tests rejection of an omission, duplication and extraneous shape.

At 26 and 30, a further [Python check](check_spine_samples.py) sampled 26 forests across all four possible run counts, verified 7,903 witness rows, and directly checked 1,316,086 boundary assignments. The same Python check sampled 24 forests in the five-terminal streams at 26 and 30, checking 14,647 rows and 1,342,134 boundary assignments. The exhaustive native checks supply the theorem. The unrestricted 26-label audit is a separate calculation. [Deterministic stream digests](tip-streams.sha256)

## Reproduction

From the repository root, run the following in Bash with Python 3 and a C++17 compiler. The five four-terminal streams occupy about 471 MiB combined. The five larger streams occupy about 11 GB combined.

~~~bash
set -e
src="$PWD/research/rainbow"
out=$(mktemp -d)
c++ -O3 -std=c++17 -c -Drainbow_witness=reference_witness "$src/search.cpp" -o "$out/reference.o"
c++ -O3 -std=c++17 "$src/spine_generate.cpp" "$src/leaf_search.cpp" "$out/reference.o" -o "$out/generate"
c++ -O3 -std=c++17 -pthread "$src/spine_verify.cpp" -o "$out/verify"
python3 -B -m research.rainbow.check_tip_forests --binaries "$out/generate" "$out/verify"
python3 -B -m research.rainbow.check_tip_forests --tips 5
"$out/generate" 26 0 1 "$out/k26-t6.spn" --tips 6
"$out/verify" 26 --tips 6 "$out/k26-t6.spn"
python3 -B "$src/check_spine_samples.py" "$out/k26-t6.spn" --stride 1600000
"$out/generate" 27 0 1 "$out/k27-t6.spn" --tips 6
"$out/verify" 27 --tips 6 "$out/k27-t6.spn"
python3 -B "$src/check_spine_samples.py" "$out/k27-t6.spn" --stride 2400000
for t in 4 5; do
    for k in 26 27 28 29 30; do
        "$out/generate" "$k" 0 1 "$out/k$k-t$t.spn" --tips "$t"
        "$out/verify" "$k" --tips "$t" "$out/k$k-t$t.spn"
    done
done
python3 -B "$src/check_spine_samples.py" "$out/k26-t4.spn" --stride 21000
python3 -B "$src/check_spine_samples.py" "$out/k30-t4.spn" --stride 35000
python3 -B "$src/check_spine_samples.py" "$out/k26-t5.spn" --stride 350000
python3 -B "$src/check_spine_samples.py" "$out/k30-t5.spn" --stride 600000
(cd "$out" && shasum -a 256 -c "$src/tip-streams.sha256")
~~~
