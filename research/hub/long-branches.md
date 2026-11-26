# A hub with few terminal vertices elsewhere

**Theorem.** For every sufficiently large $k$, take any tree $H$ rooted at $o$ with at most $(\log_2 k)/100$ nonroot terminals. Adjoin any number of leaves at $o$. The resulting tree is $k$-cordial, with no restriction on its order or on the lengths of paths in $H$. In particular, at each fixed bound on the number of leaves away from the neighbors of a specified hub, only finitely many tree–modulus pairs can fail. For the finitely many remaining moduli this last assertion uses the [order bound](../large-order/diagonal.md).

The main asymptotic step permits many more terminals. Fix $0<\epsilon,\delta<1$. For sufficiently large $k$, if $\delta k\le h=|H|\le k$ and $H$ has at most $k^{1-\epsilon}$ nonroot terminals, every number of further hub leaves works. The proof couples random vertex and color sets across two collections of paths. It uses Müyesser and Pokrovskiy's perfect matching and prescribed path-factor results. [Theorem 3.1 and Lemma 3.2 in *On the Graham–Sloane harmonious labelling conjecture*](https://arxiv.org/html/2509.05280v2#S3.SS1) · [*A random Hall–Paige conjecture*, including the published path-factor Lemma 6.22](https://doi.org/10.1007/s00222-025-01328-x)

## A short core with arbitrarily elongated edges

For $h\le k$, it suffices to give $H$ distinct residues with $x_o=0$ and its edge weights distinct members of its vertex label set. The [periodic list](README.md) then adds any number of hub leaves. Conversely an ordinary cordial labeling after adding $k-h$ such leaves gives this property by translating its root to zero and stripping the leaves. The order-$k$ tree uses every vertex residue once.

The [twelve-site path](../large-order/flexible-path.md#subdividing-edges-with-controlled-multiplicities) preserves this certificate on elongating an edge with nonzero endpoints $p,q$ and nonzero sum $p+q$. When $k>12h+132$, where $h$ bounds the **final** order of the core, one can keep all new labels distinct from each other and all old labels. A collision with an old vertex excludes $k$ of the $k^2$ choices of $u,v$. For two different free-coefficient pairs a nonzero coefficient of their difference has magnitude at most two, so a collision excludes at most $2k$ choices. At identical coefficient pairs the two constants differ by one of $\pm p,\pm q,\pm(p+q)$, as verified by the list. The union bound proves the assertion. In particular the new edge labeled $u,v$ is available for the next elongation: $u,v,u+v$ all occur as fresh labels.

Let $a$ be the number of nonroot terminals. Mark $o$ and every vertex of degree different from two; there are at most $2a$ segments. Retain a short segment, and on a segment of length greater than 14 use its congruent length in $[3,14]$ modulo twelve. The reduced tree has order at most $28a+1$. The [integer one-hub theorem](universal-hub.md) labels it modulo every $k$ exceeding $(2b+4)b2^{b-1}$ for its order $b$. This holds for $a\le (\log_2 k)/100$ and sufficiently large $k$. Every shortened segment contains a good edge: at most one of its edges touches the root and at most one edge of the entire tree has weight zero. Expand the selected good edges successively. This proves the desired certificate when $h<k/20$, including a star or a single vertex directly where necessary.

## Cutting long segments in the positive-density case

Let $a\le k^{1-\epsilon}$ and $\delta k\le h\le k$. Work on the order-$k$ tree with $m=k-h$ ordinary hub leaves. If $m\le k^{1-\epsilon/4}$ its total degree excess above three is at most $a+m$. This follows from the leaf degree sum, counting the root if it is an undirected leaf. The [degree-excess theorem](../bounded-degree/excess.md) applies, for example with exponent $\epsilon/8$. Hence assume $m>k^{1-\epsilon/4}$.

Take $t=\lceil2(\log k)^7\rceil$, in the permitted path-factor range for large $k$. In the interior of each marked segment put two disjoint consecutive chains of the same length in vertices, a multiple of $t+1$, leaving fewer than $2(t+1)$ interior vertices outside them. Use the maximum such length, omitting empty pairs. Assign the first chain of every pair to collection 1 and the second to collection 2. Each chain consists of $\ell$ disjoint paths of $t$ edges, with one connector edge between successive paths. Let $c$ be the number of chains per collection and $r$ the total number of paths per collection. There are $O(at+a+1)$ vertices outside the chains. Write $V_0$ for their eventual labels. Each collection contains $(t+1)r$ vertices, so $g=(t+1)r/k$ lies between $\delta/3$ and $1/2$ for sufficiently large $k$.

Prescribe distinct labels for all vertices outside the chains and the first and last vertices of every chain, keeping $o$ at zero. Prescribe only the edges outside chain interiors and connectors, that is, all edges except the edges lying entirely along a chain. They form a forest on the specified vertices. Use parent-before-child greedy assignment in each component, starting the root's component at $o$, to make these edge sums distinct. Each new vertex has at most one earlier neighbor in this forest, so $O(at+a+1)=o(k)$ forbidden labels suffice. Denote the resulting weight set by $W_0$. If $F_i$ denotes the sum of the fixed first and last labels of collection $i$, fix a residue $s$ outside $W_0$ to be the unused weight.

We shall arrange a vertex set $A$ of size $h$ containing these fixed labels, $W_0$ and $s$. Its required sum in $\mathbb Z/k$ is
$$
\sum A=2\sum V_0+F_1+F_2-\sum W_0-s. \tag{1}
$$
The visible sets in the next construction give all the remaining sums and adjacencies, not only the counts.

## Joint choice of the random sets

At each residue independently select its vertex collection and its color collection using the following joint probabilities. Index 0 means that it belongs to neither collection at this initial stage.
$$
\begin{pmatrix}
1-2g&0&0\\
0&g^2&g-g^2\\
0&g-g^2&g^2
\end{pmatrix}.
$$
The union of the two vertex collections equals the union of the two color collections; call it $A_0$. For each $i=1,2$, its vertex collection membership and its **own** color collection membership are independent, each of probability $g$. Conditional on the collection indices, assign the finer roles independently. Within vertex collection $i$ the three probabilities for start, middle and end are $1/(t+1),(t-1)/(t+1),1/(t+1)$. Within color collection $i$ the two probabilities for path and connector are $t/(t+1),1/(t+1)$. Thus each individual factor sees exactly the independent color set and disjoint random vertex sets of the cited theorems. The two factors need no mutual independence.

Write $q=r/k$ and $p=(t-1)q$. The path theorem sees start and end density $q$, middle density $p$ bounded below, and color density $tq$. The connector matching theorem sees densities $q,q,q$, where $q$ is of order $(\log k)^{-7}$. The number of requested theorems is four, so with high probability all their robust conclusions hold together.

We specify why the exact edits below are within their tolerances. With high probability every role size differs from its mean by at most $k^{1/2+1/20}$. All required edits, including the fixed forest, then cost $o(k^{1-\epsilon/3})$ elements in total. Here $at=O(k^{1-\epsilon}\log^8 k)$. We also use the following simultaneous reservoir properties:

- For each nonzero residue $d$ there are $\Omega(m)$ pairs $x\in A_0$, $x+d\notin A_0$. Indeed $2g\ge2\delta/3$ and $(1-2g)k\ge m$.
- Between any two different fine color roles and for every $d\ne0$, there are $\Omega(k/(\log k)^{14})$ pairs $x,x+d$ with the specified roles.

For either claim choose a matching of at least $k/3$ disjoint ordered pairs $x,x+d$ from the shift cycles. Each pair then has the indicated independent membership probability, and different pairs use independent coordinates. Chernoff's inequality and a union bound over the differences and the finitely many role pairs prove both claims. These supplies dominate the number of edits, including when $m$ is as small as allowed here.

First edit $A_0$ to size $h$ with all prescribed inclusions. To obtain (1) use at most one additional exchange $x\mapsto x+d$ between the set and its complement, avoiding all prescribed elements, for the necessary nonzero difference $d$. Next adjust the vertex roles to partition $A\setminus V_0$ into the prescribed sizes and put each fixed first and last label into its required start or end role. Adjust the four color roles to partition $A\setminus(W_0\cup\{s\})$, with $tr$ path colors and $r-c$ connector colors per collection. Counts are consistent because $|W_0|=|V_0|+2c-1$. These size and membership adjustments need only move misassigned prescribed elements, elements added or removed from the union, and the remaining size errors between roles.

Let $S_i,I_i,E_i$ be the final start, interior and end sets. The path and connector color sums we need in collection $i$ are respectively
$$
\sum S_i+2\sum I_i+\sum E_i,\qquad \sum S_i+\sum E_i-F_i.
$$
Their grand total is $2(\sum A-\sum V_0)-F_1-F_2=\sum A-\sum W_0-s$ by (1). Adjust the sums of three color roles successively by a single exchange each with the fourth, using the second reservoir property. Sizes stay fixed, and the last sum then follows automatically.

All symmetric differences in a path-factor application are at most $k^{1-\gamma}$ for a sufficiently small fixed $\gamma>0$ in terms of $\epsilon$. For a connector matching, also remove the $c$ first starts and $c$ last ends of its chains. The total symmetric-difference allowance $q^{10^{18}}k/(\log k)^{10^{18}}$ of Theorem 3.1 dominates the edits for large $k$. Its density lower bound also holds. Our cyclic group is not an elementary abelian 2-group at these large orders.

## Reassembling the tree

In each collection take a perfect rainbow matching between all ends except the fixed last ones and all starts except the fixed first ones, using precisely its connector colors. The sizes and sum identity above are exactly the matching hypotheses. Partition these matched edges into ordered lists of the desired lengths $\ell-1$, one per chain. This specifies a bijection from starts to ends for the path factor: the fixed first start leads to the first connector's end, its matched start leads to the next connector's end, and so on to the fixed last end. For a one-path chain the fixed start leads directly to the fixed end.

The prescribed-bijection theorem now supplies the disjoint length-$t$ paths using exactly the required middle vertices and path colors. The chains, connectors and fixed forest form the original $H$. Its vertex set is $A$ and its edge weights are exactly $A\setminus\{s\}$. Assign the $k-h$ remaining residues to leaves at the zero hub. This proves the positive-density assertion and the one-site criterion then gives every population.

## From order k to all core orders

For $a\le(\log_2 k)/100$, the short-core and positive-density results (take $\delta=1/20$) cover all $h\le k$. Use strong induction on $h$ above this range, uniformly over the additional hub population $m$. If $n=h+m$ is $1\bmod k$, remove one nonroot terminal of $H$, apply induction, and restore it at the unique deficient edge weight. Otherwise remove a suffix of $(n-1)\bmod k$ vertices in a parent-before-child order of $H$. Its length is between one and $k-1$, and the root of $H$ stays. The remaining tree has order $1\bmod k$. Pruning cannot increase the number of nonroot terminals, since each new one has a separate original terminal descendant.

Each suffix component contains an original terminal. Its free degrees have total excess above three at most $a$, since they are bounded by their degrees in $H$. Thus the number of components plus their degree excess is $O(a+1)$. Pad the suffix to $k-1$ free vertices with a terminal path. The [prescribed forest lemma](../bounded-degree/excess.md#forest-lemma) gives distinct free labels avoiding the core's surplus vertex label and distinct weights with the actual boundary labels. Restrict to the suffix. Both histograms are balanced after restoration. This proves the theorem.

The same induction explains where a failure with at most $k^{1-\epsilon}$ terminals in $H$ would have to occur. Take a failing family with minimum $h$ at that modulus (any hub population). It has $h\le k$ by the forest lemma, and the order-$k$ member must fail. Along an unbounded sequence of such moduli the positive-density assertion forces $h=o(k)$. The logarithmic-terminal theorem rules out one further part of that remaining range.

## Independent checks

The verifier checks the role probabilities as exact rationals and the equal-coefficient collision exclusions at every modulus from 2 to 40. It elongates actual labeled trees, checks their vertex and edge sets, cuts them into chains, reconstructs the prescribed bijections and independently verifies all four color sums and (1). Four prime and composite moduli exercise sixty separate color-sum repairs. These checks cover the finite identities. The large-group matching and path-factor hypotheses and the asymptotic edits are justified above. [Verifier](check_path_pools.py)

~~~sh
python3 -B -m research.hub.check_path_pools
~~~
