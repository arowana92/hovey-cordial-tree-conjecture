# Eight labels on every finite tree

**Theorem (computer-assisted).** Every finite tree admits an 8-cordial labeling. The argument below reduces arbitrary order to a finite lemma about attaching rooted forests. The accompanying certificate supplies the labelings for that lemma. The conjecture with unrestricted modulus remains open.

## The extension lemma

Let a connected labeled core have order $8m$, with $m\ge 1$. In a cordial labeling each vertex residue occurs $m$ times. There are $8m-1$ edges, so one residue $d$ occurs $m-1$ times and every other residue occurs $m$ times.

Attach a forest of $r$ new vertices, where $1\le r\le 8$. Each component attaches to the core by exactly one edge. Root the component at the new endpoint of that edge and record the residue of the old endpoint. Different components may attach to the same core vertex. Only its residue enters the edge formula. Thus the input consists of an unordered collection of rooted trees, each carrying one prescribed boundary residue. There are exactly $r$ new edges, including the attachments.

**Finite lemma.** For every such input and every $d\in\mathbb Z/8\mathbb Z$, there is an injection from its $r$ vertices to the eight residues with the following property. If $h(a)$ counts the new edges of weight $a$, then for all $a$,

$$
1\ \le\ \mathbf 1_{a\ne d}+h(a)\ \le\ 2.
$$

When $r=8$, the sum of these eight quantities is 15, so exactly one is 1. In particular the deficient residue may change between successive blocks. Keeping the quantifier over every $d$ allows the next block to handle that change.

**Example.** Attach eight leaves, seven to boundary vertices labeled 0 and one to a vertex labeled 1. For a prescribed deficient weight $d$, give the exceptional leaf the label $d-1$ modulo eight and distribute the other seven labels bijectively. The new weights contain two copies of $d$, omit $d-1$, and contain every other residue once. This explains why the lemma allows a new weight to repeat.

## From the lemma to arbitrary trees

For order eight the certificate gives a bijective labeling with seven distinct edge sums for every rooted tree shape. Every smaller nonempty tree is a subtree of an eight-vertex tree obtained by adding leaves. Restrict its labeling. All surviving vertex labels and all surviving edge sums are distinct, so their counts are zero or one. The empty tree, under conventions that include it, has all counts zero.

For a tree of order $n>8$, write $n=8m+r$ with $m\ge1$ and $1\le r\le8$. Successively remove $r$ leaves. The remaining core is a tree, and each component of the removed vertices has one attachment to it. Connectivity gives at least one attachment. A second would make a cycle with the paths in the component and the core. By strong induction, give the core a cordial labeling and let $d$ be its deficient edge weight. Apply the finite lemma with the actual boundary residues.

The new vertex counts are $m$ or $m+1$ by injectivity. The total edge count at $a$ is

$$
(m-1)+\mathbf 1_{a\ne d}+h(a) \ \in\ \{m,m+1\}.
$$

This proves cordiality and closes the induction. A second route for the universal conclusion uses only the order-eight base and order-eight forest rows, which meet Hovey's sufficient test as stated in Theorem 2.2 of the six-label paper. [Driscoll, Krop and Nguyen](https://www.ejgta.org/index.php/ejgta/article/download/231/pdf_33)

## Certificate and independent coverage check

A line of the decompressed archive contains a JSON array `[kind, parents, witnesses]`. Vertices are numbered from zero. A nonnegative parent is an earlier vertex. In an attachment case a negative parent `-1-c` prescribes an external endpoint of residue `c`. A base case has one root whose negative parent is ignored. Each witness lists the labels in vertex order.

The generator recursively builds unordered forests as sorted multisets of rooted trees, then searches for injective assignments. If all boundary and new labels are translated by $s$, each edge sum moves by $2s$. This permutes the set of deficit targets for every $s$, including for even modulus. The generator can therefore fix a boundary label to zero. Several stored rows can belong to the same translation orbit.

The independent verifier computes edge sums directly and checks the inequalities for every target. It represents a rooted tree by a matched pair of parentheses around its sorted child codes. This code is complete by induction on size, since the matching parentheses recover the multiset of children. The verifier independently checks the following two coverage claims.

1. Every rooted eight-vertex tree can be numbered in parent-before-child order. Enumerating all $7!=5040$ possible parent arrays and comparing their codes recovers all 115 rooted shapes.
2. Start with the empty forest. From every certified row of order $r-1$, attach a leaf to each possible internal parent or add a singleton at any of the eight boundary residues. Check that every resulting colored forest occurs among the translations of certified rows at order $r$. Every nonempty forest has a deletable leaf, and leaf insertion commutes with isomorphism and simultaneous translation. Induction therefore exhausts all colored forests.

| New vertices | Certificate rows | Colored forests covered before translation equivalence |
|---:|---:|---:|
| 1 | 1 | 8 |
| 2 | 9 | 44 |
| 3 | 46 | 200 |
| 4 | 212 | 814 |
| 5 | 839 | 3,072 |
| 6 | 3,184 | 10,996 |
| 7 | 11,308 | 37,832 |
| 8 | 38,843 | 126,301 |
| **Total** | **54,442** | **179,267** |

The archive contains 115 base labelings and 333,703 extension labelings. A labeling can serve several deficient weights. Each of the 179,267 colored forests has coverage for all eight targets.

## Reproduction

From the repository root, use Python 3 with its standard library to verify the supplied archive. Regeneration is optional.

```sh
python3 research/eight/verify.py
python3 research/eight/generate.py > /tmp/hovey-eight-regenerated.jsonl
gzip -dc research/eight/certificate.jsonl.gz | cmp - /tmp/hovey-eight-regenerated.jsonl
```

The SHA-256 of the **decompressed** JSON Lines is `4b1467798598a00cff52c6964ce67a266b5a18ae8f88fc91afc35650b5e6f5c8`.

## The complete eight-label theorem in Lean

Lean 4.36.0 proves `Cordial.Eight.allTrees` with no finite-test hypothesis. For any natural number $n$ and parent function $p$ with $p(i)\le i$, the conclusion supplies $n$ vertex labels and proves the two pairwise frequency inequalities modulo eight. The theorem `Cordial.Eight.trees` also proves the result directly for trees built from single vertices by joining two disjoint rooted trees at their roots. It counts each edge by its actual two endpoints. Every finite nonempty rooted tree has such a construction by cutting off a branch at its root and inducting on the two resulting trees. The order-zero case is included in the parent-array statement. [Tree representation and transfer proof](Tree.lean) [Final theorem and certificate checker](Certificate.lean) · [General induction](../Reduction.lean)

For the order-eight base, the Lean kernel directly recomputes all vertex and edge frequencies on all $1\cdot2\cdots7=5{,}040$ parent arrays. Each witness uses eight three-bit labels and a three-bit missing weight. Small batches reduce by kernel computation and a binary tree of range proofs covers every index. The base theorem prints only `propext` and `Quot.sound` as axioms. A separate compiled Lean search independently finds labels for the same 5,040 parent arrays. [Kernel checker and parent indexing](BaseCheck.lean) · [Packing the base witnesses](kernel_base.py) For attachments, the table builder rearranges the existing witnesses into absolute boundary colors. It also proposes an index map after adding each possible leaf. Lean checks 1,434,136 witness–deficit combinations and 773,848 proposed transitions. On each transition it checks that the index map is a permutation and preserves the actual parent or external boundary color. The proof composes these maps from the empty forest and transports both histograms. Thus a missing case anywhere in the reachable states would fail the closure test. [Base search](Base.lean) · [Reindexing and tally proofs](Representation.lean) · [Table builder](lean_tables.py)

Run the following from the repository root with Lean 4.36.0 and Python 3. All generated tables and module files go in a fresh temporary directory.

~~~sh
research/eight/verify_lean.sh
~~~

The script prints the axioms of the final theorem. Its two attachment evaluations use Lean's `native_decide`, which trusts compiled evaluation. The order-eight base uses direct kernel reduction. The table builder writes data, and Lean checks their mathematical content. As negative controls, changing one order-one witness label and the destination of the first leaf insertion caused the witness and closure evaluations to fail separately. The standard-library Python checker above remains an independent verification route.
