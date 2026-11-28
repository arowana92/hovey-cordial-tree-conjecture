# When a rooted tree can use the same labeling at two parents

Let $F$ be a rooted tree of order $k-1$ with root $r$. Seek a bijection from its vertices to $G\setminus\{0\}$ for $G=\mathbb Z_k$. It must give distinct edge sums after attaching $r$ to a parent of label $b$, and the **same bijection** must also work for parent $c\ne b$. The two parent choices are alternatives for one attachment edge. This is the condition that permits one stored permutation to serve both inputs when extending a cordial core with surplus zero.

**Theorem.** Fix a maximum degree $D$. For all sufficiently large $k$, every such $F$ except a path rooted at an endpoint admits a shared labeling for **every pair of distinct parents**. More precisely, prescribe the first label $x\ne0$ at $r$ and put
$$
             h=\gcd(k,d_F(v)-1:v\ne r).
$$
A shared labeling exists exactly when $h$ divides $(d_F(r)+1)x+b+c$. For an endpoint-rooted path the condition instead is $x+S+b+c\notin\{0,x\}$, where $S=\sum G$. [Endpoint-rooted paths](path-parent-pairs.md)

## Proof

In a successful labeling the internal sums omit precisely $x+b$ and $x+c$. Subtract the sum $S$ of the vertex labels from the sum $S-2x-b-c$ of the internal weights. This gives
$$
            \sum_{v\ne r}(d_F(v)-1)x_v=-(d_F(r)+1)x-b-c.
$$
Hence the divisibility is necessary.

For sufficiency, interchange $b,c$ if needed so $y=x+b$ is nonzero. Add one new leaf $o$ of label zero to $F$. If $b=0$, attach it directly at $r$. If $b\ne0$, choose a nonleaf $t$ different from and nonadjacent to $r$, of a degree occurring at least three times, and attach $o$ there. Prescribe $x$ at $r$ and $y$ at $t$. Such a degree occurs linearly often since the maximum degree is bounded and $\sum(d_F-1)=k-3$. When $b=0$, write $t=r$. Require the enlarged tree to miss weight $w=x+c$. The pinned labels are distinct at distinct sites and the sole induced pinned edge has sum $y\ne w$.

The enlarged tree has two unpinned leaves, since the original tree had two leaves other than $r$. The gcd of the unpinned degree-minus-one coefficients is still $h$. If $t\ne r$, its excluded coefficient is duplicated at another nonroot vertex. Apply the [completion theorem for pins and a prescribed missing weight](partial-gap.md). Its only further condition is that $h$ divide $w+\sum_{v\text{ pinned}}(d(v)-1)x_v$, using degrees of the enlarged tree. For $t=r$ this is exactly $(d_F(r)+1)x+b+c$. For $t\ne r$ the difference from that expression is $(d_F(t)-1)(x+b)$, divisible by $h$. Thus the completion exists. Delete $o$ to obtain internal weights missing $y$ and $w$. Either parent fills one. The cited completion theorem uses [Müyesser and Pokrovskiy's Lemma 4.9](https://arxiv.org/html/2509.05280v2#S4).

Finally, $h$ divides both $k$ and $\sum_{v\ne r}(d_F(v)-1)=k-2-d_F(r)$, hence $h\mid d_F(r)+2$. In particular $d_F(r)+1$ is a unit modulo $h$, and $h\le D+2$. Every pair $b,c$ therefore permits a choice of nonzero $x$ when $k$ is sufficiently large.

The [prescribed forest spectrum](forest-spectrum.md#changing-one-parent-without-relabeling-the-forest) extends the two-parent criterion to sublinear total degree excess and arbitrary additional rooted components with their own boundary labels.

## Exact row counts

With $x$ fixed, let $m=k/h$, $t=-(d_F(r)+1)x\bmod h$, and $f=|\{j\bmod h:2j=t\}|$. The minimum number of permutations covering all $k$ parent labels is
$$
                       \frac{k+f\,(m\bmod2)}2.
$$
Indeed, the parent-pair graph has a complete bipartite component on each pair of distinct residue classes $j,t-j\bmod h$, and a complete graph on each fixed class. A pair of distinct classes takes $m$ rows. A fixed class takes $\lceil m/2\rceil$, since $m\ge2$ for large $k$. With $x$ free the graph is complete, so the minimum becomes $\lceil k/2\rceil$. With $x$ free and unit multiplication allowed it becomes $\lceil\tau(k)/2\rceil$, where $\tau(k)$ counts the unit orbits, one per divisor. The same two free-root minima hold for endpoint-rooted paths by the [path-pair theorem](path-parent-pairs.md#the-minimum-number-of-preselected-rows).

**An all-moduli extremal example.** Without a degree bound, a star of order $k-1$ rooted at its center requires exactly $k-1$ stored rows, or $\tau(k)-1$ with units. If the center is $y\ne0$, its internal weights omit $y,2y$, so its two parents are exactly $0,y$. Every $y\ne0$ works. These counts are the worst possible among all single-component forests that individually extend at each parent. Choose a row working at zero. It automatically works at a second, nonzero parent because exactly two internal weights are unused. Thereafter one row per uncovered parent, or per uncovered orbit, suffices.

Root the same star at a leaf with label $x$, retaining center label $y\ne x$. Its parents are $y-x,2y-x$. An ordered pair $b,c$ in these roles requires $y=c-b$ and $x=c-2b$. It works if $b\ne0$ and $c\ne2b$. Testing both orders, the only impossible unordered pairs are $\{0,k/2\}$ for even $k$ and $\{k/3,2k/3\}$ for $3\mid k$. These star claims hold at every $k\ge3$, with an endpoint serving as center in the two-vertex star.

## Independent checks

At $k=8$, exhaustive enumeration of all $7!$ permutations on each of the 47 rooted seven-vertex trees other than the endpoint-rooted path found 5,849 feasible root-label and parent-pair triples. There were 2,758 further triples satisfying the necessary gcd but failing at this small modulus. With the root label free, 59 shape and parent-pair combinations failed. An independent run generated rooted trees as multisets of children and searched each fixed triple by reserving its two missing weights before assigning the remaining vertices. It reproduced all four counts. These are obstructions to sharing a row between parents. The ordinary eight-label theorem permits choosing the row after learning the actual parent.

The [checker](check_tree_parent_pairs.py) implements direct enumeration through eight labels, compares the two star formulas with 29,369 literal label choices through 45 labels, computes 67 maximum matching sizes independently, and verifies the enlarged-tree gcd and pinned moment on 6,000 attachments.

~~~sh
python3 -B research/bounded-degree/check_tree_parent_pairs.py
~~~
