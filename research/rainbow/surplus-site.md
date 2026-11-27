# A divisor test when one star attaches at the surplus

**Theorem.** On a fixed cordial core of order one modulo $k$, attach two stars of orders $s$ and $t=k-1-s$. The parent of the first star carries the surplus label. Subtract that label from all vertex labels; the parents now carry $0$ and $c$. The case $c=0$ always extends. Otherwise let $d$ be the additive order of $c$ in $\mathbb Z_k$. The old labeling extends exactly when there is a divisor $m\ge2$ of $k$ satisfying the corresponding row of this table. In each row $r=s\bmod m$ must also satisfy $r\le m-2$.

| Relation between the orders | Additional requirement |
|---|---|
| $d\nmid m$ | $s\ge m$ |
| $d\mid m$ and $m>d$ | $r\ge m/d-1$ |
| $m=d$ odd | $r\ge1$ |
| $m=d$ even | $r\ge2$ |

At **every odd prime power**, every such input extends. At **every power of two**, the only failures have $s=1$ and $c$ odd. At a general even modulus, setting $c=k/2$ specializes the table to the [antipodal classification](surplus-antipodes.md).

## The two ways to realize the center sum

Write $x,y$ for the centers of the stars at $0,c$. All free labels are distinct and nonzero. If the entering edge at $c$ supplies $x+y$, then $x=c$. The entering edge at zero cannot supply that weight since $y\ne0$. When $x\ne c$, the weight $x+y$ is absent and the moment gives $y=c+s(x-y)$. [Derivation from actual endpoint sums](two-star-surplus.md#a-quadratic-decision-procedure)

**Case $x=c$.** Put $h=y-c$, let $m$ be its order and $H=\langle h\rangle$. Take $B$ to be the $t-1$ leaf labels at $y$. With this star first, the histogram identity simplifies to
$$
                    (\tau^h-1)1_B=e_c-e_{c-(t-1)h}.
$$
On $c+H$, avoidance of $c$ forces the last $z=(t-1)\bmod m$ positions immediately before $c$ into $B$, and no other positions of that orbit. Other orbits are entirely in or entirely out. Avoiding $c+h$ requires $z\le m-2$. This excludes $r=m-1$ and gives $z=m-2-r$.

If $c\notin H$, the orbit $H$ cannot be taken because it contains zero. There are enough other whole orbits exactly when $\lfloor(t-1)/m\rfloor\le k/m-2$. With $r\le m-2$ this is equivalent to $s\ge m$. If $c\in H$, write $c=Ch$ with $1\le C<m$. The center $y$ is nonzero when $C\le m-2$. The selected segment avoids zero when $z<C$, or equivalently $r\ge m-1-C$. All outside orbits are available, so these conditions suffice.

**Case $x\ne c$.** Put $h=x-y$ and $m=|\langle h\rangle|$. Now $y=c+sh$. For the first star's $s-1$ leaves the same identity gives
$$
                    (\tau^h-1)1_B=e_0+e_{c+sh}-e_h-e_c .
$$
The right side is the translate difference of $U-e_0$, where $U$ is the multiset of $s$ consecutive positions beginning at $c$ in steps of $h$. Solutions therefore differ from $U-e_0$ by constants on the step orbits. Remove the full laps of $U$ and let $I$ be its last $r$ positions starting at $c$. The next position $y$ lies outside $I$ and is forbidden. Also $r\le m-2$, since $r=m-1$ would give $x=c$.

If $c\notin H$, the orbit $H$ must supply every label except zero, and $c+H$ supplies $I$. Hence $s-1\ge m-1+r$, implying the condition $s\ge m$ already obtained. If $c=Ch\in H$, the forbidden nonzero center $y$ fixes the indicator on $H$ to be $1_I-e_0$. This requires $0\in I$, or $r\ge m-C+1$. Conversely, in that range choose $I\setminus\{0\}$ in $H$ and $\lfloor s/m\rfloor$ full outside orbits. The two consecutive positions after $I$ are outside it and nonzero, and $x\ne c$. This constructs the required $B$.

## Optimizing the step of a given order

There is one subgroup of order $m$, so $c\in H$ exactly when $d\mid m$. For $d\mid m$ write $w=m/d$. As the generator $h$ varies, the possible positions $C$ are $w$ times the unit residues modulo $d$. Indeed every unit modulo $d$ lifts to a unit modulo $m$ by choosing a representative avoiding the additional prime divisors of $m$.

For $w\ge2$ the largest position is $C=m-w\le m-2$. It gives the second table row in the case $x=c$; the bound from $x\ne c$ is stronger. For $w=1$, the generator with $C=m-1$ realizes the case $x\ne c$ throughout $2\le r\le m-2$. In the case $x=c$ one needs a unit $C\le m-2$. When $m$ is odd, $m-2$ is such a unit and allows $r=1$ as well. When $m$ is even every such unit is at most $m-3$. This gives exactly the last two table rows, including the empty range at $m=2$.

## Prime powers

Let $k=p^e$. For odd $p$, take $m=d$ whenever $s\bmod d$ lies in $[1,d-2]$. In the remaining cases choose $D=s$ or $s+1$ divisible by $d$. Then $0<D<k$. Take $m=p^{1+v_p(D)}$, so $d<m\mid k$. The residue of $D$ modulo $m$ is between $m/p$ and $m-m/p$. Subtracting at most one gives $m/d-1\le s\bmod m\le m-2$, as required.

For $p=2$ and $d=2$, use $D=s$ for even $s$ and $D=s+1$ for odd $s$. Again $m=2^{1+v_2(D)}>d$ divides $k$ and the residue of $s$ is $m/2$ or $m/2-1$, both in the allowed range. For $d\ge4$, the choice $m=d$ handles residues $2$ through $d-2$. For $s>1$ and residue $0,1$ or $d-1$, choose $D=s,s-1$ or $s+1$, respectively. With $m=2^{1+v_2(D)}$ we have $m\ge8$ and $s\bmod m$ differs by at most one from $m/2$. This satisfies the second row. For $s=1$ and $d<k$ use $m=2d$. For $s=1$ and $d=k$, the first row would require $s\ge2$ and the last requires $r\ge2$. In a cyclic group of order a power of two, $d=k$ means precisely that $c$ is odd.

The [divisor implementation](two_star_surplus.py) and [independent endpoint search](check_surplus_pairs.cpp) verify all $s,c$ at every modulus from 3 through 63. [Reproduction commands](two-star-surplus.md#verification)
