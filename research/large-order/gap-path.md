# A linear maximum-degree bound at every modulus

**Theorem.** Every tree of maximum degree at least $13001k$ is $k$-cordial. More generally, adjoining at least $13000k$ leaves to **any chosen vertex of any tree** suffices. The constants are absolute and the tree order is unrestricted.

We prove a stronger labeling statement. In every rooted tree of order $b$, the root can receive zero and the vertex and edge histograms can satisfy
$$
  E=V-\mathbf e_s,\qquad |V_x-b/k|\le13000
$$
for some residue $s$ and every $x$. The previous [recursive peeling argument](flexible-path.md#a-recursive-histogram-bound) gave logarithmic error. Here a fixed number of peeling rounds provides enough actual paths to repair every edge of a compressed tree.

## Transferring a missing weight

Below any existing parent of label $p$, give seven successive vertices on a downward path the labels
$$
t,\quad -p-2t,\quad p+t,\quad s+t,\quad -t,\quad -p-t,\quad p+s+2t .
$$
Number these entries from 1 to 7. In path order the seven new edge sums are entries $3,6,5,7$, then $s$, then entries $2,4$. Thus the change in $E-V$ is $\mathbf e_s-\mathbf e_t$ for arbitrary $p,s,t$. Integer addition gives the identity before reduction at any modulus. [Lean verification on the path edges](GapPath.lean)

Use two consecutive copies, transferring from $s$ to an intermediate $z$ and then from $z$ to $t$. The second parent is the last vertex of the first copy, of label $p+s+2z$. Of the fourteen new sites only two are independent of $z$, with labels $t,-t$. Every other coefficient of $z$ has absolute value 1, 2, or 3. In the second copy the five varying coefficients in path order are $-2,2,1,-2,3$.

Consider $m$ successive or disjoint fourteen-vertex blocks whose parents become available in the chosen order. Suppose their targets $t$ together have maximum multiplicity $B$. The fixed labels contribute at most $2B$ to any bin. For the twelve varying labels in each block, avoid all bins that already hold at least $36\lceil12m/k\rceil+1$ varying labels. There are fewer than $k/36$ such bins. Each bin precludes at most 36 values of $z$ in total, including at composite moduli, by the coefficient bound. A choice exists and the final varying load per bin is at most $36\lceil12m/k\rceil+12$. The bound is independent of the parents and of the requested sources $s$.

## Finding enough paths in a tree

Assume $k\ge2$. Set aside batches of $k$ simultaneous nonroot terminals until there are fewer than $k$. Next peel all remaining nonroot terminals synchronously for 336 rounds, or until only the root remains. In these rounds the number of terminals does not increase, since any newly terminal vertex can be charged to a different removed child. Write $C$ for the tree left by these rounds and $r$ for its nonroot terminals.

Each of these $r$ vertices has a downward path of 336 edges in the peeled part, and their paths are vertex-disjoint including their starting vertices. Indeed, a nonroot vertex in the tree before synchronous peeling survives $j$ rounds exactly when its original descendant subtree there has height at least $j$. A residual terminal has all children removed and supplies the required path. When the root alone remains take $r=0$.

Mark the root and the vertices of degree other than two in $C$. Shorten each segment between marks to its unique length in $\{1,\ldots,12\}$ congruent to its original length modulo twelve. The resulting $C_0$ has at most $24r$ edges, since there are at most $2r$ segments. Use the breadth-first ranks $0,1,\ldots,|C_0|-1$ as integer labels and reduce modulo $k$. In the child list the parent ranks are nondecreasing, hence the ordinary edge sums strictly increase. The order of $C_0$ is at most $24r+1<24k$. Both its vertex counts and its edge counts are bounded, the latter by 49 per bin.

Restore the original lengths of the segments using the [simultaneous twelve-vertex subdivision lemma](flexible-path.md#subdividing-edges-with-controlled-multiplicities). The gain in the two histograms is the same, with deviation at most 96 from its mean in each bin.

For every directed original edge $u v$ of $C_0$ with child $v$, take a fourteen-vertex block with source $s=x_v$ and target $t=x_u+x_v$. Use the downward paths supplied by the residual terminals, working outwards within each, with $336/14=24$ blocks on each path. All requested transfers fit. The edge of $C_0$ contributed $\mathbf e_t-\mathbf e_s$ when counted together with its child vertex. Each transfer cancels this difference, even when the old edge has since been subdivided. The current connected tree therefore has $E=V-\mathbf e_0$. All parent labels on the blocks are the labels of the actual preceding vertices.

Here $m\le24r<24k$, so the fourteen-vertex blocks altogether add at most $12012+98$ vertices in any bin. Their mean gain is at most 336. Thus the deviation incurred by the blocks is at most 12110 on either side.

## Completing all peeled layers

The following leaf operation applies whenever the old histograms have $E=V-\mathbf e_g$ and $j\le k$ new leaves have known parents. For $j<k$, take their parent labels as displacements and append one distinguished displacement equal to minus their sum, then enough zeros to reach $k$ entries. By Hall's permutation theorem these are the differences between the heads and tails of a permutation of the residues. Translate all arcs so the distinguished one has tail $g$. Removing it and the padding loops leaves the actual arcs with total head histogram minus tail histogram equal to $\mathbf e_g-\mathbf e_{g'}$, where $g'$ is its head. Give each leaf its assigned tail, making its actual sum equal to the head. The enlarged tree has a single gap $g'$ and all new labels are distinct. [Marshall Hall, *A combinatorial problem on abelian groups* (1952)](https://doi.org/10.1090/S0002-9939-1952-0050579-7)

For $j=k$ do this for the first $k-1$, then give the last leaf the label that makes its weight $g'$. If the resulting gap is $g''$, this full batch contributes $\mathbf1$ in edges and $\mathbf1-\mathbf e_g+\mathbf e_{g''}$ in vertices. Each vertex bin increases by at most two.

Restore the 336 layers in reverse order, omitting the sites already used by the blocks. Each layer's parents are present. This costs at most $2\cdot336$ more deviation per bin and keeps a single gap. All initially set-aside complete batches together cost at most one further deviation, since their unit corrections telescope. Adding the initial rank discrepancy (at most one), the subdivision error 96, the block error 12110 and these restoration bounds gives less than 13000. This also proves the statement when $C_0$ consists only of the root. At $k=1$ it is immediate.

If at least $13000k$ leaves are available at the zero root, every old vertex count is at most the floor of the new average. Fill to a balanced vertex histogram with $s$ among the high bins if any. Every new leaf has its own label as its weight, so the final edge histogram is balanced as well. For the maximum-degree assertion, protect the star at a vertex of degree $\Delta$ and use [protected leaf deletion](high-degree.md#preserving-a-connected-subtree-while-removing-leaves). At most $k-1$ of its neighbors still have exterior branches, so at least $\Delta-k+1$ neighbors are actual leaves. The one-vertex theorem labels the reduced core, and the protected batches extend it to the entire tree.

## Reproduction

The checker compares both actual path edge multisets with the requested transfer. It separately enumerates partial and full Hall batches, constructs entire trees with branches off the repair paths, restores their peeled leaves, and fills the single gap at the root. [Construction](../large_order_gap_paths.py) · [Independent checker](../check_large_order_gap_paths.py)

~~~sh
python3 -B -m research.check_large_order_gap_paths
lean research/large-order/GapPath.lean
~~~
