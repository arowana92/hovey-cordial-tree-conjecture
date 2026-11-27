# Reconnecting several parts of a tree through one period of new vertices

**Theorem.** Fix $D\ge2$ and $0<\epsilon<1$, and take a sufficiently large modulus $k$. Remove $t-1$ edges from a labeled old tree. Reconnect the $t$ resulting components to a new $k$-vertex tree $U$ of maximum degree at most $D$, with one entering edge from each old component to a distinct port of $U$. Suppose $2\le t\le k^{1-\epsilon}$ and at least two leaves of $U$ are outside the ports. The old labels can be kept with every vertex and edge bin gaining exactly one if and only if
$$
  \gcd(k,c_v:v\in U)\ \mid\ M,\qquad
  c_v=d_U(v)-1+\mathbf1_{\{v\text{ a port}\}},\qquad
  M=\sum_{j=1}^{t-1} W_j-\sum_{i=1}^t a_i, \tag{1}
$$
where $W_j$ are the actual removed weights and $a_i$ the old endpoint labels of the entering edges. The old labeling can be arbitrary. Any cordial old core therefore gives a cordial result whenever (1) holds.

In particular **three ports always work**, independently of all old labels and removed weights. Indeed $\sum_v c_v=k+t-2$, so the divisor in (1) divides $t-2$. The same conclusion holds for $\gcd(k,t-2)=1$, or whenever every prime factor of $k$ exceeds $D$. In the two-port situation of replacing the old edge between those very sites, $M=0$, so the ports can even be adjacent.

Consequently a smallest counterexample cannot have a connected part $U$ of order $k$, maximum degree $D$, with at least two original leaves and exactly three edges to its complement at distinct vertices of $U$. Delete $U$, connect the three outside components in a path, and label the resulting smaller tree by minimality. The theorem restores $U$. The outside vertices, degrees and sizes are unrestricted. This is a restriction on the shape of a counterexample for sufficiently large moduli.

The [sparse-port classification](sparse-ports.md) also settles uniform increments when fewer than two leaves lie outside the ports.

## The necessary moment

Uniform vertex increments make the free labels $x_v$ a permutation with sum $S=\sum\mathbb Z_k$. The net edge sum is
$$
       \sum_v d_U(v)x_v+\sum_{i=1}^t (a_i+x_{r_i})-\sum_j W_j ,
$$
where $r_i$ denotes a port. Equating this to $S$ gives $\sum c_v x_v=M$ and proves necessity. We now construct the labeling using Lemma 4.9 of Müyesser and Pokrovskiy. [Primary embedding theorem](https://arxiv.org/html/2509.05280v2#S4)

## A bounded-degree unicyclic replacement

Protect all ports, two leaves outside the ports, and one representative of each distinct positive coefficient $c_v$. These representatives will adjust (1) in a small quotient. There are at most $D$ of them.

Choose $t-1$ internal edges with both endpoints of degree at least two, at distance at least four from the protected vertices and from one another. This is possible because the nonleaves induce a tree with $\Omega_D(k)$ vertices, and each protected vertex or choice forbids only $O_D(1)$ nearby edges. Remove these pairs $(b_j,b'_j)$ from $U$. Later we prescribe labels $X_j,W_j-X_j$ there, so their sums reproduce all old deleted weights. The remaining forest has $t$ components.

In each component choose an anchor, a neighbor of one of its cut endpoints on the component side. Both endpoints of every cut had degree at least two, and the separation guarantees an unprotected anchor distinct from all endpoints. Some degree $d\ge2$ occurs $\Omega_D(k)$ times in $U$. Away from the closed neighborhoods in the remaining forest of all marks, cut endpoints and anchors, choose an independent set of sites of original degree $d$. There are $\Omega_D(k)$ such sites. Order the components $C_0,\ldots,C_{t-1}$ by nonincreasing site counts. In $C_0$, connect its anchor $h_0$ to a site $s_0$. For each $j>0$, connect the anchor $h_j$ of $C_j$ to a fresh site $s_j$ in an earlier component. The first $j$ components together have $\Omega_D(jk/t)>j$ sites for sufficiently large $k$, so an unused site exists. The first edge closes a simple cycle; subsequent ones attach new components. The auxiliary graph $R$ is simple, connected and unicyclic with bounded degree. The two protected leaves still have degree one. Linearly many unaffected vertices still have degree $d$.

Associate the $t$ wires $h_js_j$ in any order with the $t$ actual entering edges, and prescribe
$$
                 x_{s_j}=x_{r_i}+a_i-x_{h_j}.
$$
Thus replacing the wires by the entering edges preserves their weights. The cut-pair edges, when restored, replace the old deleted weights. It suffices to find a harmonious labeling of $R$ that keeps both sets of prescriptions.

## Setting the residues of the marks

Put $g=\gcd(k,d-1)$ and work first modulo $g$. Give the first endpoint of each cut pair residue zero and the second residue $W_j$. Start all other independent marks at zero. Site residues are determined by the wire formula, but each site has original coefficient $d-1$, zero modulo $g$. The residues at the protected representatives can now be varied independently. They may be ports, in which case the additional changes affect only sites of coefficient zero modulo $g$.

We can arrange $\sum c_v x_v=M\pmod g$ over all marks, with unmarked vertices regarded as zero. Indeed every coefficient occurs among the representatives except zero, and $\gcd(g,c_v:v\in U)=\gcd(k,c_v:v\in U)$ because an unaffected degree-$d$ nonport has coefficient $d-1$. The contribution already fixed at the cut endpoints is a multiple of this gcd. Solvability follows from (1).

Choose actual lifts of the independent variables in their assigned residue classes. The original endpoints of cut pairs have the two signed variable labels $X_j,W_j-X_j$. Ports, anchors and other representatives have independent variables, identifying an overlap between a port and a representative. The additional site expressions have unique negative anchor variables and a positive port variable. These vertex expressions have different coefficient vectors.

For the induced edge sums on the marks, each wire gives one distinct port variable plus an old constant. Each retained marked edge has two distinct underlying variables: the only two original vertices sharing a variable are a cut pair and their edge has been removed. The sign of the variable identifies which endpoint of a cut pair occurs. Thus retained edge expressions are distinct from one another and from the wire expressions. Sites have no other marked neighbors. The protected leaves can be kept aside for the final sum adjustment.

Each variable occurs in $O_D(1)$ expressions in either list since the original degrees are bounded, ports are distinct, cut pairs are disjoint, and each anchor occurs on one wire. Consequently only $O_D(t)$ pairwise inequalities involving a given variable can be decided at its greedy assignment step. Decide each difference at its last variable with a nonzero coefficient. That coefficient has absolute value at most two. With a prescribed residue modulo $g$, at most two of the $k/g$ lifts violate each inequality, by solving a linear congruence in the subgroup of size $k/g$. For sufficiently large $k$, some lift remains. The actual marks therefore give a rainbow injection on the induced auxiliary edges while preserving their prescribed residues and all wire and cut-pair sums.

## Completing the two moments

The degree sum on the marks changes from $U$ to $R$ by subtracting the sums on the cut pairs and adding the sums on the wires. Hence
$$
     \sum_{v\text{ marked}}(d_R(v)-1)x_v
       =\sum_{v\text{ marked}} c_v x_v-M
       =0\pmod g .
$$
This identity uses only changed-edge endpoints and ports, all of which are marked.

Cut the auxiliary closing wire and enlarge the marks to a degree core of that spanning tree. Give new ordinary marks labels zero modulo $g$, chosen to preserve injectivity and distinct induced sums in the closed graph. Add two isolated unaffected vertices of degree $d$. If $A$ is the current sum with coefficients $d_R-1$, the congruence $(d-1)(x_z+x_{z'})=-A$ is solvable modulo $k$ because $g\mid A$. Vary one label to avoid the $O_D(t)$ occupied labels and equality with the other. Finally the two protected leaves supply the pair sum needed for all marked labels to sum to $S$. Their coefficients $d_R-1$ vanish. Each contributes at most one induced edge, so only $O_D(t)$ choices cause a collision. These are precisely the two moments in the [unicyclic extension proof](unicyclic.md#a-closed-graph-with-at-least-two-leaves).

The resulting core has $O_D(t+1)$ vertices. Choose the embedding parameter sufficiently small for the fixed auxiliary maximum degree and smaller than $\epsilon$. Lemma 4.9 extends the prescribed rainbow embedding of the cut tree with the auxiliary closing weight omitted. Restoring that wire gives the harmonious bijection of $R$. Undoing the prescribed replacements proves sufficiency in (1).

## A four-port obstruction to uniform increments

For even $k$ large enough, take a tree on $k-4$ vertices whose degrees are all one and three and subdivide four distinct edges once. Use the four degree-two vertices as ports. All positive $c_v$ equal two. Use an old path on four vertices with labels $0,1,2,3$ in order, delete all three edges, and attach its four vertices to the ports. This old labeling is cordial, and $M=1+3+5-(0+1+2+3)=3$. The parity obstruction in (1) certifies that uniform increments are impossible. The calculation concerns this prescribed operation and does not disprove ordinary cordiality.

## Verification

~~~sh
python3 -B research/bounded-degree/check_multiport.py
~~~

The [constructor](multiport.py) computes the small quotient, the cut pairs, the wire labels and the final prescribed core. The [independent checks](check_multiport.py) recover the original edge set, compare actual cut and entering sums, test connectivity of the cut auxiliary graph, recount degree classes and verify both embedding moments. They cover 168 successful cores with two through twelve ports, including 48 with a nontrivial quotient at the lifting step, and twelve cases blocked by the necessary moment. The infinite completion is an application of the cited embedding lemma.
