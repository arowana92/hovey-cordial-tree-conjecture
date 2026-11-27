# Prime moduli and a prescribed joint

**Full-block lemma.** Let $p$ be prime. Start with a $p$-cordial labeling of a core of order divisible by $p$. Attach a tree $F$ with $p$ edges at any specified shared vertex $r$. If the trees on $p$ vertices used below have bijective labelings with distinct edge sums, the original labeling extends. Only one such auxiliary labeling is needed for a given input.

Write $c$ for the label at $r$ and $d$ for the deficient core weight. The $p$ free labels must permute the field. It suffices that the new weights are a permutation, or a permutation with one weight replaced by $d$.

- If $d=2c$, contract any edge $rv$. Give the contracted tree a bijective rainbow labeling and translate so the merged vertex has label $c$. Split it into two vertices both labeled $c$. All weights from the contraction are retained, and the restored edge weighs $d$.
- If $d\ne 2c$ and $F$ is a star centered at $r$, every permutation on its leaves gives uniform increments. Otherwise a leaf $w$ farthest from $r$ has a parent $v\ne r$. Give $F-w$ a bijective rainbow labeling $f$. In $\mathbb F_p$, choose the nonzero scalar $u=(d-2c)/(f(v)-f(r))$. Relabel each old vertex $x$ by $c+u(f(x)-f(r))$ and give $w$ the label $c$. The resulting free labels are a permutation, the old edge sums are distinct, and the edge $vw$ weighs $d$.

The two cases explicitly allow every choice of $c,d$. For composite $k$ the second argument still works whenever the two differences have the same gcd with $k$. A unit relates any two elements of the cyclic group having the same additive order.

**Short-block lemma.** The same implication holds for $1\le t<p$ edges provided the auxiliary bases for the following padding are available. Choose a leaf $w\ne r$, and add $p-t$ twins of $w$ at its parent. Apply the full-block lemma. Some new edge has weight $d$. If only dummy edges have this weight, swap one such leaf's label with $w$'s. Removing the dummy leaves preserves a hit on $d$, leaves its multiplicity at most two and gives at most one occurrence of every other weight. The free labels are still distinct. A forest with all its attachment edges meeting vertices of the same prescribed color also fits this lemma. Identify those external vertices for purposes of constructing the labels, and then use the resulting labels at the actual edges.

Thus an ordinary order-$p$ theorem gives a prescribed-core extension over **every** tree on at most $p$ new edges at a single joint. The same holds for a class closed under the leaf padding, leaf deletion and contraction used in the proof. In particular the unrestricted local statement holds at each prime through 23. The integer census supplies the base independently there. The full tree conjecture at arbitrary primes still has forests with *different* incoming colors. [Order census](README.md) · [Ordered-cut forest conditions](../rainbow/ordered-cut.md)

## Every rooted caterpillar, of arbitrary size, at every prime

Caterpillars stay caterpillars under the three operations above. Their staircase labeling gives a bijection with distinct edge sums at order $p$. It remains to handle $t>p$. A leaf joint is also covered by the single-edge bridge rule at arbitrary moduli. [Staircase labeling](caterpillar-leaf.md#a-labeling-at-every-multiple-of-the-modulus) · [Bridge translation](two-branch-joint.md#other-joints-and-arbitrary-size) · [Hovey's caterpillar theorem](https://doi.org/10.1016/0012-365X(91)90254-Y)

Here is a cut procedure that includes leaf joints. Use the nonleaf path as spine. Mark the joint's spine position, or its parent on the spine if the joint itself is a leaf. Let $L,R$ count all edges into the arms to its left and right, and let $h$ count direct leaves at the marked position other than the joint. Then $L+R+h=t-e$, where $e$ is one for a leaf joint and zero otherwise. Starting from the left end one can remove any number through $L+h$ as a connected tail that meets the remainder in one vertex and leaves the original joint in the remainder. At each position take direct leaves before the onward spine edge, and stop as soon as the count is attained. The right side gives every count through $R+h$. The larger capacity is at least $\lceil(t-1)/2\rceil$.

For $t>p$, remove $t\bmod p$ edges if this is positive, or $p$ edges if $p\mid t$. In the former case the remainder $b$ satisfies $t\ge p+b\ge 2b+1$, and in the latter $t\ge 2p$. The capacity always suffices. Continue until $p$ edges remain. Apply the full-block lemma to the remainder and reattach the removed tails in reverse order. All but possibly the very last extension add a multiple of $p$ vertices, so the hypothesis on the labeled core is available each time. This proves the result for every joint, every caterpillar size and every prime.

## Diameter four and five

**Theorem.** At every prime $p$, a cordial core of order divisible by $p$ extends across any rooted tree of diameter at most four, at arbitrary size. The same holds for diameter at most five at every prime for which the order-$p$ diameter-five base is known, including all primes through 31.

Both diameter bounds survive cloning a leaf, deleting a leaf and contracting an edge. The short and full blocks therefore follow from the corresponding ordinary order-$p$ results. In diameter four the repository's integer theorem supplies all primes. [Diameter-four base](../hub/all-radius-two.md) · [Diameter-five bases through order 36](../hub/diameter-five.md)

For larger sizes first handle a leaf joint by the bridge rule. The free tree is again of the stated diameter and has an ordinary cordial labeling by the all-orders results at the same modulus. For a nonleaf joint, write $N$ for the number of nonleaf vertices. If $N\le p+1$, choose a connected $p$-edge prefix containing all of them. Apply the full-block lemma. Every remaining vertex is a leaf at an already labeled vertex. At any core of order divisible by $p$, any number of such leaves can be attached. Use one to fill the deficient weight, then attach up to $p-1$ leaves with distinct weights and distinct labels avoiding the first leaf's label, by Hall's partial permutation lemma. A full batch of $p$ new vertices restores the order condition. [Hall extension](../counterexample-bound.md#removing-leaves)

If $N>p+1$, choose the middle vertex or middle edge of a longest path as center. At diameter at most five there are at most two center vertices and every other nonleaf is adjacent to a center. Each such nonleaf has a leaf child. Choose $p+1$ nonleaf vertices forming a connected prefix that contains the joint and the centers. The prefix has at least $p-1$ off-center vertices, each supplying an available leaf. Every omitted nonleaf is also available, so at least $p$ vertices can be added with already labeled parents. Apply the full-block lemma to the prefix. Process batches of $p$ available vertices as above, taking remaining nonleaf vertices first. Whenever a batch consists entirely of nonleaf vertices, it makes at least $p$ new leaves available. Once a batch contains the last nonleaf, all remaining leaves can be added. This proves the theorem.

In this last case the prefix is itself a double star or a star. Thus the [full-block result for at most three nonleaf vertices](two-branch-joint.md) also works at composite $k$ when $N>k+1$ and the joint is nonleaf. For a leaf joint the ordinary diameter-five theorem already gives the bridge rule in that same range.

## Verification

A base solver written independently of the attachment algorithm enumerates permutations and checks the actual edge sums on the contracted or pruned tree. The checker tested every rooted shape with $1$ through $p$ free vertices and every prescribed pair $c,d$ at $p=2,3,5,7$, totaling 10,726 extensions. It separately checked 1,899 arbitrary-order caterpillar extensions, including moduli 29 and 103, against the actual original edges. The diameter-five reduction above additionally uses the already verified ordinary bases and Hall's theorem. [Constructor](prime_joint.py) · [Direct checker](check_prime_joint.py)

~~~sh
python3 -B -m research.census.check_prime_joint
~~~
