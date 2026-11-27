# Which repeated vertices can the degree sum rule out?

A tree with $k$ edges is $k$-cordial exactly when its edges use every residue and its vertices use every residue with one repeated. Fix two vertices $r,v$ as the repeated pair, and identify them to form a connected multigraph $H$ with $k$ vertices and $k$ edges. A loop counts twice in a degree. Translating allows the repeated label to be zero. Write $f$ for a bijection of $V(H)$ onto $\mathbb Z_k$.

**Theorem.** For $k\ge5$, the necessary degree equation
$$
\sum_{u\in H}(\deg_H(u)-1)f(u)=0\pmod k
$$
excludes the pair exactly in the following cases.

1. All degrees are two and $k$ is even.
2. The degrees are one, three and otherwise two, and $k$ is odd.
3. There are precisely two nonleaves, and the degree of one of them minus one is coprime to $k$.

To derive the equation, subtract the sum of all vertex labels in $H$ from the sum of all edge weights. Both lists should permute the group. The coefficients sum to $k$, so any bijection solving the equation can be translated to prescribe the label at the merged vertex.

For coefficients $a_i=\deg_H(i)-1$, put $S=k(k-1)/2$ and $g=\gcd(k,a_i-a_1:i\le k)$. The permutation sums form the coset $Sa_1+g\mathbb Z_k$, with one exceptional pattern. If there are $k-2$ entries $c$ and two entries $c+b,c-b$ modulo $k$ for a unit $b$, every residue except $Sc$ occurs. These are equations (4.2) and (4.3) of Grynkiewicz, Philipp and Ponomarenko. [Primary proof, §4](https://arxiv.org/pdf/1102.5351) · [Nagy's zero-target formulation](https://arxiv.org/pdf/1211.6875)

If $H$ has no leaves, the average degree is two and every coefficient equals one. The only sum is $S$. If one coefficient is $k$, all others vanish and the equation holds. In all other cases with a leaf, the coefficients include zero and are ordinary integers in $[0,k-1]$. The coset always contains zero. In the exceptional pattern take $c$ in this interval. The bound $(k-2)c\le k$ forces $c\le1$. At zero the other entries are positive, sum to $k$, and must be units. At one the other entries are zero and two, and the missing residue is zero exactly at odd $k$. This proves the list.

## When the repeated partner is free

There is a second necessary test. Vertices at distance two cannot share a label, since their edges to the common neighbor then coincide in weight. These are exactly the pairs whose identification creates parallel edges.

**Corollary.** Fix the root $r$ and allow the repeated partner to vary. Every partner fails the degree equation or the distance test exactly when the hub $r$ has two neighbors with $a,b\ge1$ leaf children, no direct leaves, and both $a$ and $b$ are coprime to $k=a+b+2$.

Let $N$ and $L$ be the numbers of nonleaves and leaves in the original tree.

* If $r$ is internal and $N\ge4$, merge it with an adjacent nonleaf. There are still at least three nonleaves and two leaves. A star works by merging its center and a leaf. For $N=2$, the two nonleaves may be merged, leaving only one.
* If $N=3$, the nonleaves form a path of length two. An internal root with a leaf neighbor may be merged with that leaf. This leaves three nonleaves and at least two leaves, since a path with three nonleaves has only four edges. The only other internal root is the middle of that three-vertex path with no direct leaves. Every partner except its two neighbors is at distance two. Merging one of the neighbors gives two nonleaves. The coefficient of the other is its child count. The exact condition follows from case 3.
* If $r$ is a leaf, a star is immediate. With at least three leaves and three nonleaves, merge $r$ with its parent. With two nonleaves, merge $r$ with a leaf on the opposite side. This leaves three nonleaves and $k-3\ge2$ leaves. On a path, merge the two ends when $k$ is odd and merge the root with its neighbor when $k$ is even. Each choice passes both tests.

In the excluded two-center family the earlier coset construction proves that the gcd test also characterizes actual uniform extensions. Outside it, the two tests may admit a partner even though every labeling fails. A path of three edges on one side of the root gives an infinite family with that property. An unrestricted tree can always take a leaf as its nominated repeated vertex and pass these two necessary tests. [Two-center construction](two-branch-joint.md) · [Exact path-and-star obstruction](leaf-kernel.md#three-edges-on-one-side-of-the-joint)

A subset dynamic program enumerates the attainable degree sums directly by assigning distinct residues. Separately the checker constructs every quotient edge, including loops, and tests for duplicated edges. Through $k=12$ it compared 230,630 specified pairs on 20,282 rooted shapes, found 887 degree exclusions, and found 12 rooted shapes on which the two tests rule out every partner. [Independent computation](check_repeated_moment.py)

~~~sh
python3 -B -m research.census.check_repeated_moment
~~~
