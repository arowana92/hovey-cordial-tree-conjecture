# Unicyclic graphs with unbounded maximum degree

**Theorem.** Fix $D\ge3$ and $0<\epsilon<1$. For all sufficiently large $k$, let $R$ be a simple connected unicyclic graph of order $k$ such that
$$
              E_D(R)=\sum_v\max(0,d_R(v)-D)\le k^{1-\epsilon}.
$$
If $R$ has at least two leaves, it has a bijection to $\mathbb Z_k$ making all $k$ endpoint sums distinct. Thus the [complete classification by leaf count and parity](unicyclic.md) also holds under this degree-excess hypothesis. The maximum degree may grow with $k$. Inserting any such harmonious graph opened at any cycle edge preserves all old labels and increases every count by one. The remainder of the old tree can have arbitrary degrees.

The construction replaces edges of $R$ temporarily. It prescribes labels making the replaced edges and their replacements have the same multiset of sums. This uses the attachment idea for [trees with unbounded degrees](excess.md), with a cycle among the reconnected pieces and a subgroup constraint on their prescribed labels.

## Redistributing the cut edges

Orient the unique cycle cyclically and all other edges away from it. Every vertex has one original parent and $d_R(v)-1$ children. Protect two original leaves $p,q$. At every vertex keep at most $D-1$ outgoing edges by cutting exactly its excess, giving priority to the two protected leaf edges. Also cut one designated cycle edge if it has not already been cut. This gives rooted tree components of maximum degree at most $D$; each root was the child of a cut edge. There are at most $1+E_D(R)$ cuts so far.

Cut five more edges with disjoint endpoints, avoiding all previous cut endpoints and the protected leaves. Before these five choices, the remaining graph has $k-O(k^{1-\epsilon})$ edges, degree at most $D$, and only $O(k^{1-\epsilon})$ vertices are excluded. Thus all five choices exist, and their parents are distinct from every final component root. Let $m\le6+E_D(R)$ denote the final number of cuts and components. Write $r_i$ for the roots and $b_i$ for their original parents. Put $P_* = \{r_i,b_i:0\le i<m\}$ and give each distinct vertex $v\in P_*$ its own variable $X_v$. The original cut weight is $W_i=X_{r_i}+X_{b_i}$.

In the remaining forest choose an independent set of sites outside the closed neighborhoods of $P_*\cup\{p,q\}$. Greedy choice produces at least $(k-O_D(m))/(D+1)$ sites. Order the components $C_0,\ldots,C_{m-1}$ by decreasing numbers of sites, reindexing their roots accordingly.

Choose a permutation $\sigma$ of all $m$ indices with $\sigma(j)\ne j$ and $b_{\sigma(j)}\ne r_j$. In the bipartite matching problem each right index excludes at most two left indices. Thus any three left indices see all right indices. Each individual left index also sees at least four of the five extra cuts, since their parents are outside the roots. This verifies Hall's condition for every left set.

Choose a site $s_0$ within $C_0$ and join it to $r_0$, creating a simple cycle since they were distinct and nonadjacent. For $j\ge1$, choose a fresh site $s_j$ in $C_0\cup\cdots\cup C_{j-1}$ and join it to $r_j$. Those first $j$ components contain at least $j(k-O_D(m))/((D+1)m)$ sites; this exceeds $j$ for sufficiently large $k$. The resulting graph $R'$ is connected and unicyclic, has maximum degree at most $D+1$, and retains the two original leaves. Prescribe
$$
                           x_{s_j}=W_{\sigma(j)}-X_{r_j}
$$
for every $j$, including the closing edge. All new edges now have exactly the cut weights as formal expressions.

## Keeping the labels in a subgroup

Some degree $d\ge2$ occurs $\Omega_D(k)$ times in $R'$, since $\sum(d_{R'}-1)=k$ and the maximum degree is bounded. Set $g=\gcd(d-1,k)$. We choose all variables in the subgroup $H=g\mathbb Z_k$. The site labels automatically lie there as well.

The vertex expressions on $P=P_*\cup\{s_j\}$ are distinct. Each site expression has its only negative coefficient at its own $r_j$, without cancellation by the choice of $\sigma$. The edge expressions induced on $P$ are exactly the $W_i$ and the weights of retained original edges between members of $P_*$. These are distinct as formal expressions because the original graph was simple. Sites had no other neighbors in $P$.

Order the variables by a parent-before-child order after ignoring the one designated cycle edge. For every original edge except that single edge, its child is its latest variable. Thus each variable is latest in at most two edge expressions. It is latest in only a bounded number of vertex expressions: its own variable, a site at which it is the positive child or negative root, and possibly the site using the exceptional edge. The original parent precedes the positive child on every other cut edge.

For either list test inequalities between all pairs. For pairs with different latest variables, at most $O_D(m)$ comparisons are decided at any one variable. Across the whole list there are only $O_D(m)$ pairs with the same latest variable. If that variable cancels, test the difference at its last surviving variable. Coefficients of differences have absolute value at most two. A nonzero such coefficient excludes at most two choices in the cyclic group $H$ for the last variable. Since $|H|=k/g\gg_D m$, greedy choice gives an injection on $P$ with all induced edge sums distinct. This argument also covers a cycle edge whose parent is assigned later than its child.

## Matching the two target moments

Open $R'$ at $s_0r_0$. Enlarge $P\cup\{p,q\}$ to a degree core $Q$ of this spanning tree as in the [bounded-degree construction](unicyclic.md#a-closed-graph-with-at-least-two-leaves). Add two isolated vertices $z,z'$ of the abundant degree $d$, away from the rest of the marks. These choices cost only $O_D(1)$ vertices beyond $P$, and the forbidden neighborhoods before selecting the pair have size $O_D(m)=o(k)$. The degree class still has at least six representatives outside.

Assign the other unprescribed vertices of $Q\setminus\{p,q,z,z'\}$ greedily in $H$. Only $O_D(m)$ labels are excluded per step, including collisions of edge sums in the closed graph. On the assigned vertices write $A=\sum (d_{R'}(v)-1)x_v$. We have $g\mid A$ because every assigned label lies in $H$. The congruence
$$
                       (d-1)(x_z+x_{z'})=-A\pmod k
$$
is therefore solvable. Fix a solution for the pair sum, and choose the two isolated labels distinct and fresh in $\mathbb Z_k$. The final two leaves supply $x_p+x_q$ needed to make the total core label sum equal to $\sum\mathbb Z_k$. At most $O_D(m)$ choices cause a vertex or edge collision, exactly as in the bounded-degree proof. This gives the two required moments, with the closing edge's weight absent on the cut tree.

Take the embedding parameter $\alpha$ sufficiently small for $D+1$ and smaller than $\epsilon$. Then $|Q|=O_D(k^{1-\epsilon})\le k^{1-\alpha}$. Lemma 4.9 gives the spanning rainbow bijection extending the prescribed labels. Restore the auxiliary closing edge to get a harmonious labeling of $R'$. Now restore **all** original cut edges in place of the auxiliary edges. None of their endpoint labels have moved, and their weight multiset agrees by construction. This proves the theorem. [Müyesser and Pokrovskiy, Lemma 4.9](https://arxiv.org/html/2509.05280v2#S4)

## Verification

~~~sh
python3 -B research/bounded-degree/check_unicyclic_excess.py
python3 -B research/bounded-degree/check_unicyclic_core.py
~~~

The [redistribution checker](check_unicyclic_excess.py) constructs graphs with adjacent high-degree vertices and computes actual site and root labels. It checks 76 cases through order 1,600, with as many as 35 cut edges. It checks simplicity, connectedness after removing the auxiliary closing edge, the degree bound, the two target moments, the degree-core condition, and equality of the original and restored endpoint-sum multisets. Four cases require a proper subgroup to solve the pair-sum congruence. The checker verifies the prescribed core; existence of its completion is the asymptotic theorem cited above.
