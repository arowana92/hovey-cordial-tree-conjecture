# Deficient edge sums at large prime-power factors

Let a cordially labeled piece of order $qk-1$ have two deficient edge weights $d,e$ and a bridge port labeled $b$. Fix any cordial labeling of a core whose order residue is $k-a$, with $a\ge1$. All residues belong to $\mathbb Z/k$. Join the pieces at arbitrary ports.

**Large-factor theorem.** If every affine permutation of the piece labels fails to give a cordial join, then for every prime power $p^j$ exactly dividing $k$ with $p\ge2a+5$,
$$
d\equiv e\equiv 2b\pmod {p^j}.
$$
In particular, if the piece has consecutive integer vertex labels and consecutive integer edge sums, it attaches to every such core whenever *any* prime factor of $k$ is at least $2a+5$. Its two missing edge weights are consecutive modulo $k$. If all prime factors meet the bound, every cordial piece attaches, since the distinct missing weights would have to agree modulo $k$.

Use the [normalized coordinates and balancing rule](deficit-cut.md#balancing-the-two-deficits). The low vertex of the piece is now zero and the old port is zero. The set $A$ of high core vertex residues misses $a$ elements. The set $C$ of low core edge residues has size $a+1$. The congruences in the theorem are unchanged by translating the piece. The proof permits an arbitrary offset on the bridge.

## Filling a hole or choosing a low bridge

Write $P=p^j$. A direction nonzero modulo $P$ has a unit orbit of size at least $p-1$. Filling the hole $d$ works if both $b-d$ and $e+2b-2d$ are nonzero modulo $P$, since $2a+1<p-1$. We can also interchange the holes.

If $d\ne e\bmod P$, the two vertex directions differ and the two edge directions differ, since 3 is invertible modulo $P$. Failure of both sufficient tests requires, after interchanging the holes, $d=b$ and $e=3b/2$ modulo $P$, with $b\ne0\bmod P$. If $d=e=v\bmod P$, the test succeeds unless $v=b$ or $v=2b$. It remains to handle the two configurations
$$
(d,e)=(b,3b/2)\quad\text{or}\quad(d,e)=(b,b)\pmod P,\qquad b\ne0\pmod P.
$$

Let $H$ be the subgroup of order $p$ in $\mathbb Z/k$. Select a coset containing as many members $m$ of $C$ as possible, and fix $z_0$ in that coset. Write $z=z_0+Z h$ and $x=z_0-b+Xh$ for the bridge and low vertex, with $h$ a generator of $H$ and $X,Z\in\mathbb F_p$. The list of allowed $Z$ has size $m$. The list of $X$ with $x\in A$ has size $n\ge p-a$.

We can arrange $ub=b+(Z-X)h$, keeping $u=1$ modulo $k/P$. In the $P$-coordinate write $b=p^v b_1$ with $p\nmid b_1$, $0\le v<j$, and take $u=1+p^{j-v-1}t$. Then $(u-1)b$ runs through $H$ as $t$ runs modulo $p$. If $j-v=1$, exclude the one $t$ for which $u$ is divisible by $p$. Otherwise they are all units. In either case at most one difference $Z-X$ need be forbidden. The Chinese remainder theorem supplies the unit modulo $k$.

The two new holes are $ud+2x,ue+2x$. Each stays in a fixed coset of $H$. In the $H$-coordinate their variable parts are $X+Z$ and $(X+3Z)/2$ in the first configuration, and both are $X+Z$ in the second. Indeed $(u-1)d=(u-1)b$ and $(u-1)e$ is respectively $3/2$ or one times this group element. Each hole must avoid at most $m$ values, by the choice of the bridge coset. Count the forbidden values for the two holes with multiplicity even when the forms coincide.

The grid polynomial has one factor forbidding a difference and factors making the holes avoid $C$. Its leading coefficients are those of
$$
f(t)=(1-t)(1+t)^i(1+ct)^j,\qquad c\in\{1,3\},\quad 0\le i,j\le m.
$$
Here the univariate exponents count forbidden hole values. We may exclude one difference even when every difference is available. A coefficient at $t^w$ works on the grid when $w<m$ and $D-w<n$, where $D=1+i+j\le2m+1<p$.

## Two adjacent coefficients at the boundary

As in the [prime gluing proof](deficit-cut.md#the-remaining-configuration), three consecutive coefficients cannot vanish. The product rule gives a first-order differential equation with denominator $(1-t)(1+t)(1+ct)$ and the leading coefficient is nonzero. When $c=1$ the denominator $(1-t)(1+t)$ suffices, so two consecutive zeros are impossible.

If $w=0$ fits the grid, its coefficient works. Otherwise there are $n+m-1-D\ge n-m-2\ge p-2a-3\ge2$ allowable indices. Only equality at the lower bound of two needs further work. This forces $p=2a+5$, $m=a+1$, $i=j=m$, and $n=p-a$. The allowable indices are $m-2,m-1$.

For $c=3$ put $g(t)=(1+4t+3t^2)^m$ so that $f=(1-t)g$. If $f_w=f_{w+1}=0$, then $g_{w-1}=g_w=g_{w+1}$. Their common value cannot be zero since the analogous order-two recurrence for $g$ would propagate to its leading term. The identity $(1+4t+3t^2)g'=m(4+6t)g$ gives
$$
(w+1)g_{w+1}=4(m-w)g_w+3(2m-w+1)g_{w-1}.
$$
Thus $4w=5m+1$ in $\mathbb F_p$. At $w=m-2$ this requires $m=-9$, yet $2m=p-3$ and $p\ge7$ does not divide 15. Hence a grid coefficient works in every case, proving the theorem by interpolation.

## Exact obstruction at twice an odd number

Let $k=2M$ with $M>1$ odd and *every* prime dividing $M$ at least $2a+5$. In the normalized coordinates put $K=\{0,M\}$, let $\pi$ reduce modulo $M$, and let $t$ be the least multiplicative order of 2 modulo a prime divisor of $M$. A fixed piece profile fails for **some** cordial core exactly in the following cases.

1. $b\in K$ and $\{d,e\}=K$.
2. $b\notin K$, $d=e=2b\bmod M$, and either $a=1$ or $a>t$.

The large-factor theorem requires $d=e=2b\bmod M$. Thus the two transformed holes form the entire fiber over $2\pi(z)$ for a bridge $z=x+ub$. If $b\notin K$, the orbit of $b$ has at least $p-1>a$ elements for some prime $p\mid M$. At any prescribed bridge value we can therefore put $x$ in $A$. For $z\in K$ the bridge fills one hole and its opposite must be high. For $z\notin K$ the bridge can only work by lying in $C$ with both holes high. It follows that failure for a *given* $C$ is exactly
$$
K\subseteq C,\qquad 2\pi(C)\subseteq\pi(C).
$$
Any nonzero doubling cycle modulo $M$ has length at least $t$, by passage to a prime divisor of the additive order of its elements. A subgroup of prime order attaining $t$ has its nonzero elements partitioned into cycles of length exactly $t$. With $K$ already used, there are $a-1$ entries left in $C$. The closed projection exists for zero remaining entries or for at least $t$. Indeed when $a-1\ge t$, take $v=\lfloor(a-1)/t\rfloor$ distinct cycles in that subgroup. There are enough since the prime exceeds $2a$. Use one element of each fiber over those $vt$ points and a second element in as many fibers as needed, since $vt\le a-1\le 2vt$.

When $b\in K$, every unit fixes $b$. Take $C$ to contain $K$. A bridge in $K$ now leaves a low hole. The other viable bridges must belong to $C\setminus K$, with at most $a-1$ corresponding vertex choices $x=z-b$. Choose the $a$ low vertices to include them. This gives an obstructed fixed core. All the high sets used here can occur on ordinary trees: start with a star using every residue once and retain at least one uniform period of spare counts. For each remaining vertex and prescribed edge sum choose a parent in the star giving that sum. These failures concern affine changes to two given labelings.

## The twenty-six-label cut

For $k=26$, the order of 2 modulo 13 is 12. At order $26m+s$ of a least counterexample, $21\le s\le26$. Suppose one component of an edge cut has order $-1\bmod26$.

- For $s=21,22,23$, every cordial labeling of this component must, after its low vertex residue is translated to zero, have its port in $\{0,13\}$ and have deficient edge residues $\{0,13\}$. Here $a=25-s$ is 4, 3 or 2.
- For $s=24$, its two deficient edge weights must both equal twice its port label modulo 13. Both sides of the cut have order $-1\bmod26$, so this holds on both sides. Here $a=1$.
- For $s=25$ the other side has divisible order, which already excludes the cut.

Consequently a component of **exactly 25 vertices** is impossible at all five residues $21$ through $25$. The [integer census](../census/README.md) supplies a labeling with consecutive edge weights for each such tree, making its two deficient weights distinct modulo 13. The same argument excludes a component of any order $-1\bmod26$ admitting consecutive integer vertex labels and edge sums. The remaining residue $s=26$ has a complementary component of order $1\bmod26$ and lies outside this argument. [Universal order restrictions](../rainbow/short-forests.md)

## Reproduction

The [exhaustive checker](check_double_prime_cut.cpp) tests actual affine images. For each pair of holes and port label, modulo unit symmetry, it enumerates every low edge set. It counts how many possible vertex holes admit a bridge by trying the affine permutations directly. This determines exactly how many low vertex sets obstruct the join. At 26 it checks all 708 piece orbits and all core inputs at each of the four relevant losses. At loss four this accounts for 8,309,822,950,000 normalized inputs, with 1,649,360 failing for the two given labelings. A [separate Python check](check_large_factor_cut.py) constructs and joins 560 pairs of actual trees, including prime-power factors with noninvertible ports and concentrated low edge sets. It also realizes 26 fixed pairs and exhausts their affine changes to certify the stated obstructions.

~~~sh
out=$(mktemp -d)
c++ -O3 -std=c++17 research/prime/check_double_prime_cut.cpp -o "$out/check"
"$out/check"
python3 -B -m research.prime.check_large_factor_cut
~~~
