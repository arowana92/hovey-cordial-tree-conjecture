# Prescribing the edge histogram of a bijectively labeled tree

Fix $D\ge3$ and $0<\epsilon<1$. Let $G=\mathbb Z_k$, $S=\sum_{x\in G}x$ and $E_D(F)=\sum_v(\deg_F(v)-D)_+$. A target histogram $H$ is a multiset of residues of size $|E(F)|$. Let $Q$ be the set of residues absent from $H$ and $P$ the multiset of copies above the first in its occupied bins. Thus $H=G-Q+P$, allowing arbitrarily many copies of one residue.

**Tree theorem.** Let $F$ be a tree on $k$ vertices. Specify $x_r=a$ at any vertex. An edge $ij$ has weight $x_i+x_j+\eta_{ij}$, where at most $b$ offsets differ from a common value. Suppose $E_D(F)+b+|Q|\le k^{1-\epsilon}$. Write
$$
 A=\sum H-S-\sum_e\eta_e,\qquad C=S-A,\qquad c_v=\deg_F(v)-1.
$$
For all sufficiently large $k$ there is a bijection $x:V(F)\to G$ with exactly histogram $H$ and the specified label if and only if
$$
             \gcd(k,c_v:v\ne r)\mid A-c_ra .
$$
When the tree is a path and $r$ is an endpoint, also require $2a\ne C$. With ordinary weights and no prescribed label the only condition is $\gcd(k,c_v:v\in V(F))\mid A$. In particular, at odd order every such unpinned tree realizes every target satisfying the size bound, since $\sum c_v=k-2$.

**Unicyclic theorem.** Let $F$ instead be a connected simple unicyclic graph on $k$ vertices, with ordinary weights and $E_D(F)+|Q|\le k^{1-\epsilon}$. Specify a cycle vertex $r$ and its label $a$. For a graph with exactly one leaf, choose $r$ away from its degree-three junction. At all sufficiently large $k$ the exact conditions on $H$ are as follows.

| Leaves | Condition |
|---|---|
| None | $A=S$ |
| One | $A\ne S$ |
| At least two | $\gcd(k,c_v:v\in V(F))\mid A$ |

The [all-divisor extension](spectrum-projection.md) allows sparse original ring offsets and proves the exact two-edge-tail condition for a forced repeated weight. The prescribed cycle label introduces no additional congruence. For a unicyclic graph $\sum c_v=k$, so the gcd with $k$ is unchanged on deleting any one coefficient. The uniform target specializes to the [harmonious census by leaf count](shifted-rings.md). For trees the single-omission ordinary case specializes to the [root and missing-weight theorem](rooted-gap.md).

## Moments and construction

The incidence sum gives $\sum c_vx_v=A$ and $\sum(\deg_F(v)-2)x_v=-C$. The latter forces the two path endpoints to sum to $C$. On a cycle it gives $C=0$, and on a one-leaf graph the tip label equals the junction label plus $C$. This proves necessity. For an unpinned tree take any internal root. An admissible $a$ exists exactly when the gcd using all vertices divides $A$.

Subtract the common offset from every tree edge and translate the target weights by the same amount. The quantities $A,C$ are unchanged. In the unicyclic case open a cycle edge incident with $r$, marking both ends. Denote its eventual weight by $w$. In the tree case reserve one $w\in Q$, possible since there are $k-1$ edges. Pair every extra copy $p\in P$ with a distinct omission $q$. On a ring use every omission. On a tree use every omission except $w$.

We will select a separate ordinary edge for each pair, prescribe its endpoint sum to be $p$, and temporarily give it an offset $q-p$. In the temporary problem this edge must therefore have weight $q$. A temporary bijection using every weight once on the ring, or every weight except $w$ on the tree, gives exactly $H$ when these offsets are undone. The fictitious offsets need not be equal and the extra values $p$ may repeat.

### Choosing the edges

In the spanning tree cut all its original nonzero-offset edges and at most $E_D(F)$ more edges to cap the remaining degrees at $D$. Mark all cut endpoints, the prescribed vertex, and the opening endpoints if present. Put $M=1+E_D(F)+b+|Q|$. If at least two original leaves other than $r$ are still unmarked, reserve two. Some degree $d$ between two and $D$ occurs on $\Omega_D(k)$ original vertices, since degrees above $D$ contribute $O_D(E_D(F))$ to $\sum c_v$, and this sum is $k$ or $k-2$. Put $g=\gcd(k,d-1)$ and mark a representative other than $r$ for each nonzero residue of $c_v$ modulo $g$ occurring there. These representatives are never leaves. Otherwise mark every vertex of original degree different from two. In this case the original number of leaves is $O(M)$ and the degree sum bounds the number of branching vertices by $O(M)$ as well.

Choose the paired edges above as an induced matching away from the marks, reserved leaves and their neighbors. Their endpoints are marked and they are also cut. There is room for all $|P|$ edges. Any set of $O_D(M)$ excluded vertices meets $O_D(M)$ edges, since its degree sum is bounded by $D$ times its size plus $E_D(F)$. The same bound holds after excluding its neighbors. At each fresh edge both endpoint degrees are bounded, as all high-degree vertices were marked or incident to a cap cut. Consequently each choice rules out only $O_D(1)$ more endpoints, and $M=o(k)$.

Apply the [paired reconnection](sparse-offset-growth.md#a-bijective-rainbow-base-with-sparse-offsets) to these cuts. For each cut choose a private edge, with all private edges forming an induced matching away from the enlarged marks and reserves. Cut it too. In the components select independent sites away from these neighborhoods, of original degree $d$ in the reserved-leaf case. The total pool is $\Omega_D(k)$. Order components by decreasing pool size. Root the original spanning tree in the first component. Each later component has as root the child of one of the cuts and can be joined to a fresh site in an earlier component. An initial segment of $j$ components has at least $\Omega_D(jk/M)>j$ sites. Within each pair exchange the two cut weights when choosing these new edges. Specifically, if $b,t$ are the cut children of a main edge $ab$ and its private edge $st$, the new sites have labels $X_s+X_t-X_b$ and $X_a+X_b+\delta_{ab}-X_t$, respectively. Here $\delta$ includes the temporary offsets.

The result is a bounded-degree tree $U$. Let $K$ comprise the original marks, private endpoints and used sites. Its size is $O_D(M)$. All degree changes are in $K$. The induced weights of $U[K]$, together with the opening weight on a ring, have exactly the temporary weights between the original marked endpoints. No used site has another marked neighbor in the original tree, and all its new incident wires are prescribed. It remains to make these weights distinct, give $U$ the missing weight $w$ and apply the embedding theorem.

### Assigning the pins

Give the two endpoints of each paired edge labels $Z_i,p_i-Z_i$. The shared edge is the only original marked edge incident to these endpoints, by the neighborhood exclusions for subsequent private endpoints and sites. Its temporary weight is the constant $q_i$. Give $r$ its prescribed label $a$.

With two reserved leaves, choose residues modulo $g$ for the marked representatives so that
$$
                    \sum_{v\in K} c_v X_v=A\pmod g.
$$
Give other independent original variables residue zero. Each second paired endpoint has residue $p_i$, the anchor has residue $a$, and the new sites have original coefficient zero modulo $g$. The gcd of the representative coefficients with $g$ is exactly $h=\gcd(k,c_v:v\ne r)$, since some unpinned degree-$d$ vertex remains. The contributions of the paired endpoints are multiples of $h$, so the assumed divisibility is precisely what is needed to choose the representatives.

Without two reserves, every unpinned original position has degree two, as do the private endpoints before the cuts. Impose $\sum_v(\deg_F(v)-2)X_v=-C$ directly. The cycle needs no equation beyond $C=0$. With one leaf substitute $X_y=X_j+C$ for its tip $y$ and junction $j$. On a path anchored at an endpoint the far endpoint is the constant $C-a$, distinct from $a$. In all other cases there are two leaves $z,y$ other than the anchor. Eliminate the second by setting
$$
              X_y=C-X_z+\sum_{v\ne z,y}(\deg_F(v)-2)X_v .
$$
All positions in this last sum with nonzero coefficients are ordinary original marks.

We give details of the inequality count because the number of paired edges can exceed $\sqrt{k}$. The two lists to make injective are the marked vertex labels and the induced temporary weights, including $w$ (the opening edge on a ring, a reserved constant on a tree). All constant weights $q_i$, and the additional constant $w$ on a tree, are distinct. They produce $O(M)$ comparisons per nonconstant form. Each paired vertex variable occurs on just its two individual labels outside the site forms. On a pair of cuts the private coefficients of the two endpoints and two sites are respectively $e_s,e_t,e_s+e_t,-e_t$. These four vectors are distinct and private to this pair, even after the imposed sums and leaf substitutions. Thus comparisons involving a site cannot become identical vertex forms.

Order ordinary free variables parent before child in the spanning tree, followed by the private variables. Before the two-leaf substitution every nonconstant ordinary edge form has its child as latest variable, except for a bounded number of edges (the opening, an edge into a fixed endpoint, or the substituted one-leaf edge). Moving the private variables to the end affects only their induced matching edges. The paired edges are constants. Thus each variable is latest in $O(1)$ nonconstant weight forms. The same bound holds for the vertex list by the private coefficient vectors and the two labels per paired variable. For comparisons with different latest variables this costs $O(M)$ per variable. There are only $O(M)$ pairs sharing a latest variable in either list, so a cancellation there also costs at most $O(M)$ at any earlier variable.

For the one-leaf substitution the only original weights that could have identical variable pairs are the edges to a common neighbor of the leaf and its junction. Their constants differ by $C\ne0$, as all ring edges were ordinary before the remote pairs were selected. A direct leaf-junction edge has the unique doubled variable. Fixing the single regular anchor does not identify other edge forms. A single remaining endpoint variable comes from an edge at that anchor, which cannot neighbor both the junction and its leaf. For a path with its two ends fixed, their incident edges have different neighbors for $k>3$. Other ordinary edge forms have distinct pairs of variable endpoints.

In the two-leaf substitution put $X_z$ last. Each edge comparison involving $z$ or $y$ has coefficient $\pm1$ or $\pm2$ there, since each leaf has one incident edge and the two leaf edges differ. There are $O(M)$ such comparisons. Each leaf occurs in only a bounded number of vertex forms before substitution, including sites, since at most one main cut touches that leaf. If the $X_z$ coefficient cancels in such a comparison, either a private coefficient survives or the comparison is between individual vertex labels. In the latter case a comparison involving $z$ or $y$ has a nonzero $X_z$ coefficient. When a private coefficient survives, its variable follows all ordinary variables and its absolute value is at most two. Thus even a large branching coefficient in the substituted sum never decides a comparison. The preceding count applies to the other inequalities.

Each last surviving coefficient therefore excludes at most two residues of the group at its step, or at most two choices within the required coset when choosing the actual variable there. Each coset has $k/g\gg_D M$ elements ($g=1$ without reserves). Greedy choices give an injection and all the required weight inequalities.

### Completing the bijection

Apply the [partial-label and missing-weight criterion](partial-gap.md) to $U$ and its pins. With reserves, both leaves are unpinned in $U$. The gcd of $k$ and the unpinned coefficients $\deg_U(v)-1$ divides $g$ because an untouched degree-$d$ vertex remains. On the pins the exchanged weights give
$$
             \sum_{v\in K}(\deg_U(v)-1)X_v+w
                      =\sum_{v\in K}c_v X_v-A\pmod k .
$$
Indeed on a ring the sum of all temporary offsets is $-A$, and the removed opening contributes $w$. On a tree the sum of all temporary offsets is $-A-w$. This proves the required divisibility. Without reserves, all unpinned positions of $U$ have degree two. The identical exchange of edge sums gives $\sum_{v\in K}(\deg_U(v)-2)X_v=-S-w$ from the imposed original moment. This is the exhausted-degree case of the criterion. In both cases the criterion extends the pins to a full bijection using $G\setminus\{w\}$ on $U$. Undo the reconnections, restore the opening on a ring, and remove only the fictitious offsets to obtain $H$. The external completion theorem is [Müyesser and Pokrovskiy, Lemma 4.9](https://arxiv.org/html/2509.05280v2#S4).

## An attached forest with a prescribed missing weight

At a sufficiently large modulus, take a prescribed cordial core of order one modulo $k$. Translate its surplus label to zero. Attach a rooted forest of $k-1$ new vertices, with $t$ roots at prescribed old parent labels $b_1,\ldots,b_t$ in these coordinates. Write $a_v$ for the number of children of a new vertex. If $E_D(F)+t\le k^{1-\epsilon}$, a permutation of the nonzero residues can give all new weights except a prescribed $w$ exactly when
$$
                        \gcd(k,a_v:v\in F)\mid w+\sum_i b_i .
$$
For a single endpoint-rooted path also require $S+w+b_1\ne0$. The same labeling is cordial on every parent-first prefix of the attachment. This includes components that are single vertices and needs no assumption on the number of nonroot leaves.

Use one dummy vertex of prescribed label zero. Join it to the roots, putting offset $b_i$ on each entering edge, and apply the tree theorem with $H=G\setminus\{w\}$. Each nondummy coefficient $c_v$ is $a_v$, the total offset is $\sum_i b_i$, and the augmented excess increases by at most $2t$. Decrease the exponent slightly to absorb this constant factor. The endpoint exception is exactly the dummy-rooted path. The actual entering sums equal the shifted dummy sums. New labels enter distinct low vertex bins and new edges enter distinct initially uniform bins. The argument also prescribes an entire sparse histogram $H$ on the attachment by the same substitution in the tree theorem. [Earlier prescribed-gap result with additional pins](forest-spectrum.md)

## Several edge replacements with exactly uniform total increments

Take any labeled tree. Replace specified edges by simple unicyclic graphs on $k$ new vertices opened at specified cycle edges. The old endpoints attach to the two ports. For the moment assume each piece has at most $k^{1-\epsilon}$ leaves. Require each new piece to use every vertex label once, and all edge frequencies together to gain exactly the number $t$ of pieces. For all sufficiently large $k$ this is possible under the following exact conditions, at arbitrary old labels and tree order.

* If all the pieces are cycles, require $tS=0$.
* If just one piece has leaves and it has exactly one, require $tS\ne0$.
* If some piece has at least two leaves, or at least two pieces have leaves, it is always possible.

To see this, assign a sum difference $A_i$ to each piece. On a cycle it must equal $S$. With one leaf every value except $S$ is available. With two or more leaves every value is available, because the leaf bound gives $E_3=O(k^{1-\epsilon})$ and leaves an ordinary degree-two vertex. These restrictions are necessary even with free port labels, since the net sum of entering edges minus the old edge restores exactly the two endpoint incidences lost at the opening. Summing over pieces, uniform total increments require $\sum_i A_i=0$.

The listed conditions suffice to select these differences. One unrestricted difference can supply any remainder. With two one-leaf pieces, the last two differences can sum to any remainder while both avoid $S$. Put $z_0=0$ and $z_i=z_{i-1}+A_i$. Prescribe the closed edge histogram $G+[z_i]-[z_{i-1}]$ on piece $i$, taking $G$ when the two bins agree. At the opening $uv$ attached to old endpoints $a,b$ by $au,vb$, specify $x_v=x_a$. The new edge at $a$ then replaces the opening weight and the new edge at $b$ replaces the old weight. Either direction can be used, so in the one-leaf case choose the regular port as the anchor. The unicyclic theorem applies. Since $z_t=z_0$, every frequency transfer cancels. In particular any two one-leaf pieces at large odd modulus jointly give exact uniform increments on arbitrarily labeled old edges.

More generally the same argument allows $E_D$ in place of the leaf bound on each piece. A piece with at least two leaves permits the differences in its coefficient-gcd subgroup, by the unicyclic theorem. Existence of one permitted difference per piece summing to zero is still necessary and sufficient. The number of pieces is unrestricted, since the size threshold for each use of the theorem depends only on $D,\epsilon$.

## Checks

The [constructor](edge_histogram.py) builds the auxiliary tree, all prescribed labels and the embedding core. A [separate checker](check_edge_histogram.py) recomputes the actual tree degrees, two embedding moments, modified weight multisets and the original sums on every selected edge. The checks produced 720 tree cores, including twelve with a proper coefficient divisor, and 354 unicyclic cores. They rejected 16 tree targets and 101 ring targets. In 202 successful ring cases an extra weight was prescribed repeatedly. A separate enumeration checked 35,390 small bijections and 26,414 opened pieces, and an independent sumset calculation checked 10,527 simultaneous difference tests. A literal attachment replay checked 2,110 balanced prefixes covering 364 attained gaps. It also found 58 additional failures at small moduli outside the asymptotic claim. The large-modulus sufficiency uses the embedding lemma above.

~~~sh
python3 -B research/bounded-degree/check_edge_histogram.py
~~~
