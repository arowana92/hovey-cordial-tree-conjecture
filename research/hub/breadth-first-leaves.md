# Two or three leaves at every vertex

**Theorem.** Let $H$ be any tree of order $h\ge k$, for any positive integer $k$. Attach at least three new leaves at each vertex of $H$. The resulting tree is $k$-cordial. Two leaves at each vertex suffice if $h\ge2k$ or $k$ divides $h$. Each site's population may be chosen independently.

The proof constructs the labeling at the given modulus. It uses a breadth-first numbering to bound the old edge counts, then realizes the exact residual counts by zero-sum partitions. For sufficiently large $k$ a [different construction](private-leaves.md) allows just one leaf per vertex at orders divisible by $k$ and tolerates some unoccupied sites near order $k$.

## An exact criterion with uniform parent colors

Write $G=\mathbb Z_k$ and $\sigma=\sum_{x\in G}x$, so $2\sigma=0$ in $G$. Suppose the old labeling uses each vertex residue $a$ times. Let $M_w$ count its edges of weight $w$. Attach $Bk$ leaves, $B\ge1$, whose parents have each residue exactly $B$ times. At the resulting order $(a+B)k$ an extension preserving the old labels exists exactly when
$$
 M_w\le a+B\quad(w\in G),\qquad M_d<a+B,\qquad
 d=(a+B)\sigma-\sum_w wM_w.
$$
Indeed the new leaf labels must use each residue $B$ times. The sum of all new edge weights is $2B\sigma=0$, forcing $d$ to be the one final deficient bin. The displayed inequalities mean that the required additional multiset of weights, of size $Bk$ and sum zero, has nonnegative counts.

Partition this multiset into $B$ blocks of size $k$ and sum zero. With at least $2k$ positions left, the Erdős–Ginzburg–Ziv theorem finds a block in any $2k-1$ positions. The last $k$ entries sum to zero. Hall's prescribed-differences theorem realizes each block as the termwise sums of two permutations of $G$ (negate the sources in the difference formulation). Match the first permutation to the physical parents and use the second for the leaf labels. This proves sufficiency even if the original edge counts were unbalanced. [Erdős–Ginzburg–Ziv, original paper](https://combinatorica.hu/~p_erdos/1961-25.pdf) · [Marshall Hall Jr., original paper](https://doi.org/10.1090/S0002-9939-1952-0050579-7)

Once a divisible order is labeled cordially, arbitrarily many further leaves at the original sites can be added. The first fills the deficient weight. From order one modulo $k$, up to $k-1$ leaves can use distinct labels avoiding the surplus vertex color and can have distinct weights. Repeat these steps as needed. [Leaf extension proof](../counterexample-bound.md#removing-leaves)

## The old edge counts

The case $k=1$ is immediate. Write $h=qk+r$, $0\le r<k$. Number the original vertices $0,\ldots,h-1$ in breadth-first order, with the children of each vertex consecutive. For each $i>0$ let $p_i$ be its parent's number. Then $p_i$ is nondecreasing, so the integers $i+p_i$ are strictly increasing and belong to $[1,2h-3]$. Give vertex $i$ label $i\bmod k$.

For $r=0$ the old vertices use each residue $q$ times and the old edges use each at most $2q$ times. Take two leaves per vertex, giving $B=2q$ and target $a+B=3q$. The criterion applies with strict slack at every bin. For a single leaf at every vertex the same fixed numbering succeeds exactly when the forced bin $d=-\sum_{i>0}(i+p_i)$ occurs fewer than $2q$ times. For instance at $h=k=5$ the parent indices $(0,0,0,3)$ give weights $(1,2,3,2)$ and $d=2$. This fixed numbering cannot extend with one leaf per site.

For $r>0$, put $R=\{0,\ldots,r-1\}$ and $t=k-r$. The original vertex bins have size $q+1$ on $R$ and $q$ elsewhere. Give $t$ chosen leaves the labels $r,\ldots,k-1$ to bring the old labeling to uniform multiplicity $a=q+1$. Call these the helper leaves. After their shifts and weights have been chosen we will reserve $B$ leaves at each parent color and apply the criterion. Take $\ell=2$ for $q\ge2$ and $\ell=3$ for $q=1$. There are at least $\ell q\ge q+2$ available leaves at every color and another $\ell$ at each color in $R$.

For $2r\le k$, the original edges use each bin at most $2q+1$ times. Bins reaching $2q+1$ must belong to $[1,2r-3]$. For $2r>k$ the corresponding maximum is $2q+2$, attained only in $[1,2r-k-3]$. These bounds count the possible occurrences in $[1,2h-3]$. Each interval is empty if its upper bound is less than one.

## Choosing the helpers

* **$2r\le k$ and $t\le\ell r$.** Reserve $B=q+2$ leaves per color. For helper input $r+i$ use shift $\lfloor i/\ell\rfloor$, $0\le i<t$. Each shift belongs to $R$ and is used at most $\ell$ times. The increasing integer weights $r+i+\lfloor i/\ell\rfloor$ lie in an interval of length $t+\lceil t/\ell\rceil-1<k$. Hence each bin gains at most one. The resulting maximum $2q+2$ is strictly below $a+B=2q+3$.
* **$2r\le k$ and $t>\ell r$.** Reserve $B=q+1$, leaving at least one helper available at every color. Assign the helper inputs distinct shifts giving distinct weights. For odd $k$, the shift $x$ at input $x$ works. For $k=2m$, use shifts $x$ for $0\le x<m$ and $x+1$ for $m\le x\le2m-2$. Both shifts and weights are distinct (the latter run over disjoint parity classes). Add one to every input while keeping those shifts, so the omitted input becomes zero, then restrict to the desired $t$ inputs. Translating all helper shifts by $c$ preserves their distinctness and that of their weights. It moves the forced deficiency $d$ by $-tc=rc$. One can place $d$ outside $[1,2r-3]$, since $k>(\ell+1)r$ and the complement contains $\gcd(k,r)$ consecutive residues. Each bin now has at most $2q+2=a+B$ edges. At $d$, at most $2q$ original edges and one helper contribute.
* **$2r>k$.** Reserve $B=q+2$. For $0\le i<t-1$ give helper input $r+i$ shift $i$. The weights $r+2i$ are distinct modulo $k$, since $t<k/2$. Let the last helper, with input $k-1$, take a shift $s\in R$. Each such shift still has helper capacity because $\ell\ge2$. At most $t-1$ choices repeat an earlier helper weight. As $s$ varies, $d$ varies with slope $-1$. At most $\max(0,r-t-3)$ more choices put $d$ in the interval of original bins of maximum size. Together these exclusions are fewer than $r$. Thus the combined maximum is at most $2q+3=a+B$, with strict inequality at $d$.

In each case the criterion labels the reserved leaves. The remaining leaves can then be restored from divisible order, proving the theorem.

## Construction check

Run the [constructor and direct histogram checker](breadth_first_leaves.py) from the repository root.

~~~bash
python3 -B -m research.hub.breadth_first_leaves
~~~

The replay builds 4,707 labelings using all rooted ordered core shapes through eight vertices and all $k\le h$ for those shapes. It builds another 348 with independently varying site populations at moduli through 45. For each it recomputes both histograms from the physical endpoints and includes bins of count zero. It also checks the fixed five-vertex failure above. The universal theorem follows from the counting argument and the two zero-sum results.
