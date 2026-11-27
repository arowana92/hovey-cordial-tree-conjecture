# Two-star obstructions at antipodal sites and semiprime moduli

Use the full [divisible-core packet](two-star-extension.md#one-full-period) of two stars of orders $s,t$ with $s+t=k$. The old parents have labels $a,b$ and the old edge deficit is $D$. Set $P=D-a-b$ and $Q=b-a$. Translations preserve $P,Q$ and multiply the shift of an edge deficit by two relative to the shift of a vertex. Normalize the first parent to zero.

## Antipodal sites at every even modulus

Suppose $k=2n$, $Q=n$ and $D=2a$. The prescribed labeling fails to extend exactly when
$$
                    2^{v_2(k)}\mid s
             \quad\text{and}\quad \gcd(n,s^2-1)=1 .
$$
The first condition means $s$ contains the entire power of two dividing $k$. Without it, $\gcd(s,k)\mid n$ and the first-center construction works. Assume it holds. Then $P=n$ and the forced-center lemma applies. For the orientation with second center zero and first center $h$, the leaf-indicator equation becomes
$$
       (\tau^h-1)1_B=2e_0-e_n-e_{n-(s-1)h}.
$$
An indicator difference can have no coefficient greater than 1. Hence $(s-1)h=n$ and the right side is $e_0-e_n$. On the orbit of zero, $B$ must run from $n$ to just before zero in steps of $h$. The order $L$ of $h$ is even, and $n=(L/2)h$. When $L=2$ this segment uses the first center $h$, so it is impossible. For $L\ge4$ the segment avoids both centers. Add enough whole outside orbits to reach $s-1$ labels. This is possible since $s-1\equiv L/2\pmod L$ and $s-1<k$.

Here $s-1$ is odd. An even divisor $L\ge4$ of $k$ meeting that congruence exists exactly when some odd divisor $u>1$ of $n$ divides $s-1$. Take $L=2u$; the quotient $(s-1)/u$ is odd. Exchanging the two stars preserves the normalized antipodal boundary and changes $s-1$ to $t-1\equiv-(s+1)\pmod n$. These possibilities give the displayed test. For $s=2$ it recovers the [earlier two-star example](ten-prescribed.md#exact-two-star-criterion-for-every-even-modulus).

## Complete classification at twice an odd prime

Let $k=2p$ with $p$ odd and prime. Assume the elementary gcd construction fails. By the [subgroup reduction](two-star-extension.md#reduction-to-a-subgroup), any obstruction has $Q\in\langle P\rangle$ and the order of $P$ divides $s$. Thus it suffices to consider orders $2$ and $p$.

If $P$ has order two, then $P=p$, $s,t$ are even and $Q$ is 0 or $p$. For $Q=0$ take the smaller star first and use $h=1$ and the $s-1$ consecutive first-star leaf labels $p-s+1,\ldots,p-1$. The first position is at least two because $s$ is even and $s\le p-1$. The translate difference is $e_p-e_{p-(s-1)}$, as required. For $Q=p$, the antipodal test gives failure exactly when $s\notin\{p-1,p+1\}$.

If $P$ has order $p$, both stars have order $p$, and $Q,P$ are even. For $Q\ne0$, choose a unit $h$ such that $(p-1)h=P$. This is possible since $\gcd(p-1,2p)=2$ and $P$ is nonzero modulo $p$. In units of $h$, the new deficit is zero and the required difference is $e_{Q+p-1}-e_Q$, writing $Q$ now for its scaled coordinate. One of $Q,-Q$ is an even integer between 2 and $p-1$. Choose that orientation, and use the interval of $p-1$ positions beginning there. It avoids 0 and 1. If $Q=0$, choose a unit with $(p-1)h=-P$ and use positions $2,\ldots,p$ instead. They produce the required $e_{p+1}-e_2$. This rules out all further obstructions.

Thus the only failures at 26 have $b-a=13$, $D=2a$ and smaller star size $2,4,6,8,10$. The split $12+14$ always works. The result and positive constructions hold for all actual old labels and all tree orders divisible by 26.

## A failure at every product of distinct primes except six

Let $k=p\ell$ with distinct primes $p<\ell$ and $\ell>p+1$. Attach stars of sizes $p,k-p$. In coordinates with first parent zero, take any nonzero $P,Q$ in the order-$p$ subgroup $H$, and old deficit $Q+P$. All these prescribed inputs fail. For example take $Q=\ell$, $P=-\ell$, and use the $k$-vertex star centered at zero as the old core. This exhibits an actual fixed-label obstruction on a caterpillar.

The gcd criterion fails since $p\nmid P$. Try either orientation with second center zero and first center $h$. Both orientations keep $P,Q$ nonzero in $H$. If $h$ has order $p$, all histogram defects in (1) lie in $H$, and every outside orbit contributes either 0 or $p$ first-star leaves. The required first-leaf count is $-1\pmod p$, but at most $p-2$ labels of $H$ are available after reserving its two centers. If $h$ has order $\ell$, summing (1) in the quotient by $\langle h\rangle$ requires the multisets $\{0,Q+P\}$ and $\{Q,P\}$ to agree there. Neither of the latter entries is zero.

It remains to try a generator $h$. In units of $h$ all coordinates in $H$ are multiples of $\ell$. In (1) the negative term at $Q$ cannot cancel either positive term, since $Q\ne0$ and $P\ne0$. The corresponding occupied interval begins at $Q$ and ends just before 0 or $Q+P$. Its length is at least $\ell$, the smallest positive distance between distinct multiples of $\ell$ in this cyclic order. If the first star has size $p$, it has only $p-1$ leaf labels. In the reversed size case, apply the same argument to the complement of $B$: its interval ending just before $Q$ must start at 0 or $Q+P$. Now the complement has size $p+1<\ell$. Both orientations are impossible.

Every pair of distinct primes except $2,3$ satisfies the required inequality. The twice-prime classification gives no failures at six. Together with the [prime-power theorem](two-star-extension.md#every-prime-power-modulus), this identifies which semiprime moduli admit unconditional fixed-core extensions across all two-star packets. [Literal and whole-tree checks](check_two_star_extension.py)
