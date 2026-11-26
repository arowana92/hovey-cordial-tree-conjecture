# A rainbow forest test for cordial trees

**Theorem.** Every finite tree is $k$-cordial for $k=9,10,11,12,13$. These are computer-assisted results. The reduction below applies to all moduli $k\ge5$. Its finite hypotheses are verified here at nine, ten, eleven, twelve and thirteen. The last two cases use the leaf-centroid bound below.

## The two finite hypotheses

1. Every tree on $k$ vertices has a bijective vertex labeling with distinct edge weights.
2. Let $F$ be a forest on $k-1$ vertices. Orient each component away from a root and prescribe a boundary residue on one external parent of each root. Count the edge to that parent. If $F$ has at most
   $$
   B(k)=k-3-\left\lfloor\frac{k-2}{4}\right\rfloor
   $$
   vertices without children, it has a bijection onto the nonzero residues whose $k-1$ edge weights are distinct.

Here a singleton component counts as one vertex without children. Boundary residues are arbitrary and may coincide. A simultaneous translation of vertex and boundary labels shifts every edge weight by twice the translation. Consequently hypothesis 2 also allows the forbidden vertex residue to be any specified $u$.

## Why the hypotheses suffice

Choose a smallest counterexample, of order $n$. Hypothesis 1 and restriction from a $k$-vertex supertree rule out $n\le k$. Write $n=mk+1+t$ with $m\ge1$ and $0\le t<k$. If $t=0$, remove one leaf, label the smaller tree and choose the leaf label to produce its unique deficient edge weight. Thus $t>0$. If there are at least $t$ leaves, remove $t$ original leaves. The core has a unique surplus vertex residue $u$ and uniform edge counts. Hall’s theorem lets us add the leaves with distinct labels avoiding $u$ and distinct weights. Hence the number of leaves $L$ satisfies $L<t\le k-1$. [Proof of the leaf extension](../counterexample-bound.md#removing-leaves)

**Choosing the core.** A closed contour traversal of a plane drawing of the tree uses each edge twice and visits each of the $L$ leaves once in cyclic order. The lengths of the $L$ gaps between consecutive leaves sum to $2(n-1)$. Set $h=1+\lfloor L/4\rfloor$. By averaging, some run of $h-1$ consecutive gaps has total length at most
$$
\frac{2(n-1)(h-1)}L\ \le\ \frac{n-1}{2}\ \le\ mk.
$$
The last inequality uses $t<k\le mk$. For $h=1$, start with any leaf. In general the part of the traversal in this run spans a connected subtree on at most $mk+1$ vertices containing $h$ original leaves. Grow it to a connected core on exactly $mk+1$ vertices, adding adjacent vertices one at a time.

The complement is a forest on $t$ vertices with one boundary edge per component. Every vertex without children in this orientation is an original leaf outside the core. The forest therefore has at most $L-h=L-1-\lfloor L/4\rfloor$ such vertices. This expression is nondecreasing in $L$, so $L\le k-2$ gives the bound $B(k)$.

**Finishing the labeling.** Give the core a cordial labeling by minimality. Exactly one vertex residue $u$ occurs $m+1$ times, all others occur $m$ times, and every edge residue occurs $m$ times. Pad the nonempty outside forest to order $k-1$ by extending one of its terminal vertices by a path. The number of terminal vertices stays the same. Apply hypothesis 2 with forbidden label $u$ and restrict the labeling to the original outside vertices. The added labels are distinct and avoid $u$. The added weights, including the boundary weights, are distinct. All vertex and edge counts in the whole tree are now $m$ or $m+1$, a contradiction.

## Choosing the core with a leaf centroid

There is also a sufficient test with at most $\lfloor 2(k-2)/3\rfloor$ terminal vertices. The same base hypothesis and the same proof after the core is chosen apply.

Let $L\ge2$ be the number of original leaves in an $n$-vertex tree with $n>k$. Choose an internal vertex $v$ such that no component of $T-v$ contains more than $L/2$ original leaves. To find one, start at an internal vertex and step into any component with more than half the leaves. This walk stays at internal vertices and cannot traverse an edge back, since the reverse side contains fewer than half the leaves. It must terminate.

The components of $T-v$ can be divided into two groups so that each group contains between $L/3$ and $2L/3$ leaves. If a single component contains at least $L/3$ leaves, take it as one group, since it has at most $L/2$. Otherwise accumulate components until the sum first reaches $L/3$, at which point it is less than $2L/3$. Each group together with $v$ induces a connected tree. Their orders add to $n+1$, so the smaller has order at most $(n+1)/2$ and contains at least $\lceil L/3\rceil$ original leaves.

In the minimum-counterexample argument $n=mk+1+t$ with $t<k\le mk$. Thus $(n+1)/2\le mk+1$. Grow the smaller subtree to a connected core of order $mk+1$. At most $L-\lceil L/3\rceil=\lfloor2L/3\rfloor$ original leaves remain outside. Since $L\le k-2$, the terminal bound follows.

## Verification

| Modulus | Rooted base tree shapes | Maximum terminal vertices | Forest shapes | Forest witness rows | Colored forests covered |
|---:|---:|---:|---:|---:|---:|
| 9 | 286 | 5 | 248 | 15,270 | 85,140 |
| 10 | 719 | 5 | 550 | 67,724 | 263,500 |
| 11 | 1,842 | 6 | 1,595 | 215,770 | 2,141,469 |
| 12 | 4,766 | 6 | 3,688 | 1,828,036 | 6,688,476 |
| 13 | 12,486 | 7 | 10,813 | 4,642,374 | 55,571,893 |

Each archive row gives a parent vector and one explicit vertex labeling. The format follows the eight-label archive. The record kind `rainbow` requests distinct nonzero vertex labels and distinct weights on all edges, including edges from boundary parents. Multiplication of every label by a unit permutes both the allowed nonzero labels and the edge weights, which lets one row cover several boundary colorings.

The verifier checks the labels and weights directly. Independently of the generator’s multiset recursion, it constructs the complete list of rooted tree shapes by repeatedly inserting a leaf at every vertex. Canonical child codes identify isomorphic trees. Deleting the root of each $k$-vertex rooted tree gives every unordered rooted forest on $k-1$ vertices. For each required forest shape, if a component type occurs $c$ times its boundary colors form a multiset with $\binom{k+c-1}{c}$ possibilities. The verifier collects the distinct colorings actually witnessed under unit multiplication and compares their cardinality with the product of these binomials over the component types. It checks each shape separately.

Run these commands from the repository root with Python 3.8 or later.

```sh
python3 -B -m research.rainbow.verify 9 research/rainbow/k9.jsonl.gz
python3 -B -m research.rainbow.verify 10 research/rainbow/k10.jsonl.gz
python3 -B -m research.rainbow.verify 11 research/rainbow/k11.jsonl.gz
python3 -B -m research.rainbow.verify 12 research/rainbow/k12.jsonl.gz --centroid
python3 -B -m research.rainbow.verify 13 research/rainbow/k13.jsonl.gz --centroid --grouped
```

To regenerate a certificate, substitute 9, 10 or 11 for the modulus below. Compare the decompressed data to allow for different gzip implementations.

```sh
k=9
python3 -B -m research.rainbow.generate "$k" > /tmp/hovey-rainbow-regenerated.jsonl
gzip -dc "research/rainbow/k$k.jsonl.gz" | cmp - /tmp/hovey-rainbow-regenerated.jsonl
```

For twelve or thirteen labels, run the generator with the additional option `--centroid`. The verifier’s optional `--grouped` flag discards a forest shape’s colorings after checking its consecutive records and rejects any shape that reappears. The decompressed thirteen-label archive has SHA-256 `5e02439f353e913aa1a354977f71362da9fdb009a8cc77f2209211ae3d67ff6a`. The decompressed twelve-label archive has SHA-256 `bc4d25dbb6c76367946c3a0afff3fc1029ff0a87da6a806d766079219c544903`.

The finite hypotheses here differ from the eight-label hypotheses checked by the earlier scripts. The contour argument above is a mathematical proof. The certificate checks run in Python.

At eleven labels a second computation using signed moments proves the extension property for all 1,842 forest shapes, including shapes with more than six terminal vertices. It gives an alternative induction for all tree orders. [Unrestricted eleven-label proof](../prime/README.md#a-second-proof-at-eleven-labels)
