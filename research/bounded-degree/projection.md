# A near-linear bound on the smallest counterexample

**Theorem.** For every $\gamma>0$ and all sufficiently large $k$ (in terms of $\gamma$), if some tree is not $k$-cordial then a smallest such tree has fewer than $k^{1+\gamma}$ vertices. There is no degree assumption. The [explicit quadratic bound](../counterexample-bound.md) remains available at each particular modulus. The present estimate is asymptotic.

The proof works in a larger cyclic group and prescribes which elements to omit. If the omitted elements project to distinct residues modulo $k$, deleting them from a whole group leaves balanced counts after projection.

## Omitted colors with a given sum

Let $N=Mk$, with $k\ge5$ and $M\ge2$. Write $\pi:\mathbb Z_N\to\mathbb Z_k$ for reduction. In $\mathbb Z_N$ take a set $R$ consisting of one representative from every fiber, together with the two whole fibers over 1 and 2. Choose the representatives to avoid zero, for instance $k,\ldots,2k-1$. Thus $0\notin R$ and $|R|\le k+2M$.

**Lemma.** For $2\le r\le k-1$ and every $s\in\mathbb Z_N$, one can choose $r$ elements of $R$ with distinct projections and sum $s$.

First find $r$ distinct residues of sum $\pi(s)$ containing at least one of 1 and 2. For $r=2$, choose $a\in\{1,2\}$ with $2a\ne\pi(s)$ and use $a,\pi(s)-a$. For $r=k-1$, omit the unique residue that gives the required sum. For $3\le r\le k-2$, insist on using $a=1$. After translating all selected residues by $-a$, include zero and choose $r-1$ distinct integers from $1,\ldots,k-1$. Their possible sums fill an integer interval of width $(r-1)(k-r)\ge k-1$. To see there is no gap, start with the first $r-1$ integers, move the largest up to its maximum, then the next largest up to its maximum, and continue. Each move increases the sum by one. Hence every residue, in particular $\pi(s)-ra$, occurs.

Choose representatives for all but one selected residue $a\in\{1,2\}$. The unique value needed for the final summand projects to $a$, whose entire fiber lies in $R$. This proves the lemma.

## A large-order sufficient condition

**Proposition.** Fix $D\ge3$ and $0<\delta<1$. Let $T$ have order $n$ and set $N=k\lceil n/k\rceil$. For sufficiently large $k$ in terms of $D,\delta$, it is enough for $k$-cordiality that
$$
k+E_D(T)\le N^{1-\delta}.
$$
Here $E_D(T)=\sum_v(\deg_T(v)-D)_+$. In particular $k/N\to0$ in this regime.

Put $e=N-n$. If $e=0$, apply the [degree-excess theorem](excess.md) at modulus $N$. A bijective labeling with $N-1$ distinct weights projects to uniform vertex counts and edge counts $M$ or $M-1$. If $e=k-1$, remove one leaf. The smaller order $N'=n-1=N-k$ is a multiple of $k$, tends to infinity, and satisfies $E_D(T-\text{leaf})\le (N')^{1-\delta/2}$ for large $k$. The same projection gives a unique deficient edge residue. Add back the leaf with the label that supplies it. It remains to handle $1\le e\le k-2$.

**An auxiliary tree of order $n$.** Root $T$ at a leaf $o$, set its label to zero, and regard all other vertices as one free component with external parent label zero. Carry out the cuts, site selection and matching of the [edge-excess construction](excess.md#forest-lemma). It gives a tree $U$ on $n$ vertices of maximum degree at most $D+1$, and a prescribed set $P$ with $O_D(q)$ labels, where $q=O(1+E_D(T))$. For a labeling extending the prescribed relations, restoring the edges of $T$ gives precisely the same weight multiset as in $U$. The vertex $o$ plays the role of the auxiliary zero and is retained in the original tree.

All size estimates for choosing sites hold with $n$ vertices because $n\ge N-k$ and $q=o(N)$. Choose the variable labels in $\mathbb Z_N$. Require every prescribed vertex label and every edge sum on $P$ to avoid $R$ as well. The only constant vertex label is zero; no edge expression is constant. In the original parent order each variable is latest in at most four vertex expressions and one edge expression. Imposing avoidance of $R$ adds only $O(|R|)$ exclusions per step, including over a composite modulus. The existing distinctness tests cost $O_D(q)$ per step. These costs are $o(N)$ as $k\to\infty$, since
$$
(q+|R|)/N=O_D(N^{-\delta}+1/k).
$$

**Vertex and color targets.** Fix any $e$ of the representatives in $R$ with distinct projections, forming a vertex omission set $A$. The vertex target $V=\mathbb Z_N\setminus A$ has size $n$. Enlarge $P$ to an induced degree core $Q$ for $U$ as in the bounded-degree proof, and add two isolated vertices $z,z'$ of one abundant degree. Its size is $O_D(q+1)$. Greedily assign distinct labels and distinct edge sums on $Q\setminus\{z,z'\}$, keeping the prescribed labels and avoiding $R$ on both vertices and edges. The number of exclusions per vertex is $O_D(q+|R|)$. Choose the label at $z$ and force the label at $z'$ by $\sum_Q\phi=\sum V$. Avoiding the previous vertex labels and $R$ at both positions costs at most $2(|Q|+|R|)$ choices. Equality of the two new labels rules out at most two further choices. Neither new position belongs to an edge of $Q$.

Put $S_N=\sum_{x\in\mathbb Z_N}x$. Use the lemma with $r=e+1$ to choose a color omission set $B\subseteq R$ of distinct projections and sum
$$
S_N-\sum_{v\in Q}d_U(v)\phi(v).
$$
The color target $C=\mathbb Z_N\setminus B$ has size $n-1$ and contains every edge sum on $Q$. The prescribed vertex and degree-weighted sums now equal $\sum V$ and $\sum C$ respectively.

Take the embedding parameter $\mu$ sufficiently small for the bound $D+1$, with $\mu<\delta$. Then $|Q|\le N^{1-\mu}$ and $n=N-e\ge N-N^{1-\mu}$. Thus Müyesser and Pokrovskiy's Lemma 4.9 applies with group order $N$, preserving $\phi$ and using exactly the two targets. Restore the original edges of $T$. After projection, each residue has $M$ preimages in the full group, and each of $A,B$ removes at most one preimage per residue. Consequently both histograms have counts $M$ or $M-1$. This proves the proposition. [Primary embedding theorem and extension implication](https://arxiv.org/html/2509.05280v2#S4)

## Consequence for a minimum counterexample

A minimum-order $k$-counterexample has fewer than $k$ leaves by the leaf deletion and Hall permutation argument. For a tree with at least two vertices, $\sum_v(\deg(v)-2)_+=L-2$ where $L$ is the number of leaves. In particular $E_3(T)<k$. [Leaf and degree proofs](../counterexample-bound.md)

Suppose $n\ge k^{1+\gamma}$. Take $\delta=\gamma/(2(1+\gamma))$. Then $N\ge n$ gives
$$
k+E_3(T)<2k\le k^{1+\gamma/2}\le N^{1-\delta}
$$
for sufficiently large $k$. The proposition supplies a $k$-cordial labeling, a contradiction. This proves the theorem. It still permits counterexamples of order comparable to the modulus, including the case $n=k$.

## Verification

The Python check constructs omission sets for 65,580 sums and checks membership, distinct projections and the sum directly. It also builds 24 degree-core assignments, checks the prescribed targets and their sums in the larger group, and counts each target's projections in the smaller group. The fixtures use prime, even composite and odd composite projection moduli.

Lean 4.14.0 verifies the integer interval step for unrestricted parameters. The theorem states that $t$ strictly increasing integers in $[1,t+w]$ can realize every sum from the minimum through the minimum plus $tw$. Taking $t=r-1$ and $w=k-r$ gives the interval in the omission lemma. The full asymptotic argument uses the primary embedding result and the mathematical proof above.

~~~sh
python3 -B research/bounded-degree/check_projection.py
lean research/bounded-degree/SubsetSums.lean
~~~

[Omission and projection checks](check_projection.py) · [Lean theorem](SubsetSums.lean)
