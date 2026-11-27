# The exact uniform-increment criterion for two branching neighbors at a prime

Let a joint have two neighbors with respectively $a,b\ge1$ leaf children and $\ell\ge0$ direct leaves. Let the number of free vertices be the prime $p=a+b+\ell+2$. A **uniform increment** uses each residue once on the free vertices and once on the new edges, with the joint's label prescribed.

**Theorem.** Put $t=a+b$ and $h=\ell+2=p-t$. A uniform increment exists exactly when $t-h$ cannot be written as a nonnegative integer combination of $a,b,h$. This includes every negative $t-h$. A shortest-path construction produces a labeling whenever one exists. In the excluded cases the same rooted tree still permits a cordial extension over every deficient core weight. [Cordial extension without a uniform increment](two-branch-joint.md)

In particular, $\ell\ge (p-3)/2$ suffices for all choices of the two positive populations. This threshold is sharp at every prime $p=2s+1\ge5$. With $a=1,b=s,\ell=s-2$ the target is $1$, giving an obstruction despite all those direct leaves.

## Displacements of the free labels

Translate the joint to zero. Call its two center labels $x,y$. From the free vertex labels to their child-edge weights, the $a$ children at $x$ shift by $x$, and the $b$ children at $y$ shift by $y$. Exactly $h$ positions stay fixed, including both centers. For a permutation of the weights the sum of all shifts is zero, so $ax+by=0$. The two center labels are distinct. After scaling by $(x-y)^{-1}$, they are $x=j+1,y=j$, where $j$ is the representative of $-a/t$ in $[1,p-2]$. Both are nonzero. Put $q=(jh-a)/p$, an integer since $h=p-t$.

In these normalized coordinates let $e_i$ indicate a fixed position and $s_i$ a position assigned to one of the $a$ children of the first center. Indices are cyclic. At output $i+j$ the three possible preimages are the fixed position $i+j$, the first-center child $i-1$, and the second-center child $i$. Counting these preimages gives
$$
s_i-s_{i-1}=e_{i+j}-e_i .
$$
Choose prefix counts $H_i$ on the integers with $H_i-H_{i-1}=e_i$ and $H_{i+p}=H_i+h$. The recurrence and $\sum s_i=a$ give $s_i=H_{i+j}-H_i-q$. Thus the complete constraints are
$$
0\le H_i-H_{i-1}\le1,\qquad H_{i+j}-H_i\ge q,\qquad
H_{i+j}-H_{i-1}\le q+1.
$$
The last inequality is $e_i+s_i\le1$. Conversely, integer prefix counts satisfying these inequalities and the period give $a$ first-center children, $b$ second-center children and $h$ fixed positions. The preimage equation proves that the resulting weights form a permutation. The two centers must additionally be fixed, i.e. $H_{j+1}-H_{j-1}=2$.

## Three ordinary integer generators

Set $i_0=j-1$ and $X_i=pH_i-h(i-i_0)$. The $X_i$ are periodic. In terms of these potentials the inequalities bound the increase along steps $-1,-j,j+1$ by $h,a,b$, respectively. The remaining bound for step $+1$ is $t$ and follows by taking steps $-j,j+1$ in succession. Multiply cyclic indices by $t$. It is a unit, and these three steps become, respectively, $h,a,b$ modulo $p$. Their costs are exactly their **positive integer** representatives $h,a,b$.

Fixing both centers requires $X_{i_0+2}-X_{i_0}=2t$. If $t-h=2t-p$ is a nonnegative sum of the three costs, following the corresponding steps reaches $i_0+2$ at cost strictly below $2t$, which is impossible. Every such representation is a checkable obstruction certificate.

Conversely let $D(v)$ be the smallest nonnegative sum of $a,b,h$ congruent to $v\pmod p$. All residues occur since $a$ is a unit. The candidate $2a+2b=2t$ reaches $2t\bmod p$, and $2t<2p$. If $2t-p$ is absent, $D(2t\bmod p)=2t$. Now take
$$
X_i=D\big(t(i-i_0)\bmod p\big),\qquad
H_i=\big(X_i+h(i-i_0)\big)/p.
$$
These $H_i$ are integers with the required period. Appending one generator to a shortest sum verifies every step inequality, and the distance at $2t$ fixes both centers. The indicators above now construct all vertex labels. Adding the prescribed root label to every residue restores the original joint. The distances are obtained by Dijkstra's algorithm on $p$ vertices with three directed edges out of each.

A related enumeration by Loehr, Warrington and Wilf uses determinants for cyclic permutations with three possible displacements. Our two center positions must additionally stay fixed. The prefix argument gives the numerical semigroup condition with these two constraints directly. [Loehr, Warrington and Wilf, *The combinatorics of a three-line circulant determinant*](https://arxiv.org/abs/math/0312350)

## Verification

For all positive splits at primes through 131, a verifier recomputed the labels and actual endpoint sums in 57,026 uniform constructions. Ordinary integer knapsack independently confirmed all 16,440 exclusions. For 49 ordered splits at primes through 11 it tested existence directly by trying center labels and disjoint child label sets, independently of the arithmetic condition. [Constructor](prime_neutral.py) · [Independent checks](check_prime_neutral.py)

~~~sh
python3 -B -m research.census.check_prime_neutral
~~~
