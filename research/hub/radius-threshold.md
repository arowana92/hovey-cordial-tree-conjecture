# A near-modulus order bound for every radius-two tree

**Theorem.** For each fixed $0<\delta<1/9$ and all sufficiently large $k$, every tree of radius at most two and order at least
$$
k+4k^{1-\delta}
$$
is $k$-cordial. For example one may take $\delta=1/10$. The center degree and the distribution of children at its neighbors are unrestricted. The proof constructs a cordial subtree of order $k$ containing every parent of every remaining leaf. It leaves open radius-two trees at order $k$.

We use two constructions. With many branching neighbors, trim partial layers of grandchildren. With a small number of branching neighbors, use rotations of integer intervals to serve unequal numbers of children at their parents.

## Completing integer intervals using rotations

Suppose an integer-labeled seed uses the vertex interval $[L,U]$ and has edge sums $[L+1,U]$. The remaining tasks are leaves at $s$ distinct integer parent labels $p$, including 0 and 1. Put $D=2+\max |p|$. We give a construction when enough leaves at 0 and 1 are available, and after setting aside those reserves the weighted mean of the remaining parent labels belongs to $[0,1]$.

Let $m_p$ denote these remaining counts, $M=\sum m_p$, $W=\sum p m_p$. Split the counts over the nonnegative reals as $m_p=u_p+l_p$, such that
$$
\sum p u_p=0,\qquad \sum(p-1)l_p=0 .
$$
For $0<W<M$ choose mass exactly $W$ for the lower list $l$, of total weight $W$. Taking a uniform fraction $W/M$ of all counts gives weight $W^2/M\le W$. Taking the largest $W$ units of mass gives weight at least $W$: if they are all at positive labels this follows by integrality, and otherwise the excluded labels are nonpositive. Interpolating the two allocations gives the required mass and weight. At $W=0$ take all upper, and at $W=M$ take all lower. Zero remaining counts require no tiles.

For the upper list use shifts $p$, and for the lower list use shifts $p-1$. Each list has weighted sum zero. A zero shift can use singleton tiles. For a positive shift $a$ and negative shift $-b$, a tile uses $b$ copies of the former and $a$ copies of the latter. On $[0,a+b-1]$ the permutation $x\mapsto (x+a)\bmod(a+b)$ has exactly these displacements. Match positive and negative weighted mass greedily, taking the largest real multiple of each tile that fits both remaining counts. Every step exhausts a parent type on at least one side. Together the two lists use at most $2s+2$ real tile coefficients including singletons.

Round each coefficient down and lay the integer tiles end to end. An upper tile takes the next interval above $U$ for both its new vertices and its weights. A lower tile takes the next interval below $L$ for its vertices and that interval shifted up by one for its weights, since the real parent label is one above the chosen shift. In either case the two full intervals keep their prescribed form. Fewer than $(2s+2)2D$ leaves remain from rounding. Insert every remaining leaf other than those at 0 or 1 with the [two-hub insertion rule](two-hubs.md#growing-a-labeled-subtree): a positive parent $p$ uses child $L-p$ and fills the intervening positions with $p-1$ leaves at 0, and a negative parent $p$ uses child $U+1-p$ and fills the intervening positions with $-p$ leaves at 1. Thus reserving $B=8(s+1)D^2$ leaves at **each** of 0 and 1 before splitting suffices. Add any remaining leaves at 0 above the interval and any at 1 below. All counts are exact, including those rounded down. The resulting tree is super edge-magic and cordial at every modulus. [Consecutive sums and cordiality, Youssef, Theorem 4](https://ajc.maths.uq.edu.au/pdf/43/ajc_v43_p031.pdf)

## Choosing labels at five well-populated branches

Consider an order-$k$ tree consisting of its center, $c$ marked neighbors, and $M=k-c-1$ leaves at the center and those neighbors. In this application $c<k^\delta$, $\theta=k^{-2\delta}$, and five of the marked neighbors each have at least $M\theta/3$ children. Write $\alpha_p$ for the proportion of leaves at each position, before labeling; these proportions sum to one. Among the five designated neighbors choose one of least proportion for a label $y$ to be determined, so $\alpha_y\le1/5$. Use the other four as the parents labeled $0,1,-2,x$.

Give the center label 2. Start with its three neighbors $0,1,-2$ and one child labeled 3 at $-2$. The vertices so far are $-2,0,1,2,3$ and the weights are $0,1,2,3$. Add a leaf labeled $-1$ at parent 0, supplying weight $-1$. The resulting vertex and edge intervals are $[-2,3]$ and $[-1,3]$. 

Insert all marked neighbors except $x,y$ and the initial three using the positive-parent rule at the center 2. Each receives $L-2$ and requires one gap leaf at 0. Thus all these neighbor labels are $O(c+1)$ and the upper end remains 3. Insert the neighbor $x$ in the same way, first using leaves at 1 to lower $L$ if necessary. We may choose any integer $x\le L-2$.

For the final neighbor $y$, take an integer $y>3$. Fill from the old upper end through $y-1$ with leaves at 0. Insert the neighbor $y$ at the center 2 and a child $y+2$ at parent $-2$. Their weights are $y+2$ and $y$, respectively. Use a leaf at 0 with label $y+1$. This restores both intervals.

Choose these two adjustable labels to make the mean $\sum p\alpha_p$ lie in $[2/5,3/5]$, counting the center's leaves at $p=2$. Indeed, let $A$ be the contribution excluding $x,y$; $|A|=O(c+1)$. Decrease $x$ just enough, if needed, that $(1/2-A-\alpha_x x)/\alpha_y\ge5$. Take $y$ nearest to this quotient. The error in the mean is at most $\alpha_y/2\le1/10$. If the constraint first becomes true by decrementing $x$, the overshoot in its numerator is at most $\alpha_x$. If it held initially, $|A+\alpha_x x|=O(c+1)$. Consequently $|x|,|y|=O((c+1)/\theta)$, as is $D$. The seed consumes $O(c+D)$ leaf tasks, all at 0, 1 and $-2$. Only the two displayed children are needed at $-2$.

For the rotations take $s\le c+1$. The needed reserve at each of 0 and 1 is $O(cD^2)=O(k^{7\delta})$, whereas each has $\Omega(k^{1-2\delta})$ available leaves. The first quantity is smaller for large $k$ since $9\delta<1$. Removing the seed leaves and the reserves changes both the remaining mass and its total weighted sum by $O(cD^2)$: the removed parent labels belong to $\{-2,0,1\}$. The mean before these removals is between $2/5$ and $3/5$, and $M\sim k$, so the residual mean belongs to $[0,1]$. The rotation construction supplies the exact order-$k$ tree.

## Trimming many branching neighbors

Let $c$ neighbors have positive child counts. Keep the $b$ greatest counts, where $b$ is $c$ or $c-1$ chosen odd. If $A$ is the total number of grandchildren this loses at most $A/c$. A retained count sequence is a diagram of layers, each using one child from each of its first $r$ parents. Keep a full first layer of rank $b$. For each odd rank $r>1$ with odd multiplicity among the other layers, shorten one such layer to rank $r-1$. The number $j$ of reductions is at most $\sqrt A$: the original diagram contains distinct odd ranks at least $3,5,\ldots,2j+1$ of total size $j(j+2)$. All but the initial layer are now rank-one layers, even layers, or pairs of the same odd rank.

Every total from $b$ up to the remaining number of cells can be taken, keeping at most one unmatched odd layer beyond the initial layer. Take complete groups until the last group would exceed the desired size. An even layer can be shortened to any prefix. For a pair of rank $r$ odd, use two prefixes of size at most $r-1$ when at most $2r-2$ cells are needed: take one full even prefix before a partial one. At $2r-1$ take ranks $r-1,r$. The [odd-branch construction](branch-levels.md#constructing-the-interval-for-odd-c) handles exactly this condition by integer intervals. Other neighbors of the center can be included as ordinary leaves at this stage. At order $k$ distinct interval vertex labels give all residues and the distinct edge weights in the interval remain distinct modulo $k$.

## Applying the constructions

Let $d$ be the center degree. The [wide first level lemma](subdivided-stars.md#a-radius-two-tree-with-a-wide-first-level) handles $d\ge k-1$. Otherwise we need $t=k-1-d$ grandchildren to make an order-$k$ core containing all $d$ neighbors. If $t\le c$, take one from each of $t$ different neighbors, forming a partially subdivided star. Hence suppose $t>c$. Trim the given tree to order $n'=\lceil k+4k^{1-\delta}\rceil$ by deleting grandchildren, keeping all $d$ neighbors and at least one child at each formerly branching neighbor. This is possible since $1+d+c<k$. We will use the original tree again after finding its core.

If $c\ge k^\delta$, the preceding trimming of layers loses at most $A/c+\sqrt A$ grandchildren with $A=n'-1-d\le 2k$ for large $k$. This is less than $n'-k$. Hence at least $t$ can be used, and $t\ge b$. This gives the desired core.

Suppose $c<k^\delta$. Call a branching neighbor large when it has at least $k^{1-2\delta}$ children in the trimmed tree. If there are at most four large neighbors, the other branching neighbors together have at most $k^{1-\delta}$ children. Choose all $t$ required grandchildren among the large neighbors. The resulting core is [cordial with at most four branching neighbors](branch-levels.md) and includes all the others as ordinary neighbors of the center.

With five or more large neighbors keep the center and all $c$ branching neighbors as the fixed skeleton. Choose $M=k-1-c$ of the $n'-1-c$ leaf tasks (including ordinary center leaves) to form an order-$k$ subtree. Allocate them proportionally among their parents, taking floors and distributing the remaining units without exceeding the counts. Each of five large neighbors retains at least $M k^{-2\delta}/3$ children for large $k$ since $n'\le2k$. The five-parent construction gives integer intervals on this subtree.

In every case all remaining vertices of the **original** tree are leaves of parents in the order-$k$ core. The first leaf supplies the unique missing edge weight. All further leaves attach in complete batches of $k$ and a final partial batch by [Hall's extension](../counterexample-bound.md#removing-leaves). This proves the theorem.

## Direct checks

The [executable construction](radius_threshold.py) extracts 12,034 diagrams of specified sizes, checks their capacities and reconstructs their integer labelings. Two unequal five- and seven-branch examples exercise the rational mass split, rounded rotations and exact completion. The checker independently recovers degrees, vertex sets and edge sums from the resulting 45,706- and 247,008-vertex labeled trees. The asymptotic estimates in the proof do not depend on these examples.

~~~sh
python3 -B -m research.hub.radius_threshold
~~~
