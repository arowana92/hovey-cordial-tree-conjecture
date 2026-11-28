# Two stars giving exact uniform increments at every modulus

Attach stars of positive orders $s,t$ by their centers to old vertices labeled $a,b$ in $G=\mathbb Z_k$. A singleton is allowed, and the old sites may coincide. Let $s+t=qk$. We ask for exactly $q$ copies of **each residue** among the new vertices and among all new edges, including the two entering edges. Such an attachment preserves any cordial old labeling at any order and also makes sense when the old labeling is arbitrary.

**Theorem.** Put $\delta=b-a$. For two or more periods ($q\ge2$), a labeling exists exactly when $\gcd(k,s-1,2)\mid\delta$. Thus at odd $k$ every split and every pair of old labels work. At even $k$ the sole excluded case has both star orders odd and the old labels of opposite parity.

For one period ($q=1$), let $g_1=\gcd(k,s-1)$ and $g_2=\gcd(k,t-1)$. A labeling exists exactly when **at least one** $g\in\{g_1,g_2\}$ satisfies
$$
                 g\mid\delta\quad\text{and}\quad
                 (g>1\ \text{or}\ s\delta\ne0\text{ in }G).
$$
At the same parent label this reduces to $\gcd(k,s^2-1)>1$. In particular, for every prime $p\ge5$ and every $2\le s\le p-2$, the pair of stars on $p$ vertices works precisely at unequal parent labels. At $k=8$ the split $4+4$ fails at every parent difference of even parity and succeeds at every odd difference. These failures concern the uniform increment. The [ordinary two-star extension theorem](two-star-moduli.md) allows a change in the deficient old weight.

## The counting identity

Translate all labels to put the first parent at zero and the second at $\delta$. Let the centers have labels $x,y$, put $h=x-y$, and let $f(z)$ count first-star leaves labeled $z$. Write $e_u$ for the unit mass at $u$, $\boldsymbol 1$ for the all-ones vector and $(\tau_h f)(z)=f(z-h)$. For uniform new vertex counts, the second-star leaf vector must equal $q\boldsymbol 1-e_x-e_y-f$. Translate all new edge weights down by $y$. The two entering edges give $h,\delta$, and the leaf edges give $\tau_h f$ and the second leaf vector. Consequently the problem is equivalent to
$$
 (\tau_h-1)f=e_x+e_y-e_h-e_\delta,\qquad
 0\le f\le q\boldsymbol 1-e_x-e_y,\qquad \sum f=s-1.                 \tag{1}
$$
Also, subtracting the sum of the new labels from the sum of the new edge weights yields $(s-1)x+(t-1)y+\delta=0$ in $G$. Thus $\gcd(k,s-1,t-1)=\gcd(k,s-1,2)$ divides $\delta$.

## One period

The center labels are distinct. No leaf edge can give weight $x+y$, because its leaf would have to repeat the other center's label. Thus the first entering edge gives $x+y$ and $y=0$, or the second does and $x=\delta$. Exchanging the stars and translating reduces the latter case to the former with difference $-\delta$. When $y=0$, we have $x=h\ne0$ and distinct entering weights force $h\ne\delta$. Equation (1) reduces to $(\tau_h-1)f=e_0-e_\delta$. Taking its first moment gives $(s-1)h=-\delta$.

Conversely let $h\notin\{0,\delta\}$ solve this congruence. Write $H=\langle h\rangle$, $L=|H|$ and $r=(s-1)\bmod L$. Give the first star the $r$ leaves $-h,-2h,\ldots,-rh$. This interval avoids both centers, since $-rh=\delta\ne h$ implies $r\le L-2$. Its translate difference is $e_0-e_\delta$, also when $r=0$. Add $(s-1-r)/L$ whole other cosets of $H$, which exist since $s-1<k$. The resulting vector satisfies (1).

The congruence is solvable precisely when $g_1\mid\delta$, with $g_1$ solutions. At $\delta=0$ one must discard zero. Otherwise zero is already excluded, and the only further inadmissible solution is $h=\delta$ when $s\delta=0$. This proves the stated oriented test. In the other orientation $t(-\delta)=s\delta$ in $G$. At $\delta=0$ use $t-1\equiv-(s+1)\pmod k$ for the simplification.

## Two periods

Exchange the stars if needed so $s\le k$. For $\delta=0$, put both centers at zero. Allocate the $s-1$ first leaves from two copies of each nonzero label, then give the rest to the other center. Every new edge has the same label as its new lower endpoint.

Now let $\delta\ne0$, assume the divisibility test passes and let $L_0$ be its additive order. Put $r=(s-1)\bmod L_0$. We construct $h\ne0$, $y$ and $x=y+h$. An interval starting at $u$ of length $d$ in step $h$ has translate difference $e_{u+dh}-e_u$, including for length zero.

- If $r$ is odd, put $h=\delta$ and $d=(r+1)/2$. Set $y=dh$. Use intervals starting at $h$ and $\delta$ of lengths $d$ and $d-1$. Their respective ends, excluded from those intervals, are $x$ and $y$.
- If $r$ is even and $L_0$ is odd, put $h=((L_0+1)/2)\delta$. Then $2h=\delta$ and $h$ has order $L_0$.
- If $r$ and $L_0$ are even, $s$ is odd and $k$ even. The test makes the standard representative of $\delta$ even. Take half that representative for $h$. Its order is $2L_0$, since the order of $2h$ is even and equals $L_0$. Replace $r$ by $(s-1)\bmod 2L_0$, still even.

In the last two cases take $d=r/2$, $y=(d+1)h$ and intervals of length $d$ starting at $h$ and $\delta=2h$. Their excluded ends are $y$ and $x$. In all cases their summed indicators give the required translate difference. Each interval is shorter than $L=|\langle h\rangle|$ and misses its own end. Thus the sum is at most two everywhere and at most one at each of the two distinct centers. Its mass is $r$. Add $(s-1-r)/L$ whole cosets outside $\langle h\rangle$, possible since $s-1<k$. The complement in (1) labels the second star.

## More periods

While $s+t>2k$, at least one star has more than $k$ vertices. Remove $k$ leaves from it. The solvability test is invariant because the star orders change by multiples of $k$. After the two-period construction, restore each removed batch with one copy of every label. Adding its center label permutes those residues on the new edges. This completes the proof for all orders and degrees.

## Reproduction

The [constructor](neutral_stars.py) outputs both center labels and the two full leaf histograms. The [independent checker](check_neutral_stars.py) tries every pair of centers and every allocation of the remaining vertex multiset at $k\le9$ through two periods, and at $k\le6$ through three. It counts actual edge sums, leaving the second entering edge until last to recover the possible parent difference. All 1,017 decisions agree, including 154 exclusions. On a larger grid it recounts 127,938 constructed pairs of histograms and independently checks 18,642 exclusions. Another 1,051 witnesses include examples up to 270 labels and 100,000 periods.

~~~sh
python3 -B -m research.rainbow.check_neutral_stars
~~~

The [general forest theorem](../bounded-degree/forest-period.md) gives the gcd criterion asymptotically under a degree-excess bound. A star of order proportional to the whole forest can violate that bound. The two-star result above has no size threshold or degree restriction.
