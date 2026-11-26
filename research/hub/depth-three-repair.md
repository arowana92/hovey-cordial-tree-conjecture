# Three-edge branches and the shape of a remaining counterexample

**Branch theorem.** Fix $D\ge3$, $s\ge1$, $l\ge0$ and $m\ge1$. At a vertex $p$ consider a branch with first vertex $x$, its child $y$, another $l$ leaf children at $x$, and $m$ leaf children at $y$. When a tree with at most $s$ vertices above degree $D$ contains sufficiently many disjoint such branches, it is cordial at every positive modulus. The attachment vertices can coincide or be far apart. Here the removed branches are vertex-disjoint and all attachment vertices remain after their removal. The case $(l,m)=(0,1)$ consists of pendant paths of three edges.

**Structure theorem.** For fixed $D,s$ there is a bound on the number of rooted leaves left after deleting two rounds of childless vertices in any counterexample of this degree class, with **any** choice of root. Also, deleting just the direct leaf neighbors of the high-degree vertices leaves a tree of bounded maximum degree.

**Finiteness consequence.** Fix $D,s,r,R$. Among trees of this degree class with all leaves within distance $R$ of at most $r$ specified vertices there are only finitely many counterexample pairs $(T,k)$ up to isomorphism. In particular, for **each fixed diameter bound**, every tree of that diameter or smaller in the class is $k$-cordial at every sufficiently large modulus, at every tree order. The unbounded-diameter case in the distance-cover statement allows the specified vertices to be arbitrarily far apart.

## A free leaf parent on a three-edge path

Start with three branches at labels $a,b,c$. In each take the first two vertices on the distinguished path and in the last two take one further tip. Use these labels in path order.

| Boundary | First vertex | Second vertex | Tip |
|---|---|---|---|
| $a$ | $d-a$ | $d$ | open |
| $b$ | $d-a-b$ | $2d-a$ | $-4d+2a-c$ |
| $c$ | $-2d+a-c$ | $-2d+a$ | $3d-2a-b$ |

Adding adjacent entries including each boundary gives $d,2d-a,d-a,3d-2a-b,-2d+a-c,-2d+a,-4d+2a-c,d-a-b$. These eight weights permute the eight new labels, with the free parent $d$ available for an open leaf. At slope one the offsets are $-a,0,-a-b$, and at slope minus two they are $a-c,a$. All repeated-slope intercepts are distinct if $a,b,c,a+b$ are nonzero. No entry has slope minus one. [Lean check of both tables](DepthThreeRoots.lean)

For a common zero boundary use two branches. Put $(x,d)$ on the first and $(-2x-d,x+d,-x)$ on the second, including a tip on the latter. The five new sums are $x,x+d,-2x-d,-x,d$. Set $x=Jd$ with $|J|=2m+10$, taking $J>0$ when $m-1\ge l$ and $J<0$ otherwise. The five nonzero slopes $J,1,-2J-1,J+1,-J$ are all distinct and none is minus one.

## Repairing one surplus and moving the omission

Suppose $t$ is a surplus weight held free as a vertex label, $b_0$ the corresponding occupied deficit, and $g$ the old omission. Use five groups with parameters $A,B,b_0-t-A-B,U,V$. On the first open tip in each of the first three groups put $t,t+A,t+A+B$. Their edges contribute $[b_0]-[t]$ to the weight histogram minus vertex histogram. The primary moving labels with slopes $A$ and minus the third group's parameter slope require only $t\notin\{0,-a,-a-b\}$ in the first group. There is no minus-one entry in the third. At a common zero boundary just $t\ne0$ is needed.

Every remaining vertex in the saved branches is a leaf with a known jump equal to its parent's label. Walk backwards from $g$, subtracting the jumps to obtain the new vertex labels. Process one leaf at the free parent $U$ and then one at $V$. In each of these guard groups process the rest of its positive-coefficient parents before its negative-coefficient parents. Complete the last three unprocessed leaf lists (from the first three groups) after the two guard lists. With the three-boundary table the total coefficient in one guard list is
$$
l(1+1-2)+m+2(m-1)-2(m-1)=m>0.
$$
With the zero-boundary table it is $m+(m-1-l)(J+1)>0$ by the choice of sign. The initial jump is positive, so every nonempty guard prefix has positive coefficient. The first tail $g-U$ misses all group entries by the absence of slope minus one. After the second jump every tail has nonzero coefficients in both $U,V$, hence different slope from every group entry and primary leaf. The final gap $g'$ is one of these moving tails. The contribution from these jumps is $[g]-[g']$.

Specialize $(A,B,U,V)=(z,R_0z,R_0^2z,R_0^3z)$, using an integer radix $R_0$ larger than twice the maximum coordinate difference plus two. All list sizes and coefficients are bounded in terms of $l,m$. Equal slopes inside a group were checked above, and directions from different groups are nonproportional. The [common palette and sparse collision count](pendant-stars.md#one-repair-with-a-moving-omitted-weight) therefore applies with bounded slopes at every sufficiently large modulus, including composite moduli. Keep the new gap free of the previous labels and special values. Erase simple cycles in the backward walk and translate each separately to fresh labels outside the palette. The remaining path is simple. This yields distinct actual labels and the exact combined change $[b_0]-[t]+[g]-[g']$. [Constructor](depth_three_repair.py)

## Routing the boundary labels

We need either many copies at a single attachment vertex or many distinct attachment vertices, and enough copies force one of these alternatives. For many distinct vertices discard the at most $s$ original high sites, so none receives zero. In this alternative reserve $15(C+1)$ branches at distinct vertices. In the common-parent alternative take the multiplicity larger than $D$ so its parent is a site, and reserve $30(C+1)$ branches. As in the [paired-star proof](paired-stars.md#from-the-local-identity-to-the-theorem), first remove direct leaves at all original high sites. Ordinary order $h\ge\delta k$ is already settled. In the sparse case take total order $k$ and prepare the remaining ordinary tree after withholding the selected branches, keeping all their boundary vertices and sites. The preparation gives $e\le C$ protected errors. Choose palette list and slope bounds before the palette, then $C$, then a sufficiently small fixed $\delta$. None of these bounds depends on the number of branches removed.

For distinct positive boundary residues choose $a$ for the first group avoiding $-t$, then $b$ avoiding $-a,-a-t$, and any third $c$. There are at least fifteen candidates at the start of each job. In each of the next four arbitrary triples order two as $a,b$ with $a+b\ne0$. At most one other distinct label can equal $-a$. All the requirements of the table now hold. For a common positive site digit $p$ all three labels equal $p$, and $2p\ne0$ for large $k$. The [small-residue exclusions in the sparse preparation](pendant-stars.md#applying-the-repair-at-arbitrary-orders) give $t\ne0,-p,-2p$. Fixed errors between marks also satisfy these exclusions. A common zero site uses the second table.

Use five groups per error, consuming fifteen or ten branches as appropriate. For spare groups of five take $b_0=t$ fresh and admissible. This restores all reserved branches and gives $E=V-[g']$. The direct leaves at zero fill the complement. Pad by direct leaves for smaller orders, and at larger orders apply the [induction restoring direct leaves](bare-path-repair.md#repairing-the-actual-weights) while retaining the selected branches and original sites. Finally increase the threshold to cover the finitely many small moduli by the [general large-order theorem](../large-order/linear.md).

## Two rounds of pruning

Root a counterexample anywhere. Exactly the vertices of descendant height at least two survive two rounds of removal of the childless vertices. Their tips have height exactly two. Their descendant subtrees are disjoint. Exclude the root itself if it is a tip, and exclude subtrees containing an original vertex above degree $D$. This loses at most $s+1$ tips.

At each remaining tip there are leaves and one or more children which are roots of pendant stars. If there are two or more such children, that tip supplies the configuration of the [paired-star theorem](paired-stars.md) at its own distinct vertex. Their total number is bounded in a counterexample. If there is just one such child, the whole tip subtree is exactly a branch of the present theorem, attached at the tip's parent. Their arities $l,m$ lie in a finite range depending on $D$. The attachment vertices are outside all these subtrees, since the height of each attachment is at least three. For each profile there can be only boundedly many such tips. This proves the bound on the number of surviving tips.

Call the surviving rooted subtree $J$. When nonempty its maximum degree is bounded by its number of tips plus one. Each child outside $J$ of a vertex in $J$ is a leaf or the root of a pendant star. There are boundedly many of the latter at any vertex in a counterexample: at most $s$ have degree above $D$ and the [single-site theorem](pendant-stars.md) bounds each other arity. Delete the original direct leaves at high sites to obtain $H$. A high vertex in $J$ has now only boundedly many neighbors, including its possible parent. A high vertex outside $J$ had descendant height at most one, so loses all its child leaves. Other vertices have degree at most $D$. The cases of empty $J$ and singleton trees satisfy the same conclusion. This proves the claimed maximum degree bound for $H$.

In the distance-cover setting, replace any specified vertex deleted in forming $H$ by its parent site. Distances to surviving vertices do not increase. Each leaf of $H$ is either an original leaf or a site that lost neighbors. Thus all such leaves lie in at most $r+s$ balls of radius $R$ in $H$. Its bounded degree bounds the sizes of these balls and hence its total leaf count. The original tree comes from this bounded-leaf tree by adding leaves at at most $s$ sites. The [finiteness theorem for such decorations](bare-path-repair.md) proves the last assertion. For diameter bounded by $R$ a single ball suffices.

## Reproduction

The independent checker recounts 128,700 local histograms, compares two rounds of deletion against the branch classification on 3,047 rooted trees, and rebuilds 48 full trees with 3,145,184 actual endpoint sums. These checks include zero, positive common and distinct boundary labels and both signs of the zero-boundary multiplier. The universal bounds use the counting and structural arguments above. [Independent checks](check_depth_three_repair.py)

~~~sh
python3 -B -m research.hub.check_depth_three_repair
python3 -B -m research.hub.check_paired_stars
python3 -B -m research.hub.check_star_repair
lean research/hub/DepthThreeRoots.lean
~~~
