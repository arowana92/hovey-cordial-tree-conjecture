# Harmonious unicyclic graphs of bounded degree and a tree reduction

**Theorem.** For each fixed $\Delta$, there exists $k_0(\Delta)$ such that a simple connected unicyclic graph $R$ on $k\ge k_0(\Delta)$ vertices, of maximum degree at most $\Delta$, has a bijection onto $\mathbb Z_k$ making its $k$ endpoint sums bijective exactly in the following cases.

| Leaves of $R$ | Orders admitting the two bijections |
|---|---|
| None | Odd $k$ |
| One | Even $k$ |
| Two or more | All $k$ |

The two bijections are a harmonious labeling. The result is a deduction from Müyesser and Pokrovskiy's rainbow embedding theorem for **trees**. We cut a cycle edge and choose the small prescribed embedding needed to put that edge back. [Definition 2.1 and Theorem 2.3](https://arxiv.org/html/2509.05280v2#S2) · [Lemma 4.9](https://arxiv.org/html/2509.05280v2#S4)

**Consequence for Hovey's conjecture.** Take any edge $ab$ of any labeled tree, open a cycle edge $ij$ of $R$, and insert $R-ij$ by joining $a$ to $i$ and $j$ to $b$. In all the harmonious cases, every vertex and edge frequency can increase by exactly one, with all old labels preserved. Translate the bijection so $j$ carries the label of $a$. The two entering edges then reproduce the deleted cycle weight and old edge weight. Only the piece has a maximum-degree restriction. For a one-leaf piece at odd $k$, a different construction below preserves every cordial old labeling.

In particular, a smallest counterexample at sufficiently large $k$ cannot contain a $k$-vertex middle component between two retained edges whose boundary vertices are at distance at least two and whose closure has bounded maximum degree. If it contains leaves, this follows here for every old order. If it contains none, it is a bare path. The [period-subdivision theorem](../census/period-subdivision.md) handles the latter at every order of a smallest counterexample, since order one modulo $k$ is already excluded. The result gives no explicit upper bound on $k_0(\Delta)$.

## A closed graph with at least two leaves

Fix an arbitrary cycle edge $ij$ and put $T=R-ij$, a spanning tree. Set $G=\mathbb Z_k$ and $S=\sum G$. Seek a small set $Q$ including $i,j$ with injective labels $x$ whose edges in $R[Q]$ have distinct sums, and such that
$$
    \sum_{v\in Q}x_v=S,\qquad
    \sum_{v\in Q}(d_R(v)-1)x_v=0. \tag{1}
$$
Write $D=x_i+x_j$. On $T[Q]$ the color $D$ is absent. Also
$$
          \sum_{v\in Q} d_T(v)x_v
       =  \sum_{v\in Q} d_R(v)x_v-D
       =  S-D
       =  \sum(G\setminus\{D\}).
$$
Thus (1) gives exactly the two moment conditions of Lemma 4.9 with vertex target $G$ and color target $G\setminus\{D\}$. The lemma extends the prescribed core to a rainbow bijection on $T$; restoring $ij$ supplies the missing color $D$. Cyclic groups of sufficiently large order are outside the lemma's elementary-abelian 2-group exception.

Start $Q$ with $i,j$ and two original leaves $p,q$. For each degree in $T$, take all vertices of that degree if necessary, or ensure that at least six occur both in $Q$ and outside it. Starting with four marked vertices, this requires only $O(\Delta)$ more. For example, add vertices until six of that class are inside or the class is exhausted, then include the remainder if it has fewer than six. This makes $T[Q]$ a core in the paper's sense.

Since $\sum_v(d_R(v)-1)=k$, some degree $d\ge2$ occurs at least $k/(\Delta-1)^2$ times in $R$. Choose two such vertices $z,z'$ at distance at least two from $Q$ and from each other. The bounded degree and fixed size of $Q$ leave room, with at least six others of their class still outside. Add them to $Q$. They are isolated in $R[Q]$, and their degrees in $T$ equal $d$. The resulting core has size $O(\Delta)$, within the size bound of Lemma 4.9.

Assign all vertices of $Q\setminus\{p,q,z,z'\}$ distinct labels represented by integer multiples of $d-1$. Greedy choice suffices. At one vertex the used labels and the previously used edge sums exclude only $O_\Delta(1)$ choices. Two new incident edges always have distinct sums because their other endpoints have different labels. There are at least $\lfloor k/(d-1)\rfloor$ available representatives before exclusions. Include the closing edge in this test.

Let $A$ be the integer sum of $(d_R(v)-1)x_v$ on the assigned vertices, using the chosen representatives. The integer $d-1$ divides $A$. Set $x_z+x_{z'}=-A/(d-1)$ modulo $k$. Thus the second equation of (1) already holds irrespective of the labels on the two original leaves. Vary $x_z$ to give both isolated vertices fresh distinct labels. Equality between the two excludes at most two choices. Finally set $x_p+x_q=S-\sum_{Q\setminus\{p,q\}}x_v$. Vary $x_p$ again. Each leaf introduces at most one edge in $R[Q]$, the leaves are nonadjacent, and the equality of their two new edge sums excludes at most two values. All other label and edge collisions exclude only $O_\Delta(1)$ more values. This gives (1) and completes the proof for any number of leaves at least two.

## A path with at most four prescribed positions

The following direct consequence of Lemma 4.9 will handle the remaining constructions. Let $P$ be a path of order $k$ or $k-1$ with vertex target $V\subseteq G$ and color target $C\subseteq G$ of sizes $|P|$ and $|P|-1$. Mark both endpoints and at most two more positions. Suppose their labels lie in $V$, are distinct, and every edge between marked positions has a distinct sum in $C$. For sufficiently large $k$, the labels extend over the path provided the endpoint labels $b,r$ satisfy
$$
                    \sum C=2\sum V-b-r. \tag{2}
$$

Add six internal vertices to the marked set, mutually nonadjacent and nonadjacent to all marks. There are still at least six degree-two vertices outside. Assign four of the six fresh labels arbitrarily from $V$ and make the last two supply the sum needed for the entire core's labels to sum to $\sum V$. Vary one label to avoid the finitely many used or excluded residues and equality with its partner. The new vertices add no edges to the core. Both path leaves are present, so the weighted sum of core labels is $2\sum V-b-r=\sum C$. This verifies all hypotheses of the lemma. Necessity of (2) follows by incidence counting along the full path.

## Cycles and the one-leaf case at even order

On a cycle the sum of weights is $2S$. It can equal $S$ only at odd order, where the consecutive labels around the cycle give all weights. For a graph with one leaf, writing $J,Y$ for its degree-three joint and tip gives total $2S+x_J-x_Y$. Hence a harmonious labeling requires $x_Y=x_J+S$, impossible at odd $k$. The closed odd-order obstruction is known for dragons. [Seoud and Youssef (1999), publication record](https://research.asu.edu.eg/handle/123456789/179938)

At even $k$, cut the cycle between $J$ and a neighbor $B$, leaving a Hamilton path with endpoints $B,Y$. Prescribe $x_J=0$, $x_Y=k/2$ and any $x_B=t$ outside $\{0,k/2\}$. The only possible retained edge among these marks is $JY$ and its weight differs from $t$. Use $V=G$, $C=G\setminus\{t\}$. Equation (2) holds since $S=k/2$. The cut edge supplies $t$. This completes the classification.

## Preserving cordiality with one leaf at odd order

Here $S=0$. Fix a cycle of length at least three and an arbitrary positive pendant length, with $k$ total vertices. A cycle edge is designated for insertion at the old edge. All group calculations below are modulo $k$. We give three applications of (2). In each case the marked set consists of the two endpoints and at most two other positions.

**Two old edge levels.** Choose a port $v$ different from the joint $J$ and normalize the corresponding opposite old endpoint to zero. Choose any low old weight $D$ and any high old weight $F$ in these translated coordinates. Cut an auxiliary cycle edge $JB$ with $B\ne v$. This is always possible. On the resulting path put
$$
    x_v=0,\quad x_J=h,\quad x_B=D-h,\quad x_Y=h+F-D .
$$
Take $V=G$ and $C=G\setminus\{F\}$. The endpoints $B,Y$ sum to $F$, giving (2). The joint and tip are distinct because $F\ne D$. Other vertex equalities exclude boundedly many $h$. The only possible marked edge weights are $h,D-h,2h+F-D$, with the third possible when the tail has length one. These affine functions have distinct integer slopes, so pairwise equalities and equality with $F$ each rule out at most three values of $h$. For large $k$ a choice remains. Closing $JB$ repeats $D$. Open the designated edge using $v$ as anchor: all vertex bins gain one and the edge increment is $G+e_D-e_F$, preserving balance.

**Uniform old edge counts with a nonzero endpoint.** Normalize the sole surplus vertex label to zero. Let $v$ be the anchor that must carry a prescribed nonzero label $a$. Remove the tip $Y$, denote its neighbor by $P$, and cut an auxiliary cycle edge $JB$ with $B\ne v$. The resulting path has endpoints $B,P$ and vertex target $V=G\setminus\{0\}$. Write $x_J=h$, $x_B=t$, $x_P=r$ and $x_v=a$, identifying repeated marks: $h=a$ if $v=J$, and $r=h$ if $P=J$. Take
$$
                  D=h+t,\qquad F=r-h,\qquad C=G\setminus\{D,F\}.
$$
Since $D+F=t+r$, (2) holds. One can arrange $D\ne F$, distinct nonzero vertex labels at distinct marks, and distinct retained edge sums avoiding both omissions. To see this, choose the unfixed variables $h,t,r$ independently. Besides $JP$ when $P\ne J$, the only possible marked edges are $vJ,vB$ when $v\ne J$. Their sums are respectively $h+r,a+h,a+t$. Comparisons with $D$ reduce to distinct vertex labels. For $JP$, equality with $F$ would give $2h=0$, impossible for nonzero $h$ at odd $k$. When $P=J$, the forbidden $F$ is zero, and $JP$ is absent. All remaining collisions which are possible in the indicated cases impose proper affine equalities with bounded integer coefficients in the unfixed variables. Each excludes an $O(1/k)$ fraction of the choices. Restore $JB$ at weight $D$ and give the tip label $-h$, adding weight $F$. The free vertices now omit zero and repeat one nonzero label, and all closed edge sums occur once. Opening with the specified anchor transfers the old surplus to the repeated label.

**Both old endpoints at the surplus.** Normalize both labels to zero. Replace the designated cycle edge by a path through a virtual vertex $O$ labeled zero. This represents the two entering edges. Remove $Y$, and cut an auxiliary edge $JB$ of the original cycle different from the designated edge. This gives a path of order $k$ with endpoints $B,P$, where $P$ is the tip's former neighbor. Put
$$
             x_O=0,\quad x_J=h,\quad x_B=-h,\quad x_P=r,
             \qquad C=G\setminus\{r-h\},\quad V=G.
$$
When $P=J$ take $r=h$. The endpoint sum is $r-h$, giving (2). Take $h\ne0$. The potential retained sums at marked positions are $h,-h$ and, when $P\ne J$, $h+r$. With $P=J$, both possible sums are distinct and nonzero. Otherwise choose $r$ avoiding vertex equalities, coincident sums and the omission $r-h$; equality $h+r=r-h$ is already excluded by $2h\ne0$. Restoring $JB$ adds weight zero, and restoring $Y$ at $-h$ adds $r-h$. The resulting $k+1$ edges have counts $G+e_0$. Replacing the virtual vertex by the actual endpoints preserves those sums, and deleting the old edge subtracts $e_0$. The $k$ new vertices omit zero and repeat $-h$, so both histograms are balanced. This proves the one-leaf replacement at every old order for all sufficiently large $k$.

## Independent checks and scope

~~~sh
python3 -B research/bounded-degree/check_unicyclic_core.py
python3 -B research/bounded-degree/check_tadpole_pins.py
~~~

The [small-core construction](unicyclic_core.py) is checked on 423 actual graph and cut instances through order 1,875. The [checker](check_unicyclic_core.py) reconstructs the cut-tree degrees, induced edge sums, both target moments and the number of inside and outside vertices of every degree. The examples include graphs with only degrees one and three. A [separate path-target checker](check_tadpole_pins.py) rebuilds each cut graph in the one-leaf proof and checks its endpoints, target sums and marked positions in 18,572 cases. These checks verify the local inputs. The sufficiently-large-order completion uses Lemma 4.9 of the cited paper.

For the one-leaf edge replacement, [independent full-label certificates](../census/one-leaf-period.md) also settle every modulus from 4 through 63. Neither result gives the unknown numerical starting point of the asymptotic argument. The unrestricted all-moduli tree conjecture remains open.
