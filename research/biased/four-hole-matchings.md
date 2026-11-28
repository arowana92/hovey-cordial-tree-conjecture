# Four omitted residues in a matching at 27 labels

**Theorem (computer-assisted).** Let each of three sets in $\mathbb Z_{27}$ have size 23. They can be partitioned across the three sets into zero-sum triples, using every entry once, if and only if the sums of the three sets add to zero. The same holds at every size from 23 to 27. This gives the four-hole case of the finite matching question in Problem 7.4 of Müyesser and Pokrovskiy. [*A random Hall–Paige conjecture*, Section 7.4](https://doi.org/10.1007/s00222-025-01328-x)

**Tree consequence.** Every 52-vertex tree with 23 leaves at 23 different parents is 27-cordial. Any 52-vertex counterexample with 23 leaves must have between **eight and twenty-two** different leaf parents. The remaining order-52 cases stay open. [Lower bound on parent count](seven-shift-lists-27.md) · [Order-52 results](../census/order-fifty-two.md)

## From sets to prescribed repeated labels

Work in an abelian group of order $k$. Suppose the sum condition suffices for three sets of size $b>k/2$. Take three multisets of a common length $m$ and put
$$
E=\sum_{i=1}^3 (m-|\operatorname{supp} M_i|).
$$
If $m-E\ge b$, the sum condition is necessary and sufficient for a partition into zero-sum triples. While some shore has a repeated value, select one copy. The other two supports have more than $k/2$ values each, so a translate of the negative of one must meet the other in a compatible pair. Remove the triple. The length drops by one and $E$ drops by at least one. Once the shores are sets, use the same intersection argument to remove any triple until their size is $b$. The total sum stays zero. This proves the assertion and the larger-size part of the finite theorem.

At 27 the argument allows $b=23$. For comparison, for sufficiently large cyclic groups there is an absolute $c>0$ allowing $b\le (1-c)k$, with $b>k/2$. This follows from the linear lower bound for the cyclic group stated after Problem 7.4 of Müyesser and Pokrovskiy and the same deletion argument. [Primary result](https://doi.org/10.1007/s00222-025-01328-x)

## Leaves on a fixed cordial core

Take a core of order $ak+h$, where $1\le h<k$. Let $U$ be its $h$ high vertex residues and $W$ its $h-1$ high edge residues, meaning the bins of size $a+1$. Attach $r\le k-h$ leaves with prescribed effective parent shifts $S$, including any edge offsets. Write $e=r-|\operatorname{supp}S|$. Suppose $h+e\le k-b$ for a valid matching threshold $b>k/2$ above.

At $r=k-h$ an extension exists exactly when
$$
z=\sum U-\sum W-\sum S\quad\text{satisfies}\quad z\notin W.
$$
All low vertex labels must be used once. The new weights must use all residues except $W$ and one further residue $z$. Subtracting the sums forces the displayed value. Conversely, use the three shores $G\setminus U$, the shift multiset $S$, and $-(G\setminus(W\cup\{z\}))$. They have zero total and $m-E=k-h-e\ge b$. Each triple assigns its first entry to a leaf with the indicated shift.

At $r<k-h$ every such input extends. Pad the shifts to size $k-h$ with fresh, pairwise distinct values. On the last dummy, at most $h-1$ choices put $z$ in $W$, while at least $h+1$ unused choices remain. Apply the full-size result and discard the dummies. Each real vertex and weight then increments a distinct low bin. This works on cores of arbitrary order, with independently prescribed offsets on the entering edges.

For the order-52 consequence, delete the 23 leaves. Every 29-vertex tree is 27-cordial. On any such labeled core each of two residues occurs twice and all others once. Among 23 *physically distinct* parent vertices the shifts therefore have excess $e\le2$. Here $h=2$, $r=23<25$ and $h+e\le4$. The same argument gives the exact fixed-core test for 25 leaves at distinct vertices of a 29-vertex core. [Known orders at 27](../census/order-fifty-one.md)

## Checking the finite matching theorem

Regard the three sets as separate copies, so they may overlap. Translating each by minus its sum divided by 23 centers it at sum zero. These translations add to zero. The inverse of 23 exists modulo 27. Each centered complement consists of four residues summing to zero, and every translation orbit of four-element sets has 27 members. There are $\binom{27}{4}/27=650$ centered complements. Multiplication of all three shores by the same unit and permutation of the shores preserve the problem.

The generator tries bijections on the full group of the form $x=as+t$ indexed by the shift $s$, with $a$ and $a+1$ units. It keeps compatible triples, optionally frees further positions, and completes the unused entries by exact search. Only explicit complete matchings are accepted. The separate verifier builds its own four-element catalog, checks the canonical representative, and counts every used input and third entry for the 23 middle entries. For an independent count, let a unit permute the catalog with $f_i$ cycles of length $i$. It fixes exactly $\binom{f_1+2}{3}+f_1f_2+f_3$ unordered triples with repetition. Burnside's lemma gives **2,560,588** required records. They represent **200,201,625,000** ordered triples of uncentered sets with the prescribed total sum.

A separate replay inverts all three symmetry operations and rebuilds the edges of 1,072 whole trees. These include 120 with exactly 23 leaves at distinct parents at order 52. It also checks 270 multiset instances and eight forced collisions for fixed labelings. These collisions obstruct those fixed extensions. The finite theorem and the counting argument justify its use on every allowed tree.

The full uncompressed stream has SHA-256 `7dfdd0175009bb00a42950db3baed2bf50f0408d7dea45cde84fb2d1c7b75a5a`. Run from the repository root in Bash.

~~~bash
set -euo pipefail
out=$(mktemp -d)
c++ -std=c++17 -O3 research/biased/four_hole_matchings.cpp -o "$out/generate"
"$out/generate" | python3 -B -m research.biased.check_four_hole_matchings
python3 -B -m research.biased.check_four_hole_trees "$out/generate"
~~~
