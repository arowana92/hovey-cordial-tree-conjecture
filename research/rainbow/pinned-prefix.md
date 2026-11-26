# Almost-spanning rainbow trees with prescribed labels

**Theorem.** Fix $0<\varepsilon<1$. For all sufficiently large $N$, let $T$ be a tree of order at most $(1-\varepsilon)N$. In any proper edge coloring of $K_N$, every given rainbow embedding of a connected subtree $S\subseteq T$ of order at most $N/(\log N)^{11}$ extends to a rainbow embedding of $T$. Here embeddings are injective, and rainbow means that all edge colors are distinct.

Montgomery, Pokrovskiy and Sudakov proved the almost-spanning embedding theorem without a prescribed image. We adapt their decomposition and random partitions below. The extension permits a prescribed parent for each component of an ordered tree cut. [Primary paper, Lemmas 4.2 and 7.1, Corollary 8.4 and Section 10](https://rhmontgomery.warwick.ac.uk/papers/14rainbowtreesanddecomposition.pdf)

## Keeping the prescribed subtree in the initial forest

Use the source's slack parameter $\eta=\min(\varepsilon/2,1/10)$, local color bound 1, and $D=\lceil(\log N)^{10}\rceil$. Choose its constant $\mu>0$ sufficiently small in terms of $\eta$. At every vertex of $S$ add $\lceil10^6 D/\mu^2\rceil$ pendant vertices to $T$, then apply the construction of Lemma 4.2 to the resulting tree. Its order increases by $O_\eta(N/\log N)$ and stays at most $(1-\eta)N$ for large $N$. If $S$ is empty the unprescribed theorem applies directly.

In the first stage at most $10^4D/\mu^2$ rounds remove leaves with distinct parents. Each prescribed vertex loses at most one of its added leaves in each round and stays in the tree. The next stage retains three leaf neighbors of each such vertex. Each vertex of $S$ therefore has degree at least three when the bare paths are removed. A removed path deletes its internal vertices and its edges, retaining its endpoints. No vertex of $S$ is internal, and no edge of $S$ is on a removed path since both its endpoints have degree at least three and the paths have length greater than one. Thus $S$ lies in the initial forest $T_0$.

In the proof of Lemma 4.2 a new detached edge can start the middle section of each removed bare path. Put one vertex of each such edge, as an isolated vertex, into all earlier forests. There are at most $\mu N$ such paths. The initial forest now has at most $2\mu N$ vertices. Each ordinary matching step adds one new leaf per center. The star step and the step inserting at most $\mu N$ bare paths of length three keep their form. Empty matching steps may be included. The number of steps is $O_\eta(D)$.

## Random partitions in the presence of prescribed vertices

Write $P$ for the prescribed images and $Q$ for their prescribed edge colors. Put $h=|P|$, so $|Q|<h$. Generate the source's initial independent vertex and color reservoirs $X_0,C_0$ with probability $p_0=\eta/200$. We will use the following simultaneous properties.

- Every vertex has at least $100\mu N$ neighbors in $X_0$ by colors in $C_0$. For a fixed vertex the count is binomial with parameters $N-1,p_0^2$, by properness.
- For every two distinct vertices there are at least $100\mu N$ length-three paths between them with disjoint interiors in $X_0$ and with all their colors distinct and in $C_0$. To see this even for endpoints in $X_0$, start before sampling. For fixed endpoints $u,v$, greedily build $\lfloor N/30\rfloor$ paths $u,a,b,v$. After $s$ paths, pick $a$ avoiding the endpoints, $2s$ used interiors and the at most $3s$ neighbors at $u$ with used colors. For $b$ avoid these used vertices, $u,v,a$, used colors at $a$ or $v$, and the color of $ua$ at $v$. At most $8s+4$ candidates are lost. Properness handles consecutive edges. Each path survives in the reservoirs with probability $p_0^5$, independently across this family. A binomial tail bound and a union bound over pairs give the claim when $\mu$ is sufficiently small.
- With probability tending to one, $|X_0|\le\eta N/100$ and at each vertex at most $\eta N/100$ incident edges have colors in $C_0$. The binomial estimates apply for any number of colors in the host.

Place $S$ as prescribed and grow its component in $T_0$ one vertex at a time using $X_0,C_0$. Start other components at fresh reservoir vertices. The first property permits this since each used vertex and each used color blocks at most one neighbor at any step. The image of $T_0$ lies in $X_0\cup P$ and its colors in $C_0\cup Q$.

For the large-star step delete all edges internal to $X_0\cup P$ and all edges of colors in $C_0\cup Q$. The center images form an independent set in the resulting graph, which has minimum degree at least $(1-\eta/40)N$ for large $N$, since $h=o(N)$. Apply Corollary 8.4 exactly to the enlarged demands in Section 10.3. In detail, if the desired leaf counts are $d_i\ge D$, with $d=\sum d_i$, the demands are $\lceil(1-\eta/8)Nd_i/d\rceil$. Their sum is at most $(1-\eta/10)N$ and there are at most $N/D$ centers. These meet the corollary's bounds using $\eta/40$. The resulting candidate leaf sets $Y_i$ avoid $X_0\cup P$, and their paired colors avoid $C_0\cup Q$.

Use the probabilities and coupling of Section 10.2–10.3 with the modified forest sizes. If $m_i$ vertices are added at step $i$, the nonfinal probabilities are $p_i=(1+\eta/4)m_i/N+\eta/(4\ell)$, and the final probability takes the remaining mass. In particular $p_i\ge N^{-1/10^4}$ and $m_i\le p_iN$. We may append an empty final step so the star step is nonfinal. The sets $Y_i$ are chosen before sampling $X_1$ in the complement of $X_0$. Each candidate leaf is coupled to its own distinct edge color when choosing $C_1$, just as in the source. These pairings lie entirely outside the original reservoirs. Consequently, conditional on $X_0,C_0$, every remaining color's membership in $C_1$ is an independent Bernoulli draw with parameter $p_1/(1-p_0)$, including colors without a partner. The remaining classes are drawn as in the source. This gives the required independent marginals *within* the vertices and within the colors. On a failure of the preliminary properties one can take the pairing empty, so the laws hold unconditionally.

The star concentration estimate of Section 10.3 applies since the enlarged demands and probabilities are the same. Thus there are enough paired candidates in $X_1,C_1$ at every center. Lemma 7.1 gives, simultaneously at every matching layer, a rainbow matching from each $A\subseteq V(K_N)\setminus X_i$ of size at most $p_iN$ into $X_i$ using $C_i$, missing at most $\mu p_iN$ centers. Its failure probability per layer is $o(1/N)$. There are only $O_\eta(D)$ layers. Fix one successful outcome.

## Finishing the embedding

Use the paired candidates for the large stars. At an ordinary matching step with center set $A$, first omit $A\cap X_i$. All its elements are in $P$ because every other old image belongs to an earlier palette. Apply Lemma 7.1 to the remaining centers. Discard edges whose new endpoint belongs to $P$ or whose color belongs to $Q$. The surviving matching is disjoint from previously used vertices at its new ends and entirely avoids used colors. Its deficiency is at most $\mu p_iN+3h$.

Complete each matching greedily using unused vertices in $X_0$ and unused colors in $C_0$. Complete the single path layer greedily using the length-three families above. The cumulative number of reserve entries needed for *all* matching completions is at most $\mu N+3h\ell=\mu N+o(N)$ on each side, by the bound on $h$. The initial forest uses at most $2\mu N$ on each side. The path layer uses at most $2\mu N$ further vertices and $3\mu N$ further colors. These bounds also hold at every intermediate step. At a matching center each occupied reservoir entry blocks at most one choice. At a path pair the used interior vertices and used colors each kill at most one candidate path per entry. Thus the total losses in either greedy operation are less than $100\mu N$. Vertices and colors previously used outside the reservoirs cannot block an interior choice from them. This completes the padded tree; deleting added leaves gives the assertion.

## Orders of minimum cordiality counterexamples

Let a rooted forest have $t\le(1-\varepsilon)k$ free vertices, with its component roots attached to prescribed residues, at most $\lfloor\log_2 k\rfloor$ distinct. For sufficiently large $k$, the free vertices can receive distinct residues avoiding any specified residue $u$, with all $t$ edge sums distinct, including the boundary sums.

Indeed, add one hub for each distinct prescribed value and include a hub for $u$ if necessary. Join all hubs to a new central vertex and connect each component root to its corresponding hub. Prescribe their star in the sum-colored complete graph on $\mathbb Z_k$, using any unused residue at its center. This is an injective rainbow embedding because translation permutes the hub values. Its order is $O(\log k)$, and the enlarged tree has at most $(1-\varepsilon/2)k$ vertices for large $k$. Apply the theorem, then discard the auxiliary edges. The embedding also avoids every hub label on the free vertices.

**Corollary.** For every fixed $\varepsilon>0$, if $k$ is sufficiently large and a smallest $k$-counterexample has order $n$, then
$$
(n-1)\bmod k > (1-\varepsilon)k .
$$
Take the child-size ordered preorder and write $n=mk+1+t$ with $0\le t<k$. Its first $mk+1$ vertices form a connected prefix. For $t>0$ this prefix is smaller and hence cordial, with a unique surplus vertex label and uniform edge counts. This includes the singleton prefix when $m=0$. The [ordered-cut inequalities](ordered-cut.md) give at most $\lfloor\log_2(t+1)\rfloor$ distinct boundary parents. If $t\le(1-\varepsilon)k$, the forest construction adds distinct labels avoiding the surplus, and distinct edge sums. Both histograms are then balanced, a contradiction. If $t=0$ and $n>1$, delete one leaf and use the unique deficient edge weight on restoring it. The singleton is cordial.

The corollary places a minimum counterexample close to a multiple of $k$ from below, allowing the multiple itself. Together with the [near-linear bound](../bounded-degree/projection.md), it restricts both the size and the residue of a minimum counterexample. The range within $o(k)$ of a multiple still includes the bijective base case $n=k$.

The direct check constructs 29,462 path families in two types of properly colored complete graph and recomputes their vertex and color disjointness. It also embeds 870 small forests through the auxiliary star and recomputes all original boundary and internal weights. The [cut verifier](../bounded-degree/check_prefix.py) checks the boundary-parent bound independently on 362,879 cuts. These finite checks exercise the constructions; the large-$k$ threshold follows from the proof.

~~~sh
python3 -B research/rainbow/check_pinned_prefix.py
python3 -B research/bounded-degree/check_prefix.py
~~~
