# A short alpha-labeled supertree and a modulus bound on the original tree

**Theorem.** Every tree with $m\ge1$ edges and diameter $D$ occurs as an induced subtree of an $\alpha$-labeled tree with at most $2m-D$ edges. More precisely, root the input at height $h$. Choose a vertex at level $h-1$ with $c\ge1$ children. There is such a host with at most $2m+1-h-c$ edges, in which the original root has within-class rank zero. Every host admits one integer labeling that is cordial at every modulus.

**Original tree.** Let $P$ be any path between two leaves of an $n$-vertex tree. Count the vertices on $P$ and all original leaves adjacent to it, counting each vertex once. If this leaves $d$ vertices uncounted, then the original tree is $k$-cordial for **every $k\ge n+d$**. This bound permits arbitrary numbers of leaves at any vertices of the path. A sharper test for any particular breadth-first ordering is given below.

Okechukwu's Theorem 1.1 constructs a graceful host of at most $2m-D$ edges by matching missing differences in a level ordering to intermediate vertices. Its last-level attachment can put both endpoints on the same side of the label threshold. We use the level-block idea with two within-class rank lists, and complete their upper ends to keep every edge between classes. Earlier work studied super edge-magic tree hosts and range-relaxed labelings using layered trees. [Okechukwu, §§2–3](https://arxiv.org/html/2611.01340v1#S3) · [Ichishima, Muntaner-Batle and Rius-Font](https://www.researchgate.net/publication/268711436_Embedding_trees_into_super_edge-magic_trees) · [Barrientos and Krop](https://arxiv.org/abs/1402.0196)

## Completing the two rank lists

Order children arbitrarily at each vertex and use breadth-first levels $0,\ldots,h$. Write $t_i$ for the width of level $i$, $c_{ij}$ for the child count of vertex $j$ in it, and $P_{ij}=\sum_{l<j}c_{il}$, using indices starting at zero. For $i<h$ choose $s_i$ between zero and the number of initial childless vertices in that level, inclusive. In particular $s_0=0$. Start $a_0=a_1=0$ and put
$$
a_{i+2}=a_i+t_i+t_{i+1}-1-s_{i+1}\qquad(0\le i<h-1).
$$
Give vertex $(i,j)$ rank $a_i+j$ in class $i\bmod2$. Between original blocks of either class, fill each rank gap with auxiliary vertices. The vertices for level $1\le i<h$ have ranks $a_{i+1}-t_i+j$ in the class opposite to $i$, one for each $s_i<j<t_i$. These ranks run from the end of level $i-1$ plus one to the start of level $i+1$ minus one.

Put $K_i=a_i+a_{i+1}$. The original edges out of $(i,j)$ have rank sums
$$
K_i+j+P_{ij}+[0,c_{ij}-1].
$$
Allow an empty interval for a childless vertex. Over all $j$, these intervals together with the single omitted sums $K_i+j+P_{ij}-1$ for $s_i<j<t_i$ partition
$$
[K_i+s_i,\ K_i+t_i+t_{i+1}-2].
$$
Indeed consecutive starts advance by $c_{ij}+1$. The first $s_i$ parent blocks are empty. The next transition begins immediately after the current one, since $K_{i+1}+s_{i+1}=K_i+t_i+t_{i+1}-1$. The transitions begin at zero and end at the sum of the two largest original ranks.

For the omitted sum at $(i,j)$ attach its auxiliary vertex to rank $a_i+t_i-1+P_{ij}$ of class $i\bmod2$. The ranks add to the specified sum. A host of this rank is either the last original vertex of level $i$, a vertex farther down the level order, or beyond the current largest rank of that class. Let $M_b$ be the largest original rank in class $b$ and let $H_b$ be its maximum with all host ranks required in that class. Add ranks $M_b+1,\ldots,H_b$ in class $b$. First attach all these new class-zero vertices to original rank $M_1$. Attach the new class-one vertices to rank $H_0$ in class zero. The two batches use precisely the remaining consecutive sums from $M_0+M_1+1$ through $H_0+H_1$. They connect to the original tree. Every interior auxiliary vertex points either to an original vertex, a later auxiliary vertex, or a member of these final batches. Hence all vertices are connected, and there is one extra edge per extra vertex. The original tree is induced.

The final within-class ranks are $[0,H_0]$ and $[0,H_1]$, and their edge sums are $[0,H_0+H_1]$. Adding $H_0+1$ to the ranks of class one gives consecutive vertex labels and consecutive edge sums. Reflecting one class in its rank interval gives the equivalent $\alpha$-labeling by differences.

To obtain the size bound, order the children on the path to the specified penultimate vertex so it is last in its level. First use $s_i=0$ everywhere. Before the last transition, every required host rank lies between the final rank of level $i$ and the initial rank of level $i+2$, inclusive, since $P_{ij}\le t_{i+1}$. At the last transition the largest required excess above level $h-1$ is at most $t_h-c$. Thus the number of new vertices is at most
$$
\sum_{i=1}^{h-1}(t_i-1)+t_h-c=n-h-c.
$$
The claimed bound follows. With $h=D$ this is at most $2m-D$ edges. Increasing the $s_i$ only lowers starting ranks, removes some host requests, and decreases or preserves each remaining requested rank. Thus each final $H_b$ can only decrease. The two-list completion is linear in the input order. A singleton is immediate.

## Restricting the original sums

There is a shorter construction when only distinct labels and sums on the original tree are needed. Let $\ell_i$ and $r_i$ be the number of initial and final childless vertices at level $i<h$. Leave exactly
$$
g_{i+1}=\max(0,t_{i+1}-1-r_i-\ell_{i+1})
$$
unused ranks between original levels $i$ and $i+2$ in the same class. The first two levels still start at rank zero. These are the least nonnegative gaps making the entire spans of successive transition sums disjoint and increasing. The last actual edge in transition $i$ has sum $a_i+a_{i+1}+t_i+t_{i+1}-2-r_i$. The first in the next has sum $a_{i+1}+a_{i+2}+\ell_{i+1}$. Substituting $a_{i+2}=a_i+t_i+g_{i+1}$ gives the formula. Within a transition the child blocks give strictly increasing sums.

The combined span lengths of the two vertex classes total $N=n+\sum_{i=1}^{h-1}g_i$. Put the second rank interval immediately above the first. All original vertex labels lie in an interval of length $N$, all original weights in one of length at most $N-1$, and each list is injective. Reduction therefore gives cordiality at every $k\ge N$.

For the path assertion, root at one end of $P$. At each path vertex order its children by putting its original leaf children first (except the successor on $P$), then its successor, then all remaining children. Up through its last vertex, the path vertex at level $i$ is preceded only by the selected leaves at its predecessor. This holds by induction since those earlier vertices produce no children. At every intermediate level $i<h$, the $t_i-1-\ell_i$ allowance is at most the number of uncounted vertices of that level if it contains a path vertex. This also holds at the level containing the final path vertex, since all vertices up to and including it are childless. At intermediate levels beyond the path all vertices are uncounted. The final level has no rank-gap cost. Summing $g_i\le t_i-1-\ell_i$ gives $N\le n+d$. If the final path vertex is childless at an intermediate level, the initial leaf count may include it, which only improves the bound.

## Verification

The checker constructs both hosts for all 3,046 rooted tree shapes of orders 2 through 11. It reconstructs the induced original graph, checks connectedness, and verifies every vertex rank and integer edge sum. Compression reduced the host order in 1,963 of the tested orderings. A separately chosen leaf-to-leaf path on each input checks the $n+d$ bound and the actual residue labels at the calculated cutoff. [Construction](level_hosts.py) · [Independent verifier](check_level_hosts.py)

~~~sh
python3 -B -m research.census.check_level_hosts
~~~
