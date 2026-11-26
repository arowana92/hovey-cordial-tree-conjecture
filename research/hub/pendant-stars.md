# Repeated pendant stars repair the actual edge sums at every modulus

**Theorem.** Fix $D\ge3$, $s\ge1$ and $m\ge1$. There is a number $N(D,s,m)$ with the following property. Suppose at most $s$ vertices of a tree have degree greater than $D$. If one vertex has at least $N(D,s,m)$ branches each consisting of a neighbor with exactly $m$ leaf children and no other vertices, then the tree is $k$-cordial for every positive $k$. The vertex supporting these branches may also have arbitrary other branches. The theorem includes $m=1$ (two-edge arms), all composite moduli, and arbitrarily distant high-degree vertices.

**Leaves close to a bounded set.** Fix $D,s,r$. Among trees in the degree class above whose leaves all lie within distance two of at most $r$ specified vertices, only finitely many counterexample pairs $(T,k)$ exist up to isomorphism. Thus all sufficiently large moduli work at every tree order for this class. In particular the conclusion holds for diameter-five trees with at most $s$ vertices above $D$, using the two ends of their central edge. This supplements the [finite-modulus and order bounds for diameter five](diameter-five.md). Trees of diameter at most four already have a [separate proof at all moduli](all-radius-two.md).

To prove this, take the minimal subtree $H$ connecting the specified vertices. It has at most $r$ leaves when nontrivial and maximum degree at most $\max(r,2)$. Each branch leaving $H$ has depth at most two, since its deepest vertex is an original leaf. A branch of depth two has to attach at one of the specified vertices itself to meet the distance bound. Its root has $m$ children, all leaves. Those with $m+1>D$ account for at most $s$ roots. For each of the other arities and each specified vertex, there are fewer than $N(D,s,m)$ such branches in a counterexample. A direct leaf off $H$ can only attach within distance one in $H$ of a specified vertex, giving at most $r(1+\max(r,2))$ attachment sites. Keep the boundedly many small stars and just the roots of the large ones as additions to $H$. This base has bounded leaf count, regardless of the distances between the specified vertices. All further vertices are direct leaves at boundedly many sites. Apply the [bare-path finiteness theorem](bare-path-repair.md). The argument also works when $H$ is one vertex.

A further consequence allows arbitrary subdivisions. Start with any tree having at most $l$ leaves and attach arbitrary direct leaves and arbitrary pendant stars of arities $1,\ldots,r$ at at most $s$ sites. For fixed $l,r,s$ there are only finitely many counterexample pairs. Degrees outside the sites are bounded by $\max(l,r+1,3)$. A sufficiently abundant star arity at any one site gives the theorem. Otherwise the total number of extra stars is bounded. The ordinary tree before adding the direct leaves then has bounded leaf count, so the [bare-path finiteness theorem](bare-path-repair.md) applies.

Related work constructs super edge-magic labelings for a family of diameter-four trees. Consecutive vertex labels and edge sums give cordiality for all moduli by Youssef's Theorem 4. The proof here directly balances residues on trees with arbitrary other branches. [Fukuchi and Oshima (2008)](https://www.pphmj.com/abstract/3265.htm) · [Youssef (2009)](https://ajc.maths.uq.edu.au/pdf/43/ajc_v43_p031.pdf)

## Five roots with a free choice of one parent label

Write $[x]$ for one occurrence of $x$ in a histogram. All equations in the construction hold in $\mathbb Z_k$. At an already labeled vertex of small positive digit $p$, take five of the saved $m$-leaf stars. For a parameter $d$ put the following labels on their roots and on one child of four of the roots.

| Root label | First child label |
|---|---|
| $d$ | left open |
| $d+p$ | $-2d-4p$ |
| $d-p$ | $d+2p$ |
| $-d-3p$ | $-d-p$ |
| $-d-2p$ | $2d+p$ |

The five boundary weights are $d+p,d+2p,d,-d-2p,-d-p$. The four child weights are $-d-3p,2d+p,-2d-4p,d-p$. These are exactly the nine assigned labels, counted with multiplicity. In particular the parent of the open first child has the independently selectable label $d$. At a zero boundary use just one star and assign $d$ to its root. Its single assigned edge then has the same label. [Lean verification of the nine actual sums](FiveStarRoots.lean)

## One repair with a moving omitted weight

Suppose the current edge histogram minus vertex histogram contains $-[g]+[t]-[b]$, with $t$ reserved as a free vertex label. Our new branches will contribute $[b]-[t]+[g]-[g']$, leaving one new omission. Equal $b=t$ also works as a step on unused branches, with $t$ chosen fresh. Let $p$ be the supplier's label. Use five groups of the previous construction with parameters
$$
d_1=A,\quad d_2=B,\quad d_3=b-t-A-B,\quad d_4=U,\quad d_5=V .
$$
At the first open child of the first three groups, assign $t,t+A,t+A+B$ respectively. The three weights are $t+A,t+A+B,b$. This gives $[b]-[t]$.

Every remaining open child has a known parent label $J$. Starting with the desired edge weight $g$, place the next leaf at the current value minus $J$, and update the current value to that leaf label. These jumps telescope. Their final value $g'$ gives the contribution $[g]-[g']$. The construction only subtracts parent labels and never divides by $m$ in $\mathbb Z_k$.

We specify the order to keep these moving labels available. In groups four and five list the children at positive-coefficient roots first, starting at the root labeled $d_i$, then the children at negative-coefficient roots. Interleave the two lists, starting in group four. Finally process the rest of groups one through three in any order. Within each of groups four and five the signed prefix count of jumps is positive after its first step. At $p\ne0$ the list has $m+2(m-1)$ positive jumps and $2(m-1)$ negative ones, ending at $m$. At zero all $m$ jumps are positive. After the first two steps every new tail label has nonzero coefficient in **both** $U,V$. This holds also throughout the final three groups, since their jumps have zero $U,V$ coefficients. In particular $g'$ is moving even when $k$ shares a factor with $m$ and $k$ is sufficiently large.

Here are the full collision checks as affine forms in $A,B,U,V$. Assume all small nonzero multiples of the positive digit $p$ used below are nonzero modulo $k$. All fixed group entries have nonzero slope vectors. Within any group, repeated coefficient $+1$ has offsets $0,p,-p,2p$ and repeated coefficient $-1$ has offsets $-3p,-p,-2p$. At $p=0$ each group has just its root. Different groups have distinct slope directions up to proportionality. The main leaf $t+A$ can have the same slope as a group entry only in group one, so require $t\notin\{0,p,-p,2p\}$. The main leaf $t+A+B=b-d_3$ can collide identically only if $b\in\{-p,-2p,-3p\}$. For the backward walk its first tail $g-U$ has the same three exclusions on $g$ at $p\ne0$. At $p=0$ it has no group entry with that slope. All subsequent tails have both guard coordinates and hence different slopes from the groups and main leaves. At the zero supplier only $t\ne0$ is needed for the main leaves. We allow repetitions among backward tails.

To specialize, replace $(A,B,U,V)$ by $(z,Rz,R^2z,R^3z)$ with $R=24m+17$. Each coordinate in the walk accumulates at most the number of jumps of the relevant groups. For $A,B$ only the corresponding single group and group three contribute, each with absolute prefix count at most $5m$. For $U,V$ only one group contributes. These bounds, including the group entries and the main leaves, give differences of magnitude at most $20m+4<R-1$ per coordinate. Successive reduction modulo $R$ shows that distinct slope vectors give distinct integer slopes and nonzero vectors give nonzero slopes. The number and absolute slopes of all forms are bounded in terms of $m$ alone.

Use the [common interval lemma](bounded-error.md#a-common-set-of-intervals-for-the-direct-leaves) to put all moving forms outside the palette $S$ set aside for the large leaf populations. There are at least $ck$ common parameter choices. Avoid all collisions with the sparse occupied and protected values, between the group entries and the main leaves, and between these entries and the backward tails. Each unequal-slope comparison excludes at most the absolute difference of slopes, also at composite moduli. The inputs above handle equal slopes. These exclusions cost $O_{D,s,m}(h+1)$ choices for an ordinary tree of order $h$, plus a fixed constant for the bounded set of special values. Require also that $g'$ avoids the small fixed residues and the old gap.

A backward walk may revisit a label. Read it forward from $g'$ to $g$ and erase a simple cycle each time a position repeats. The residual path has distinct tails and gives the same histogram difference. For each erased cycle translate all its tails by a common fresh offset. Their actual parents, hence their jumps, are unchanged. Its heads and tails still have identical histograms. The common interval lemma applied to the bounded list of translates (all slopes one), and the same linear exclusion bound, place each cycle injectively outside $S$ and previous labels. This finishes the step with $g'$ among the occupied labels. [Implementation](star_repair.py)

## Applying the repair at arbitrary orders

For large $k$ mark all high-degree vertices as sites. Make the branch threshold larger than $D$, so the supplier is a site. Remove direct leaves at sites and write $h$ for the surviving order. For $h\ge\delta k$ use the [positive-density theorem](concentrated-leaves.md). For $h<\delta k$ first take total order $k$. Reserve exactly $25C$ of the repeated branches, where $C$ will bound the number of errors. Apply the [sparse preparation](bare-path-repair.md#keeping-the-surplus-weights-available) to the remaining ordinary tree. Root it at a site with the largest direct leaf population, give it zero and give the other sites and marked branching vertices distinct powers of three. The supplier's digit $p$ may be zero. The resulting labels, including the direct leaves at nonzero sites, satisfy
$$
E-V=-[0]+\sum_{i=1}^e([t_i]-[b_i]),\qquad e\le C.
$$
The $t_i$ are protected and none is occupied. All $b_i$ are occupied. At this stage $g=0$.

For the few extra noncollision conditions, let $P$ be the largest marked digit, or one for a lone site. Remove the whole bounded interval $[-3P-1,3P+1]$ modulo $k$ from the direct-leaf palette and forbid it for moving ordinary labels and targets. This only adds a bounded cost to the sampling and interval placement. The only earlier fixed errors, on direct edges between marks, have $b_i$ a positive digit and $t_i$ a sum of two distinct positive powers of three. Such a sum is neither $p$ nor $2p$ by its base-three digits and is different from $0,-p$ for large $k$. The initial omission zero satisfies the gap condition at a positive $p$. Every later omission and every temporary $t$ in an unused group can be chosen outside the small interval.

As in the sparse preparation choose the bounds for single palette calls first, including the forms and cycles above. Choose the palette, then the fixed error bound $C$ and then a sufficiently small $\delta$. Removing branches at the site before preparation does not change the bounds on other degrees, on batch sizes, or on the number of error-producing shapes and sites. The constant $C$ is therefore independent of the number set aside. When $p\ne0$, each repair uses 25 stars. At zero it uses five. In both cases use the remaining groups on $b=t$ until all $25C$ stars are restored. Fill the unused labels at the direct leaves of the zero site. The full tree now has a bijective labeling and all actual edge weights except $g'$ exactly once.

For smaller orders pad to $k$ by direct leaves at a site and restrict. For larger orders the [leaf-removal induction](bare-path-repair.md#repairing-the-actual-weights) preserves the saved branches. It removes one direct leaf at order $1\bmod k$ and otherwise $(n-1)\bmod k$ leaves, then restores a deficient weight or uses Hall's distinct-leaf extension. This proves the theorem at every order for sufficiently large moduli. Each of the finitely many smaller moduli has an order threshold above which every tree is cordial. Increase $N(D,s,m)$ beyond these thresholds to cover them simultaneously. [General order bound](../large-order/linear.md)

## Reproduction

The verifier rebuilds the parent list of each expanded tree and computes all endpoint sums afresh. Its modular checks include moduli sharing factors with the arity, both kinds of supplier and actual omission changes. The checks include 23,821 nine-edge identities, 252 isolated repairs and 49 expanded trees with 3,210,704 actual weights. The finite examples use enough branches to cover their own error counts. The uniform threshold follows from the counting argument. [Independent checks](check_star_repair.py)

~~~sh
python3 -B -m research.hub.check_star_repair
python3 -B -m research.hub.check_pendant_repair
lean research/hub/FiveStarRoots.lean
~~~
