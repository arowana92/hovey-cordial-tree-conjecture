# A polynomial-size modulus for a star with arbitrary outside branches

**Theorem.** Let $H$ be a tree rooted at $o$, with $a$ terminal vertices other than $o$. There is a prime $p=O((a+1)^4)$ such that **every positive multiple of $p$ works for $H$ with any number of extra leaves at $o$**. The bound is independent of the lengths of all paths and of the order of $H$. The choice of $p$ may depend on $H$. A single computable positive integer $N_H$ with $\log N_H=O((a+1)^4)$ controls the exceptional moduli.

More precisely, fix $0<\epsilon<1$. At all sufficiently large $k$ with $a\le k^{1-\epsilon}$, a failure for any leaf population requires $k\mid N_H$. The same integer works for every population. Consequently among primes in $[X,2X]$ there are at most $O((a+1)^4/\log X)$ exceptions in this range. Among **all** integers in that interval the bound is $O(X\log(2+a)/\log X)$, so the fraction of exceptions tends to zero for $a=X^{o(1)}$, uniformly in the tree and its order.

There is a complementary uniform result. If a root-to-terminal path has at most $d$ nonroot branching vertices, for fixed $d$ on **every** such path, all sufficiently large $k$ work as soon as
$$
a\le k^{1/(30(d+2))}.
$$
Here branching means having at least two children before the extra hub leaves are added. Both parts use the [positive-density embedding and the twelve-vertex path](long-branches.md).

## One list of short trees for all prefixes

Take a depth-first preorder of $H$. Mark its root, its terminals and its vertices with at least two children. Each of at most $2a$ segments between marks is visited consecutively from its upper end. At a prefix, keep all the original marks that have been reached and the current unfinished segment endpoint. For each nonempty segment portion of length $t$, keep $t$ edges when $t\le14$ and otherwise its congruent length in $[3,14]$ modulo twelve.

The resulting compressed prefixes have at most $28a+1$ vertices. There are at most $28a+1$ entries to consider, regardless of how many prefixes the original order gives. In fact, for any one currently traversed segment all previously completed lengths are fixed. The retained length on that segment has only fourteen possibilities. Include the initial root. This counts entries even if some rooted shapes coincide.

On each listed prefix $B$, use the [ordinary integer construction](universal-hub.md) with labels $x$ and zero at the hub. Multiply the positive differences $|x_i-x_j|$ for all unordered pairs of vertices in this certificate, then multiply over all listed prefixes to obtain $N_H$. Empty products are one. A single span has logarithm $O(a+1)$ by the construction, there are $O((a+1)^2)$ pairs on a prefix and $O(a+1)$ prefixes. This proves the logarithm estimate.

If $k\nmid N_H$, every listed certificate remains injective modulo $k$; the edge sums still use all but one of its vertex labels. For a prefix of actual order $h<k/20$, expand the compressed segments as in the twelve-vertex proof. Each to be expanded has at least three edges, so one edge has two nonzero endpoints and nonzero sum: there is only one zero vertex, at the root, and at most one zero edge. The bound $k>12h+132$ holds at sufficiently large $k$. Thus every such small prefix works with all hub populations.

For $k/20\le h\le k$, any of these prefixes has at most $a$ terminal vertices other than the hub. The positive-density theorem labels it at every population. For $h>k$, use strong induction along this same list of **original** prefixes. At total order $1\bmod k$ remove the last prefix vertex, a nonroot terminal, then restore the deficient edge weight. Otherwise remove the final $(h+m-1)\bmod k$ vertices, where $m$ is the number of added hub leaves. Each suffix component contains a terminal of the current prefix. Its total degree excess and number of components are $O(a+1)$, because degrees inside the suffix including its single entering edge are bounded by those of the prefix, which has at most $a+1$ undirected leaves. Thus the [prescribed forest lemma](../bounded-degree/excess.md#forest-lemma) restores it, padding to $k-1$ if necessary and taking its exponent smaller than $\epsilon$. This is the [prefix induction](long-branches.md#from-order-k-to-all-core-orders), with the cut order now fixed for every modulus and population. It proves the divisibility assertion.

## Counting the possible divisors

The prime bound follows by adding the logarithms of distinct prime divisors. For arbitrary integers put $Y=\max(2,\log N_H)$. Summing over prime powers gives
$$
\sum_{j\le2X}\log\gcd(j,N_H)
\le 2X\sum_{p\mid N_H}\frac{\log p}{p-1}
= O(X\log(2Y)).
$$
For $p>Y$ the contribution to the prime sum is at most $2\log N_H/Y$. For $p\le Y$, summing $\lfloor Y/p\rfloor\log p$ counts a divisor of $\lfloor Y\rfloor!$, while $\lfloor Y/p\rfloor\ge Y/(2p)$. This bounds the remaining sum by $O(\log(2Y))$. Every divisor $j\in[X,2X]$ contributes at least $\log X$ to the left, proving the count.

To produce a polynomially bounded prime, take $M=C(a+1)^4$ with a sufficiently large absolute $C$. The sum of $\log p$ over $p\le M$ is at least $cM$ for an absolute $c>0$ at large $M$. Indeed the largest binomial coefficient at order $2b$ is at least $2^{2b}/(2b+1)$; each prime's valuation in it is at most the number of its powers up to $2b$, by the factorial formula. Powers of exponent at least two account for at most $\sqrt{2b}\log(2b)$ in the logarithm. Take $b=\lfloor M/2\rfloor$. The primes up to $\sqrt M$ also contribute only $O(\sqrt M\log M)$. The remaining total exceeds $\log N_H$, so there is a prime $p\in(\sqrt M,M]$ that does not divide $N_H$. Enlarge $C$ to exceed the absolute threshold for $\epsilon=1/2$ (with fixed density cutoff $1/20$) even when $a$ is small. Every multiple of this $p$ has $a\le\sqrt k$ and cannot divide $N_H$. This proves the theorem, including the singleton directly.

## All moduli at bounded branching depth

On a rooted core with $b$ vertices and height $l$, apply the integer construction in breadth-first order. Its span is at most $8(b+1)^{l+4}$. In the running-positive construction each distance level increases the current maximum by at most $b$ times the previous maximum, since the parents have already been assigned. Start at most $b+1$; the four final sites and their leaf lists multiply the bound by at most $2b+4$. In the anchor construction both running magnitudes grow by at most the same factor per level. The delayed anchor and its leaf children multiply the final bound by at most $2(b+1)$, with an extra factor two for the span. These estimates include stars.

Each completed or partial path from the root in a compressed prefix uses at most $d+1$ segments, of at most fourteen edges each. Thus $l\le14(d+1)$. With $a\le k^{1/(30(d+2))}$, the above span is strictly smaller than $k$ for sufficiently large $k$ in terms of $d$, since $(14(d+1)+4)/(30(d+2))<1$. Every compressed prefix certificate therefore remains injective. The small-prefix expansion, positive-density case and induction give the all-modulus assertion without a divisibility test.

The [checker](check_prefix_moduli.py) compares the short list against independently rebuilding every actual prefix and checks the integer labels, ordinary edge sums, height bound and modular collisions. The [catalog and product](prefix_moduli.py) use only Python's standard library and the published integer constructor.

~~~sh
python3 -B -m research.hub.check_prefix_moduli
~~~
