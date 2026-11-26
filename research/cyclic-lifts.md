# Prescribed cordial labelings can fail to lift through every factor

**Theorem.** For every $k,s\ge2$, there is a specified $k$-cordial labeling of a caterpillar on $sk$ vertices that has no $sk$-cordial lift through reduction modulo $k$. This includes odd factors relatively prime to $k$.

Use adjacent vertices $u,v$ of label zero. Attach $s-2$ more zero-labeled leaves to $u$. Of the $s$ leaves labeled 1, attach one to $v$ and the other $s-1$ to $u$. For each $j=2,\ldots,k-1$ attach $s$ leaves of label $j$ to $u$. Every residue occurs $s$ times on vertices, and each edge to a leaf has the leaf's label as weight. The edge $uv$ weighs zero. Thus weight zero occurs $s-1$ times and every other weight occurs $s$ times.

In a lift to modulus $sk$, all vertex labels are distinct and all edge weights are distinct. The $s$ leaves of old label 1 must use the entire fiber over 1. Their $s$ edges must use that same fiber as weights. Subtracting the sums of those two multisets gives
$$
(s-1)X_u + X_v = 0 \pmod{sk}.
$$
Here $X_u$ and $X_v$ reduce to zero modulo $k$, so $sX_u=0\pmod{sk}$. Therefore $X_v=X_u\pmod{sk}$, contradicting distinctness. The underlying caterpillar has ordinary cordial labelings at all moduli by Hovey's theorem. [Hovey, *A-cordial graphs*](https://doi.org/10.1016/0012-365X(91)90254-Y)

## A local criterion

Suppose all $s$ vertices above a residue $c$ are leaves whose parents have the same base residue $a$, and their edges exhaust the fiber over $a+c$. Assume the parent lifts are given. Write each parent label as $a+kh_i$, with an entry for each leaf. The two full fibers differ by a fixed translation, and choosing the leaf labels amounts to permuting their high digits $t_i$ in $\mathbb Z_s$. Up to the common carry, the edge high digits are $t_i+h_i$. Thus a choice filling both fibers exists exactly when $\sum_i h_i=0\pmod s$, by Hall's permutation theorem. This criterion concerns the two fibers in question with the parent lifts already specified. [Marshall Hall Jr., *A combinatorial problem on abelian groups*](https://doi.org/10.1090/S0002-9939-1952-0050579-7)

For two parents with multiplicities $r$ and $s-r$, the condition becomes $r(h_1-h_2)=0\pmod s$. Directly, the subset of high digits used at the first parent must be invariant under translation by $h_1-h_2$. It can be chosen as a union of orbits precisely when the order of that difference divides $r$. When $r=1$ distinct parent lifts always fail. This is the case used above.

The finite check reconstructs both base histograms and enumerates every lift up to translation in three small instances. It independently counts the attainable leaf configurations for two fixed parents by enumerating subsets. Lean checks the cancellation step for arbitrary positive parameters and canonical representatives.

~~~sh
python3 -B research/check_lifts.py
lean research/Nonlifting.lean
~~~

[Finite checker](check_lifts.py) · [Lean cancellation lemma](Nonlifting.lean)

## A matching obstruction for even factors

**Proposition.** For every $k\ge2$ and every even $s\ge2$, some $k$-cordial labeling of a tree on $sk$ vertices has no $sk$-cordial lift through reduction modulo $k$.

Make a path of $s$ vertices, each labeled zero. Attach one leaf labeled 1 to each path vertex. For every $j$ with $2\le j<k$, add $s$ leaves labeled $j$ at the first path vertex. Every vertex residue occurs $s$ times. The path gives $s-1$ edges of weight zero and the leaves give $s$ edges of every other weight. Thus the specified labeling is $k$-cordial.

A lift at modulus $sk$ must use each vertex residue once and have distinct edge weights. The possible lifts of zero are $ki$ for $0\le i<s$, and the possible lifts of 1 are $1+ki$ for the same indices. Both sets must be used in full. The $s$ edges joining path vertices to their label-1 leaves form a matching covering both fibers. All their weights reduce to 1, so their weights must also run through the full set $1+ki$. Write $S=0+1+\cdots+(s-1)$. Summing those weights in two ways gives
$$
s+2kS\equiv s+kS\pmod{sk}.
$$
This would require $S\equiv0\pmod{s}$, whereas $S\equiv s/2\pmod{s}$ for even $s$.

For $k=s=2$, the example is the four-vertex path with base labels $1,0,0,1$ in path order. An ordinary 4-cordial labeling in path order is $0,2,1,3$, with weights $2,3,0$.

The obstruction fixes the complete base labeling in advance. It rules out an induction that lifts an arbitrary cordial labeling through an even factor. These trees are caterpillars and hence have ordinary cordial labelings for every modulus. [Hovey, *A-cordial graphs*](https://doi.org/10.1016/0012-365X(91)90254-Y)
