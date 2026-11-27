# A new center on a core of order one modulo the modulus

Fix a cordial core of order one modulo $k$, and translate its surplus label to zero. Add one new center, $c$ leaf children of that center and $s$ externally attached singleton leaves. The center attaches to an old vertex. First suppose the center's old parent has label $p$, the singleton parents all have label $b$, and there are no edge offsets.

**Theorem.** For $c+s+1=qk$, every attachment with $q\ge2$ extends the prescribed labeling. For $q=1$ and $b=0$ it extends exactly when $\gcd(c,k)\mid p$ or $\gcd(c+1,k)\mid p$. With arbitrary $p,b,q$ the cycle equations below determine all possible center labels.

For a prime-power modulus, arbitrary singleton-parent colors and arbitrary additive offsets on the new edges are allowed, and every such attachment on **at least $k$ new vertices** extends. Conversely, every modulus with two distinct prime divisors admits a one-period example with ordinary edge sums that fails to extend.

## Equations for equal singleton-parent labels

Fix center label $a$, set $d=a-b$, and write $B,C$ for child and singleton label multiplicities. We must add exactly $q$ edges of each weight because the initial and final edge histograms are uniform. If $x$ is the new surplus, the new vertex counts must be $q\mathbf1-e_0+e_x$. Let $z^d$ denote the shift taking $e_i$ to $e_{i+d}$. Subtract $b$ from the edge weights. The vertex and edge equations become
$$
e_a+B+C=q\mathbf1-e_0+e_x,\qquad e_{p+d}+z^dB+C=q\mathbf1 .
$$
Thus
$$
(z^d-1)B=e_0+e_a-e_x-e_{p+d},\quad
x=b-p-cd,\quad
0\le B_i\le q-\mathbf1_{i=p},\quad \sum B_i=c.
$$
The identity for $x$ comes from the first moment of the difference equation. These constraints suffice, since $C=q\mathbf1-e_{p+d}-z^d B$ is then nonnegative and realizes both histograms.

On each orbit of $i\mapsto i+d$ the right-hand side must sum to zero. If so, integration gives a particular integer solution for that orbit, unique up to an integer constant. Intersecting the coordinate bounds gives a possibly empty interval of allowable constants. Each unit increase raises the mass by the common orbit length $h=k/\gcd(k,d)$. Hence the attainable masses are exactly an arithmetic progression whose extrema come from the interval endpoints. This is an exact finite construction for a prescribed center.

## Two or more periods

For any $0\le t<k$, one can choose $t$ distinct residues with indicator $U$ such that $(z^d-1)U=e_{y+td}-e_y$. Write $t=jh+r$ with $0\le r<h$. Use the first $r$ sites from $y$ in steps of $d$ and all sites of $j$ other orbits. The inequality $t<k$ supplies enough other orbits.

For $q=2$ either $c<k$ or $s<k$. In the first case take $a=b-p$. Then $p+d=0$, $x=a-cd$, and the right-hand side is $e_a-e_x$. Apply the distinct-residue construction with $y=x,t=c$ to obtain $B$. Since $B$ is an indicator, its upper bounds hold. In the second case take $a=p$ and put $B'=2\mathbf1-e_p-B$. The desired equation is now $(z^d-1)B'=e_x-e_0$, with $x=sd$ and $\sum B'=s$. Take the indicator with $y=0,t=s$. Both $B$ and $B'$ obey the required coordinate bounds. This also covers $d=0$.

If $q>2$, at least one of the two leaf groups has $k$ vertices. Set aside $k$ leaves from one group and repeat until two periods remain. Restore each unused group with one of every label. The $k$ weights in that group also form a permutation since all its parent labels agree.

## Two sufficient congruences for arbitrary boundary colors and offsets

For each externally attached row $i$ let $b_i$ be its old parent label plus its edge offset. For each center child let $b_i$ be its edge offset alone. Put $T=\sum_i b_i$. If either $ca=-T$ or $(c+1)a=-T$ is soluble modulo $k$, there is a cordial extension. For the first congruence use the [uniform-increment construction](../biased/pinned-periods.md#exact-uniform-increments-with-one-free-parent) with center $a$. For the second, add $a$ to each child shift and also to the center row's shift. The resulting list of $qk$ shifts has sum zero. Partition it into zero-sum blocks of $k$ by Erdős–Ginzburg–Ziv. On each block Hall's permutation theorem realizes the shifts as destinations minus sources of two permutations. Translate both permutations on the center's block so its source is zero. Finally change the actual center source to $a$ and remove the extra $a$ from its row's shift. All destinations are preserved. Its children already have the correct actual shift. This gives uniform edge increments and shifts the old surplus from zero to $a$. [Hall (1952)](https://doi.org/10.1090/S0002-9939-1952-0050579-7) · [Erdős–Ginzburg–Ziv (1961)](https://www.renyi.hu/~p_erdos/1961-25.pdf)

At a prime power one of $c,c+1$ is a unit. For $qk+r$ new vertices with $q\ge1$ and $0<r<k$, set aside $r$ leaves, retaining the center. The whole-period result leaves a one-surplus core. The $r$ remaining leaf shifts are fixed. Pad the list to length $k$ and sum zero, and realize it by Hall's permutations. Translate so one dummy source equals the surplus. The real sources then avoid that surplus, and both the real sources and weights are pairwise distinct. This restores all leaves with both profiles balanced.

## Necessity for one period when $b=0$

For $p=0$ the first congruence has solution $a=0$. Take $p\ne0$. A center $a=0$ is impossible, since the cycle equation with $d=0$ would require $e_x+e_p=2e_0$. For $a\ne0$, adding the equations at the distinct coordinates zero and $a$ gives
$$
B_{-a}-B_a=2-\mathbf1_{x\in\{0,a\}}-\mathbf1_{p+a\in\{0,a\}} .
$$
If $p+a\ne0$ the last indicator is zero since $p\ne0$; the left side is at most one. If $p+a=0$ then $B_{-a}=B_p=0$, and the left side is at most zero. In each case $x$ lies in $\{0,a\}$. Hence $x=-p-ca$ implies one of the two claimed congruences, already proved sufficient. For two distinct prime factors $l_1,l_2$ of $k$, choose $0\le c<k$ with $c=0\pmod{l_1}$ and $c=-1\pmod{l_2}$. Neither congruence then permits $p=1$. Such a core exists, for instance a star on $k+1$ vertices with center zero and leaves using all residues.

## Reproduction

~~~sh
python3 -B -m research.rainbow.check_star_period
~~~

The checker compares all prescribed centers against 12,800 independent child-multiset enumerations, tests the one-period equivalence in 25,584 cases through modulus 42, and checks multiplicities on 342 constructed packets with arbitrary offsets. The unrestricted conclusions use the preceding arguments. [Constructions](star_period.py) · [Independent checks](check_star_period.py)
