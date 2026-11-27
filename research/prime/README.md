# Rainbow extensions with at most four internal edges, for every prime

**Theorem.** Fix a prime $p$ and a forbidden vertex label $u\in\mathbb F_p$. Take any rooted forest on at most $p-1$ free vertices, with one additional edge from each root to an external vertex of prescribed label. If at most four edges join two free vertices, one can label the free vertices distinctly, avoiding $u$, so that **all** new edge weights are distinct. The external parent labels may be prescribed independently, including those of isolated free vertices.

The proof has two parts. An integer attached to each fixed forest shape controls all sufficiently large primes. For the 30 nonempty shapes needed here, computation determines these integers and resolves eight exceptional shape/prime pairs using linear forms. The number of singleton components and the primes in the theorem are unbounded.

Add singleton components to make exactly $r=p-1$ free vertices. Any witness then restricts to the original forest. Translate all labels to make $u=0$. When there are no internal edges, the signed count at zero boundary is $r!$, which is nonzero modulo $p$, and boundary independence applies. This also handles $p=2$. Henceforth $p$ is odd.

## Linear information from the signed count

Let $D=\mathbb F_p^\times$. For any labeling that uses all of $D$ and has distinct new weights, let $\theta$ be the permutation of $\mathbb F_p$ sending each vertex label $x_i$ to the weight $y_i$ on its parent edge and sending zero to the unique missing weight. Sum its sign over the valid labelings to get $N(b)$, where $b$ is the boundary vector. Define $M_i(b)$ by weighting each summand by $x_i$. All counts and moments in this section are taken in $\mathbb F_p$.

**Lemma.** $N(b)$ is constant and each $M_i(b)$ is a homogeneous linear form in $b$.

Put $V(z)=\prod_{i<j}(z_j-z_i)$ and $Q(z)=\prod_{a\in D}(z-a)$. Apply the grid sum
$$
L(f)=\sum_{x\in D^r}\frac{f(x)}{\prod_i Q'(x_i)}
$$
to $V(x)V(y)$ and to $x_i V(x)V(y)$. On valid labelings $V(y)/V(x)=\operatorname{sgn}(\theta)$, while $V(x)^2$ and the denominator are fixed nonzero constants. All other terms vanish. Thus the two evaluations give $N$ and $M_i$ up to the same fixed nonzero factor. The first evaluation has degree zero in the boundary by the signed-count lemma. [Vandermonde sign and grid-sum proof](../rainbow/prime-star.md#a-signed-count-independent-of-the-boundary-modulo-p)

The grid sum kills every monomial of total degree in $x$ below $r(r-1)$, since some exponent is below $r-1$. The moment integrand has total degree $r(r-1)+1$ in $x,b$, so the result has degree at most one in $b$. At zero boundary, multiplying all labels by any $\lambda\in D$ conjugates $\theta$ by the same dilation and multiplies the moment by $\lambda$. Taking $\lambda\ne1$ shows $M_i(0)=0$. This proves the lemma.

Consequently, if the matrix whose $j$-th column is $(M_i(e_j))_i$ has full column rank, each nonzero boundary vector admits a labeling. A witness at the zero vector then suffices to settle every boundary assignment for that forest.

## An integer controlling the primes for a fixed forest

Delete all singleton components and call the remaining forest $H$. Write $v$ for its order, $m$ for its internal edge count, and $s=p-1-v$ for the number of singleton positions. Work at zero boundary. The roots of $H$ and the singleton vertices have their own labels as weights. Thus $\theta$ fixes these letters, and permutes only the $m$ nonroot letters and the dummy letter 0. For an injective assignment $z$ of nonzero labels to $H$, all $s!$ ways to assign the unused labels to singleton positions give the same sign. Write $U_p(H)=N(0)/s!$ as an integer.

For a permutation $\pi$ of the $m+1$ possible moving positions, extend the coordinates by $z_0=0$, using the dummy as index 0. For each nonroot position $i$ impose
$$
z_{\pi(i)}-z_i-z_{\operatorname{parent}(i)}=0.
$$
With injectivity among all $v+1$ positions, these equations are exactly the condition that $\pi$ gives the required permutation. The image of the dummy is the remaining unused weight.

For a partition $P$ of the $v+1$ positions, identify all coordinates in each block and fix the dummy's block to zero. Give $P$ coefficient $\mu(P)=\prod_{A\in P}(-1)^{|A|-1}(|A|-1)!$. Summing the block-equality indicators with these coefficients gives the indicator of injectivity. Indeed, for a fixed assignment the sum is the sum of the signs of permutations preserving every equal-label class, grouped by their cycles. That signed sum is 1 for an injective assignment and zero whenever a class has size at least two.

If $P$ has $b+1$ blocks, write $A_{\pi,P}$ for the resulting integer matrix with $b$ columns after omitting the dummy block. Over the field, the homogeneous system has $p^{b-\operatorname{rank} A_{\pi,P}}$ solutions. Hence its contribution modulo $p$, before the permutation and partition signs, is exactly the indicator of full column rank. This also covers $b=0$.

Define the integer
$$
C(H)=\sum_{\pi,P}\operatorname{sgn}(\pi)\mu(P)
  \,{\bf1}\{\operatorname{rank}_{\mathbb Q} A_{\pi,P}=b\}.
$$

**Stability lemma.** If $p>\max(v,\lfloor5^{m/2}\rfloor)$, then $U_p(H)\equiv C(H)\pmod p$. Moreover $|C(H)|\le(m+1)!(v+1)!$.

Each matrix row starts with one positive and two negative unit coefficients. Upon identifying columns and deleting the dummy column, its Euclidean norm is at most $\sqrt5$. Hadamard's inequality bounds every nonzero $b\times b$ minor by $5^{b/2}\le5^{m/2}$. A full-rank rational matrix therefore stays full rank in the stated range, and deficient rational rank cannot increase. This proves the congruence. The absolute bound follows by counting the permutations $\pi$ and using $\sum_P|\mu(P)|=(v+1)!$, the latter identity again grouping permutations by their cycles.

In particular, for any fixed $H$ with $C(H)\ne0$, only primes below the cutoff or dividing this single integer can require a separate test. This statement makes no restriction on $m$.

## Finite verification for four edges

Every component of $H$ has at least one edge, so $v\le2m\le8$. Adding a dummy root adjacent to each component root represents each forest as a rooted tree. The checker grows rooted trees by all one-leaf insertions, deletes the dummy, and keeps exactly the eligible forests with no singleton component. Pruning a nonroot leaf proves the completeness of this enumeration. The counts for $m=1,2,3,4$ are respectively 1, 3, 7 and 19.

For each shape, the counter evaluates $U_q(H)$ at primes $q$ above the cutoff, using the permutation equations and enumerating distinct nonzero points after Gaussian elimination. It normalizes the first label to 1 at zero boundary and restores its $q-1$ dilations. The Chinese remainder theorem recovers the signed integer $C(H)$ once the product of the primes exceeds twice the absolute bound. Every reconstructed integer is nonzero. The checker tests each candidate prime $p>v$ below or at the cutoff or dividing $C(H)$. When $U_p$ is nonzero, $s!$ is invertible, so the scalar lemma proves existence for all boundary assignments.

At each of the eight remaining pairs, the counter returns an explicit zero-boundary witness. For a coordinate boundary $e_j$, move the marked root into the permutation's support along with the nonroots and dummy, and use the equation $z_{\pi(j)}-z_j=1$. If the marked root is a singleton, keep it as one extra active vertex. Unmarked singleton positions may again be filled arbitrarily. Each active moment gains the factor $s'!$ for $s'$ remaining singleton positions. If $s'>0$, each remaining position has moment $-(s'-1)!$ times the sum of the unpadded active moments, since all of $D$ has sum zero. Permuting singleton positions recovers the other singleton columns. The checker computes the rank over $\mathbb F_p$ and separately checks the returned zero-boundary witness by evaluating its labels and weights. In ascending order of $p$, the exceptional pairs have the following column ranks.

| Prime | Full ranks, one per exceptional shape |
| ---: | :--- |
| 11 | 6, 7 |
| 13 | 9 |
| 17 | 13 |
| 19 | 14, 14, 14 |
| 61 | 56 |

The linear lemma settles every nonzero boundary in these eight cases. This completes the computer-assisted proof.

From the repository root, run

~~~sh
c++ -O2 -std=c++17 -Wall -Wextra -pedantic research/prime/template_counts.cpp -o /tmp/hovey-template-counts
python3 -B -m research.prime.verify_templates /tmp/hovey-template-counts
~~~

The executable handles only the auxiliary primes below 64 used by this verification. The stability lemma is what extends the result to arbitrarily large primes. [Counter](template_counts.cpp) · [Verifier](verify_templates.py)

## A second proof at eleven labels

**Theorem.** At $p=11$ every rooted forest on at most ten free vertices has the rainbow extension, with arbitrary prescribed external parent labels and any forbidden vertex label. This removes the terminal-vertex bound from the [first eleven-label certificate](../rainbow/README.md).

A separate counter enumerates distinct nonzero vertex labels in parent-first order, discarding any repeated weight immediately. Its sign calculation keeps the inversion parities of the vertex tuple and the weight tuple. When a weight $d$ is missing, prepending $d$ to the weight tuple contributes $d$ additional inversions, and prepending zero to the vertex tuple contributes none. Multiplying the signs gives $\operatorname{sgn}(\theta)$. At zero boundary fix the first vertex label to 1 and multiply the scalar count by $p-1$ to restore its dilation orbit.

For 1,592 of the 1,842 forest shapes the scalar is nonzero. Of the remaining 250, the matrix of first moments has kernel dimension zero for 245 shapes, one for three shapes, and two for two shapes. For each of the 250 shapes, the checker verifies a direct witness at zero boundary. For each nonzero one-dimensional subspace of a kernel it also verifies one witness there. Multiplying all labels by a unit gives witnesses along the rest of that line. A two-dimensional kernel over $\mathbb F_{11}$ has 12 such lines. This requires $250+3+2\cdot12=277$ direct witnesses in total. The signed count or a first moment certifies every other boundary vector.

The stronger extension property directly implies the ordinary eleven-label tree theorem. For order eleven, choose a root, give it label zero and apply the extension to the other ten vertices. Restriction from an eleven-vertex supertree deals with smaller orders. For larger orders, take a connected core on $11m+1$ vertices when the remaining order is between one and ten. A cordial labeling on this smaller core has equal edge counts and one surplus vertex residue. Use that residue as forbidden and apply the extension. At orders $11m+1$, deleting a single leaf leaves one deficient edge weight, which the leaf can fill. This induction uses neither a contour traversal nor Hall's theorem.

~~~sh
c++ -O2 -std=c++17 -Wall -Wextra -pedantic research/prime/forest_moments.cpp -o /tmp/hovey-forest-moments
python3 -B -m research.prime.verify_forests 11 /tmp/hovey-forest-moments
~~~

The same check at 3, 5 and 7 finds the scalar nonzero on all 2, 9 and 48 forest shapes respectively. [Enumeration by label assignments](forest_moments.cpp) · [Kernel and witness verifier](verify_forests.py)

A direct witness stream independently covers **6,912,367** colored ten-vertex forests at eleven labels in **693,333** unit orbits. Each row uses all nonzero labels, with ten distinct actual edge weights. There are no failed rows. The orbit checker sums raw orbit cardinalities and compares them with an independent rooted-tree multiset recurrence. The stream SHA-256 is `060fc56ffc770f0f0dd403066450362ebe9978c2a3d3eba7a4302dd1ad335bc7`.

~~~sh
out=$(mktemp -d)
c++ -O3 -std=c++17 -shared -fPIC research/rainbow/search.cpp -o "$out/search.so"
python3 -B -m research.rainbow.surplus_spectrum 11 --native "$out/search.so" > "$out/eleven.jsonl"
python3 -B -m research.rainbow.check_surplus_spectrum 11 "$out/eleven.jsonl"
shasum -a 256 "$out/eleven.jsonl"
~~~
