# Solving the quotient equations by deleting leaves

**Prime-factor theorem.** Let $q\ge3$ be odd. Join $q$ equally large $p$-cordial trees by edges forming a quotient tree with a bijection onto $\mathbb Z_q$ and distinct edge sums. For **every prime** $p$ and common piece order $s$ with $p\nmid s$, the resulting tree is $qp$-cordial. Attachments may occur at any vertices, including the same vertex for several connecting edges. For $p=2$, or whenever the quotient determinant is coprime to $p$, every $s$ works.

The prime theorem is a special case of the following general bound. Use the [odd quotient matrix](odd-quotient.md) $M$ and its determinant $D$. Set $g=\gcd(D,m)$, which is odd. If $g=1$ every order works. When $g>1$ is a power of a prime $p$, it suffices for each active piece to have more than $m/p$ minimum-frequency internal weights. At equal order $s$ this means
$$
(s-1)\bmod m < m-m/p .
$$
There is also a bound covering **every** $g$: at least $\lceil m/2\rceil$ minimum-frequency weights per active piece always suffice. When $m=p$ is prime, at least two such weights are available exactly when $p\nmid s$. The [center-joined stars](path-quotient.md) show that at $p\mid s$ a prescribed quotient labeling can obstruct this construction.

## The local condition over an odd modulus

Retain the notation of the quotient proof. For each active midpoint $c$, let $W_c\subseteq\mathbb Z_m$ be its allowed internal slots. For cordiality take all minimum-frequency weights. Write $a_{ic}$ for the high label at the attachment in endpoint piece $i$ of this row. Allow an independent unit multiplier $u_i$ and translation $t_i$ in each piece. For the edge $ij$ with midpoint $c$ we want
$$
2t_c+u_cw_c=\eta_c+t_i+u_i a_{ic}+t_j+u_j a_{jc},\qquad w_c\in W_c,
$$
where $\eta_c=(i+j-2c)/q$ uses the standard integer representatives.

First solve the equations modulo $g$. Delete ordinary leaves of the **quotient tree** one at a time, with the last isolated vertex deleted as well. On deleting vertex $v$, remove all still-present rows containing it. At most one such row has it as midpoint. At most one other row has it as endpoint: any such row comes from a surviving quotient edge incident to the leaf. Each row has three distinct variables.

Restore the vertices in reverse order. For any row restored now, the other two variables are already assigned. Leave each slot unassigned until its own row is restored. A single row at $v$ can always be satisfied, since the coefficient of $t_v$ is either 2 or $-1$, both units modulo $g$. If two rows return, write $a$ for the label of the endpoint in piece $v$ and $b$ for the midpoint of that endpoint row. With constants $H,K$ determined by the previously assigned variables, the equations are
$$
2t_v+u_v w_v=H,\qquad t_v+u_v a=K+u_b w_b .
$$
Thus it suffices to find $w_v,w_b$ and a unit $u_v$ with
$$
u_v(w_v-2a)=H-2K-2u_b w_b\pmod g .
$$
The two sides before choosing $u_v$ range over affine images of $W_v,W_b$ reduced modulo $g$, with unit slopes. Multiplication by units acts transitively on residues with the same gcd with $g$. This follows prime power by prime power by dividing off the common valuation and then applying the Chinese remainder theorem. Thus it suffices for the two sets to meet the same gcd class.

When $g$ is a power of $p$, more than $m/p$ slots ensure that each image contains a unit. For any odd $g$, at least $\lceil m/2\rceil$ slots give images of size at least $\lceil g/2\rceil>g/2$, so the two images even intersect. Either condition suffices at every leaf. Once a common gcd is found, choose $u_v$ and use the second equation to give $t_v$.

Lift each multiplier to a unit modulo $m$ and take any lifts of the translations. Subtract the common root translation to normalize $t_r=0$. Each row error is divisible by $g$. Since $M\operatorname{adj}(M)=D I$, every such error vector is in the image of $M$ modulo $m$. Correcting the translations simultaneously solves the original equations while retaining all chosen slots. The global histogram argument is the same as in the [quotient theorem](odd-quotient.md#solving-for-translations-within-the-pieces). The proof also permits different piece orders under its vertex and edge capacity conditions.

## A sharper computable bound

The gcd classes modulo $g$ have sizes $\varphi(d)$, one for each divisor $d$ of $g$, indexed by the additive order $d$. Define
$$
B(g)=\max_{I\subseteq\{d:d\mid g\}}
\min\left(\sum_{d\in I}\varphi(d),\ g-\sum_{d\in I}\varphi(d)\right).
$$
Two subsets each of size greater than $B(g)$ must meet the same class. Otherwise assign the full classes that meet the first set to one side, and all remaining classes to the other side. Conversely the maximizing partition gives two such disjoint unions of classes. Hence $|W_c|>m B(g)/g$ suffices. This cutoff is exact for the local problem with arbitrary slot sets. It need only be sufficient for actual trees. For a prime power $g=p^e$ with $p$ odd, the unit class has size $g-g/p>g/2$, and $B(g)=g/p$.

One can also use the integer $E=D/\gcd(D,\{\operatorname{adj}(M)_{ij}\}_{ij})$ in place of $D$. Dividing the adjugate by the same common divisor gives an integer matrix $N$ with $MN=EI$. This sharpens the final correction to $g=\gcd(E,m)$. In fact $E$ is the least possible such positive integer, as $N=E M^{-1}$ is forced.

## Verification

The checker chooses the leaf order on the actual quotient tree, solves for units and slots at each returning leaf, lifts the congruences, and recomputes the complete vertex and edge histograms. It reconstructs 5,180 full labelings. The greedy choices fail on 242 trials outside the sufficient bound. It checks the number of live equations at each step and tests the gcd-class cutoff independently on 33,448 subsets by direct multiplication by units.

~~~sh
python3 -B -m research.check_quotient_peeling
~~~
