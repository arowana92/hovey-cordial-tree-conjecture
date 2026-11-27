# Which edge of a square can be opened?

Fix $k\ge4$. Attach $k-4$ leaves to one marked corner of a square. Its vertices cannot be labeled bijectively modulo $k$ with all edge sums distinct. Nevertheless, opening some of its edges gives a uniform insertion into any previously labeled tree.

Delete the old tree edge with endpoint labels $a,b$, cut one square edge, and join its two ends to those old endpoints. A uniform insertion increases every vertex and edge count by one. Write $h=a-b$ in $\mathbb Z_k$.

| Square edge that is cut | Exact condition for a uniform insertion |
|---|---|
| An edge away from the marked corner | Every $h$ works for $k\ge6$. No $h$ works for $k=4,5$. |
| An edge incident to the marked corner | $k$ is even, $h\notin\{0,k/2\}$ and $2h\ne k/2$. |

In particular, at every modulus $k\ge6$ one can replace an arbitrary labeled edge by a path on four new internal vertices with $k-4$ pendant leaves at either of the **two middle** new vertices. This works at every core order. At an **end** new vertex the second line governs the same operation. The negative cases concern uniform increments with the old labels prescribed.

## Four labels determine the answer

Translate all labels so the marked corner is zero. In cyclic order let the corner labels be $0,x,y,z$, all distinct. Give the leaves every remaining residue. Each pendant edge then weighs exactly its leaf label, so those contributions cancel. The closed square would require $\{x+y,y+z\}=\{0,y\}$ as multisets after canceling $x,z$. Either possibility forces $x=0$ or $z=0$. Hence the closed graph always fails.

For either cut, write $A,B$ for the old labels after the translation, so $A-B=h$. The target multiset on the five new nonpendant edges is $\{0,x,y,z,A+B\}$. Summing their weights by endpoint incidence gives $2(x+y+z)+A+B$, forcing
$$
x+y+z=0.
$$
Conversely it suffices to construct normalized corner and endpoint labels with difference $h$ and the required multiset. Translating back matches the original endpoints and permutes both histograms.

**Cut at the marked corner.** Cut $0x$, joining $A$ to zero and $B$ to $x$. After canceling the edge of weight $z$, the equation is
$$
\{-z,-x,A,x+B\}=\{0,x,y,A+B\}.
$$
The value $-z$ equals none of $0,x,y$, since all four labels are distinct and $x+y+z=0$. Thus $A+B=-z$. Now $-x$ must equal $x$ since it is neither zero nor $y$. This forces even $k$ and $x=k/2$. The two remaining assignments are $(A,B)=(0,-z)$ and $(A,B)=(y,x)$. They give $h=z$ and $h=-z$, respectively. The four corner labels $0,x,x-z,z$ are distinct exactly when $z\notin\{0,k/2\}$ and $2z\ne k/2$. These conditions are invariant under negation. Taking $z=h$ in the first assignment proves sufficiency.

**Cut away from the marked corner.** Cut $xy$, joining $A$ to $x$ and $B$ to $y$. Cancel $x,z$ from the two multisets to obtain
$$
\{-x,A+x,B+y\}=\{0,y,A+B\}.
$$
Again $-x$ is neither zero nor $y$, forcing $A+B=-x$. The surviving choices are $(A,B)=(-x,0)$ and $(A,B)=(y-x,-y)$. If $h=0$ and $k\ge6$, use the second choice with $x=2,y=1,z=-3$. If $h\ne0$, use the first choice with $x=-h$ and $z=-x-y$. To make the labels distinct, avoid $y\in\{0,x,-x,-2x\}$ and $2y=-x$. At most six residues are excluded, so $k\ge7$ suffices. At six every nonzero $x$ belongs to one of the zero-sum triples $\{1,2,3\}$ and $\{3,4,5\}$. At four or five there is no triple of distinct nonzero residues summing to zero. This proves the classification.

## A fixed-matrix decision for other marked graphs

Let $H$ be any fixed connected simple unicyclic graph on $c$ vertices with one marked vertex. At any $k\ge c$ add $k-c$ leaves to the mark. Whether a chosen cycle edge can be opened for prescribed $h$ can be decided from a finite list of integer matrices **depending only on $H$ and the chosen edge**. This also gives a test for the closed graph.

Normalize the mark to zero. The other original labels must be distinct and nonzero. The leaves receive the unused residues and cancel exactly as above. For an opening, the $c+1$ remaining actual sums must be a permutation, with multiplicities, of the $c$ vertex labels and $A+B$. Enumerate all bijections of positions between the two lists. For each such bijection impose its homogeneous linear equations on the unmarked labels and the two old labels. Distinctness can be enforced by summing over partitions of the $c$ original vertices. Identify the labels in each block, pin the marked block to zero, and weight the count by $\prod_D(-1)^{|D|-1}(|D|-1)!$. This weight is the partition form of inclusion–exclusion. For an assignment having an equality class of size $b$, summing these weights over partitions within the class is the sum of permutation signs on $b$ letters, obtained by grouping permutations by cycle supports. It is one for $b=1$ and zero for $b>1$.

Write $M$ for a resulting equation matrix and $M'$ for $M$ with the row $A-B$ adjoined. If a unimodular diagonalization has nonzero entries $d_1,\ldots,d_r$ and the matrix has $v$ columns, put
$$
K(M,k)=k^{v-r}\prod_{i=1}^r\gcd(k,d_i).
$$
This is the kernel size modulo $k$, since unimodular operations are invertible modulo every $k$. The image of $A-B$ on that kernel has size $D=K(M,k)/K(M',k)$ and is the unique subgroup of that order in $\mathbb Z_k$. The count for prescribed $h$ is $K(M',k)$ if the additive order of $h$ divides $D$, and zero otherwise. For a closed graph omit the two old labels, the extra target and the difference row, and use $K(M,k)$ directly. The signed partition sum followed by the sum over position bijections counts compatible distinct-core assignments with their weight matchings. Repeated weights can give one labeling several matchings. Positivity decides existence.

## Independent checks

The [direct checker](check_square_ports.cpp) fixes the first old label at zero and exhausts all four distinct corner labels and second endpoint labels through modulus 16. It evaluates the edges on the actual replacement, including every leaf and the deleted old weight. Across the two ports it made 4,158,336 exhaustive tests. It separately checked the constructive formulas on all 12,209 feasible choices through modulus 128. The [integer-matrix implementation](square_ports.py) reproduced all 16,500 port decisions through 128 and the closed-square result. On a triangle with an extra leaf it also agreed with literal enumeration on 123 exact multiplicities. The proofs above apply to arbitrary moduli.

~~~sh
out=$(mktemp -d)
c++ -O3 -std=c++17 research/census/check_square_ports.cpp -o "$out/check"
"$out/check"
python3 -B -m research.census.square_ports
~~~
