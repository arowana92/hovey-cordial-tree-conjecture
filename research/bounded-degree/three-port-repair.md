# Every three-port tree insertion preserves cordiality at large moduli

**Theorem.** Fix a degree bound $D$ and $0<\epsilon<1$. For all sufficiently large $k$, remove $t-1$ edges of a prescribed cordial tree and reconnect the $t$ resulting components through a tree on $k$ new vertices of maximum degree at most $D$. Use one entering edge per old component, at distinct free ports. If
$$
                    3\le t\le k^{1-\epsilon},
                    \qquad \gcd(k,t-2)=1 ,
$$
the old labeling extends. The free tree can have **any number of leaves**. In particular **every three-port insertion** works, at every old order and for every choice of old endpoints and removed edges. Only the inserted tree's degree is bounded.

In a smallest counterexample at sufficiently large $k$, there is therefore no connected $k$-vertex part of bounded degree with exactly three edges to the complement at distinct free vertices. For example, at a degree-three joint with three corridors leading to retained vertices, their available degree-two vertices cannot contain $k-1$ choices in terminally truncated initial segments with distinct ports. A smaller tree is obtained by joining the three outside components in a path. The theorem restores the original.

## The only shape that can need a repair

Use $S=\sum\mathbb Z_k$, old endpoint labels $a_i$, removed weights $W_i$, $M=\sum W_i-\sum a_i$, and $T=M-S$. If the free tree has at least two nonport leaves, the [multiport gcd](multiport.md) divides both $k$ and $t-2$, so uniform increments always work. With one nonport leaf and $t\ge3$, they also always work. With none and at least two positive $\delta_v=d_U(v)-2+\mathbf1_{\{v\text{ a port}\}}$, their gcd with $k$ again divides $t-2$. [Sparse-port classification](sparse-ports.md)

The remaining shape has no nonport leaves and a unique positive position $J$ with $\delta_J=d=t-2$. It consists of internally disjoint paths from $J$ to the tip ports; $J$ can also be a port. Its degree bounds $t\le D+1$. A longest arm has length $\Omega_D(k)$. Uniform increments can force an incompatible joint label. The constructions below adjust a pair of edge or vertex counts. In all cases the old edges really are deleted and the entering weights are computed at their prescribed endpoints.

## When the old edge frequencies are nonuniform

Select a low old weight $B$ and a high old weight $F$. Give the free vertices every residue once and aim for net edge increments $G+e_B-e_F$, writing $G$ for one copy of each residue. The new joint label must be
$$
                       h=d^{-1}(T+B-F).
$$
We may choose $B,F$ so $h$ differs from all old attachment labels and, if $J$ is a port, $h+a_J\ne F$. Indeed, fix one element of the smaller of the high and low sets and vary the other over at least $k/2$ residues. Each prohibited attachment value for $h$ costs at most one choice. If $F$ varies, the last equality has at most $d+1$ solutions; if $B$ varies it has at most one. The number of exclusions is bounded in terms of $D$.

Pin $J$ at $h$ and assign distinct fresh labels to all other ports. Make the entering weights and the internal sums between pinned vertices distinct and different from $F$. The only such internal edge at a tip port is a one-edge arm to $J$. Its sum differs from that port's entering weight since $h\ne a_i$. The entering weight at $J$, if present, already avoids $F$. Greedy choice therefore excludes only $O_D(1)$ labels for each port.

On a longest arm select $t$ disjoint short segments far from the marked vertices. In each, delete a middle edge $bc$ and reconnect across that cut by an edge between two fresh vertices $P,Q$, one on either side. Choose $P$ at distance two from $b$ and $Q$ at distance two from $c$, leaving gaps between the segments. These changes give a tree on the $k$ free vertices. Prescribe the $t$ sums on the deleted $bc$ edges to be the $t-1$ old $W_i$ and $B$, and those on the $t$ wires $PQ$ to equal all the entering weights. Each prescribed sum on a fresh pair admits two fresh distinct labels since only boundedly many values are used. Among marked vertices these windows have only the new wire edges in the auxiliary tree.

Use vertex target $G$ and color target $G\setminus\{F\}$ on the auxiliary tree. For the marked vertices the original free degree correction $\sum(d_U-2)x$ equals $dh-\sum_i x_{r_i}$. Subtract the cut-pair sums and add the wire sums. The auxiliary correction becomes
$$
                        dh-M-B=-S-F .
$$
All vertices of auxiliary degree different from two are marked. Add six mutually isolated degree-two vertices outside the marked neighborhoods and make the core labels sum to $S$, using the last two for the required pair sum. Then the weighted core sum is $2S-S-F=S-F$, precisely the sum of the target colors. The core contains every non-degree-two vertex and has at least six degree-two vertices both inside and outside. Lemma 4.9 completes the pinned rainbow embedding. Undoing the wire replacements gives the required edge transfer, and both histograms are balanced. [Müyesser and Pokrovskiy, Lemma 4.9](https://arxiv.org/html/2509.05280v2#S4)

## When all old edge frequencies are equal

Normalize the sole surplus vertex label to zero. Aim to increase every edge bin by one and give the free vertices $G-e_0+e_R$, $R\ne0$. Recompute the old labels and weights in these coordinates. The required joint label is
$$
                              h=d^{-1}(T-2R).
$$
Choose $R$ so $h\ne0,R$ and $h$ avoids all old attachment labels. Each attachment equality excludes at most two solutions for $R$, and $h=R$ excludes at most $d+2$. Assign all port labels as before, using distinct nonzero residues and avoiding $R$; the joint and any port at it share their single prescribed label.

Mark an ordinary degree-two vertex well inside the longest arm with label $R$. Far from it and from the ports, select another internal degree-two vertex $z$ to remove temporarily and ultimately also label $R$. Give its neighbors $b,c$ distinct fresh nonzero labels so the two reserved sums $F_1=R+x_b$ and $F_2=R+x_c$ are distinct and avoid every earlier entering and marked edge weight. Reconnect the two sides of the omitted $z$ using a wire between two fresh positions, at distance two beyond $b,c$ respectively. Separately use $t-1$ ordinary cut-pair segments as above, all disjoint. There is space since $t$ is bounded and the longest arm grows with $k$. The $t-1$ ordinary cuts supply the $W_i$, and the $t$ wires, including the one across the omitted vertex, supply the entering weights. Assign all pairs fresh nonzero labels avoiding the other marks.

The auxiliary tree has $k-1$ vertices. Use $V=G\setminus\{0\}$ and $C=G\setminus\{F_1,F_2\}$. Removing $z$ decreases the degree correction by $x_b+x_c=F_1+F_2-2R$; $z$ itself had degree two. The ordinary cuts and wires give the same cancellation as above. Thus the auxiliary degree correction is
$$
                       dh-M-F_1-F_2+2R=-S-F_1-F_2 .
$$
The six isolated degree-two positions can still make the core sum $S=\sum V$ while avoiding zero. Its weighted sum is now $S-F_1-F_2=\sum C$, so Lemma 4.9 again completes the embedding. Restore $z$ at $R$ to supply the two omitted weights. The wire identities restore the actual entering and removed sums, yielding uniform net edge increments. On vertices the surplus moves from zero to $R$. This proves the theorem.

## Verification

~~~sh
python3 -B research/bounded-degree/check_three_port_repair.py
~~~

The [constructor](three_port_repair.py) constructs both types of auxiliary tree and prescribes the labels. The [checker](check_three_port_repair.py) independently inspects 560 instances at moduli through 1,024. It checks connectivity, target cardinalities, prescribed label and weight multiplicities, every degree class, both global moments, and the signed multiset of the actual changed edges.

For a complete finite example, take the [obstructed all-zero tripod boundary](sparse-ports.md#the-single-joint) at $k=11$ and arm lengths $1,1,8$. The free labels at the joint, the two short tips, and then along the long arm are
$$
                         9;\quad 1,2;\quad 5,1,10,6,3,4,7,8 .
$$
The checker inserts these labels into the actual 23-vertex old star. Every final edge bin has size three and the sole vertex bin of size four is 1. Uniform simultaneous increments were impossible on this same input.
