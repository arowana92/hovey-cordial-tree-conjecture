# Completing a prescribed tree by leaves at fixed sites

Let $S$ be **any labeled tree** on $r$ vertices. Choose $m\ge1$ distinct sites of $S$, with labels $p_i\in G=\mathbb Z_k$, and attach $L_i\ge4kr$ new leaves at each. Write $n=r+\sum_i L_i$ and $e=(n-1)\bmod k$. The old vertex and edge histograms may be unbalanced.

Choose $p_m$ as a reference. Put $H=\langle p_i-p_m:1\le i\le m\rangle$ and $l=|H|$. For each coset $J$ of $H$ let $g_J$ be the number of old labels in $J$ minus the number of old edge weights in $J+p_m$. Write $b=\sum_J\max(0,-g_J)$.

**Theorem 1.** There is a cordial labeling preserving every old label if and only if
$$
       |g_J|\le l\quad\text{for every }J,\qquad
       b\le\min(e,k-1-e).
$$
In particular, when the site differences generate $G$, every choice of old labels extends. It suffices to leave one site free in addition to any other site, since the free label can differ from the other by one. When $n\equiv0,1\pmod k$, the criterion requires the old coset differences to be zero except for a single $+1$.

At four labels, take a path labeled $0,0,1,1$ in that order and add leaves only at its first two vertices. Then $H=\{0\}$ and the old differences are $(1,1,-1,0)$. For both populations at least 64, exactly the final orders two and three modulo four admit completion. At 30 labels, sites labeled $0,6,10,15$ always allow completion under the size bound. Together their differences generate the group even though no two of these labels differ by a unit.

**Additional leaves at arbitrary old vertices.** Suppose the selected sites meet the size bound, with at least $4kr+k-1$ leaves at one site. If the old coset differences are a single unit, any number of other leaves can be attached anywhere on the prescribed tree as well. Reserve at most $k-1$ leaves at the larger site to make the order using just the retained large sets equal to one modulo $k$. Theorem 1 extends the old labels to this intermediate tree. Restore all reserved and other leaves at their actual parents. From an order-one-modulo-$k$ cordial tree, each batch of at most $k-1$ leaves extends by Hall's permutation theorem. For a batch of exactly $k$, the last leaf supplies the unique deficient weight after the first $k-1$ and returns the tree to order one modulo $k$. This gives the conclusion, in particular whenever the selected differences generate $G$. [Leaf extension and primary reference](../counterexample-bound.md#removing-leaves)

## Completing specified histograms

The following construction is shared by both theorems. Subtract $p_m$ from all destination weights, and let $h_i=p_i-p_m$, so a leaf with label $z$ has normalized weight $z+h_i$. Suppose the desired leaf source and destination vectors are $U,W$ of the same mass $\sum L_i$. Write $D=W-U$, $\rho=\sum_z\max(0,D_z)$ and $\mu(f)=\sum_z zf(z)$ in $G$. Two necessary conditions are
$$
           \sum_{z\in J}D_z=0\quad(J\in G/H),\qquad
           \mu(D)=\sum_iL_i h_i.
$$
These conditions suffice whenever $L_i\ge\rho(l-1)$ for $i<m$ and
$$
             \min_z U_z\ge \rho+m-1+\sum_{i<m}\lfloor L_i/k\rfloor.       \tag{1}
$$

In each coset pair the negative units of $D$ with the positive units. Route each pair along a simple directed path of steps $h_i$ for $i<m$, putting one leaf of the corresponding site at each step's tail. These directed generators reach the whole subgroup, since the inverse of a group element is a nonnegative multiple of it. A path uses at most $l-1$ steps and visits any tail at most once. Hence the site supplies cover the paths and at most $\rho$ leaves occupy any one source. The resulting destination vector minus source vector is $D$.

For each $i<m$ consider its remaining population $a_i$. First assign $\lfloor a_i/k\rfloor$ whole copies of the group, which make no displacement discrepancy. Keep a single cursor, initially zero. Divide $a_i\bmod k$ by the order of $h_i$ to give quotient $t$ and remainder $s$. Put one copy on each of $t$ whole $\langle h_i\rangle$-cosets outside the cursor's coset. Use $s$ consecutive steps from the cursor on its own coset, and keep the cursor at the resulting endpoint. The remainder contributes at most one per source at this site. After all sites, the cursor returns to zero because its displacement is $\sum_{i<m}a_ih_i=0$ by the moment identity and the initial paths. The remainders therefore make zero net discrepancy. Condition (1) leaves nonnegative remaining source counts. Fill them at the last site, whose normalized step is zero. Their total is exactly $L_m$ and the final destination vector is $W$.

## Proof of Theorem 1

Write $A,C$ for the old vertex and normalized edge histograms. Balanced final vertex and normalized edge vectors take the form $Q\boldsymbol1+1_X$ and $Q\boldsymbol1+1_Y$ with $Q=\lfloor(n-1)/k\rfloor$, $|Y|=e$, $|X|=e+1$, allowing $X=G$. Every leaf stays in its coset. Thus $|X\cap J|-|Y\cap J|=g_J$. The allowable integer interval for $y_J=|Y\cap J|$ is
$$
            \max(0,-g_J)\le y_J\le\min(l,l-g_J).
$$
Each interval is nonempty exactly when $|g_J|\le l$. Its lower endpoints sum to $b$ and its upper endpoints sum to $k-1-b$ because $\sum g_J=1$. This proves necessity and gives coset counts whenever the criterion passes.

Inside each coset choose the two subsets nested, with a difference set of size $|g_J|$. We need
$$
                \mu(1_X-1_Y)=\mu(A-C)-\sum_i L_i h_i .
$$
The coset counts give this equality modulo the subgroup $H$. If $l>1$, some coset has $0<|g_J|<l$, since the $g_J$ sum to one. In a cyclic group of order $l$, subsets of size $s$ with $0<s<l$ attain every sum. Indeed the integer sums of $s$ distinct positions in $[0,l-1]$ form an interval of width $s(l-s)\ge l-1$. Starting at positions $0,\ldots,s-1$, successively move the rightmost positions by up to $l-s$ to attain every intermediate value. In the chosen coset we can therefore change the signed difference sum by any element of $H$, then choose the common positions outside that difference set. This gives the required moment. If $l=1$ it already holds.

Take $U=Q\boldsymbol1+1_X-A$ and $W=Q\boldsymbol1+1_Y-C$. Here $D=A-C+1_Y-1_X$ has $\rho\le r+b\le2r-1$. The second bound holds since $C$ has mass $r-1$. Also $m\le r$ and $\min U\ge Q-r$. The hypothesis $L_m\ge4kr$ gives $Q-r\ge3r+\sum_{i<m}\lfloor L_i/k\rfloor$; each other population exceeds $\rho(l-1)$. The construction above now realizes both balanced targets.

## Uniform increments from forests with prescribed labels

Let $S$ now be a rooted forest on $r$ new vertices, each root attached by one edge at a prescribed old parent. Add $L_i\ge3kr$ terminal leaves at each of $m\ge3$ distinct sites of $S$. Assume $k\mid n=r+\sum L_i$. Let $a_v$ count all children of $v$, including the new leaves, and $B$ be the sum of the old parent labels over the component roots. Prescribe labels $x_v$ on a set $P\subseteq S$; at least two of the sites must be free.

**Theorem 2.** The entire attachment adds $n/k$ to each vertex and edge bin while respecting all prescriptions exactly when
$$
             \gcd(k,a_v:v\in S\setminus P)
                 \ \bigm|\ B+\sum_{v\in P}a_v x_v .
$$
This includes arbitrary star forests with three or more sufficiently large stars. It also allows old parent labels repeated in any pattern, pins on adjacent vertices, and any internal structure of the prescribed forest. The two-star case without pins has a [separate exact theorem even for very small populations](../rainbow/neutral-stars.md).

Subtracting the sum of the new labels from the sum of the new edge weights gives $B+\sum_v a_vx_v$, proving necessity. We can solve this linear congruence while making the differences of the site labels generate $G$. To see this, work separately at each prime power $p^j\mid\mid k$. Divide the congruence by the common gcd of $p^j$ and its free coefficients. If a nontrivial congruence remains, one coefficient is now a unit. Modulo $p$ the free solutions form an affine hyperplane, and every solution lifts by adjusting that unit coordinate. With a trivial remaining congruence all free coordinates are available. The affine subspace in which all sites agree modulo $p$ has codimension at least two, or is empty. Indeed, pick two free sites and any third site, imposing equality of each of the two with the third. Hence there is a solution with two unequal site residues modulo $p$. The Chinese remainder theorem combines these prime-power solutions, and no prime divisor of $k$ divides every site difference. For $k=1$ all requirements are automatic.

Fix these labels, let $A$ count them and $C$ count the $r$ entering and internal edges normalized by the final site label. Use $U=(n/k)\boldsymbol 1-A$, $W=(n/k)\boldsymbol 1-C$. There is only one subgroup coset. The solved congruence is exactly the leaf moment condition. Now $\rho\le r$, and $(n/k)-r\ge2r+\sum_{i<m}\lfloor L_i/k\rfloor$. The same construction applies. This proof uses no asymptotic embedding result.

## Verification

The [constructor](leaf_cosets.py) assigns actual leaf populations and solves the prime-power congruences. A [separate checker](check_leaf_cosets.py) enumerates balanced target palettes, directly enumerates leaf allocations in small cases, and recounts every actual vertex and edge bin of each generated witness. At moduli through 12, the palette enumeration agrees on 4,073 completions and 487 exclusions. Literal leaf enumeration checks another 275 decisions, including 34 exclusions. The forest checker recounts 4,381 witnesses and verifies 219 gcd exclusions, reaching modulus 210. It also checks 2,275 joint moment and subgroup decisions by exhaustive assignment at small composite and prime moduli.

~~~sh
python3 -B -m research.biased.check_leaf_cosets
~~~
