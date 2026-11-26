# Seven protected errors on an arbitrary sparse rooted tree

**Sparse preparation.** For every rooted tree of order $h$ and every $k>100(h+1)^2$ there is an injection into $\mathbb Z_k$ taking the root to zero, for which the actual edge and vertex histograms satisfy
$$
 E-V=-[0]+\sum_{i=1}^e([t_i]-[b_i]),\qquad e\le7.
$$
The deficits $b_i$ are occupied vertex labels. All $t_i,-t_i$ are pairwise distinct, free of the entire vertex labeling, and $b_i+2t_i\ne0$. The bound seven is independent of degrees, tree shape and modulus. At order $k$, after filling the complement by leaves at zero, changing at most seven recorded edge weights would give the desired histogram.

**Exact repair.** Suppose the tree has a path with 129 consecutive internal degree-two vertices, all different from the prescribed root. If $k>10^5(h+1)^2$, the root-zero injection can satisfy $E=V-[0]$ exactly. It then extends cordially to **every number** of additional leaves at the root.

**Arbitrary branch lengths and orders.** For all sufficiently large $k$, take any rooted tree $H$ having at most $\sqrt{k}/10^5$ nonroot terminals. If it contains the 129 internal vertices above, adjoining any number of leaves at its root gives a $k$-cordial tree. For $a\ge1$ nonroot terminals a sufficient condition for the path is $|H|>258a+1$. These assertions allow arbitrarily many vertices of arbitrarily high degree. The square-root bound with this path hypothesis improves on the earlier [unconditional small-core exponent](modular-injection.md).

## Neutral rounds and the last seven levels

Label the root zero and its children with distinct nonzero values. Their entering edges supply just those new labels. At any later point let the frontier consist of all children outside the labeled subtree whose parents are inside. Whenever a frontier vertex starts a path of eight unassigned vertices descending from it, use the [eight-vertex round](modular-injection.md#a-round-using-eight-consecutive-vertices). Expose the other frontier vertices as ordinary new vertices and the chosen path as the transfer. Its parent is nonzero. The round labels all ordinary vertices and seven or eight vertices of the path, preserving $E=V-[0]$. In its cycle translations at most $h(h+2)$ parameters are excluded. At its common specialization, all distinct-slope comparisons have nonzero coefficient of magnitude at most seven among at most $h$ labels. Equal slopes have distinct intercepts as in the [transfer proof](ModularLayer.lean). The modulus bound suffices throughout.

When the rounds stop, each remaining component rooted at a frontier vertex has at most seven levels, counting its root. Process one full level at a time. For the new vertices, the known parent labels are prescribed jumps in $\mathbb Z_k$. Start a walk at zero with those jumps, assigning the tail to each step, and erase each simple cycle as it forms. Let $P$ be the terminal. For $P=0$ translate the cycles individually to fresh vertex labels. Their entering edges permute those labels.

For $P\ne0$, the residual simple path begins at zero and has no tail at $P$. Before a common translation, translate each erased cycle to avoid all other offsets, the residual tails and $P$. With at most $h+1$ forbidden offsets and a cycle of length at most $h$, a translate exists. Now add $X$ to all offsets. The new edges minus new vertices contribute exactly $[X+P]-[X]$. The label $X$ is occupied at the start of the residual path, and $t=X+P$ differs from every new arrival. Choose $X$ so that the arrivals avoid previously occupied and reserved values, $t,-t$ also avoid those values, $-t$ misses all arrivals, $t\ne-t$, and $X+2t\ne0$. The old set has size at most $h+14$. Each arrival or endpoint against this set has unit coefficient. The comparisons with $-t$ cost at most $2h$ exclusions and the last two tests at most five. The total is at most $(h+2)(h+14)+2h+5<100(h+1)^2$. This also covers composite moduli. Reserve both signs of $t$ for all further layers. At most one discrepancy per level proves the preparation.

## An exact correction with unrestricted degrees

Compress the specified 129 interior vertices to one edge with endpoints labeled $u,v$ after preparation. Starting at $u$ use ten bare vertices for a neutral round, then seven successive groups of fourteen, and finish with the [21-vertex bridge](bare-path-repair.md#a-bridge-giving-a-prescribed-edge-weight) to $v$. The first round ends at a fresh nonzero parent. For one group of fourteen per error use the [paired transfers and equal-slope checks](bare-path-repair.md#repairing-the-actual-weights). The constant arrivals in the pair are precisely $t_i,-t_i$. Its edge histogram minus its new labels is $[b_i]-[t_i]$. Keep all other protected labels free. For a spare group of fourteen use the neutral batch with seven ordinary arrivals followed by a seven-step closing transfer. In the last bridge prescribe the old virtual weight $u+v$. Counting that removed edge gives exactly $E=V-[0]$.

For an explicit bound, each placement here has at most 21 moving forms. Even in a fourteen-vertex neutral batch, the ordinary forward recurrence adds an earlier slope to its current terminal at most seven times starting at one. Its seven closing forms have slopes bounded by $4\cdot2^7+2$. Bridge slopes have magnitude at most 126. Thus comparison with an old occupied or reserved value costs at most 514 choices, and an unequal-slope comparison within a placement costs at most 1028. With at most $h+14$ old values these bounds fit inside $10^5(h+1)^2$ for $h\ge131$. Translating cycles or specializing the initial preparation also fits this bound. This construction needs no control on degrees outside the compressed segment. For the extension, the periodic list of hub leaf labels consists of the complement, then the gap zero, then the occupied nonzero labels. Each leaf contributes its label to both histograms. [Proof for every prefix of the period](README.md#uniform-witnesses-for-large-moduli)

## Recovering long branches

Write $h=|H|$. For $h\ge k/20$ the [positive ordinary density theorem](concentrated-leaves.md) applies directly to $H$ with one decoration site. Indeed $H$ has at most $a+1$ unrooted leaves, so it has at most $a+1$ vertices of degree greater than three and at most that many ordinary leaves adjacent to them. These counts lie below $k^{2/3}$ for large $k$. The result covers every number of added leaves and every order.

For $h<k/20$ mark the root, the terminals and the branching vertices. There are at most $2a$ segments between consecutive marks. On each segment of more than 14 edges retain the congruent length between 3 and 14 modulo 12, except on the distinguished segment containing the selected 129 vertices. There retain the smallest length at least 130 congruent to its length modulo 12, hence between 130 and 141. Other short segments keep their lengths. The compressed tree has order at most $28a+142$ and still has the 129 internal vertices, with its root outside them. Under the displayed bound on $a$, $10^5(28a+143)^2<k$ for sufficiently large $k$. Use the exact repair.

Every shortened segment retained at least three edges. There is no zero edge weight and only the root carries zero, so one edge on each such segment has nonzero endpoints and sum. Repeatedly insert the [twelve-vertex neutral subdivision](long-branches.md#a-short-core-with-arbitrarily-elongated-edges) until the original lengths are recovered. Its requirement $k>12h+132$ holds for large $k$. This preserves the injection, the root and the omitted weight. Add the leaves at the root as before. Finally, if every segment has at most 129 edges then $h\le258a+1$. The stated order condition therefore ensures a segment of length at least 130.

## Reproduction

The checker recomputes the signed discrepancies on all 7,813 rooted tree shapes through order 12. It reconstructs all adjacencies in 48 path repairs, including trees using every one of the seven correction groups. It tests 15 hub extensions on both sides of modulus order using 1,180,179 actual endpoint sums. The numerical examples also include moduli below the sufficient bound. [Constructor](seven_errors.py) · [Independent checker](check_seven_errors.py)

~~~sh
python3 -B -m research.hub.check_seven_errors
lean research/hub/ModularLayer.lean
lean research/hub/PathBridge.lean
~~~
