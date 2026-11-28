# Joining two fixed labeled trees by a long path

**Theorem at every modulus.** Join two independently $k$-cordial trees by a path with $t$ new internal vertices. Let $k\ge2$, put $e=2$ if $4\mid k$ and $e=1$ otherwise, and suppose $t\ge(3k-3)(ek+1)$. All old labels extend, subject to just one necessary condition. If $k$ is even and the final order is $qk+1$, the sum of the labels at odd-degree vertices of the final tree must have the parity of $q\sum\mathbb Z_k$. Those vertices are all in the fixed parts. For two divisible-order parts the bound improves to $k(ek+1)$. The one-label case is immediate.

Consequently an edge of **any prescribed cordial tree, of any order**, can be subdivided by any $t\ge(2k-2)(ek+1)$ while keeping all labels, subject to the same parity condition. Here the degrees of old vertices stay the same. Equivalently their old edge-weight sum must have the required parity. At large moduli, much shorter bridges suffice between two divisible-order parts. [Exact large-modulus result](../bounded-degree/bridge-cores.md)

## Realizing target counts

The construction allows **arbitrary initial labels** and prescribed final histograms. Write $V_0,E_0$ for the combined counts on the two disjoint nonempty trees, and let $a,b$ be the attachment labels. For a histogram $F$ write $m(F)=\sum_x xF_x$ in $G=\mathbb Z_k$. Every completion satisfies
$$
 m(E)-2m(V)=m(E_0)-2m(V_0)+a+b=:I.
$$
Indeed the new path-edge weights sum to $a+b$ plus twice the sum of the internal labels.

Choose $s\ge1$ and $Q\ge es$ with $t=Qk+s$. Let $V,E$ be target lists of the correct final sizes and moment. Suppose $X=V-V_0-Q\mathbf1$ and $W=E-E_0-Q\mathbf1$ are nonnegative. Their masses are $s$ and $s+1$. **Every such pair of targets can be attained.**

Write the internal path as $s$ consecutive disjoint blocks of orders $q_i k+1$ with $q_i\ge e$ and $\sum q_i=Q$. On each block we may prescribe its surplus residue $x_i$ and its first label independently. Its edges have uniform counts. If its first and last labels are $l_i,r_i$, summing the internal edge weights gives
$$
                 l_i+r_i=q_i S+2x_i,\qquad S=\sum G .
$$
This uses the endpoint version of the [prescribed-surplus path theorem and explicit rank construction](prescribed-path-surplus.md).

List the multisets $X$ and $W$ in any order, as $x_1,\ldots,x_s$ and $w_0,\ldots,w_s$. Start with $r_0=a$. Give block $i$ first label $w_{i-1}-r_{i-1}$. The endpoint identity gives $r_i=r_{i-1}+q_iS+2x_i-w_{i-1}$. After summation the last edge has weight $r_s+b=w_s$, precisely because the target moment requires $m(W)=a+b+QS+2m(X)$. Each block supplied its uniform counts and its chosen surplus. Each joining weight, including the two outside edges, occurred at its assigned position.

## Choosing balanced targets

For given old histograms take
$$
 h=\max\{1,\ k\max V_0-|V_0|,\ k\max E_0-|E_0|-1\}.
$$
Here $|F|$ denotes the sum of the entries. Take the least $s\ge h$ congruent to $t$ modulo $k$. The sharper sufficient length test is $t\ge s(ek+1)$. For every balanced final histogram, subtracting $Q\mathbf1$ leaves vertex bins of minimum at least $\lfloor(|V_0|+s)/k\rfloor\ge\max V_0$, and likewise for the edges with $|E_0|+s+1$. Thus any balanced targets meeting the moment are realizable.

If the edge counts have $j$ high bins with $1\le j<k$, fix any balanced vertex histogram. The $j$ high weights can have any prescribed residue sum. Starting at $0,\ldots,j-1$, distribute an increment of up to $j(k-j)$ from right to left, adding at most $k-j$ to each entry. The labels stay strictly increasing and $j(k-j)\ge k-1$. This gives the required edge moment. If all edge counts are $q$, the vertex counts are $q$ with one surplus $x$ and the equation becomes $2x=-qS-I$. This is automatic at odd $k$. At even $k$ it is solvable exactly at the parity in the theorem, since the sum of edge weights modulo two counts just the labels on odd-degree vertices.

For two cordial trees, each old histogram contributes at most $k-1$ to $k\max F-|F|$, so $h\le2k-2$ and $s\le3k-3$. For two divisible-order trees $h=1$. Upon cutting one edge of a cordial tree, the vertex list has discrepancy at most $k-1$ in the same expression, and deleting the edge increases the expression for edges by at most one. The minus one in $h$ absorbs this. Hence $s\le2k-2$ for subdivision.

## Arbitrary prescribed labels elsewhere in a tree

Let a tree carry any $p$ prescribed vertex labels, possibly on adjacent vertices. Suppose it has a path with at least
$$
                 13003\,k(p+2)(ek+1)
$$
unprescribed internal vertices of degree two. Then those prescriptions extend at every $k\ge2$, except when all of the following hold: $k$ is even, the order is $qk+1$, every odd-degree vertex is prescribed, and the sum of their prescribed labels has parity different from $qS$.

Remove the open path interval and partition the two remaining components into $m\le p+2$ connected pieces, each containing one prescribed vertex or one auxiliary root if the component has no pins. Growing simultaneously from all the seeds gives such a partition. The [rooted discrepancy theorem](../large-order/gap-path.md) gives each piece of size $n_i$ vertex counts within 13000 of $n_i/k$ and edge counts bounded above by $n_i/k+13000$. Translate at its root to keep the prescription. Translation permutes the two histograms. With $N_0$ old vertices and $m-2$ edges joining the pieces,
$$
 \max V_0\le N_0/k+13000m,\qquad
 \max E_0\le N_0/k+13000m+m-2 .
$$
If an even-modulus parity correction is necessary, change the label of an unprescribed odd-degree vertex by one. Choose an unprescribed leaf if one exists. Otherwise all leaves are prescribed, so any vertex has degree at most the leaf count, at most $p$. Thus this correction adds at most one to the vertex maximum and at most $m$ to the edge maximum. It flips exactly the required parity, including when the chosen vertex is an outside port. If every odd-degree vertex is prescribed, the parity is already determined. The preceding bound on $h$, using $|E_0|=N_0-2$, now gives $s\le 13003k(p+2)$. The long bridge completes the whole tree.

## Many prescribed positions on a path

At **every** $k\ge2$, any assignment on path vertices at mutual distances at least
$$
                     k(ek+1)+2k-1
$$
extends to a cordial labeling. The sole exception occurs at even $k$, order $qk+1$, when both tips are prescribed and their sum has parity different from $qS$. This includes repeated prescribed residues.

With at most one pin, translate a consecutive-sum path labeling. At a larger pin set, choose two consecutive pins. Inside their gap remove a segment of $t=k(ek+1)+r$ vertices, where $r$ is the residue of the whole order. Choose its start so that the first component has order divisible by $k$, advancing at most $k-1$ places. The stated distance guarantees room and leaves both pins outside. The second component is also divisible. Each can be labeled by induction, and the two-divisible-core bridge restores them. At even $k$ with final order one modulo $k$, if either tip is unpinned, first delete that tip. The remaining divisible path admits the prescribed labels, and the final edge fills its unique deficient weight. If both tips are pinned, they are exactly the odd-degree vertices used in the bridge test.

## Reproduction

~~~sh
python3 -B -m research.census.check_long_bridge
~~~

The [constructor](long_bridge.py) supplies all internal labels, and also constructs paths with multiple prescribed positions. The [separate checker](check_long_bridge.py) recomputes the actual vertex and edge counts on 890 complete joins and verifies 110 parity obstructions. It realizes 1,000 additional freely chosen, generally unbalanced target pairs and tests all 87,360 subset-sum inputs through modulus 64. On multiply prescribed paths it verifies 260 actual labelings and 40 impossible endpoint pairs.
