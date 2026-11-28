# A linear-size completion using only pendant leaves

**Theorem.** From any tree $H$ on $h\ge3$ vertices one can construct a tree on at most $2h-3$ vertices by adding leaves directly to vertices of $H$, so that its vertex labels and its ordinary edge sums each form an interval of consecutive integers without repetitions. Two distinct original vertices can then receive any further numbers of leaves, independently, preserving both intervals.

In particular the constructed tree, and every one of these continuations, is cordial at **every positive modulus** by reducing its integer labels. Translating the vertex labels to start at one also gives a super edge-magic labeling. The restriction to pendant leaves means that every added vertex has degree one in the finished tree. Related results give smaller hosts allowing auxiliary vertices to be internal, or allow all leaves to be concentrated at one prescribed original site with a larger threshold. [Level construction and references](../census/level-hosts.md) · [One prescribed site](endpoint-hub.md) · [Youssef, Theorem 4](https://ajc.maths.uq.edu.au/pdf/43/ajc_v43_p031.pdf)

## Placing the original labels

Choose any original leaf $v$ with neighbor $p$. Number $H-v$ from $0$ to $h-2$ in breadth-first order starting at $p$, with children of each vertex consecutive. If $p_i$ is the parent index of $i>0$, then the $p_i$ are nondecreasing. Hence the $h-2$ sums $i+p_i$ are strictly increasing and belong to $[1,2h-5]$. They include 1.

Let $c$ be the first integer at least $h-1$ missing from these sums and write $b=c-(h-1)$. Give $v$ the label $c$, so that its edge has weight $c$. For $b>0$, the consecutive old weights $h-1,\ldots,c-1$ come from consecutive children of one parent of rank $g$. An increment of one in the weight requires the parent rank to stay constant. The first child has rank $h-1-g>g$, and the last has rank $c-1-g\le h-2$. Thus $b\le g\le\lfloor(h-2)/2\rfloor$. After the last child there are exactly $g-b$ old weights, all greater than $c$.

Use the $b$ intervening vertex labels $h-1,\ldots,c-1$ on preliminary leaves. Assign them, in order, the first $b$ unused weights greater than $c$. For input $x=h-1+i$ and its assigned weight $y$, the parent label $y-x$ lies between $b+1$ and $g+1$, since at most $g-b$ old weights can be skipped. These are original labels. The occupied vertex interval is now $[0,c]$. Its edge-weight set $W$ has size $c$ and contains $[h-1,c]$. If $b>0$, its maximum $M$ is at most $\max(2h-5,c+g)\le2h-3$. For $b=0$ one simply has $M\le\max(2h-5,h-1)$.

## Filling the two intervals

Put $u=|\{w\in W:w<c\}|$ and $\alpha=c-u$. The weights below $c$ include $h-1,\ldots,c-1$ and 1, so $1\le\alpha\le h-2$. If $b>0$, the last old child below $c$ has index $c-1-g$, giving $u=c-1-g$ and $\alpha=g+1$.

Set $\delta=1$ if $b>0$, $g=b$ and $h-2$ is missing from $W$, and $\delta=0$ otherwise. Target the edge interval $[1-\delta,M]$. Form the increasing lists of missing weights below and above $c$, of lengths $A=\alpha+\delta-1$ and $B=M-c-\alpha+1$. Match the new vertex labels $-A,\ldots,-1$ and $c+1,\ldots,c+B$ to the respective weight lists in increasing order. A matched input $x$ and weight $y$ request a parent of label $y-x$.

In each list the requested parent labels are nondecreasing. On the right they lie in $[0,\alpha-1]$. On the left the first difference is at least $\alpha$, and the last is at most $h-1$, since every missing lower weight is at most $h-2$. The original vertices carry $[0,h-2]\cup\{c\}$. For $b=0$ every requested parent is available.

For $b>0$ the only unavailable request is $h-1$. Its occurrences form a terminal segment of the left list. If there are $t>0$ occurrences, then $h-2$ is missing, and $A=g+\delta\ge b+1$. Rotate the inputs in the last $m=\max(b+1,t)$ positions. Assign the first $b$ outputs in the block the last $b$ inputs in order, and the last $m-b$ outputs the first $m-b$ inputs in order. The latter outputs all requested $h-1$, so their parent labels increase by $b$ to $c$. In the first group the labels decrease by $m-b\ge1$. They remain nonnegative because $m\le g+\delta$ and each was at least $g+1$. All other requests already lie in the original label set. Each added vertex is therefore a leaf at an original site.

The resulting order is $N=M+1+\delta\le2h-1$. The vertex interval $[L,U]$ and edge interval satisfy $[1-\delta,M]=[L+\alpha,U+\alpha-1]$. Both $\alpha$ and $\alpha-1$ label original sites. A new leaf of label $L-1$ at the first site extends the lower ends of both intervals. A leaf of label $U+1$ at the second extends the upper ends.

## Choosing the initial leaf

For a caterpillar use its direct consecutive-sum labeling. Traverse the spine from one end, listing each vertex's pendant edges just before the edge to the next spine vertex. Each successive edge retains one endpoint and introduces a new vertex. In each bipartition class use ranks $0,1,\ldots$ in order of first appearance. Each edge uses the latest rank on both sides, so its rank sum increases by one along the list. Shift the second class by the size of the first. The vertex labels and sums are consecutive. Their two extensible sites are the first label of the second class and the last label of the first.

Otherwise choose $p$ to maximize the number of original leaf neighbors, and $v$ to be any such leaf. If $N>2h-3$ then $b>0$ and $b=g=\lfloor(h-2)/2\rfloor$. Indeed for $\delta=0$ this would require $c+g\ge2h-3$ and hence $b+g\ge h-2$. For $\delta=1$ one already has $b=g$, and $c+g\ge2h-4$ forces $2g\ge h-3$.

All trees on at most five vertices are caterpillars, so here $g\ge2$. When $g=b$, the last $b$ indices of $H-v$ are the children of rank $g$ in the consecutive run. These are original leaves since no later edge has any of them as a parent. The original root $p$, of rank zero, must also have at least $g$ leaf neighbors by its choice. These two sets of leaves are disjoint. This leaves at most $h-2g\le3$ nonleaf vertices, which form a path. That would make $H$ a caterpillar. Consequently $N\le2h-3$.

## Prescribed leaf populations at a fixed modulus

Run the construction on $H$, obtaining site populations $f_v$, order $N$ and the two distinguished sites. Suppose prescribed populations $m_v$ satisfy $m_v\ge f_v$ everywhere. If the two sites jointly have at least $(-N)\bmod k$ unused leaves, the ordinary tree with exactly the prescribed populations is $k$-cordial. Take that many leaves at the two sites to reach a divisible order with consecutive labels and sums. All other leaves can be appended in batches by [Hall's leaf extension](../counterexample-bound.md#removing-leaves).

In particular the following uniform sufficient condition works for every $h\ge3$ and $k\ge1$.
$$
\min_v m_v\ \ge\ \max\{h-3,\ \lceil(k+h-4)/2\rceil\}.
$$
The initial construction spends at most $h-3$ leaves in total. After that expense the two sites together have at least $2\min m_v-(h-3)\ge k-1$ unspent leaves. This includes cores smaller than the modulus. For $h\ge k$ the [two- or three-leaf construction](breadth-first-leaves.md) gives smaller thresholds.

The [constructor and independent interval checks](linear_leaf_host.py) test 9,412 small choices of ordered tree and marked original leaf through nine vertices, and 480 further trees through 151 vertices. They reconstruct the actual sums, check that all added vertices are leaves at original sites, and test independent additional populations at both distinguished sites. A further 2,534 choices verify the $2h-3$ bound, and 125 modular labelings with prescribed populations are checked on their actual edges.

~~~bash
python3 -B -m research.hub.linear_leaf_host
~~~
