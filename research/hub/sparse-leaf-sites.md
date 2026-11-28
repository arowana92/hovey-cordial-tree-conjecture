# Leaves at a sparse set of sites, with arbitrary edge offsets

**Theorem.** Let $H$ be any tree of order $h$, let $k\ge2$, and attach arbitrary positive populations of leaves at $P$ distinct vertices of $H$. The resulting tree is $k$-cordial whenever
$$
P\ \ge\ 8\sqrt{hk\log(8k)} .
$$
The logarithm is natural. Every edge, including each original edge of $H$, may independently have a prescribed additive offset in $\mathbb Z_k$. In particular one leaf at every vertex suffices for every $h\ge64k\log(8k)$. More generally, for any fixed $\rho>0$, occupying a fraction $\rho$ of the original vertices suffices at $h\ge64\rho^{-2}k\log(8k)$.

## Pairing prescribed vertex and edge counts

Let $X,Y$ be multisets in $\mathbb Z_k$ of the same length. If no element of $X$ has multiplicity greater than $D$, pair $X$ to $Y$ so each difference $y-x$ occurs at most $2D$ times. Split $X$ into $D$ layers with distinct entries and distribute $Y$ in any sets of positions of the corresponding sizes, allowing repeats. Within each layer, take the representatives of $X$ in increasing order and those of $Y$ in decreasing order. The integer differences strictly decrease within $[-(k-1),k-1]$. Each residue has at most two representatives in this interval. Interchanging $X,Y$ also works if the smaller maximum multiplicity is on the other side. The factor two is sometimes needed even when both are sets. For $X=Y=\mathbb Z_k$ with even $k$, the sum of the differences is zero, whereas the sum of all distinct residues is $k/2$ modulo $k$.

For a fixed initial labeling let $V_i$ and $E_i$ count its vertex residues and adjusted edge weights. Put
$$
a=\max_i\{V_i,E_i\},\qquad D=a-\min_i V_i .
$$
Suppose at least $2D$ available leaves have each effective shift $s$, the old parent's label plus the offset on that leaf edge. Then the tree can be completed cordially, preserving the given labels. Choose any $d$ with $E_d<a$. There is such a bin since $h-1<ak$. Request $a-V_i$ copies of each new vertex label $i$, and $a-E_i-\mathbf 1_{i=d}$ copies of each new weight $i$. Both multisets have length $ak-h$. The pairing supplies a leaf with shift $y-x$ for each matched pair. The chosen subtree now has uniform vertex bins and just the one deficient edge bin $d$. Append the remaining leaves from this divisible order by [Hall's leaf-extension argument](../counterexample-bound.md#removing-leaves). When $D=0$ the old labeling already has this balance.

In particular, from a prescribed cordial core of nondivisible order, **two available leaves of every effective shift suffice**, and any initially low edge bin can be the deficient bin at the next divisible order. Here each required label and weight occurs just once. At odd $k$, **one leaf of each shift suffices**. The cyclic case of Snevily's theorem pairs the two sets $-X$ and $Y$ with distinct sums. Thus at odd $k$ a cordially labeled ordinary tree of order at least $k$ can take one or more leaves at every vertex. At every $k$ this holds at order at least $2k$. Divisible initial orders follow directly by Hall's extension. [Dasgupta, Károlyi, Serra and Szegedy, Theorem 1](https://services.math.duke.edu/~dasgupta/papers/finallatin.pdf)

## Finding the initial labeling

Fix one available leaf at each occupied site. Give the old vertices independent uniform labels. Write $q=h/k$, $\theta=P/k$, and $t=\theta/5$. Each old vertex bin is binomial of mean $q$. For a fixed weight the old edge bin is binomial of mean $(h-1)/k$. After rooting the tree, the root label and **all adjusted edge sums** are independent uniform variables, since together they recover all vertex labels successively. Each selected shift bin $S_i$ is binomial of mean $\theta$. The selected parents are distinct and each prescribed offset is fixed.

With positive probability all residues simultaneously satisfy
$$
q-t\le V_i\le q+t,\qquad E_i\le q+t,\qquad S_i\ge\theta-t .
$$
Indeed for a binomial of mean $\mu\le q$, either one-sided deviation by $t$ has probability at most $\exp[-t^2/(2(q+t/3))]$ by the binomial Chernoff bounds. Here $t\le q/5$, so the exponent in absolute value is at least $3\theta^2/(160q)$. The assumed $P^2\ge64hk\log(8k)$ makes this greater than $\log(8k)$. There are at most $4k$ bad events, giving total failure probability less than $1/2$. The three families need no joint independence.

For a successful labeling, $D\le2t$ and $S_i\ge\theta-t=4t\ge2D$. The multiset construction finishes the proof. Independent random trials therefore need fewer than two attempts on average under the stated bound. There is also a deterministic choice by conditional expectations. Reveal a connected parent-first prefix. The remaining adjusted sums are still independent uniform variables conditional on its labels, by the same tree bijection. For each individual bin the conditional bad-event probability is a binomial tail with its already known count included. Choose the next color minimizing the sum of these conditional probabilities. It starts below one, never increases, and at the end counts the violated inequalities.

## Replay

The [constructor and direct checker](sparse_leaf_sites.py) fix the trees, occupied sites and all offsets before sampling any labels. They check the actual parent edge of every added vertex and include all zero bins in both frequency tests. The 24 examples satisfying the numerical bound include stars, paths and randomly branching trees at moduli through 32. A further 56 tests start from prescribed initial labels and use arbitrary edge offsets, supplying the needed effective shifts at just one physical parent.

~~~bash
python3 -B -m research.hub.sparse_leaf_sites
~~~
