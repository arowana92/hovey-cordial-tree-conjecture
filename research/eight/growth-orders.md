# One labeling cordial on every growing subtree

**Theorem.** At $k=8$ and $k=9$, choose any vertex of any nonempty finite tree and any label for it. There is a vertex ordering starting there, with each subsequent vertex adjacent to an earlier one, and a single labeling that is $k$-cordial on **every prefix**. Each prefix uses the actual edges of its induced tree.

At **every composite modulus** $k$, there is also an explicit tree and a prescribed connected ordering for which such a labeling is impossible. Moving one vertex earlier gives an ordering of the same tree with a cordial labeling on every prefix. The example therefore concerns the choice of growth order. [Construction at every composite modulus](#a-prescribed-order-at-every-composite-modulus)

## Adding a batch to a fixed core

Call an ordering of an attached forest admissible if every new parent appears before its children. Each component has one entering edge from a prescribed old vertex. Starting with a fixed cordial labeling at order one modulo $k$, a batch of at most $k-1$ vertices preserves cordiality throughout if its labels are distinct and avoid the old surplus and its entering weights are distinct. Any admissible order within such a batch works. For a full batch these conditions are also necessary by the final counts.

Starting at divisible order, the first new edge must supply the unique deficient weight $D$. If its parent label is $a$, its new child must receive $x=D-a$. The remaining vertices start at a one-surplus core with surplus $x$. These two steps characterize all successful admissible orders for a full batch of $k$.

For $k=8,9$ the complete one-surplus classifications give the following facts.

- Every batch of fewer than $k-1$ vertices works.
- At exactly $k-1$ every failure, after translating the surplus to zero, consists of one star with $c$ children and other singleton components. At eight, $c$ is 1, 3 or 5. At nine, $c$ is 2 or 5. In every failure some old parent differs from zero.
- In every forest of at least $k$ vertices one can choose an ancestor-closed set of $k-1$ outside those uncolored shapes. An ancestor-closed set contains the parent of each of its vertices whenever that parent is new. [Eight-label classification and ideal proof](surplus.md) · [Nine-label classification and ideal proof](../rainbow/surplus-nine.md)

Consequently a divisible-core batch of fewer than $k$ always works. In a full batch with at least three vertices having children, removing its first root leaves at least two such vertices. With just one such vertex, take it first and leave only singletons. With none, any first root works. With exactly two, take a singleton component first if one exists. If the forest is connected, removing the root gives all remaining roots a common parent of surplus label $x$, so the classified failures cannot occur. The only other possibility is two nontrivial stars centered at their component roots.

### Two stars at any modulus

Let the two star orders be $s,t$ with $s+t=k$, their old parent labels $a,b$, and $g=\gcd(s,k)=\gcd(t,k)$. There exists an admissible growth order from the divisible core exactly when
$$
                         D\equiv a+b\pmod g.
$$
Either choice of first center works under this condition. Take the first center at $a$, with forced label $x=D-a$. Translate $x$ to zero. The $s-1$ children of the first center become singleton components at zero, and the star of order $t$ has boundary $b-x$. The pinned-star theorem gives precisely $g\mid b-x$. The resulting rainbow labeling works in every admissible order after the first center. Interchanging the two stars gives the same condition. If a star is a singleton, the condition is automatic and the all-singleton remainder after choosing the other center works as well. [Pinned-star theorem and explicit construction](../rainbow/pinned-star.md)

Thus a full batch at eight can obstruct prefix growth only for star orders $(2,6)$ or $(4,4)$, and at nine only for $(3,6)$. The congruence decides exactly which prescribed inputs fail on those shapes.

## Choosing consecutive batches

For a block of size $k$ avoid the listed pairs of stars. For a block of size $k-1$ avoid the listed star with singleton shapes. A finite uncolored cut check proves three assertions at each modulus.

1. From $k+1$ vertices one can take an ancestor-closed block of $k$ of allowed shape.
2. With $2k-1$ vertices one can split into allowed blocks of $k-1$ and $k$ in that order, except for a single path of $k-1$ vertices whose last vertex parents both centers of a listed pair of stars.
3. With $2k$ vertices the corresponding assertion holds for two blocks of $k$. The exceptional path has $k$ vertices.

| $k$ | Free vertices | First block | Uncolored forests | First preorder cut needed replacement | Exceptional stems |
|---:|---:|---:|---:|---:|---:|
| 8 | 9 | 8 | 719 | 3 | 0 |
| 8 | 15 | 7 | 235,381 | 560 | 2 |
| 8 | 16 | 8 | 634,847 | 1,480 | 2 |
| 9 | 10 | 9 | 1,842 | 2 | 0 |
| 9 | 17 | 8 | 1,721,159 | 800 | 1 |
| 9 | 18 | 9 | 4,688,676 | 2,225 | 1 |

The checker adjoins one dummy root and enumerates depth sequences in strictly descending lexicographic order. It verifies valid depths and that each vertex's child subtrees have lexicographically sorted depth sequences. These tests make the codes injective on uncolored rooted forests. For completeness it independently computes the expected count at each order from $R(x)=x\prod_{j\ge1}(1-x^j)^{-R_j}$ for rooted trees. When the first cut fails, it branches on including or excluding each vertex, allowing inclusion only after its parent. Only the stated path-and-stars shapes exhaust the search without a structural cut. [Complete cut check](prefix_cuts.cpp)

The exceptional stems still permit growth. From a one-surplus core translate the surplus to zero and let $p$ be the stem's old parent. Give the $k-1$ path vertices the nonzero residues with distinct entering weights, ending at $z$ and missing weight $d$. Require $2z=d$ modulo 4 at eight, or modulo 3 at nine. This covers every relevant $g$ for the stars now attached at $z,z$. For each of the eight or nine choices of $p$, enumerating permutations supplies such a path and the checker recounts its actual sums. If the stem starts at divisible order, first fill $D$ on its first edge. The remaining $k-1$ stem vertices start from the one-surplus situation with normalized parent zero. [Path witness search](prefix_growth.py) · [Full-tree replay](check_prefix_growth.py)

Now take any attached forest, with its old cordial core fixed. At divisible order a size other than $k$ always admits prefix growth. For sizes above $k$, take a good first $k$ from any ancestor-closed $k+1$ vertices and induct, using the separate two-block check at size $2k$. At size $k$ the two-star criterion gives the exact exceptions. At one-surplus order the only exceptions are the previously classified $k-1$-vertex inputs. For larger sizes choose a good first $k-1$ and use the divisible result, treating size $2k-1$ by its two-block check. This proves the fixed-core version for **all** attachment sizes. Taking a single chosen vertex as core proves the opening theorem, since all its initial parents have its own surplus color.

## A prescribed order at every composite modulus

Let $p$ be the smallest prime factor of composite $k$, and put $g=k/p$. Begin with a star on $k$ vertices ordered from its center. Choose distinct vertices $v_1,\ldots,v_{p+1}$ in it, taking $v_1$ to be the center. There are $p+1$ subsequent blocks, each of size $k$. In block $i$, attach a star of order $g$ at $a_i$, then a star of order $k-g$ at $v_i$. Each center appears before its leaves. Take $a_1=v_1$ and let $a_{i+1}$ be the **second** center of block $i$. This gives a connected ordering on $k(p+2)$ vertices. In particular the example has 32 vertices at eight labels.

Suppose all its prefixes are cordial. Write $A,B$ for the old parent labels in a block, $X,Y$ for the two new center labels, and $D,D'$ for the edge deficits before and after it. The two-star congruence gives $D\equiv A+B\pmod g$, and the first edge forces $X=D-A$. Hence $X\equiv B\pmod g$. Let $S$ be the sum of all residues. At the end, the $k$ new vertices have used all residues once, and their entering edge weights sum to $S+D-D'$. Summing the same weights from their endpoints gives $S+A+B+(g-1)X+(k-g-1)Y$. Since $g\mid k$, this implies
$$
                            D'\equiv X+Y\pmod g .
$$
The next block requires $D'\equiv Y+f(v_{i+1})\pmod g$. Thus $f(v_i)\equiv X\equiv f(v_{i+1})\pmod g$ for every consecutive pair. All $p+1$ original vertices would share a class with only $p$ labels. The initial $k$ vertices have all distinct labels. This is impossible.

**An explicit successful reordering.** Move the second center of the first block to the beginning of that block, leaving all other relative positions in place. Give $v_1$ label zero and $v_2,\ldots,v_{p+1}$ the $p$ residues congruent to 1 modulo $g$. Complete the initial star by the unused labels. Its deficit is zero. Give the moved center $Y=0$ and the other center $X=1$. Give the latter's $g-1$ children $-1,\ldots,-(g-1)$ and the former's children the remaining residues other than 0 and 1. After the moved center, the $k-1$ weights are distinct and miss $1-g$. Thus the next block's parents satisfy the two-star congruence. In each subsequent block it holds again, since $D'\equiv X+Y\equiv 1+Y\pmod g$ and every later $v_i$ has label 1 modulo $g$. The pinned-star construction supplies all labels. This proves ordinary $k$-cordiality for each example at its own modulus.

At $k=2,3,5,7,11,13$, an earlier all-offset theorem gives a labeling for every prescribed connected ordering. The results here settle the opposite prescribed-order assertion at every composite. [Prime prefix construction](../near-matching.md#every-connected-prefix)

## Reproduction

Run from the repository root.

~~~sh
set -eu
out=$(mktemp -d)
c++ -O3 -std=c++17 research/eight/prefix_cuts.cpp -o "$out/cuts"
"$out/cuts"
python3 -B -m research.eight.check_prefix_growth
~~~

The Python replay checks the old and new histograms at every prefix. It covers all ordered old parent and deficit choices for pairs of stars at eight and nine, with 1,126 impossible inputs and 4,362 successful complete growth orders including stems and larger trees. A separate enumeration of center labels and leaf subsets checks the congruences through modulus 13. It also exhausts the possible initial permutations and transitions for the prescribed orders at four and six, and checks the positive reordering on the explicit examples at every composite through 100.
