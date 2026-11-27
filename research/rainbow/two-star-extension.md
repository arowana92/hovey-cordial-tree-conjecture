# Two stars at independently prescribed vertices

**Theorem.** Fix any $k$-cordial labeling of a finite tree whose order is divisible by $k$. Attach two disjoint stars, of orders $s,t\ge1$, by one edge from each center to a prescribed old vertex. The sites may coincide. The old labeling extends whenever **$s+t\ne k$**. At **every prime power**, it extends for **all** $s,t$. Modulus one is immediate.

For a full period $s+t=k$ there is a constructive exact test at every modulus. At $k=2p$ for an odd prime $p$, the only failures have old parent labels differing by $p$, old edge deficit equal to twice the first parent label, and even $s\notin\{p-1,p+1\}$. At **26** this gives precisely the smaller star orders **2, 4, 6, 8, 10**. These failures prescribe the old labeling. They occur on caterpillars, which have ordinary cordial labelings at every modulus. [Classification at twice a prime and other semiprimes](two-star-semiprimes.md)

Compare this final-count requirement with [cordiality on every intermediate prefix](two-star-growth.md). At 26, two stars of order 14 each can obstruct growth through cordial prefixes. Their final 28-vertex attachment always extends the prescribed labeling.

## One full period

Write $a,b$ for the old parent labels, $D$ for the deficient old edge weight, and
$$
         P=D-a-b,\qquad Q=b-a,\qquad H=\langle P\rangle,\qquad m=|H|.
$$
The two free centers have labels $x,y$. All $k$ free vertex labels must occur once. The multiset of new weights must be $G+\{D\}-\{D'\}$ for some new edge deficit $D'$, where $G=\mathbb Z_k$ contains each residue once. The moment obtained by summing the actual edge weights is
$$
                D'=D-a-b-(s-1)x-(t-1)y .
$$
All calculations take place in $G$ unless indices are given as integers.

When $\gcd(s,k)\mid P$, filling the deficit on the first center already gives an extension by the [pinned-star construction](../eight/growth-orders.md#two-stars-at-any-modulus). Otherwise every successful labeling must have $y=a$ or $x=b$. Indeed, no leaf can produce weight $x+y$, since it would need the label of the opposite center. Unless an entering edge produces it, it must be the missing weight $D'=x+y$. The moment then gives $s(x-y)=P$, which is impossible. Lean checks this implication directly on the lists of actual endpoint sums, including the case when deficits coincide. [Lean proof](TwoStarPacket.lean)

Translate all labels by $-a$. Now the old parents are $0,Q$ and the deficit is $Q+P$. Try center labels $h,0$ and let $B$ be the $s-1$ first-star leaf labels. All residues outside $\{0,h\}\cup B$ go to the other star. Writing $e_i$ for a unit histogram and $\tau^h$ for translation, the exact condition is
$$
  (\tau^h-1)1_B=e_0+e_{Q+P}-e_Q-e_{P-(s-1)h},\qquad B\cap\{0,h\}=\varnothing. \tag{1}
$$
This follows by replacing the weights at the first-star leaves by their $h$-translates and including both root edges. Trying the opposite orientation permits the other possible center coincidence.

### When the discrepancy generates the group

Scale by a unit so $P=1$ and work with $s,t\ge2$. A singleton star already meets the gcd criterion. In the following table the second center is zero. All the given first-star leaf sets have size $s-1$ and avoid the center labels. Substitution into (1) gives the indicated new deficit.

| Old second parent $Q$ | First center $h$ | First-star leaf labels $B$ | $D'$ |
|---|---:|---|---:|
| $0$ | $-1$ | $2,\ldots,s$ | $s$ |
| $1$ | $-1$ | $\{1\}\cup\{3,\ldots,s\}$ | $s$ |
| $2\le Q\le k-s+1$ | $1$ | $\{Q\}\cup\{-1,\ldots,-(s-2)\}$ | $2-s$ |

Empty ranges contribute nothing. Exchanging the stars and translating normalizes $Q$ to $-Q$ and leaves $P$ unchanged. The last row in that orientation covers $k-s-1\le Q\le k-2$, and the second row covers $Q=k-1$. Together they cover every input.

### Reduction to a subgroup

Only the case $\gcd(s,k)\nmid P$ remains, so $m>1$. A failure requires **both $Q\in H$ and $m\mid s$**.

If $Q\in H$ and $r=s\bmod m$ is nonzero, identify $H$ with $\mathbb Z_m$ by sending 1 to $P$. Solve the preceding generator case with star orders $r,m-r$ in $H$. Allocate every other whole coset of $H$ to the leaves of one center or the other, using $(s-r)/m$ cosets on the first side. Adding its center label permutes that entire coset. Each outside residue therefore occurs once in both histograms.

If $Q\notin H$, choose the smaller star first, so $2\le s\le k/2$. Put $h=P$. Write $s-2=jm+r$, $0\le r<m$. In fact $r\le m-2$, since $s\equiv1\pmod m$ would give $\gcd(s,m)=1$ and hence $\gcd(s,k)\mid k/m\mid P$. Use $Q$, the labels $-P,\ldots,-rP$, and $j$ whole cosets disjoint from $H$ and $Q+H$ for $B$. There is room because $m\le k/2$ and $s-2<k-m$. The negative segment avoids $0,P$. Its translate replaces $-rP$ by zero, also as a zero difference when $r=0$. The translate of $Q$ gives $Q+P$. This is precisely (1), with $D'=-rP$.

### All sizes other than one period

Below $k$ the two-star growth construction already works. Above $k$, choose $j$ vertices of the first star and $k-j$ of the second, including both centers. If a star has at least $k$ vertices then $j=1$ or $k-1$ is possible and satisfies the gcd criterion. Otherwise the possible $j$ form the interval $[k-t,s]$ of length at least two. For $P=0$ every split works. For $P\ne0$, take a split outside the multiples of $m$. The preceding subgroup argument labels the full packet and leaves a cordial tree of divisible order. All remaining vertices are leaves at already labeled parents. Hall's leaf extension finishes them. [Leaf extension](../counterexample-bound.md#removing-leaves)

Any number of extra singleton leaves at arbitrary old sites can be included whenever such a full packet is available. The same holds for a **third star** at an arbitrary site. After the first packet, give the third center the label that fills the new edge deficit. The remaining vertices are all leaves at a one-surplus core and extend in batches. In particular three stars of total order greater than $3k/2$ extend at every modulus, since the two largest together exceed $k$. At a prime power two stars of combined order exactly $k$ also suffice for this reduction.

## Every prime-power modulus

It remains to handle $Q\in H$ and $m\mid s$ when $k=p^e$. Write $m=p^r$ and $u=v_p(s)<e$. Since $P$ has $p$-adic valuation $e-r$ and the gcd criterion failed, $u>e-r$. Also $u\ge r$ because $m\mid s$. In particular $r\ge2$.

Work first in the subgroup $K$ of order $M=p^{u+1}$ containing $H$. Set $s_0=s\bmod M$, $w=M/m$, and $A=s_0/w$. Here $w\ge2$, $s_0$ is a positive multiple of $M/p$, and
$$
                       2\le m/p\le A\le m-m/p\le m-2 .
$$
After solving inside $K$, distribute its outside cosets whole as before. It suffices to give the two stars orders $s_0,M-s_0$ in $K$.

Choose generator $h$ of $K$ with $wh=P$ or $wh=-P$ as specified below. Such a generator exists because $P$ generates $H$. In units of $h$, partition the positions $0,\ldots,M-1$ into $m$ consecutive blocks of width $w$. Write $P=wP_0$, $Q=wQ_0$ in these coordinates. To construct $B$, take all positions in $A$ blocks indexed by $C\subseteq\mathbb Z_m$ and remove the first position of block $Z=P_0-A$. Require $Z\in C$ and $0\notin C$. This gives $wA-1=s_0-1$ labels avoiding both centers 0 and 1. Telescoping on each full block, then subtracting the translate difference of the removed singleton, shows that (1) holds exactly when
$$
     (\tau-1)1_C=e_0+e_{Q_0+P_0}-e_{Q_0}-e_Z
                 \quad\text{on }\mathbb Z_m .
$$

For $Q\ne0$ choose $wh=P$. After possibly exchanging the stars, $1\le Q_0\le m-A$; exchange replaces $Q_0$ by $-Q_0$ and $A$ by $m-A$. Use
$$
                    C=\{Q_0\}\cup[1-A,-1].
$$
The two parts are disjoint, zero is absent, and $Z=1-A$ belongs to the interval because $A\ge2$. For $Q=0$ choose $wh=-P$ and take $C=[-1-A,-2]$. The interval has $A$ entries, begins at $Z$ and avoids zero since $A\le m-2$. Both displayed choices have the required difference. This completes the construction at every prime power.

## Exact decision at the remaining moduli

For each nonzero $h$, integrate (1) around every orbit of adding $h$. The right side must sum to zero there. The successive values of $1_B$ are then determined up to an additive integer constant. The bounds 0 and 1, and the forced zeros at both centers, restrict that constant to an integer interval. Starting at each interval's minimum, an optional increase adds a whole orbit of size $k/\gcd(k,h)$. Thus the prescribed mass $s-1$ is attainable exactly when it lies between the resulting extrema and has the right remainder. This reconstructs $B$ directly. Try both orientations. With the forced-center lemma this is an exhaustive decision in $O(k^2)$ arithmetic operations for a full packet.

[Constructor and exact test](two_star_extension.py) · [Independent tests, including direct capacity search](check_two_star_extension.py)

~~~sh
python3 -B -m research.rainbow.check_two_star_extension
lean research/rainbow/TwoStarPacket.lean
~~~

The checker builds actual core trees realizing every prescribed deficit, joins the stars, and recounts every vertex and edge residue. It also exhausts center and leaf-label choices through ten labels. At 26, its independent backtracking search assigns every free leaf label to one of the two centers under the actual edge capacities. This confirms the five normalized failures and the adjacent successful split $12+14$.
