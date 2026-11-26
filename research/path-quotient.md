# An odd path of cordial trees

**Theorem.** Join an odd number $q\ge3$ of equally large $m$-cordial trees in a path, using any attachment vertices in the pieces. The result is $qm$-cordial if $q$ and $m$ are coprime. If $g=\gcd(q,m)>1$, let $p$ be its smallest prime divisor and $s$ the common piece order. The same conclusion holds whenever
$$
(s-1)\bmod m < m-m/p .
$$
The result includes a bijection with distinct edge sums at $s=m$ in the coprime case. At $s=m$ the conclusion also holds for *every* $m$ if an end piece is a star and the connecting edge meets it at a leaf.

## One congruence for the path

Use successive low labels $0,1,\ldots,q-1$ along the quotient path. The edge sums $2i+1$ for $0\le i<q-1$ are distinct modulo $q$. Write $r=(q-1)/2$ for the omitted midpoint and $d=2^{-1}\bmod q$. Each used midpoint $c$ has arrows to $c-d,c+d$. In step-$d$ order these give a bidirected cycle with its root row omitted. An arborescence selects an edge of the underlying cycle to delete and orients the remainder toward $r$. Thus the [quotient determinant](odd-quotient.md) is exactly $q$ and its coprime lifting theorem applies.

For a fixed right-hand side $h_c$ in the translation equations, there is also an exact solvability criterion. Put $c_j=r+jd\pmod q$ and $z_j=t_{c_j}$, with $z_0=z_q=0$. For the consecutive differences $e_j=z_j-z_{j-1}$, the equations say $e_{j+1}=e_j-h_{c_j}$ for $1\le j<q$. The endpoint condition is
$$
q e_1=\sum_{j=1}^{q-1}(q-j)h_{c_j}\pmod m.
$$
This is solvable exactly when $\sum_{c\ne r}(c-r)h_c=0\pmod g$, since $j=2(c_j-r)\pmod q$ and $g$ is odd.

## Choosing high labels and low slots

Fix an $m$-cordial labeling in each piece. In piece $i$, call its labels at the left and right attachments $a_i^-,a_i^+$, omitting nonexistent terms at the ends. For $i\ne r$, let $w_i$ be a weight with minimum internal frequency. Set
$$
B_i=i a_i^-+(i+1)a_i^+-(i-r)w_i \pmod g,
$$
omitting the slot term at $r$. Multiplying the entire high labeling and its slot by any unit $u_i$ modulo $m$ preserves internal balance. The translation criterion becomes
$$
r^2+\sum_{i=0}^{q-1}u_i B_i=0\pmod g .
$$
Indeed the midpoint of edge $(i,i+1)$ has coefficient $c-r=i+1\pmod q$. Its carry $(2i+1-2c)/q$ is $-1$ for $i<r$ and $1$ for $i\ge r$, taking representatives in $[0,q-1]$. The weighted carry sum modulo $g$ is therefore $\sum_{j=r+1}^{2r}j-\sum_{j=1}^r j=r^2$. This is a unit because $2r=q-1$.

**Exact test for this lift.** For these fixed internal labelings and fixed low cosets, translations, independent unit multipliers and slot choices succeed exactly when there is a choice of slots for which $\gcd(g,B_0,\ldots,B_{q-1})=1$. Necessity follows from the displayed equation. For sufficiency, for each prime $p\mid g$ choose an index where $B_i$ is nonzero modulo $p$. Starting from unit multipliers all equal to 1, changing this index to $-1$ alters the total by a nonzero value modulo the odd prime $p$. One choice gives a nonzero total. Choose these local signs simultaneously by the Chinese remainder theorem, using 1 at prime factors of $m$ outside $g$. This gives units modulo $m$ whose total $S=\sum_i u_iB_i$ is coprime to $g$. Multiply all units by a common unit lifting $-r^2/S$ modulo $g$. Such a lift exists by the Chinese remainder theorem. The resulting equations have translations by the preceding calculation. Adding one weight at a low slot in each active coset gives exactly the [required global histograms](odd-quotient.md#solving-for-translations-within-the-pieces).

For the stated uniform bound, there are $m-((s-1)\bmod m)$ choices of each slot. Assign a different active index $i$ to each prime $p'\mid g$, with $i-r$ nonzero modulo $p'$. Take distinct coefficients $i-r$ that are units modulo $g$. There are at least as many such residues as distinct prime factors, since $\varphi(g)\ge2^{\omega(g)}$ for odd $g$. For each assigned index, more than $m/p'$ available slots allow a choice with $B_i\ne0\pmod {p'}$. The exact test applies.

At $s=m$, an end star with center label 0 may give its attaching leaf label 1 and the other leaves the remaining nonzero labels. Its missing internal slot is zero. Place it first in the path, giving $B_0=1$, which passes the exact test for every $g$.

The criterion also exhibits a limitation for every noncoprime pair $q,m$. Take $q$ stars of order $m$ with all connections between their centers. In any bijective high labeling write $z_i$ for the center label, making the unique missing slot $2z_i$. Then each $B_i$ vanishes modulo $g$ since the endpoint coefficients total $2i+1\pmod q$, including at the ends. These stars admit no cordial lift with the prescribed successive low cosets when $g>1$. The ordinary tree is a caterpillar and is cordial at every modulus by [Hovey's theorem](https://doi.org/10.1016/0012-365X(91)90254-Y).

## Verification

The checker solves the difference equations, constructs full tree labelings and counts all vertex and edge residues. Among 2,832 instances on paths of up to 45 pieces, it constructs 2,766 full labelings and identifies 66 obstructions to this lift. On 45 small instances it independently tries the units and translations and compares the resulting full histograms with the arithmetic test.

~~~sh
python3 -B -m research.check_path_quotient
~~~
