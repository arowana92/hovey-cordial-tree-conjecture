# A reduction with no degree bound on the inserted tree

**Theorem.** There is an absolute $c>0$ such that the following holds at every sufficiently large modulus $k$. Remove $t-1$ edges from a prescribed $k$-cordially labeled tree and attach the resulting components to a tree $U$ of order $k$. Within each free vertex the incoming old endpoint labels must be distinct. Write $L$ for the number of leaves of $U$ receiving no entering edge. If
$$
                          t+L\le c\sqrt{k},
$$
the old labeling extends except precisely in the [four-condition parity case](port-parity.md). The internal degrees of $U$ and all degrees outside it are unrestricted.

Consequently a smallest counterexample at sufficiently large $k$ cannot have a connected $k$-vertex part with $t$ edges out at distinct vertices and $L$ original leaves inside when $t+L\le c\sqrt{k}$. Reconnect the outside components by any tree on their attachment vertices. The smaller tree has a cordial labeling, and its edge counts are nonuniform since the order of a smallest counterexample is never one modulo $k$. Restoring the part gives the contradiction. The [path obstruction](port-threshold.md#a-path-obstruction-at-every-large-modulus) shows the square-root order is sharp for preserving prescribed labels when repeated sites are allowed.

## Distributing the high degrees

Put $s=t+L$. There are at most $s$ leaves of $U$, since each other leaf receives at least one entry. There are at most $s-2$ vertices of degree at least three. Mark the ports and every nonzero position of $\delta_v=d_U(v)-2+m_v$, with $m_v$ the number of entries at $v$. There are $O(s)$ marks, and all vertices of original degree different from two are among them. The sum of the positive coefficients is $t-2+L=s-2$.

Root $U$ at any leaf. Cap the number of retained children at two, cutting all further child edges. There are at most $s-2$ cuts because the sum of the degree excesses above two is the leaf count minus two. In the capped forest cut five extra edges with disjoint endpoints away from prior endpoints and marks. The forest has maximum degree three and $k-O(s)$ remaining edges, so these choices exist. Keep the parent-child orientation of every cut. The $q=O(s)$ cuts leave $q+1$ components with distinct roots, the old root and the cut children. Put all roots and cut endpoints in the base marks.

Outside the closed neighborhoods of the base marks in the remaining forest, choose an independent set of original degree-two sites. There are $\Omega(k)$ such sites since only $O(s)$ vertices have a different original degree or were excluded, and the remaining degree bound is three. Order the components by nonincreasing number of sites. For each component after the first connect its root $r$ to a fresh site $u_r$ in an earlier component. The first $j$ components contain at least $\Omega(jk/(q+1))>j$ sites. The wires make a tree $A_0$ of maximum degree at most four.

Match each of these $q$ roots $r$ to an original cut edge $ab$ **not incident to it**. Each cut edge forbids at most two roots, so any three roots together see every cut. Every single root sees at least four of the five additional disjoint edges. Hall's condition follows for sets of all sizes. Give every base mark an independent variable $X_v$ and prescribe the site label
$$
                              x_{u_r}=X_a+X_b-X_r .
$$
The wires now have exactly the weights on the original cuts. The site expressions are distinct from the base variables and from each other since their unique negative variable is at their respective root. Among the marks there are no other edges at these sites. The weights on marked auxiliary edges thus have exactly the forms of distinct original internal edges on base marks. Together with the entering weights there are $O(s)$ forms, since the graph induced by any vertex subset of an original tree is a forest. These statements do not require a bound on the number of expressions involving a single variable.

## Matching the moment without losing the prescribed wires

Let $h=\gcd(k,\delta_v:v\in U)$. If every coefficient vanishes, the free tree is a path with its two tips as its only ports, already covered by the bounded-degree theorem. Otherwise $h\le s<k$ for large $k$. As in the [square-root proof](port-threshold.md#choose-the-bins-after-drawing-the-joint-labels), retain one moving bin $z$ in a compatible histogram transfer. At least one quarter of $h\mathbb Z_k$ is attainable as the required moment $K+bz$, $b\in\{-2,-1,1,2\}$. Draw all base variables independently uniformly. The actual $H=\sum\delta_v X_v$ is uniform on that subgroup, since all nonzero coefficients are at base marks, and every new site had original coefficient zero.

The $O(s^2)$ pair comparisons for vertices and weights now use coefficients bounded by two. A constant comparison between entering weights at the same vertex is satisfied by local distinctness. Fixed gaps give at most $O(s)$ further comparisons of the same size. For a moving edge gap the bad form is $H+w-K$, with $w$ an entering or internal weight; for a moving vertex gap it is $H-2x_i-K$, with $x_i$ a base or site form. Their coefficients are $O(s+1)$. Each nonconstant form therefore vanishes with probability $O((s+1)/k)$, and there are only $O(s)$ such tests.

For completeness, the very small numbers of entries can be handled with the same estimate. The coefficient sum of $H+w$ is $t-2+1$ or $t-2+2$. The only zero-sum case is $t=1$ with an entering weight. The coefficient at its port cannot be $-1$, since negative coefficients occur only at nonport leaves. For $H-2x_i$ a zero vector would require $t=4$. If there is a negative coefficient it is $-1$ and cannot be twice an integer. Otherwise a site form has a negative coefficient and cannot give $H$. Thus the only possible failure is $\delta=2e_i$ for a base vertex. Then all augmented degrees are at most four and the bounded-degree repeated-port theorem already applies.

Choose $c$ small enough that the probability of a collision is less than $1/4$. We can therefore realize the exact moment and all the inequalities, including those for the additional sites. The degree correction of the marked labels in $A_0$ agrees with that in $U$ because the removed and added sums agree, with every affected endpoint marked. There are $k-O(s)$ ordinary degree-two sites in $A_0$. Apply the [ordinary and vertex-transfer segments](port-parity.md#realizing-both-transfers-at-once) there away from the marks. These operations pin any additional degree changes. The final auxiliary tree has maximum degree at most five and a degree core of size $O(s)$. Choose six isolated ordinary positions to finish the vertex sum. The exact moment gives the required color sum as before. Lemma 4.9 extends the prescribed embedding for this absolute degree bound. Undo the segments and then restore all the high-degree cut edges in place of their matched wires. The actual changed weights have the prescribed net histogram, proving the theorem. [Müyesser and Pokrovskiy, Lemma 4.9](https://arxiv.org/html/2509.05280v2#S4)

## Verification

~~~sh
python3 -B research/bounded-degree/check_sparse_incidence.py
~~~

The [degree redistribution](port_degree_reduction.py) constructs the actual cut edges, matches roots to cuts, selects sites and prescribes their labels. The [independent check](check_sparse_incidence.py) tests the final auxiliary embedding targets against the original high-degree trees, recomputing connectivity, label and weight increments, both target moments and the degree classes. It verifies 283 positive targets and five parity obstructions, with adjacent original joints of degree up to 26 and auxiliary maximum degree at most five.
