# Prescribing every parent label at arbitrary order

Fix a positive modulus $k$ and root a tree at $o$. Prescribe a residue $f(u)$ at the root and at every vertex with children. Write $H$ for these $h$ vertices. The edge into each nonroot vertex $v$ may have its own prescribed additive offset $b_v$. Define its shift $s_v=f(p(v))+b_v$, where $p(v)$ is its parent. Its eventual weight is $f(v)+s_v$. For each residue $g$ let $N_g$ count all nonroot vertices with shift $g$ and $a_g$ count those in $H$ with shift $g$.

**Prescribed-parent theorem.** Every such partial labeling extends to a cordial labeling whenever
$$
n\ge kh,\qquad N_g\ge k a_g\quad(g\in\mathbb Z_k).
$$
The prescribed labels can repeat. In the ordinary case a sufficient condition, in addition to $n\ge kh$, is that each parent have at least $k-1$ leaf children per nonleaf child. This works simultaneously as a guarantee for **every choice** of parent labels. With offsets, the same guarantee holds if the child-count inequality holds at each parent separately for each value of the outgoing offset. The pooled inequalities in the theorem can also use leaves at a different parent with the same effective shift.

## Putting prescribed rows in separate periods

Consider $qk$ shifts $d_i$ with total zero in $\mathbb Z_k$. Seek sources $x_i$ such that the lists of sources and destinations $x_i+d_i$ each use every residue $q$ times. Some distinguished rows have independently prescribed sources. For each shift $g$ let $M_g$ be its multiplicity and $m_g$ its number of distinguished rows. A sufficient condition is that every nonempty set $S$ of shifts occurring on distinguished rows satisfy
$$
\sum_{g\in S} M_g > k\left(\sum_{g\in S} m_g-1\right).
$$
In particular any one source may always be prescribed.

Extract zero-sum blocks of size $k$ using the Erdős–Ginzburg–Ziv theorem while there are at least $2k$ rows left. The last block sums to zero by subtraction. In the bipartite graph joining distinguished rows to blocks containing their shift, a nonempty set of rows with shift set $S$ has neighbors containing all $\sum_{g\in S}M_g$ occurrences. As each block holds at most $k$ occurrences, there are at least $\sum_{g\in S}m_g$ such neighbors. Hall's marriage theorem now assigns the distinguished rows to different blocks. Put the assigned shift occurrences there and distribute the remaining equal-shift rows arbitrarily. In each zero-sum block, Marshall Hall Jr.'s prescribed-differences theorem supplies a permutation of sources whose destinations also form a permutation. Translating all its sources translates its destinations and realizes its one prescribed source if present. Concatenating proves the claim. [Erdős, Ginzburg and Ziv (1961)](https://www.renyi.hu/~p_erdos/1961-25.pdf) · [Marshall Hall Jr. (1952)](https://doi.org/10.1090/S0002-9939-1952-0050579-7)

## Proof for trees

First suppose $k\mid n$. Add a fictitious shift $\gamma=-\sum_{v\ne o}s_v$ for the root. Mark precisely the prescribed vertices, including the root. For a nonempty set $S$ of marked shifts put $A=\sum_{g\in S}a_g$. When $\gamma\notin S$, the blocks contain at least $kA$ occurrences of these shifts for $A$ marks. When $\gamma\in S$, they contain at least $kA+1$ for $A+1$ marks. In both cases the period lemma applies. The vertex histogram is now uniform. Deleting only the fictitious destination $f(o)+\gamma$ gives the actual edge histogram, uniform except for that one deficient weight. All actual parent labels have their prescribed values, so the destinations on the other rows are exactly the tree's edge weights.

For general $n=qk+r$ with $0<r<k$, remove $r$ leaf children while retaining $N_g\ge k a_g$. In class $g$ we can remove $N_g-ka_g$ leaves, since only $a_g$ of its rows are prescribed. Total removable capacity is $n-1-k(h-1)\ge r$ because $q\ge h$. The retained tree has order $qk$ and retains every prescribed vertex, including any that have become terminal. The divisible-order argument still applies since it only requires that every parent be marked. Restore the first leaf with its unique label making the deficient weight. At this point the edge counts are uniform and the vertex counts have one surplus residue. There are at most $k-2$ remaining leaf rows. Pad their shifts to a list of $k$ summing to zero, then use Hall's permutation and translate it to place the surplus vertex residue in a padding position. The real leaf rows give distinct nonsurplus vertex residues and distinct weights. Both final histograms are balanced. [Leaf-extension argument](../counterexample-bound.md#removing-leaves)

## Exact uniform increments with one free parent

Attach $qk>0$ new vertices by a forest, each component having one edge back to an already labeled core. Suppose all edges between new vertices join a specified new center to its $j$ children. All remaining new vertices, including that center, attach directly to the old core. For each externally attached vertex take its offset plus its parent's label as $b_i$. For a child of the center take just its edge offset as $b_i$. Put $B=\sum_i b_i$.

**Exact criterion.** A prescribed center label $x$ allows the new vertices and the new edge weights to use each residue $q$ times apiece if and only if
$$
jx=-B\pmod k.
$$
Thus existence with a free center is equivalent to $\gcd(j,k)\mid B$, also for $j=0$. For one complete period at a prime modulus and $1\le j<k$, each system of boundary labels and offsets admits exactly one possible center label, and it is always attained.

Indeed summing the destinations and subtracting the sources yields $B+jx$, which must vanish for equal histograms. Conversely, after fixing a solution $x$, every shift is known and their total vanishes. Apply the one-prescribed-source case of the period lemma to the center. That preserves the parent label used for every internal edge. An insoluble congruence obstructs this particular uniform increment. Cordiality of the whole tree allows other increments.

## Reproduction

From the repository root run

~~~sh
python3 -B -m research.biased.check_pinned_periods
~~~

The checker reconstructs both histograms on the actual trees for 10,647 prescribed labelings. Its finite checks include exhaustive core-label and internal-offset assignments for four small rooted skeletons, larger trees through modulus 30, and cases that use leaves at a different parent. It independently compares the **entire set** of attainable center labels against brute-force histograms in 1,426 instances, including multiple periods. It checks another 434 attachments through modulus 32. The unrestricted conclusions follow from the proofs above. [Construction](pinned_periods.py) · [Independent histogram and permutation checks](check_pinned_periods.py)
