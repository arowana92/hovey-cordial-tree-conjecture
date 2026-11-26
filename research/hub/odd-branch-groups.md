# Adjacent exceptional vertices at moduli with a fixed odd divisor

**Theorem.** Fix $D\ge3$ and an odd integer $d\ge3$. For all sufficiently large multiples $k$ of $d$, consider a tree with adjacent vertices $a,b$ and with all other degrees at most $D$. Each of the following conditions suffices for $k$-cordiality at every tree order.

1. Some vertex is at distance at least five from $\{a,b\}$.
2. Both $a$ and $b$ have at least $C(D,d)$ leaf neighbors outside their common edge, for a constant independent of the tree and its order.

In particular any counterexample in this class has diameter at most nine and one of its two direct leaf populations bounded by $C(D,d)$. Its surviving order after deleting the two populations is also $o(k)$ along any counterexample sequence with $k\to\infty$. The quotient $k/d$ need not be coprime to $d$. [Leaf concentration](concentrated-leaves.md)

## A neutral group of arbitrary identical branches

Write $k=dq$. Fix any parent label in the subgroup $q\mathbb Z_d$. Let $B$ be a rooted tree on $m$ vertices. For all sufficiently large $q$ relative to $m$ and the number of forbidden labels, **$2d$ copies of $B$ at this parent can add the same set of new vertex labels and new edge weights**, avoiding every forbidden label. For fixed $m,d$ it suffices that $k$ exceed a constant times one plus the size of the forbidden set.

Use distinct nonzero integer magnitudes $|x_v|\le81m$ whose internal edge-sum magnitudes are precisely the magnitudes of the nonroot labels. At sign $\sigma\in\{-1,1\}$ and copy index $j\in\mathbb Z_d$, put $\sigma\lambda x_v+jq$ on $v$. Choose $\lambda$ so all $2m$ residues $\pm\lambda x_v$ are distinct modulo $q$ and avoid the projections of the forbidden labels. Each forbidden residue excludes at most $81m$ choices per form, and each pair excludes at most $162m$ choices, including at composite $q$. The new labels fill these $2m$ entire fibers. For each internal edge the digit term is $2j$ and runs through all of $\mathbb Z_d$ because $d$ is odd. Both signs together supply exactly the fibers of the nonroot labels. Each boundary edge adds its parent's fixed subgroup digit to $j$ and supplies the missing root fiber of its sign. The new labels and the actual weights are thus the same set. [Signed construction for every rooted tree](signed-tree.md)

## A sparse tree with one long ordinary branch

Delete all direct leaves at the two sites, leaving a core $H$ of order $h$. Put zero at $a$ and $q$ at $b$. Their edge has weight $q$, so on this seed the edge histogram is the vertex histogram minus one occurrence of zero. Denote the direct leaf population at $b$ by $m_b$. We prove a stronger sparse conclusion when
$$
k>K_{D,d}(h+m_b+1).
$$
There is an injective labeling of $H$ with those $m_b$ leaves restored, whose edge weights are the vertex set with one omission. This permits **every** further population at $a$ by the periodic leaf construction. [Period and proof](README.md#uniform-witnesses-for-large-moduli)

Orient every exterior branch away from the adjacent sites. Measure branch height by the number of vertices on its longest path from the site, excluding the site. Protect one branch of maximum height. Among branches of height below ten, at each of the sites and for each rooted shape, set aside groups of $2d$ identical branches. Protect the chosen branch from this grouping. These short branches have bounded order depending only on $D$, hence there are boundedly many shapes. At most $2d-1$ copies of each shape at each site, and one protected branch, remain. For now also keep just $m_b\bmod d$ direct leaves at $b$.

If the protected height is at least five, withhold the four-site terminal configuration and its free boundary from within four edges of a deepest vertex. Its boundary lies outside the two-site seed because that vertex has distance at least five from the seed. Use the [bounded-batch construction](linear-hub-batches.md#scheduling-the-batches-with-a-bounded-last-remainder) with both sites already assigned. The initial number of exposed short components is bounded, even after the withholding shortens one branch. Whenever a tall component remains, use its first ten vertices on a longest path and all currently short components in one neutral batch. At most $10D$ new short components are exposed after a batch. The proof of that batch only uses the labels of its actual parents as prescribed jumps, so the initial values $0,q$ are allowed. At termination the unassigned ordinary vertices and the withheld configuration have bounded size. The final four-site construction starts with the same histogram difference as in the one-site proof. Its boundary is still a free vertex of positive affine slope, and the four-site edges restore zero and leave one gap. All these parameter specializations exclude at most $O_{D,d}(h+m_b+1)$ residues since the number of moving forms per batch is bounded. [Affine forms and terminal identities](modular-injection.md#stopping-with-at-most-twelve-levels)

Restore the groups using the odd-divisor construction, avoiding every previous label and preserving the omission. Place the remaining $m_b-(m_b\bmod d)$ leaves at $b$ in previously empty quotient fibers of size $d$. Each such fiber also gives exactly its labels as weights. At most $h+m_b$ fibers can be occupied or required, so a sufficiently large $K_{D,d}$ pays for these and for all group specializations. This proves the sparse conclusion with no requirement on $m_b$ in the long-branch case.

## Short branches and two unbounded leaf populations

Suppose all ordinary branches have height at most four. If there is no ordinary branch, the tree is a caterpillar. Otherwise each ordinary branch has at least two vertices because we removed the direct leaves. Group the short branches as above, retaining the protected branch. The residual core $H_0$ has bounded order $h_0$ depending only on $D,d$ and still has a branch of at least two vertices. This time start with all direct leaves set aside.

Apply the [order-$k$ fiber construction](cluster-lift.md#filling-the-fibers-at-order-exactly-k) to $H_0$, requesting $m_b$ leaves at $b$ and $k-h_0-m_b$ temporary leaves at $a$. It places the sites at $0,q$. The quotient of $H_0$ has a nonzero-gap certificate at all sufficiently large $q$. Both populations meet the required threshold $d(h_0-1)-h_0$ when $m_b\ge C(D,d)$ and $k>K_{D,d}(h+m_b+1)$, with the constants sufficiently large. For instance $C$ can exceed $d$ times the maximum residual order. The labeling fills every residue and omits one weight.

Delete **all** temporary leaves at $a$. Each deleted vertex has weight equal to its label, so deleting them preserves the single omission. In particular the missing weight is still a vertex label. Only $h_0+m_b$ vertices remain. Restore the neutral groups at the two prescribed sites, as in the deep case. This proves the same sparse conclusion for short branches if $m_b\ge C(D,d)$.

## All orders

The [positive-density theorem](concentrated-leaves.md) settles $h\ge\delta k$ for any fixed $\delta>0$, since only the two sites can have high ordinary degree and only they can be ordinary leaves adjacent to those degrees. For $h<\delta k$ first consider order exactly $k$. Choose $a$ to be the site with more direct leaves. When $m_b\ge dh$, both sites meet the [two-site divisor bound](cluster-lift.md) and that proof applies. Otherwise $h+m_b<(d+1)h$. Choose $\delta$ so small that the sparse modulus cutoff holds for all sufficiently large $k$. The deep case then allows any $m_b$, and the shallow case applies under the second hypothesis of the theorem.

At smaller orders pad with leaves at a site and restrict the resulting order-$k$ labeling. At orders above $k$ the ordinary core stays fixed. Retain $C(D,d)$ leaves at both sites if using the second hypothesis and retain none if using the first. Since $h+2C(D,d)<k$ in the sparse range, one can remove a leaf at $n\equiv1\pmod k$ or otherwise $(n-1)\bmod k$ leaves, keeping both reserves. Induct on order, then use the [distinct-leaf extension](../counterexample-bound.md#removing-leaves) or restore the single deficient weight. Finally, if every vertex has distance at most four from the edge, two vertices lie at distance at most $4+1+4=9$. This proves the counterexample restriction.

## Reproduction

The checker uses every rooted shape through order seven to reconstruct 120,980 actual weights on 1,445 complete groups, with all possible subgroup parents at three different divisors. It separately checks 120 two-site trees through order 3,128 and the changes to both counts after adding leaves at zero. The deep tests include a retained branch of height exactly five and 24 cases with zero leaves at the second site. The current constructor uses the stronger fixed-boundary completion when two nontrivial branches survive at the second site. The fiber checker separately verifies the alternative order-$k$ labelings used above. [Constructor](odd_branch_groups.py) · [Independent verifier](check_odd_branch_groups.py) · [Fixed-boundary improvement](adjacent-odd-divisor.md)

~~~sh
python3 -B -m research.hub.check_odd_branch_groups
python3 -B -m research.hub.check_cluster_lift
python3 -B -m research.hub.check_linear_hub_batches
~~~
