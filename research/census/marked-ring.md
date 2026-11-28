# Prescribing a most-frequent leaf at 27 and lifting to 54 labels

**Theorem.** For any tree with at most eleven leaves and any specified leaf, there is a 27-cordial labeling in which its residue has maximum vertex frequency. Consequently every tree with at most eleven leaves and a matching missing at most one vertex is **54-cordial**, at every order.

The new point in passing from the [eleven-leaf theorem](eleven-leaves.md) to the marked version is retaining a mark inside a 27-vertex piece inserted in place of an edge. The following sharp elementary bound works at all moduli.

## A unit orbit meets a prescribed interval

For $k\ge2$ let $p$ be its smallest prime divisor. Every cyclic interval of **at least $2k/p$ consecutive residues** meets every translate of every nonzero unit orbit in $\mathbb Z_k$. The length bound is best possible.

Indeed write $g=\gcd(k,d)$ for a nonzero residue $d$, and $l=k/g$. Its unit orbit consists of the residues $gj$ with $j$ coprime to $l$. Reduction of units from modulus $k$ onto the units modulo $l$ is surjective, by the Chinese remainder theorem on the prime powers of $k$. Choose a prime $q\mid l$. The $q$ values $1+i(l/q)$ modulo $l$ are all coprime to $l$ apart from at most one. Every prime dividing $l/q$ divides none of them, and the only other possible prime factor is $q$. After multiplication by $g$ these give $q$ evenly spaced positions, of which at most one is missing. Hence the maximum circular distance between successive orbit points is at most $2k/q\le2k/p$. An interval of the stated length must meet the orbit. For $d=k/p$ the orbit consists of all nonzero multiples of $k/p$ and its largest gap is exactly $2k/p$. Translating the empty interval in that gap gives sharpness.

Suppose a harmoniously labeled unicyclic graph on $k$ vertices is opened at the cycle edge $uv$, and inserted on an old edge with labels $a,b$. Write $f$ for its labels, adding edges from $a$ to $u$ and from $v$ to $b$. Replace $f(z)$ by $a+h(f(z)-f(v))$ for any unit $h$. The filling remains bijective on vertices and cycle-graph edge weights. The first entering edge replaces the open cycle weight and the second replaces the old edge weight. Thus every old vertex and edge count gains one. The image of a marked new vertex $w$ ranges over $a$ plus the unit orbit of $f(w)-f(v)$. It can be put in any interval of most-frequent old residues of length at least $2k/p$ if the difference is nonzero. A zero difference gives the anchor label $a$ itself. [Unmarked edge replacement](few-leaf-rings.md)

## The marked leaf at every tree order

At orders divisible by 27, every vertex residue is most frequent. Through order 27, the integer-label census gives an injective labeling with distinct weights. At order one modulo 27, remove the marked leaf, label the smaller tree by the ordinary eleven-leaf theorem and give the leaf the label filling the unique deficient edge weight. Its own label is then the surplus.

Whenever a cut leaves a core of order one modulo 27 and the exterior receives distinct nonsurplus residues with distinct weights, the marking is preserved as follows. An exterior mark belongs to an incremented residue. For a mark in the core, make its leaf label the core surplus by the preceding deletion argument. The marked vertex remains a leaf of the core. All new labels avoid it, so its count is still maximal. [Marked cut argument](../marked-leaves.md)

- For orders 29 through 49 there are at most 21 exterior vertices after a size-ordered leaf-centroid cut. There are at most seven exterior tips since the whole tree has at most eleven leaves. Pad a largest component to exterior order 21 and apply the [21-vertex certificate at 27](../rainbow/twenty-one-free.md#twenty-one-exterior-vertices-at-27-labels), which permits up to thirteen tips. Restricting preserves injectivity and distinct sums.
- At orders 50 through 54 the [eleven-leaf reductions](eleven-leaves.md) preserve the mark by the cut argument in each seed, suffix, six-path and final listed-forest case. The theorem for at most ten leaves already gives the marked assertion in that class. In a ring replacement the old tree has $s=n-27$ vertices, so $23\le s\le27$. Use its super edge-magic labeling with vertex palette $0,\ldots,s-1$ from the [integer census](README.md). Every old mark is in a most-frequent residue. For an inserted mark the palette has length at least 23, exceeding $2\cdot27/3=18$, and it contains both old anchor labels. The orbit bound puts this mark in the palette as well.
- Above order 54, the [three-group argument](../rainbow/few-leaves.md#a-finite-reduction-for-eleven-leaves) gives a size-ordered exterior with at most six tips for trees with at most thirteen leaves. Its proof uses the order $27m+1+t$ with $m\ge2$ and $1\le t<27$; it depends only on the tree shape. Apply the six-tip certificate and the marked cut argument. The other residue cases were handled above.

## Matching consequence and verification

Contracting a perfect matching gives a tree with at most the original number of leaves. The [odd-modulus matching lift](../matching-expansion.md) doubles 27 to 54. For a near-perfect matching move the exposure to a leaf and add a temporary mate. The quotient leaf for this last pair can be made most frequent at 27 by the theorem above. In the 54-label lift, deleting the temporary vertex and its odd matching edge reduces a most-frequent bin in each histogram. Both histograms stay balanced. [Deletion and leaf-count argument](../marked-leaves.md#returning-to-the-original-matching-tree)

The [independent checker](check_marked_ring.py) exhausts 28,680 nonzero orbit inputs through modulus 240, computing every circular gap directly. At 27 it opens a harmonious triangle with two pendant paths and checks 1,440 marked insertions on actual core trees, including 60 where the identity scaling misses the mark. It also rebuilds the matched trees on 205 such quotients and checks their complete 54-bin histograms both before and after deleting the temporary vertex.

~~~sh
python3 -B -m research.census.check_marked_ring
~~~
