# Reconnecting through a period with two leaves away from the ports

**Theorem.** Fix $D$ and $0<\epsilon<1$. For all sufficiently large $k$, remove $t-1$ edges from any prescribed $k$-cordially labeled tree, with $2\le t\le k^{1-\epsilon}$. Join each resulting component to a distinct port of a tree $U$ on $k$ new vertices of maximum degree at most $D$. If at least two leaves of $U$ are outside the ports, the resulting tree admits a cordial labeling extending the prescribed labels. In one of the two histograms all counts increase by one. In the other, at most one old high bin and one old low bin exchange their roles.

In particular, a smallest counterexample at sufficiently large $k$ cannot contain such a piece with at least two of its original leaves inside. For this consequence alone there is a shorter uniform proof. Replace the piece by a star joining its $t$ old endpoint vertices, with center at any of them. A cordial labeling exists by minimality. Write $a$ for the center label. The difference between the sum of star weights and the sum of the $t$ endpoint labels is $(t-2)a$. The divisor in the uniform criterion divides $t-2$, so restoring the piece increases all counts uniformly. The theorem also permits an independently prescribed old tree and labeling. [Uniform criterion](multiport.md)

## Consecutive bin counts

Use $G=\mathbb Z_k$, $S=\sum G$, $c_v=d_U(v)-1+\mathbf1_{v\text{ a port}}$, and
$$
 M=\sum_j W_j-\sum_i a_i,\qquad h=\gcd(k,c_v:v\in U).
$$
Here the $W_j$ are removed weights and the $a_i$ are the actual old endpoint labels of the entering edges. If $h\mid M$, the uniform theorem applies. Assume henceforth $h\nmid M$. For an old histogram call the bins above its floor count high, with the high set empty for a uniform histogram. We can make at least one of the following transfers.

| Palette | Duplicate an old low bin $B$, omit an old high bin $F$ | Required congruence |
|---|---|---|
| Edge | Net increments $G+[B]-[F]$, vertex increments $G$ | $h\mid M+B-F$ |
| Vertex | Vertex increments $G+[B]-[F]$, net edge increments $G$ | $h\mid M+F-B$ |

Indeed, draw arcs on $G$ from each residue to every residue differing from it by $M$ modulo $h$. The strongly connected classes are the residue classes modulo $h_0=\gcd(h,M)$, each of size $k/h_0$. To verify this, the allowed steps generate the subgroup of multiples of $h_0$, and each step in a finite group has an inverse expressible as a sum of forward steps. There are no arcs between classes. If the edge transfer is impossible there is no arc from a low to a high edge bin. If the vertex transfer is impossible there is no arc from a high to a low vertex bin. In either case the respective high set is a union of whole classes. The sizes of the two high sets are $n-1$ and $n$ modulo $k$, where $n$ is the old order. They cannot both be divisible by $k/h_0>1$.

## Two tree targets

We modify the [uniform construction](multiport.md#a-bounded-degree-unicyclic-replacement). Reserve two nonport leaves. Protect all ports and one representative of each positive $c_v$. Choose an original internal degree $d$ occurring linearly often and put $g=\gcd(k,d-1)$. An unaffected degree-$d$ vertex exists, so $\gcd(g,c_v:v\in U)=h$.

In the vertex transfer we also remove a third nonport leaf $z$, ultimately labeled $B$, with parent $p$. Such leaves are plentiful here. Since $h>1$, every degree-two vertex is a port. At most $t$ vertices have degree two, and the number of leaves is at least the number of vertices of degree at least three plus two. Thus at least $(k-t+2)/2-t$ leaves are nonports. Choose $z$ with $p$ outside the protected neighborhoods and protect both.

Choose $t$ well-separated internal cut edges away from the protected vertices. There are $t+1$ components. In order of decreasing counts of available degree-$d$ sites, connect the anchor of each component after the first to an unused site in an earlier component. Anchors are neighbors of cut endpoints on their component side. Sites are chosen independent and away from the marks. The first $j$ components have $\Omega_D(jk/(t+1))$ sites, so all choices exist. These $t$ wires make an auxiliary **tree** $A$. In the vertex transfer drop $z$ and its incident edge. Wire $i$ is prescribed to have the entering weight $a_i+x_{r_i}$, at port $r_i$, by setting its site label to $a_i+x_{r_i}-x_{\mathrm{anchor}}$.

Prescribe the first $t-1$ cut pairs to sum to $W_j$. In the edge transfer the last pair sums to $B$. The auxiliary target is then the full vertex palette $V=G$ and the edge palette $C=G\setminus\{F\}$. Restoring all cuts and replacing wires by entering edges produces the specified net increment. In the vertex transfer give the endpoints $b,c$ of the last cut independent variables. Use
$$
 V=G\setminus\{F\},\quad C=G\setminus\{P,H\},
             \qquad P=B+x_p,\quad H=x_b+x_c .
$$
We will keep $P,H$ distinct. Reinstating $z$ duplicates $B$ since $B\in V$, and the restored leaf edge and last cut replace the two omitted colors. This gives the specified increments in both histograms.

## Completing the embedding

Work on the initial marks before assigning the two reserved leaves. Set independent variables to zero modulo $g$ except for the protected coefficient representatives. Account for the fixed contributions from second cut endpoints. The wire sites have original coefficient $d-1=0\pmod g$. The representatives can therefore arrange
$$
   \sum_{\mathrm{marks}} c_v x_v =
   \begin{cases} M+B-F &\text{edge transfer},\\ M+F-B &\text{vertex transfer} \end{cases}
   \pmod g .
$$
The fixed contributions are multiples of $h$, and the target is a multiple of $h$ by the chosen transfer. The deleted leaf had coefficient zero.

Lift the residues to distinct labels with distinct induced edge sums. In the edge case include the constant $F$ among the edge comparisons. In the vertex case include $F$ among the vertex comparisons and $P,H$ among the edge comparisons. The new forms for $P$ and $H$ are distinct from every entering and retained edge form. The variable at $p$ belongs to a nonport, and the only edge on the two independent variables at $b,c$ has been cut. The cut endpoints are away from $p$. Every other comparison follows the signed-variable argument in the uniform proof. In particular a retained edge between marked nonsites has two different signed variables, the signs distinguishing opposite cut endpoints. Sites have no marked neighbors in the retained forest. Each variable occurs in boundedly many forms. At its last variable each nonconstant equality excludes at most two of the $k/g$ lifts, and only $O_D(t)$ comparisons involve that variable.

To check the remaining moments, subtract removed cut sums and add the wire sums. For the marks on $A$ this gives
$$
 \sum(d_A(v)-1)x_v =
 \begin{cases}
 \sum c_v x_v-M-B &\text{edge transfer},\\
 \sum c_v x_v-M-x_p-H &\text{vertex transfer}.
 \end{cases}
$$
The extra $-x_p$ accounts for deleting the pendant edge, with the leaf itself absent. In each case the result agrees with $\sum C-\sum V$ modulo $g$. Enlarge the marks to a degree core of $A$, preserving the two reserved leaves. Each new ordinary label can be chosen zero modulo $g$, avoiding occupied labels, any omitted vertex, previous weights and the omitted colors. Two isolated vertices of unaffected degree $d$ now adjust the coefficient sum to $\sum C-\sum V$ modulo $k$. This uses the solvability of a congruence with coefficient $d-1$ and a prescribed sum of two fresh labels. The two reserved leaves of coefficient zero fix the remaining label sum to $\sum V$. In both pair choices only $O_D(t)$ values are excluded by distinctness and palette restrictions. The two leaves are nonadjacent and each has at most one marked neighbor, so weight equality between their two new edges excludes at most two further values.

The labels on the resulting $O_D(t+1)$-vertex degree core sum to $\sum V$ and their degree-weighted sum is $\sum C$. Its induced edges are rainbow in $C$. Lemma 4.9 extends this prescribed embedding over $A$, taking its small exponent below $\epsilon$. The two target sizes are $k,k-1$ or $k-1,k-2$, respectively. Restoring the original edges completes the proof. [Müyesser and Pokrovskiy, Lemma 4.9](https://arxiv.org/html/2509.05280v2#S4)

## Reproducing the checks

~~~sh
python3 -B research/bounded-degree/check_two_leaf_repair.py
~~~

The [constructor](two_leaf_repair.py) computes the transfer, wires and pinned embedding. The [independent checker](check_two_leaf_repair.py) reconstructs 264 edge transfers and 66 vertex transfers through modulus 1,568, verifies the actual signed edge changes, and checks palette sizes, injectivity, connectivity, degree classes and both moments. It checks every high set for all 92 incompatible quotient parameters through modulus twelve. Two complete eight-label examples preserve an old path or star at a four-port insertion where uniform increments fail by parity. The numerical examples test the construction. The sufficiently-large-order implication uses the embedding theorem.
