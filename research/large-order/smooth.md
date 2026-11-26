# Near-linear orders for every counterexample at smooth moduli

**Theorem.** Suppose $k_i\to\infty$ and the largest prime factor $P(k_i)$ satisfies $\log P(k_i)=o(\log k_i)$. If $T_i$ is any $k_i$-counterexample, then $|T_i|\le k_i^{1+o(1)}$. Equivalently every fixed exponent $1+\gamma>1$ suffices as an order threshold along this sequence for all sufficiently large indices. This applies to all powers of each fixed integer and to arbitrary products of primes from a fixed finite set. The conclusion bounds every possible counterexample at these moduli, including ones larger than a minimum counterexample.

## Filling from a cyclic subgroup

Let $m\mid k$ and let $B$ be a rooted tree of order $b$. Pad $B$ with leaves at its root to order $b'=m\lceil b/m\rceil$. Suppose the padded tree is $m$-cordial. Translate a labeling so the root is zero. Its vertex histogram is uniformly $b'/m$ and its edge histogram is that same vector less one unit at some residue $x$. Strip the temporary leaves: each such leaf removes its own residue from both histograms. Embed the group into $\mathbb Z_k$ by $z\mapsto(k/m)z$. The resulting histograms on $B$ still differ by one unit, at the image of $x$, and the largest vertex count is at most $\lceil b/m\rceil$.

Consequently attaching at least $k\lceil b/m\rceil$ actual leaves at the root suffices for $k$-cordiality. The floor of the final average vertex count is at least every old count. Fill to a balanced target, making the distinguished bin high when there are high bins. Subtracting a unit there leaves balanced edge counts. This also works at $m=1$, with all core labels zero.

## Improving the exponent

Write $\mathcal P(a)$ for the claimed upper bound with $k_i^{a+o(1)}$ in place of $k_i^{1+o(1)}$, uniformly in the sense of sequences above. The [unrestricted order bound](dyadic.md) gives $\mathcal P(3/2)$. We prove $\mathcal P(a)\Rightarrow\mathcal P(2-1/a)$ for each fixed $a>1$.

Take any counterexample sequence. Use protected star deletion at a maximum-degree vertex. As proved in the [dyadic argument](dyadic.md#consequences-for-unrestricted-trees), the remaining core is a root with at least $\Delta-k+1$ extra leaves on a subtree $B$ of order $b=O(k(\log(2k))^5)$. Also $n=O(k(\log(2k))^5+\Delta(\log(2k))^2)$. It suffices to bound $\Delta$. Take a subsequence realizing its upper growth exponent, and a further subsequence with $\log b/\log k\to\beta\in[0,1]$. At $\beta=0$ the subgroup lemma with $m=1$ forces $\Delta<k-1+kb=k^{1+o(1)}$.

If $\beta>0$, fix $\varepsilon>0$ and set $Y=b^{1/(a+\varepsilon)}<k$ for large indices. Multiply the prime factors of $k$, counting multiplicities, stopping just before the first product that exceeds $Y$. This gives a divisor $Y/P(k)\le m\le Y$. Thus $\log m/\log k\to\beta/(a+\varepsilon)>0$ and $\log P(m)=o(\log m)$. By $\mathcal P(a)$, the padded trees of order $b'\ge b\ge m^{a+\varepsilon}$ are $m$-cordial for all sufficiently large indices. Otherwise the failed instances would form a counterexample sequence violating $\mathcal P(a)$.

The subgroup lemma forces $\Delta<k-1+k\lceil b/m\rceil$. The upper exponent of $\Delta$ is therefore at most $1+\beta(1-1/(a+\varepsilon))\le 2-1/(a+\varepsilon)$. Let $\varepsilon$ decrease to zero. The order estimate gives $\mathcal P(2-1/a)$. Starting at $a=1+1/2$ the iteration replaces $1+1/j$ by $1+1/(j+1)$. Taking arbitrarily large fixed $j$ proves the theorem.

The [subgroup checker](../large_order_subgroups.py) searches directly for labelings of padded rooted trees at six small moduli. It strips the temporary leaves, embeds the labels into three multiples of each modulus and counts both histograms after every possible final order remainder. It checks 7,560 whole-tree labelings.

~~~sh
python3 -B -m research.large_order_subgroups
~~~
