# An attached forest and a near-spanning subdivision

**Theorem.** At every sufficiently large modulus $k$, take an arbitrary labeling on an old tree and choose an edge with endpoint labels $a,b$. Attach a forest of $h$ new vertices at prescribed old parents and subdivide the chosen edge by $k-h$ vertices, where
$$
1\le h\le\lfloor\sqrt{k}\rfloor-2 .
$$
All old labels can be kept while giving **exactly one net new occurrence of every vertex residue and every edge residue**, with just one exception. The exception requires odd $k$, a single two-vertex path attached at an old label $p$, and $a+b=2p$. In that case uniform increments are impossible.

A consequence for a smallest ordinary counterexample of order at least $k+2$ is that it has no bare path with $k-\lfloor\sqrt{k}\rfloor+2$ consecutive internal degree-two vertices. The old labeling in the theorem need not even be cordial. The proof uses the sufficiently-large-group threshold of Müyesser and Pokrovskiy; it gives no numerical value for that threshold. [Theorem 6.9, author copy](https://discovery.ucl.ac.uk/id/eprint/10205648/1/Pokrovskiy_s00222-025-01328-x.pdf) · [Published paper](https://doi.org/10.1007/s00222-025-01328-x)

## A path with specified labels, weights and old endpoints

Write $S=\sum_{i\in\mathbb Z_k}i$. Let $V$ be any set of $k-h$ new vertex labels. Let $W$ be a multiset of $|V|+1$ weights, each used at most twice and with at most one repeated residue. A path from prescribed $a$ to prescribed $b$ with these internal labels and these actual edge weights exists exactly when
$$
\sum W=a+b+2\sum V .
$$
The two old endpoint labels may agree and may occur in $V$. Necessity follows by summing along the path. The same assertion holds for $h=0$ in the sufficiently-large range.

For sufficiency, the addition-graph case of Theorem 6.9 states that different endpoints $v,w$ outside a set $I$ can be joined by a path using precisely the internal vertices $I$ and distinct colors $C$ if $|I|+1=|C|\ge k-\sqrt k$ and $\sum C=v+w+2\sum I$. In the cyclic addition graph the color of an edge is its endpoint sum. We reserve a few edges to supply the external labels and the possible repeat before applying that theorem.

If $W$ has no repeat, choose distinct $u,w\in V$ with $a+u,b+w$ distinct and in $W$. Fix those two end edges. If $W$ repeats $d$, first choose $u,v\in V$ with $u+v=d$, $u\ne v$, and $a+u$ in the support of $W$ outside $d$. For $u$, the two membership conditions exclude at most $2h$ residues, doubling excludes at most two, and the weight condition excludes at most $h+1$. Now choose $w\in V\setminus\{u,v\}$ with $b+w$ in the support outside $a+u,d$. This excludes at most $2h+4$ residues. The large-modulus hypothesis leaves choices; the distinct-weight case costs even fewer exclusions. Fix edges $a,u,v$ at the start and $w,b$ at the end. After removing those three weights the remaining colors are distinct, including one remaining copy of $d$.

Apply Theorem 6.9 from $u$ to $w$ in the first case, or from $v$ to $w$ in the second. The internal set omits the two or three reserved members of $V$. Subtracting the fixed edges from the displayed moment equation gives exactly the required path moment. The remaining color count is $k-h-1$ or $k-h-2$, both at least $k-\sqrt{k}$. Reinserting the reserved edges gives the claimed path.

## Choosing labels for the small forest

The following calculation allows separate offsets on the attached forest, and even an offset on the old edge. The replacement path uses ordinary endpoint sums. Let $D$ be the actual old edge weight. Let $s_i$ be the edge offset at a free child of a free vertex, and the old parent label plus the edge offset at a component root. Write $d_i$ for the number of free children of vertex $i$, $x_i$ for its label and $y_i$ for its entering weight. Thus $y_i=x_i+s_i$ at an external edge and $y_i=x_i+x_{p(i)}+s_i$ otherwise.

The free labels must be distinct. If they form $X$, the path receives $V=\mathbb Z_k\setminus X$, and must realize $W=\mathbb Z_k+\{D\}-\{y_i\}_i$ as a multiset. If $W$ is nonnegative it automatically has at most one repeat. The path moment is equivalent to
$$
\sum_i(1-d_i)x_i=T,\qquad T=S+a+b-D+\sum_i s_i .
$$
A terminal vertex has coefficient one. When there are at least two terminals, choose two of them as the last rows. Label the remaining $h-2$ vertices in parent-first order, avoiding each earlier label and each earlier weight on the next edge. At the end the two terminal labels must sum to a prescribed residue $R$. Set them to $z,R-z$. Keeping their labels and their weights away from the previous rows excludes at most $4(h-2)$ choices of $z$. Making the two labels distinct, and the two new weights distinct, excludes at most four further choices. Since $4h<k$ for sufficiently large $k$ in our range, the forest admits distinct labels and distinct entering weights.

With one terminal the forest is a single path in its parent-first order. Its tip label is forced to be $T$. For $h=1$ this suffices. For $h\ge3$, choose all nontip labels independently and uniformly. Each possible collision of vertex labels has probability $1/k$. The same is true for any two entering weights: their difference contains a free label with coefficient $1$ or $-1$. At the two ends the only fixed vertex labels are the external label (already part of $s_1$) and the final tip. When $h\ge3$ the first and last weights use different free variables. The union of the vertex and edge collision events has probability at most $h(h-1)/k<1$.

For $h=2$ on a single path the labels are $z,T$, and the weights are $z+s_1,z+T+s_2$. If $s_1\ne T+s_2$, just avoid $z=T$. If $s_1=T+s_2$, the repeated weight must equal the removed weight $D$ to make $W$ nonnegative. This forces $z=D-s_1$. Thus the only obstruction with offsets is the simultaneous equality $s_1=T+s_2$ and $D-s_1=T$. In ordinary coordinates $T=S+p$ and $s_2=0$. The equalities become $S=0$ and $a+b=2p$, as claimed. If $h=0$ is allowed, the necessary and sufficient condition is $S+a+b-D=0$.

## Tree consequences

Put $H=\lfloor\sqrt{k}\rfloor-2\ge3$. Suppose a minimum counterexample on at least $k+2$ vertices has a bare segment with $k-H$ internal vertices. Suppress that segment, retain its replacement edge and delete $H$ more vertices by successive leaf removals that avoid the retained edge. There is sufficient room: at least $H+2$ vertices remain after suppression, and a tree larger than the retained edge always has a leaf outside its endpoints. In reverse, those deletions form an attached forest with exactly $H$ vertices. The smaller tree is cordial by minimality, and its labeling extends by the theorem, a contradiction.

More generally choose an edge of an $n$-vertex tree. For $n\ge3$, subdividing that edge by any number at least
$$
k\left\lceil\frac{n-2}{H}\right\rceil-(n-2)
$$
suffices for cordiality. Keep the chosen edge and peel batches of $H$ vertices by leaf removals until a path remains or fewer than $H$ free vertices remain. If the last smaller batch is needed, peel all vertices outside the retained edge. When its size is two, a nonpath on four vertices is a star, whose two removed vertices are independent leaves. An already remaining path needs no batch. Every other batch is covered by the theorem. If the last batch is partial and necessary, the cost of the $k-h$ subdivisions for each batch sums to the displayed quantity. Stopping earlier on a path costs at most $(k-H)\lfloor(n-2)/H\rfloor$, also within the bound. Place excess subdivisions on the starting path, then restore the batches. For a core on $3\le n\le H+2$ this gives the single-period bound $k+2-n$.

## Every prefix of a pendant path

There is another extension for a prescribed cordial core of order $qk+r$, $1\le r\le\lfloor\sqrt k\rfloor-1$. At any chosen old vertex, **one infinite sequence of labels makes every finite pendant-path prefix cordial**. At the next divisible order at least $k-2r+1$ different terminal labels are attainable.

Let $X,Y$ be the high vertex and edge sets of the old core, of sizes $r,r-1$. Set $A=\mathbb Z_k\setminus X$, $B=\mathbb Z_k\setminus Y$, and let $p$ be the old parent label. A path with new vertices exactly $A$ must use all but one color $d$ of $B$. If the new tip is $t$, taking moments gives
$$
d=t+\sum B-p-2\sum A .
$$
Thus the attainable tips are **exactly** those $t\in A$ with $d\in B$. There are at least $k-2r+1$ choices. For each, take $u\in A\setminus\{t\}$ with $p+u\in B\setminus\{d\}$. At most $2r+1$ choices are excluded. Reserve this first edge. Apply Theorem 6.9 from $u$ to $t$ with internal set $A\setminus\{u,t\}$ and colors $B\setminus\{d,p+u\}$. The displayed equation is precisely its sum condition. The color count is $k-r-1\ge k-\sqrt k$.

The new labels and the actual new weights are distinct and avoid the old high bins, so every prefix up to the divisible order works. The next vertex fills the deficient edge bin. This restores a one-surplus core and the construction repeats indefinitely. In particular a smallest counterexample of order $mk+s$ with $s>\lfloor\sqrt k\rfloor-1$ can have no terminal arm longer than $s-\lfloor\sqrt k\rfloor$. Otherwise deleting $s-(\lfloor\sqrt k\rfloor-1)$ of its tip vertices reaches a smaller tree in the covered order class.

## Verification

~~~sh
python3 -B -m research.census.check_near_period
~~~

The constructor reduces the requested packet to an actual simple-color Hamilton-path problem. The finite checker searches the reduced instance from both ends, joins its witness to an explicit old tree, and counts every original and final vertex and edge residue. It separately enumerates the moment-compatible assignments in the ordinary two-vertex obstruction. The replay includes 386 complete forest-and-path extensions, 70 incompatible inputs, 28,470 moment-compatible negative assignments, and 5,715 intermediate prefixes on 165 prescribed pendant completions. The unrestricted existence step is Theorem 6.9. [Reduction](near_period.py) · [Witness replay](check_near_period.py)
