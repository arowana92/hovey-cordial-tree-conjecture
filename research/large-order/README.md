# Every sufficiently large tree at every fixed modulus

**Theorem.** Let $k\ge2$. Every tree on $n\ge 2^{26} k^8\log(2k)$ vertices is $k$-cordial, where the logarithm is natural. The degree and shape of the tree are unrestricted. Consequently, at each fixed modulus only finitely many ordinary trees can be counterexamples.

This is an unconditional existence result at large orders. The [smaller bound for a *minimum* counterexample](../counterexample-bound.md) serves a different purpose: checking small orders suffices to prove a fixed modulus. The large-order theorem here requires no checks at small orders. At $n=k$ the original problem still asks for a bijective labeling with distinct sums. [Hovey, *A-cordial graphs*](https://doi.org/10.1016/0012-365X(91)90254-Y)

Distributing the corrections across translated groups of sites improves the bound to $(2^{34}+4)k^2$. [Quadratic theorem and checks](quadratic.md)

## Correcting two histograms by local changes

Index every vector cyclically by $0,\ldots,k-1$. Write $(\tau h)_j=h_{j-1}$ and $s(h)=\sum_j j h_j\pmod k$. Suppose some pairwise nonadjacent vertices have degree $d\in\{1,2\}$ and come in two types. Type A has all its neighbors labeled zero. Type B has one neighbor labeled 1 and the other $d-1$ labeled zero. Changing a type A vertex from $x$ to $y$ changes the vertex vector by $v=e_y-e_x$ and the edge vector by $dv$. A type B change gives $v$ and $(d-1)v+\tau v$. Nonadjacency lets all changes add without interaction, even when some neighbors coincide.

Let $a,b$ be the desired total changes in the vertex and edge vectors. Both have coordinate sum zero. Assume $s(b-da)=0$ and all prefixes of $a$ and $b$ have absolute sum at most $P$. Put $z=b-da$, $Z_j=\sum_{i=0}^j z_i$, and
$$
h_j=\frac1k\sum_{i=0}^{k-1} Z_i-Z_j.
$$
The numerator is $\sum_i(k-i)z_i$, divisible by $k$ by the moment condition. Now $\sum h_j=0$ and $(\tau-I)h=z$, including at index zero since $Z_{k-1}=0$. The two net changes we need within the respective sets of vertices are $a-h$ at A and $h$ at B. Their edge changes sum to $da+(\tau-I)h=b$. Moreover $|h_j|\le6P$ and $|a_j-h_j|\le8P$. If there are at least $8P$ sites of each initial label in each type, reassign the requisite number from the negative entries to the positive entries of each net change vector. This realizes both targets exactly.

## Choosing the balanced targets

For any total $m$, a balanced vector has $\lfloor m/k\rfloor$ in every bin and one extra in $r=m\bmod k$ distinct bins. For $0<r<k$, their index sum can be any residue. Indeed the sums of $r$ distinct integers in $[0,k-1]$ fill an interval of width $r(k-r)\ge k-1$: start at the $r$ smallest and move them to the $r$ largest, one unit at a time, starting with the largest entry.

For $d=1$, choose balanced vertex and edge targets with $s(b-a)=0$. At least one of the totals $n,n-1$ is not divisible by $k$, and its extra bins permit any needed index sum. For $d=2$, take any balanced targets. Changing the label of one leaf by $t$ changes the initial moment $s(E-2V)$ by $-t$, where $V,E$ are the initial histograms. This enforces $s(b-2a)=0$. We use this option only with sites whose two neighbors are themselves degree-two vertices. The leaf change preserves all the site types and their initial labels.

## Finding enough local changes

Give vertices independent uniform labels. Edge labels are also mutually independent and uniform: specifying the root label and every edge sum determines the vertex labels uniquely by propagation. For every prefix of residues its vertex count and its edge count separately have binomial distributions. Set $D=2\sqrt{n\log(2k)}$. With probability at least $1-4k(2k)^{-8}>1-1/(32k^2)$, every such count is within $D$ of its expectation. Apply the bounded-sum inequality to each count and a union bound over the two families. Independence between the two histograms is unnecessary. Any balanced target has each prefix within $k$ of its expectation. The optional leaf change costs at most one further unit per prefix, so $P=D+k+1$ suffices. [Hoeffding, *Probability inequalities for sums of bounded random variables*](https://doi.org/10.1080/01621459.1963.10500830)

Let $L$ be the number of leaves, $M$ the largest number of leaf neighbors at a single vertex $u$, and $L'=L-M$. We prove a dichotomy of supplies, with a direct labeling in the exceptional star-like case.

**Leaves at several parents.** Suppose $L'\ge n/(32k)$. Partition the parents into two pools by placing each parent, weighted by its number of leaf neighbors, in the currently lighter pool. The final loads differ by at most $M$, so each pool has weight $W\ge n/(64k)$. In the first pool the weight $X$ of parents labeled zero has mean $W/k$ and is at most $W$, so $\Pr(X\ge W/(2k))\ge1/(2k)$. In the second pool use parents labeled 1. The events depend on disjoint sets of parents. With probability at least $1/(4k^2)$ we therefore have at least $n/(128k^2)$ eligible leaves in each pool.

Given the parent labels, the leaves still have independent uniform labels. Each of the $2k$ site counts has mean at least $n/(128k^3)$ and variance at most its mean. By Chebyshev and a union bound, conditional failure to get at least half the mean in every bin has probability at most $1024k^4/n<1/2$. Thus the leaf supply event has probability at least $1/(8k^2)$ and intersects the prefix concentration event. Use these leaves with $d=1$.

**Leaves concentrated at one parent, or few leaves altogether.** Now $L'<n/(32k)$. Remove the $M$ leaf neighbors of $u$, obtaining a tree $R$ of order $h=n-M$. If $h\le\lceil n/k\rceil$, give every vertex of $R$ label zero. Choose a balanced vertex vector with its zero bin equal to $\lceil n/k\rceil$ and distribute its remaining labels on the removed leaves. The edge vector is the vertex vector minus $e_0$ and is balanced.

Otherwise $h>n/k$, and $R$ has at most $L'+1$ leaves. A tree with $l\ge2$ leaves has at most $2l-2$ vertices of degree different from two and at most $2l-3$ segments after suppressing degree-two vertices. These bounds follow from the degree sum. Exclude $u$ from the runs of degree-two vertices of $R$, splitting at most one run. The remaining runs consist entirely of degree-two vertices of the original tree. In a run of length $z$, take $\lfloor z/3\rfloor$ disjoint consecutive triples. In total these give at least $(h-6(L'+1)-3)/3\ge n/(8k)$ triples under the order hypothesis. Their centers are pairwise nonadjacent, including for triples in different runs.

Fix an orientation on each triple. Use the patterns $(0,x,0)$ and $(0,x,1)$ for each initial center label $x$. Disjoint triples have independent labels. Each of the $2k$ pattern counts has mean at least $n/(8k^4)$ and variance at most its mean. The probability that some count is less than half its mean is at most $64k^5/n<1/2$. The supply event again intersects prefix concentration. Use the centers with $d=2$, including the single leaf change to fix the moment.

In both probabilistic cases we have at least $n/(256k^4)$ sites of each label in each type. The order hypothesis gives $n/(256k^4)\ge32\sqrt{n\log(2k)}\ge8(D+k+1)$. The local correction applies and proves the theorem. At $k=1$ the unique labeling works at every order.

## Verification

The proof gives a randomized construction: sample labels, compute both target vectors, and apply the two prescribed lists of relabelings when their supplies suffice. The checker verifies the integer correction identities and performs the relabelings on actual trees, then independently recomputes both histograms from all original edges. It checks 87,423 prescribed target histograms, 2,520 integer correction identities, and fourteen random-tree-label repairs with up to 128,001 vertices, as well as direct fan cases. The [Lean proof](CyclicCorrection.lean) verifies the zero-mass cyclic difference equation for every modulus from its integer moment condition. The probability and structural arguments are given above.

~~~sh
python3 -B -m research.large_order_check
lean research/large-order/CyclicCorrection.lean
~~~
