# Simultaneous insertion on a fixed core at every prime power

**Theorem.** Fix a cordial labeling of a core tree at $k=p^a$. On each of any number of edges specify a chain of cordially labeled trees of orders divisible by $k$, with two ports in each tree. The interval test below is necessary and sufficient for restoring every chain by independent unit scalings and translations of its specified piece labelings, with the original core labels fixed. It handles all coefficient valuations together. After classifying the chains, the calculation visits the $1+p+\cdots+p^a$ residue classes once.

Write $w$ for an original edge weight. A piece with port labels $b,c$ and deficient edge weight $h$ contributes the coefficient $b+c-h$. The chain replaces $w$ by $w$ plus the sum of its independently unit-scaled coefficients. Everything else contributed to the two histograms is uniform. The vertex counts therefore stay balanced; the remaining task is to distribute one destination weight per core edge. [Expansion and exact chain-sum formula](period-chains.md)

## Where an edge can go

Use the tree of residue classes, starting at all of $\mathbb Z_k$ and splitting each class modulo $p^v$ into its $p$ children modulo $p^{v+1}$. A chain of zero coefficients keeps $w$ fixed. Otherwise let $v$ be the least valuation of its nonzero coefficients and $t$ their multiplicity at this valuation. Let $C$ be the class of $w$ modulo $p^v$.

* If $t=1$, or if $p=2$ and $t$ is odd, the edge must go to a different child of $C$ from the one containing $w$. Any bin in any such child works.
* If $p$ is odd and $t\ge2$, the edge can go anywhere in $C$.
* If $p=2$ and $t$ is even, the edge can go anywhere in the child of $C$ containing $w$. If this is a single bin, the destination is fixed.

Indeed, divide the chain sum by $p^v$. Each lowest-valuation term can become any unit at the remaining prime power. For odd $p$, two units can give any residue as their sum. For $p=2$, a sum with a prescribed positive number of odd terms ranges over the entire prescribed parity class. Adding higher-valuation terms preserves these sets.

## Counting capacity from the bins upwards

Let $q$ be the floor of the number of core edges divided by $k$, and put $r$ equal to the remainder. At bin $z$, let $f_z$ count fixed edges. Its interval of admissible additional contributions is
$$
                [\max(0,q-f_z),\ q+\mathbf1_{r>0}-f_z].
$$
An empty interval gives failure. At an internal class, number its children $i=1,\ldots,p$. Write $[l_i,u_i]$ for the intervals they report. There are $m_i$ local edges that must leave child $i$ and $b$ further local edges that may enter any child. Define $m=b+\sum_i m_i$ and $U=\sum_i u_i$. If any $m_i>U-u_i$, the test fails. Otherwise the interval passed up, for the number of additional edges received from ancestors, is
$$
\left[\max\left(m,\sum_i l_i,\max_i(l_i+m_i)\right)-m,\quad U-m\right].
$$
Again, an empty interval gives failure. The entire placement is possible exactly when the root interval contains zero.

For the proof suppose $A$ additional edges arrive freely from above, giving $T=A+m$ destinations among the children. Choose integer loads $x_i$ with sum $T$ in the child intervals. Given the loads, assigning the edges is possible precisely when $m_i\le T-x_i$ for each $i$. In Hall's theorem, a collection of origins all forbidden from one child sees the slots in the other children. Two distinct forbidden children, or any unrestricted origin, give all slots. Thus the allowed load intervals are $[l_i,\min(u_i,T-m_i)]$.

Their lower bounds fit when $T\ge\sum l_i$ and $T\ge\max_i(l_i+m_i)$. Their upper bounds sum to at least $T$ precisely when $T\le U$ and $m_i\le U-u_i$ for every $i$, given $T\ge m$. To verify the last equivalence, expand the sum of minima as the minimum over subsets $I$ of $\sum_{i\notin I}u_i+|I|T-\sum_{i\in I}m_i$. The empty and singleton subsets give the displayed conditions. Every larger subset satisfies the bound automatically because $T\ge\sum_i m_i$. Integer loads filling the intervals to any admissible total can be chosen one at a time. Induction up the class tree proves the criterion, and the loads and matchings reconstruct a placement.

The [checker](prime_power_insertions.py) compared the intervals against a separate matching on individual bins that explicitly enumerates the possible unit-scaled chain sums. They agreed on 5,040 instances, including 2,125 infeasible ones. For successful sampled instances the checker joined 36,624 actual pieces into 1,347 ordinary trees and recounted both histograms. An infeasible input concerns its specified core and piece labelings. [Unit-only criterion and packing bounds](period-edges.md)

~~~bash
python3 -B -m research.biased.prime_power_insertions
~~~
