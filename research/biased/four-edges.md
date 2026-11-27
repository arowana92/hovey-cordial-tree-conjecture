# Independent edge offsets at every prime near one vertex

**Theorem.** Fix a prime $p$ and a vertex $o$ of a finite tree. If at most four edges have neither endpoint at $o$, then the tree is $p$-cordial for every assignment of edge offsets. This holds for arbitrarily many neighbors of $o$ and at every tree order.

For $p\le13$ the [unrestricted offset theorem](README.md) applies. Suppose $p\ge17$. Delete the hub $o$ and let $H$ consist of all the resulting non-singleton components, of total order $v$. A component with $m_i\ge1$ edges has $m_i+1\le2m_i$ vertices, so $v\le8$. At order $p$ the remaining $s=p-1-v$ vertices are hub leaves. The [template computation](../prime/README.md#finite-verification-for-four-edges) gives a nonzero scalar for all such forests at all primes $p\ge17$, except for the five pairs below. Its zero-offset scalar is the scalar in the [degree lemma](README.md#signed-counts-and-first-moments). Thus every other case accommodates arbitrary offsets on all edges.

For a smaller order, pad to $p$ at the hub. For a larger order, retain $o$, $H$ and enough hub leaves to make $p$ vertices. Restore the other leaves from order $0\bmod p$ one at a time to fill the missing weight, and from order $1\bmod p$ in batches of up to $p-1$ using Hall's prescribed-differences theorem. Its prescribed shifts are the parent label plus each leaf's own offset. [Leaf extension](../counterexample-bound.md#removing-leaves)

## The five exceptional pairs

Index the vertices of $H$ from zero and put $-1$ for a parent at the hub. Fix the hub label to zero. As in the unrestricted theorem, first moments form a matrix in the offsets and one can set the offset of one hub leaf to zero. The dimensions below refer to the kernel **after** this normalization. Outside that kernel some signed first moment is nonzero, which proves existence.

| Prime | Parents in $H$ | Kernel dimension | Active labels for zero offsets |
| ---: | :--- | ---: | :--- |
| 17 | −1, 0, −1, 2, −1, 4 | 0 | 16, 2, 3, 1, 15, 4 |
| 19 | −1, 0, −1, 2, 2, 0 | 0 | 17, 3, 2, 1, 4, 6 |
| 19 | −1, 0, −1, 2, 3, 3 | 1 | 15, 5, 2, 1, 3, 4 |
| 19 | −1, 0, −1, 2, −1, 4, −1, 6 | 0 | 17, 3, 2, 1, 14, 9, 5, 4 |
| 61 | −1, 0, −1, 2, 3, 2 | 0 | 59, 3, 31, 1, 32, 33 |

The nonzero line has representative $(1,13,11,3,5,5)$ on the six active edges and zero on the hub leaves. Use labels $(5,6,10,2,15,3)$ in parent-list order. The active weights are $(6,5,2,15,3,10)$ modulo 19. Give the other leaves the remaining nonzero labels. Their weights equal their labels. Dilating covers the entire line.

## Checking the matrices on the small forest

For a unit vector of offsets, retain $H$ and additionally retain its marked hub leaf if the unit occurs there. Call the retained set active. Each remaining leaf has zero offset, so its label equals its weight. Active labels must be distinct and nonzero. Their weights must be distinct and in the active labels together with zero. These conditions are equivalent to the existence of a full rainbow labeling with those active labels. The permutation sign on the active labels and zero is unchanged by adjoining fixed points.

Write $a_i$ for the sum of sign times active label $i$ over these assignments. With $t$ unmarked hub leaves outside the active set, their $t!$ orders multiply every active moment by $t!$. The moment at any one of the $t$ other leaves is $-(t-1)!\sum_i a_i$, since the sum of the entire field is zero. Swapping singleton leaves recovers the other unit columns from the first. This constructs the full $(p-1)$-square matrix including the internal-edge columns.

Two programs compute the compressed sums and compare every entry. Both use the fact that unmarked component roots and unused leaves are fixed by the permutation. Its remaining possible letters are zero, the vertices whose parents belong to $H$, and the marked vertex when it is a hub child. For a candidate permutation $\pi$, the endpoint equations are $x_{\pi(i)}=x_i+x_{\rm parent(i)}+b_i$, using zero for the dummy letter and the hub. They are imposed only for real sources, leaving the image of zero as the missing weight.

The first program solves the affine systems by Gaussian elimination, enumerates free coordinates and computes signs from inversions. An internally marked edge can have its source fixed precisely when its parent's label cancels its offset. The second program propagates equations with a single unknown, branches over unused field elements, and computes signs from cycle decomposition. The Python checker recomputes rank by an independent elimination, tests the normalized representatives for membership and completeness, and recomputes their listed labels' weights. [Linear counter](../prime/template_counts.cpp) · [Propagation counter](template_check.cpp) · [Rank and witness checks](verify_templates.py)

From the repository root with a C++17 compiler and assertion-enabled Python 3, run

~~~sh
set -e
out=$(mktemp -d)
c++ -O3 -std=c++17 research/prime/template_counts.cpp -o "$out/linear"
c++ -O3 -std=c++17 research/biased/template_check.cpp -o "$out/propagate"
python3 -B -m research.prime.verify_templates "$out/linear"
python3 -B -m research.biased.verify_templates "$out/linear" "$out/propagate"
~~~

The first calculation checks the scalar classification at unbounded primes. The second prints all five normalized kernels and all six witnesses above.
