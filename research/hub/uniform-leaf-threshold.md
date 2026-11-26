# A uniform minimum number of leaves at every core vertex

**Theorem.** For every positive integer $h$ there is a computable integer $C_h$ with the following property. Take any tree $H$ of order $h$. At each vertex $v$ attach any number $m_v\ge C_h$ of new leaves. The resulting tree is super edge-magic and hence $k$-cordial for every positive integer $k$. The threshold depends only on $h$. It is independent of the largest population, the total population and all population ratios.

For five core vertices, $C_5=5940$ suffices. The proof gives an explicit, much larger recurrence at higher orders. The older five-parent construction has a different use when most sites receive few or no leaves. [Five-parent theorem](many-leaf-parents.md)

The integer labeling has vertex interval $[L,U]$ and edge-sum interval $[L+1,U]$, with no repetitions. Each interval has balanced residue frequencies at every modulus. A simultaneous translation puts the vertex labels in $[1,n]$ and preserves the consecutive-sums property. Youssef proves the implication to cordiality. Figueroa-Centeno, Ichishima and Muntaner-Batle give related constructions, including equal populations on odd-order graphs satisfying a labeling hypothesis in their Theorem 2.1. [Youssef, Theorem 4](https://ajc.maths.uq.edu.au/pdf/43/ajc_v43_p031.pdf) · [*Magical coronations of graphs*](https://ajc.maths.uq.edu.au/pdf/26/ajc_v26_p199.pdf)

## Extending a fixed labeling

A seed consists of the labeled core and finitely many additional leaves at its vertices, already satisfying the two interval identities. Write $p_v$ for the core labels. Suppose $0,1$ are both core labels. For a vector of still unspent, nonnegative integer populations $n_p$ at core labels $p$, put
$$
M=\sum n_p,\qquad W=\sum p n_p,\qquad D=1+\max p-\min p,\qquad B=(2h+2)D^2.
$$

**Exact completion lemma.** The condition $0\le W\le M$ is necessary for extending the two intervals while retaining their alignment and the seed labels. It is sufficient whenever $n_0,n_1\ge B$. With arbitrary populations, including zeros, it is equivalent to the existence of a positive integer dilation of the population vector that permits an extension.

Indeed, the total of the edge sums minus the total of the vertex labels is $-L$. A new leaf at $p$ increases this difference by $p$. The new lower endpoint must therefore be $L-W$, so exactly $W$ of the $M$ new vertex positions are below the old interval.

An upper block of length $d$ with permutation $\pi$ uses label $U+1+i$ at parent $\pi(i)-i$ for $0\le i<d$. For a lower block use $L-d+i$ at parent $1+\pi(i)-i$. The edge sums fill their required new bands. Write $j=0,1$ for the two parent offsets. A rotation by $a$ of $a+b$ positions gives $b$ occurrences of $j+a$ and $a$ of $j-b$. A singleton gives $j$.

For rational populations with $0\le W\le M$, divide the mass rationally into an upper part of moment zero and a lower part of mass and moment both $W$. A uniform fraction $W/M$ has moment $W^2/M\le W$. Taking the largest $W$ units by parent label has moment at least $W$. Indeed, if there are at least $W$ units at positive parents they all have label at least one, and otherwise the top $W$ omits only nonpositive mass. Interpolate the two choices. When $M=0$ the allocation is empty. On each side match positive and negative displacements in rational multiples of the rotation above, each time exhausting one displacement type. Use singleton blocks for zero displacement. This gives at most $K=2h+2$ coefficients, each on a block of length at most $D$. Clearing their denominators proves the dilation assertion. [Exact rational allocation](radius_threshold.py)

For the assertion at the given populations set aside $\min(B,M-W)$ leaves at zero and $\min(B,W)$ leaves at one. The remaining mass and moment still satisfy the two inequalities. Apply rational allocation and use the integer parts of the block coefficients. The residual requested populations are nonnegative integers of total $r<KD$ since they are exactly what the fractional parts would have supplied.

If $W,M-W\ge B$, both full reserves are available. Each residual $p>1$ can be supplied by a lower rotation with parents $p,0,\ldots,0$ of length $p$. Each $p<0$ can use an upper rotation with parents $1,\ldots,1,p$ of length $1-p$. At most $rD\le B$ filler leaves are charged to either reserve. Use all remaining zeros and ones singly.

If $W<B$, the working moment is zero and all its blocks are upper. Thus the residual displacements sum to zero. Read them as steps on the integer line. Split the resulting closed walk into simple cycles by removing the segment closed at each repeated position. Translate each cycle to its own upper band and fix the unused positions in its span. A cycle of $s$ steps of magnitude at most $D$ uses a band of length at most $1+(s-1)D\le sD$. The fixed positions cost at most $rD\le B$ leaves at zero. The full reserve at zero is available since $M\ge2B$. If $M-W<B$, apply the same construction below with displacements $p-1$ and filler leaves at one. Finish with the unused reserve singletons. This proves the lemma, including both extremal moments. [Constructor and verification](uniform_leaf_construct.py)

## Choosing the core labels

For proposed populations $m_v$, compute $M=\sum m_v$ and let $R=M-\max_v m_v$ be the mass away from a largest site. We prove by induction that for every $h\ge5$ there is a seed of order at most $N_h$, with $0,1$ on core vertices, whose labels satisfy
$$
\min(W,M-W)\ \ge\ \eta_h R,\qquad W=\sum_{v\in H}p_v m_v. \tag{1}
$$
Here the moment uses the **original** populations. The seed may use filler leaves before the populations are charged. The end of the proof pays for them.

### The five-vertex certificate

There are three five-vertex trees, the path, the star and the tree of degree sequence $3,2,1,1,1$. The certificate checks (1) with $N_5=17$ and $\eta_5=1/22$ simultaneously for all nonnegative populations on each tree. Each seed gives its five core labels, the endpoints of its interval and the parent of every missing integer in increasing order of the missing labels. The verifier reconstructs every edge and checks both interval identities. Both labels $0,1$ belong to the original core.

Normalize a nonzero population vector to have sum one and choose a decreasing order of its coordinates. The chamber for this order is the convex hull of the uniform distributions on its first $r$ coordinates for $1\le r\le5$. This follows by subtracting consecutive sorted coordinates. Write $e$ for the first vertex of this simplex and $z$ for an arbitrary point of the opposite tetrahedral facet. Every profile in the chamber has the form $(1-t)e+tz$ with $0\le t\le1$.

For each of the 120 orders the certificate subdivides the interval for $t$ or bisects an edge of the tetrahedron for $z$. Both child cells are included at every split. At a terminal cell, check the two moment inequalities at both endpoints of $t$ and all four vertices for $z$. Each side of (1) is affine separately in $z$ and $t$ on the chamber, since the largest coordinate is fixed. Interpolation proves (1) throughout the cell. All verification arithmetic is exact. The zero vector satisfies (1) for any seed.

| Core | Seeds | Terminal cells | Verified $\eta$ | Largest $D$ | Most fillers | Sufficient minimum population |
|---|---:|---:|---:|---:|---:|---:|
| Path | 147 | 738 | $1/22$ | 9 | 10 | 5841 |
| Star | 144 | 720 | $1/17$ | 9 | 11 | 4552 |
| Degree sequence $3,2,1,1,1$ | 152 | 726 | $1/22$ | 9 | 12 | 5940 |

For the last column, $B=12D^2$ and $R\ge4\min m_v$. If the seed has at most $F_0$ fillers, paying them lowers either moment slack by at most $F_0 D$. It suffices that $\min m_v\ge B+F_0$ and $4\eta\min m_v\ge B+F_0D$. These are sufficient bounds. Paths and stars as cores also admit direct smaller-diameter or caterpillar constructions. [Certificate](five-vertex-leaf-seeds.json) · [Independent verifier](uniform_leaf_verify.py)

### Removing a light leaf or using two adjustable labels

Suppose $h\ge6$. Write $N=N_{h-1}$, $\eta=\eta_{h-1}$ and take
$$
c=\frac{\eta}{4(N+1)},\quad F=2^{h+4},\quad
Y=2F+\lceil 2/c\rceil+4,\quad Q=2(Y+F).
$$
Use $\eta_h=\eta/2$ and $N_h=\max(2N,2Q+h,h+\lceil16FQ/c\rceil)$.

If a leaf $z$ of $H$ has $m_z\le cR$, apply induction to $H-z$. Its mass away from a largest site is at least $R-m_z$. To reinsert $z$ at a parent of label $p>0$, place $z$ at $L-p$ and add leaves at zero in the intervening lower positions. For $p\le0$, place it at $U+1-p$ and add leaves at one in the intervening upper positions. The required edge fills the first available weight in the band and the fillers supply all others. The interval length at most doubles since it contains $0,1$. Both $|p_z|$ and $|1-p_z|$ are at most $2N$. Thus each moment slack is at least $\eta(R-m_z)-2Nm_z\ge\eta R/2$. This case also handles $R=0$ by removing a zero-population leaf.

We may now assume that every leaf of $H$ carries more than $cR$ and $R>0$. First consider $M<QR$. Choose two leaves $x,y$ of $H$ and apply the adjustable-label construction to them. Its seed starts with a path in $H-\{x,y\}$ labeled $-1,1,0$, places the intervening core, then varies the negative label at $x$ and positive label at $y$. It gives $M/4\le W\le3M/4$. For clarity, once $x,y$ can start at $-F,F$, move the label with larger population outwards if necessary to cross the target $M/2$ in its direction. Finish with the nearer of two steps of the other label on the opposite side of that crossing. The error is at most $\min(m_x,m_y)/2\le M/4$. The seed construction and size estimates give $D_*=2+\max|p_v|\le4FM/\min(m_x,m_y)$ and at most $4D_*$ filler leaves. This use of a seed takes place before deducting any fillers, so it requires only positive populations at the two adjustable leaves. Hence the order is at most $h+16FQ/c$, and (1) follows. [Adjustable labels and size estimates](many-leaf-parents.md#placing-an-arbitrary-core)

### One vertex holds most of the mass

It remains to consider $M\ge QR$. Give a largest site $o$ label zero. If $H$ is a star centered at $o$, assign its neighbors $1,\ldots,h-1$. The two seed intervals hold and $R\le W\le(h-1)R$.

Otherwise choose a path $o,u,v$ and label it $0,1,-1$ in order. Its weights are $1,0$. Choose a leaf $q$ outside this path. Such a leaf exists because the tree has more than three vertices, and a component outside the path has a terminal vertex. Grow $H-q$ from the path, placing each new vertex in an upper band. At a nonnegative parent $p$, place the child at $U+1$, with $p$ filler leaves at $-1$ immediately above it. At a negative parent use the upper insertion rule from the light-leaf case. The new edge and fillers give the whole new upper weight band in either case. All new core labels are positive. At each step $U+1$ at most doubles, so the upper endpoint and all parent magnitudes stay below $F$.

Place $q$ at $Y$ by first padding above at zero and then using the same upper insertion. The resulting upper endpoint is at most $Y+F$, and the lower endpoint remains $-1$. Only the single core vertex $v$ has a negative label. We have $m_q>cR$, so $W\ge Ym_q-R\ge R$. Also $W\le(Y+F)R\le M/2$. The star case satisfies the same two bounds. This proves (1), completing the induction. [Seed implementation](uniform_leaf_seed.py)

## Paying for the seed

At order $h\ge5$ take $B_h=(2h+2)N_h^2$. All core labels lie in an interval of length at most $N_h$ containing $0,1$. Paying the seed uses at most $N_h$ leaves and changes either moment slack by at most $N_h^2$. In particular the following explicit choice suffices:
$$
C_h=\left\lceil\frac{B_h+2N_h^2}{\eta_h}\right\rceil .
$$
Indeed $R\ge(h-1)C_h$, so the unspent populations have both moment slacks at least $B_h$ and at least $B_h$ leaves remaining at each of $0,1$. Apply the exact completion lemma. For $h=5$ the direct bounds in the table improve the recurrence. For $h\le4$ the core is a path or a star. Leaves on a path form a caterpillar, and leaves on a star produce diameter at most four. The consecutive-sums results for these families give $C_h=0$. [Caterpillar construction and diameter-four proof](all-radius-two.md)

## Reproduction

Run the following from the repository root using standard Python 3.9 or later. The first command reads only the finite certificate and verifies the coverage argument. The next two reconstruct exact blocks, including endpoint moments, and independently count the requested leaves and verify the interval permutations. The tests include explicit whole-tree endpoint sums, very unbalanced populations and each case of the seed induction.

~~~sh
python3 -B -m research.hub.uniform_leaf_verify
python3 -B -m research.hub.uniform_leaf_construct
python3 -B -m research.hub.uniform_leaf_seed
~~~

To regenerate the seed certificate, the search matches unused vertex positions to weights and subdivides any population cell without a common seed. Floating-point distances only select which edge to bisect. The independent verifier reconstructs every bisection with rational numbers.

~~~sh
python3 -B -m research.hub.uniform_leaf_search > /tmp/hovey-five-vertex-leaf-seeds.json
cmp research/hub/five-vertex-leaf-seeds.json /tmp/hovey-five-vertex-leaf-seeds.json
~~~

[Certificate search](uniform_leaf_search.py) · [Earlier three-parent completion](many-leaf-parents.md)
