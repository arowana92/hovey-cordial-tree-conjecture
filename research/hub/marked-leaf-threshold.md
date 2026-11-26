# Leaf additions at any selected sites in a tree

**Theorem.** Fix a finite tree $H$ and any set $S$ of at least two of its vertices. There is a computable $C(H,S)$ such that attaching any $m_v\ge C(H,S)$ leaves at each $v\in S$ gives a super edge-magic tree. No leaves need to be attached outside $S$. Each selected population varies independently. One integer labeling gives cordial labelings at every positive modulus by reduction. [Youssef, Theorem 4](https://ajc.maths.uq.edu.au/pdf/43/ajc_v43_p031.pdf)

**Decision theorem.** For every fixed $b$, it is decidable whether every tree with at most $b$ nonleaf vertices is cordial at every modulus, including every possible tree order and leaf distribution. If counterexamples in this class exist at unbounded moduli, there is one fixed rooted tree such that adjoining leaves only at its root produces a counterexample of order $p$ at every sufficiently large prime $p$.

The two-site case follows from the [two-hub construction](two-hubs.md), including its caterpillar cases, which have consecutive-sums labelings. Earlier results cover all vertices as sites or give conditions on five particular vertices. The proof here permits arbitrarily long paths of unselected vertices between the sites and arbitrary subtrees without any sites. Related coronation theorems include constructions with uniform leaf counts and hypotheses on a labeling of the original graph. [Caterpillar construction](all-radius-two.md) · [All-site theorem](uniform-leaf-threshold.md) · [Figueroa-Centeno, Ichishima and Muntaner-Batle, *Magical coronations of graphs*](https://ajc.maths.uq.edu.au/pdf/26/ajc_v26_p199.pdf)

## Integer intervals and three available parent labels

A seed is $H$ with finitely many leaves added **only at selected sites**, with integer vertex labels $[L,U]$ and distinct edge sums $[L+1,U]$. Write $p_v$ for the original core labels. We will use seeds with one of two sets of available filler parents. The triple is $\{-1,0,2\}$. The quadruple is $\{-a,0,1,b\}$ with $a\ge1,b\ge2$. Every member of the stated set is the label of a selected site.

For an upper band of $d$ new vertices and a permutation $\pi$ of $[0,d-1]$, use label $U+1+i$ at parent $\pi(i)-i$. For a lower band use label $L-d+i$ at parent $1+\pi(i)-i$. The vertex and edge intervals extend at the same end. Write $j=0,1$ for the upper and lower offsets.

**Insertion.** A required new child at any existing parent $p$ can occupy any sufficiently high integer, or any sufficiently low integer, using only fillers at the available parents. To obtain a band first realize the displacement $p-j$ on one row of a permutation. If it is zero, a singleton works. If the available displacements include both unit steps, use a cycle with one jump $p-j$ and return by consecutive unit steps. It fills a consecutive interval. Otherwise zero displacement is available. The available steps have both signs and include a unit step, so any integer is reachable from any other. For instance with $+1$ and a negative step one can first move below a target and then advance by ones. Use the specified jump from zero and a shortest return path to zero. This is a simple cycle. Translate it to its own band and fix all unused positions there. All rows except the designated child use available parents.

Padding first moves the designated child to any sufficiently distant position. Above, use singletons at zero. Below, singletons at one work for a quadruple. For the triple, lower bands with parent lists $(2,0)$ and $(2,2,-1)$ give widths two and three, hence every width at least two.

**Subdivision.** Any core edge with endpoint labels $p,q$ can be replaced by a three-edge path while retaining every old vertex label. Insert a sufficiently low child $x$ at $p$ and an upper child $y=p+q-x$ at $q$. The lower operation leaves the upper endpoint fixed, so these positions are feasible. Replace the old edge by the edge $xy$, keeping both child edges. The replaced weight is identical. This can lengthen any specified segment by any even number. Finally grow any required off-segment subtrees by ordinary child insertions. [Band construction](marked_leaf_blocks.py) · [Subdivision and reconstruction](marked_leaf_geometry.py)

## Covering the three- and four-site geometries

Take the minimal subtree spanning the selected sites. Every terminal vertex is selected. Suppress its unselected degree-two vertices, retaining each positive segment length. With $s$ sites there are at most $s-2$ unselected junctions, by summing degrees. Start each odd segment at length one and each even segment at length two. Subdivision and insertion recover the full tree and preserve the site labels.

For three **ordered** sites there are 20 such parity representatives. Each has a seed assigning the labels $0,2,-1$ in precisely the given order. For four sites, order the marks by decreasing population. There are 432 representatives. For each, the certificate gives a seed, or a subdivision into population cells with a seed for each cell, using four available parents. Let $f_i$ be the site labels in order, $M=\sum_i m_i$ and $W=\sum_i f_i m_i$. For every sorted population profile these seeds ensure
$$
\min(W,M-W)\ \ge\ \min_i m_i. \tag{1}
$$

Each record supplies the suppressed tree, segment parities, all core labels on the representative, and the filler parent for each unused integer position. The verifier enumerates all connected edge sets on the marks and up to $s-2$ junctions, requires degree at least three at unselected vertices, and identifies permutations of those junctions. It separately checks every parity pattern. It recomputes the full vertex and edge intervals for every seed.

The sorted unit-mass simplex has as vertices the uniform distributions on the first $r$ sites, $1\le r\le4$. Indeed the coefficients in that convex combination are $r(m_r-m_{r+1})/M$, taking $m_5=0$. Each split bisects a simplex edge and keeps both child simplices. In every one of 444 terminal cells, the verifier uses exact rationals to check (1) on its vertices. Both moment slacks and the smallest coordinate are linear on the sorted chamber, so the two inequalities hold throughout each cell. These checks also cover ties. At $M=0$ they hold directly. [Finite certificate](marked-leaf-seeds.jsonl) · [Independent verifier](marked_leaf_verify.py)

## Constructing a bounded seed with moment to spare

For $s=|S|\ge3$ put $R=M-\max_{v\in S}m_v$. We prove that a **finite computable family** of seeds on the given $(H,S)$ has a constant $\eta>0$ such that some member satisfies
$$
\min(W,M-W)\ \ge\ \eta R,\qquad W=\sum_{v\in S}p_v m_v. \tag{2}
$$
Populations in this assertion are nonnegative. Fillers will be paid for after the seed is chosen.

For three sites write the populations $A\ge B\ge C$. If $A\ge3B/2$, assign them labels $0,2,-1$ respectively. Then $W=2B-C\ge R/2$ and $M-W=A-B+2C\ge R/2$. Otherwise assign them $-1,2,0$. Now $W=2B-A\ge R/4$ and $M-W=2A-B+C\ge R$. Inflate the appropriate representative to the fixed tree. The six possible orders give a finite family.

For the induction on $s$, assume we have the families for omitting each single site, still on the **entire** $H$. Let $\eta_0\le1$ be the smallest of their constants and $N$ the largest seed order in them. Their intervals contain zero and at least one positive integer, hence $|p_v|,|1-p_v|\le N$. Put $c=\eta_0/[2(N+1)]$. If any site $v$ has $m_v\le cR$, use its omission family, allowing that site to be an ordinary core vertex. The mass away from a largest remaining site is at least $R-m_v$. Reinstating the contribution of $v$ leaves both slacks at least $\eta_0(R-m_v)-Nm_v\ge\eta_0R/2$. This includes $R=0$.

Hence assume every site has population greater than $cR$ and $R>0$. At $s=4$, (1) gives (2) with factor $c$ in this case. There are finitely many expanded seeds for the fixed four sites. For $s\ge5$ use the following two constructions on the minimal spanning subtree $T$ of the marks. Any vertices of $H$ outside $T$ are unselected and are inserted last.

- **A largest site $o$ dominates.** Choose a terminal vertex $q\ne o$ of $T$. In $T-q$, use a three-site seed with $o$ at zero and any two other remaining marks at $2,-1$. This labels all of $T-q$. Let $F$ bound the absolute labels so far and the first feasible upper position for $q$. Put $Y=F+\lceil(F+1)/c\rceil+2$ and give $q$ label $Y$. The other sites besides $o$ contribute in absolute value at most $FR$, so $R\le W\le(Y+F)R$. If $M\ge2(Y+F)R$, both slacks are at least $R$.
- **Two terminal sites adjust the moment.** Take $Q$ to be the maximum of $2(Y+F)$ over the finitely many dominant-site constructions just described. In the remaining case $M<QR$. Choose two terminal marks $x,y$ of $T$. In $T-\{x,y\}$ place a triple on any three remaining marks and label the rest of this connected subtree. Choose an integer $F'$ larger than all absolute labels and large enough that any $X\le-F'$ is feasible below for $x$ and any $Y'\ge F'$ above for $y$. The opposite bands do not interfere. Start at $X=-F',Y'=F'$. If $m_x\ge m_y$, move $X$ down by the fewest steps needed to give moment at most $M/2$, then move $Y'$ up by the nearest number of steps to that target. If $m_x<m_y$, reverse the roles and directions. The error is at most $\min(m_x,m_y)/2\le M/4$. Thus both slacks are at least $M/4$.

The adjustable choices range over a computably bounded set of integers. The initial moment has absolute value at most $F'M$. Moving the first coordinate changes the moment by at most $(F'+2)M$ including a possible overshoot. Moving the second changes it by at most $(F'+3)M$, since the starting distance to the target is at most $(F'+1)M$ when the first coordinate stays put, and otherwise the overshoot is at most its population. Both populations exceed $cR>cM/Q$. Each coordinate therefore moves at most $(F'+3)Q/c$ steps. Enumerate those integer positions and grow the rest of $H$ for each. Together with the omission families, this constructs the finite family for (2), with factor $\min(\eta_0/2,c,1/4)$ for example. All orders and padding amounts may be very large. [Seed constructions](marked_leaf_construct.py)

## Realizing the exact leaf populations

Deduct the leaves used in a seed. For the remaining counts $n_p$ at core labels put $M'=\sum n_p$, $W'=\sum p n_p$ and $D=1+\max p-\min p$, over the entire core. With a quadruple we may use the [two-reserve completion lemma](uniform-leaf-threshold.md#extending-a-fixed-labeling), since zero and one are selected. It suffices that both have at least $(2h+2)D^2$ leaves and $0\le W'\le M'$, where $h=|H|$.

For a triple, let $d$ be the maximum upper insertion band length for any core parent and put $E=(2h+2)Dd$, $B=8(E+1)$. It suffices to have at least $B$ leaves at each triple site and both slacks at least $2B$. Reserve $B$ leaves at each of $-1,0,2$. This consumes mass $3B$ and moment $B$, leaving an admissible moment between zero and the new mass.

The [rational rotation allocation](uniform-leaf-threshold.md#extending-a-fixed-labeling) splits the remaining vector into nonnegative rational multiples of upper and lower permutation blocks. There are at most $2h+2$ coefficients and each block has length at most $D$. Use their integer parts. Fewer than $(2h+2)D$ requests remain. For each, perform a single upper insertion at its requested parent, charging the other positions to the triple reserve. At most $E$ fillers are needed. The only counts left are $a,b,c'$ at $-1,0,2$, each between $B-E$ and $B$.

Use $x$ upper blocks $(2,-1,-1)$, $y$ lower blocks $(2,2,-1)$, $z$ lower blocks $(2,0)$ and $w$ upper singletons at zero, where
$$
x=\lceil(2a-c')/3\rceil,\quad y=a-2x,\quad z=c'-2a+3x,\quad w=b-z.
$$
Here $0\le z\le2$, $x\ge0$, and $y\ge(2c'-a-4)/3\ge0$. The four multiplicities use exactly $a,b,c'$ leaves at the three respective sites. Each list has the required permutation displacements. Lean checks the integer rounding and both three-site moment inequalities. [Exact construction](marked_leaf_blocks.py) · [Lean arithmetic proof](MarkedLeafBlocks.lean)

Finally take a common upper bound $N'$ on the orders of the finite seed family from (2). The seed consumes at most $N'$ leaves at any site and lowers each slack by at most $(N')^2$. Compute $B_*$ bounding the reserve constants above over this finite family. It suffices to choose $C$ with $C\ge N'+B_*$ and $\eta C\ge (N')^2+2B_*$. Indeed $R\ge C$ when all selected sites have at least $C$ leaves. This pays every seed filler at a selected site and allows exact completion. The construction gives the first theorem.

## A finite decision for all distributions

For a fixed $H$ and set of sites $S$, decide the statement for **all nonnegative** populations and **all** moduli by induction on $|S|$. For at least two sites the threshold theorem covers the region with every count at least $C$. In each remaining slice choose a site with count $j<C$, absorb its $j$ leaves into the fixed core, remove it from the site set, and recurse. There are only finitely many slices at each node and the number of sites decreases.

At one site the [rational one-hub test](rational.md) decides the entire family. Failure of its rational condition yields counterexamples of order $p$ for every sufficiently large prime $p$. If the condition holds, only finitely many moduli need testing. With no sites a fixed tree is also decidable directly. Distinct powers of two give distinct integer vertex labels and distinct edge sums, so at all sufficiently large moduli the fixed tree is cordial, and the remaining labelings can be searched exhaustively.

For at most $b$ nonleaf vertices, enumerate all possible connected nonleaf cores of orders at most $b$, taking all their vertices as candidate sites. Every tree with a nonempty nonleaf core is recovered by attaching leaves to its core. Conversely every tree produced from such a core has at most $b$ nonleaf vertices. The isolated vertex and single edge work directly. This proves the bounded-core decision theorem. If the failing moduli are unbounded, at least one of the finitely many one-site leaves of the decision tree must have a failed rational test. Its ordinary prime-order counterexamples still belong to the original class, since the finitely many absorbed vertices were leaves added at original core sites. The argument gives no universal bound on the number of nonleaf vertices in counterexamples to the full conjecture.

## Reproduction

From the repository root, check the entire finite certificate with standard Python 3.9 or later. The second command reconstructs upper and lower insertions, stretches each geometry and checks its actual edges, and verifies whole-tree profiles including highly unequal populations and a fully expanded example on 120,005 vertices.

~~~sh
python3 -B -m research.hub.marked_leaf_verify
python3 -B -m research.hub.marked_leaf_check
lean research/hub/MarkedLeafBlocks.lean
~~~

The optional generator uses Prüfer codes, integer-label search and bipartite matching. The verifier has an independent tree enumeration and checks only explicit witnesses and rational simplex splits.

~~~sh
out=$(mktemp -d)
c++ -O3 -std=c++17 -shared -fPIC research/hub/marked_leaf_search.cpp -o "$out/search.so"
python3 -B -m research.hub.marked_leaf_search "$out/search.so" > "$out/seeds.jsonl"
cmp research/hub/marked-leaf-seeds.jsonl "$out/seeds.jsonl"
~~~

[Search](marked_leaf_search.py) · [Integer-label matching](marked_leaf_search.cpp) · [Reconstruction checks](marked_leaf_check.py)
