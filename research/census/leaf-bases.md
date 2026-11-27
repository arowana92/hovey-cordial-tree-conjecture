# Small trees with a bounded number of leaves

**Theorem (computer-assisted).** Every finite tree with at most 30 vertices and at most six leaves is cordial at every positive modulus. Each such tree has a bijection onto the integers from zero through its order minus one for which the integer endpoint sums are consecutive. Reduction modulo any positive integer gives the two required frequency bounds.

At each of the orders 28, 29 and 30, every tree with at most eight leaves also has a bijection with distinct endpoint sums modulo its order. These modular witnesses supply order-specific bases for the [induction on trees with few leaves](../rainbow/few-leaves.md). The two counts in each row refer to different leaf limits and different witness requirements. The [unrestricted census through order 27](README.md) supplies the smaller orders.

| Order | At most six leaves, consecutive integer sums | At most eight leaves, distinct modular sums |
| ---: | ---: | ---: |
| 28 | 546,516 | 20,723,132 |
| 29 | 744,081 | 33,223,370 |
| 30 | 1,002,054 | 52,393,232 |
| Total | 2,292,651 | 106,339,734 |

**An unbounded-order consequence of the modular bases.** At each of these three moduli, take any order-$k$ tree with at most eight leaves. Attach any number of new leaves at any of its original vertices. The resulting tree is $k$-cordial. Indeed, the base is cordial and the [prescribed-differences leaf lemma](../counterexample-bound.md#removing-leaves) restores all new leaves in batches starting at an order divisible by $k$.

In particular, suppose the $h$ nonleaf vertices of a tree form a subtree with at most eight leaves and $k-8\le h\le k$. If the tree has fewer than $k$ vertices it has at most eight leaves, and extending a tip to order $k$ and restricting the modular witness suffices. Otherwise keep all $h$ nonleaves and choose $k-h$ of the original leaves. First choose one at each end of the nonleaf subtree until that quota or the list of ends is exhausted. Every such end has an original leaf neighbor. Each of these first additions preserves the number of ends. The final number of leaves is the maximum of the original number of ends of the nonleaf subtree and $k-h$, hence at most eight. The preceding construction applies.

## Why the enumeration is complete

The [generator](leaf_centroids.hpp) lists the multisets of rooted branches at a unique centroid, with total order $n-1$ and maximum branch order strictly less than $n/2$. In the two-centroid case it lists unordered pairs of planted trees of order $n/2$. A planted tree records its terminals as if its root had a parent. Their total gives the number of leaves of the unrooted tree. The two-vertex tree is represented by a pair of singletons. Integers and modular labels use the same canonical ordering of shapes. [Integer search](generate.cpp) · [Modular search](../rainbow/leaf_bases.cpp)

The [verifier](verify.cpp) checks each vertex permutation and all edge sums. On the parsed tree it checks the leaf count, the order of every branch multiset, and the centroid and half-pair conditions. Strictly increasing keys exclude duplicate unrooted shapes. For the number of required shapes it uses vertex-edge dissymmetry with true unrooted leaf counts. Let $R_{a,b}$ count planted trees of order $a$ with $b$ terminals. The product for a multiset of planted trees and its rooted-tree identity are
$$
F(x,y)=\prod_{a,b}(1-x^ay^b)^{-R_{a,b}},\qquad
R(x,y)=x(y-1+F(x,y)).
$$
The verifier computes coefficients using the logarithmic derivative in $x$. For $n\ge2$ the vertex-rooted count with $t$ true leaves is $V_{n,t}=R_{n,t}-R_{n-1,t}+R_{n-1,t-1}$. This correction counts a root with exactly one child as a true leaf. The oriented-edge-rooted count $O_{n,t}$ is the coefficient of $x^ny^t$ in $R^2$. Put $D_{n,t}=R_{n/2,t/2}$ when both indices are even and zero otherwise. The unoriented-edge-rooted count is $(O_{n,t}+D_{n,t})/2$ by swapping the two halves. Dissymmetry therefore gives exactly $V_{n,t}-(O_{n,t}-D_{n,t})/2$ unrooted trees. The verifier requires the sum over the allowed $t$ and checks the end of every input.

An independent [Python check](check_leaf_bases.py) instead counts the centroid branch-size partitions and the unordered half pairs, using a multiset count at each size. It reproduces each of the six totals, compares the limited streams against unrestricted catalogs through order 14, and checks the permutations, leaf counts and edge sums on 257 separated records from each full stream. Three damaged modular streams test rejection of an omitted tree, a repeated tree and a repeated label.

## Reproduction

Run from the repository root in Bash with Python 3 and a C++17 compiler. The six binary streams together require about 4.1 GB. Each record contains an eight-byte little-endian tree word and one byte per vertex in preorder. Separate shards can be verified together in their numerical order using the same format as the unrestricted census.

~~~bash
set -e
src="$PWD/research/census"
rain="$PWD/research/rainbow"
out=$(mktemp -d)
c++ -O3 -std=c++17 "$src/generate.cpp" "$src/interval.cpp" -o "$out/intgen"
c++ -O3 -std=c++17 "$src/verify.cpp" -o "$out/baseverify"
c++ -O3 -std=c++17 -c -Drainbow_witness=reference_witness "$rain/search.cpp" -o "$out/reference.o"
c++ -O3 -std=c++17 "$rain/leaf_bases.cpp" "$rain/leaf_search.cpp" "$out/reference.o" -o "$out/modgen"
for n in 28 29 30; do
    "$out/intgen" "$n" 0 1 "$out/int$n-l6.bin" --leaves 6
    "$out/baseverify" "$n" --leaves 6 "$out/int$n-l6.bin"
    "$out/modgen" "$n" 8 0 1 "$out/mod$n-l8.bin"
    "$out/baseverify" "$n" --modular-leaves 8 "$out/mod$n-l8.bin"
done
python3 -B -m research.census.check_leaf_bases --binaries "$out/intgen" "$out/modgen" "$out/baseverify" --files "$out"
(cd "$out" && shasum -a 256 -c "$src/leaf-bases.sha256")
~~~
