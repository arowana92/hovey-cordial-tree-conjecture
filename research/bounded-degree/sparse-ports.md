# Uniform reconnections with few leaves outside the ports

Use the [multiport insertion](multiport.md) with $2\le t\le k^{1-\epsilon}$ distinct ports on a $k$-vertex tree $U$ of maximum degree at most a fixed $D$. This note completes its classification of **uniform** increments at sufficiently large $k$, including tree shapes with zero or one leaf outside the ports. Write
$$
  S=\sum\mathbb Z_k,\quad T=\sum_j W_j-\sum_i a_i-S,\quad
  \delta_v=d_U(v)-2+\mathbf1_{\{v\text{ a port}\}}.
$$
Let $L$ count the leaves outside the ports. Precisely those vertices have $\delta_v=-1$. The sum of all $\delta_v$ is $t-2$. A permutation of the free labels must satisfy
$$
                           \sum_v\delta_v x_v=T. \tag{1}
$$
This follows by subtracting the permutation sum $S$ from the [multiport moment](multiport.md#the-necessary-moment).

**Theorem.** For $L\ge2$ the earlier gcd criterion is exact. For $L\le1$, the following cases are necessary and sufficient.

- **One outside leaf and $t\ge3$.** All inputs work.
- **One outside leaf and $t=2$.** Extension works exactly when $T\ne0$.
- **No outside leaves and no positive coefficient.** Extension works exactly when $T=0$. Here $t=2$ and the free tree is a path.
- **No outside leaves and at least two positive coefficients.** Extension works exactly when $\gcd(k,\delta_v:v\in U)\mid T$.
- **No outside leaves and a single positive coefficient.** Apply the local test below. The free tree is a subdivided star with all tips at ports; its joint may itself be a port.

### The single joint

Let $J$ be the unique positive position, with coefficient $c=t-2>0$. Try each $h\in\mathbb Z_k$ with $ch=T$. Count the ports adjacent to $J$ whose old endpoint carries $h$; let their number be $b$. From the **distinct** values of the removed weights discard $2h$. If $J$ itself is a port, also discard $w_0=h+a_J$ unless it occurs at least twice among the removed weights. Some candidate $h$ must have at least $b$ remaining values.

Indeed $x_J=h$ is forced by (1). At each of the $b$ ports the entering and joint edges give the same weight $h+x_i$. It must occur among the removed weights. These weights are distinct by vertex injectivity and none equals $2h$. If the entering edge at $J$ also has this weight, three copies require at least two removed copies.

Conversely choose $b$ allowed distinct weights and label the adjacent ports $w-h$. Pay for each of their entering edges with one removed copy of $w$. If $w_0$ was chosen, pay for the entering edge at $J$ as well, with the second copy. The fixed joint edges have distinct weights and every unpaid fixed entering weight differs from them. Other ports are leaves with independent label variables. If such a port is adjacent to the joint, the two expressions with its variable have different constant terms: otherwise it would already be one of the $b$ ports. All other comparisons between vertex labels or between unpaid entering and induced internal sums are either satisfied constant inequalities or have a nonzero variable coefficient. For large $k$ the remaining labels can be chosen injectively with all these sums distinct. Here $t=c+2\le D+1$ is bounded.

For example at odd $k$, give a star core $2k$ leaves labeled by two copies of every residue, with center zero. Delete its edges to two zero leaves and use old sites at those two leaves and the center. Insert a tripod of order $k$ with a tip at each of the three ports and at least one arm of length one. All old site labels and removed weights are zero. Equation (1) forces the joint to zero, so its short arm would have to repeat a nonzero sum. Uniform increments are impossible. The obstruction concerns preserving both full histograms up to uniform increments.

## Realizing compatible local labels

When $L\le1$, at most $t-2+L$ vertices have positive coefficient. Mark these vertices, the single negative position if present, and all ports. This includes all original vertices whose degree is different from two. Suppose these $O_D(t)$ vertices have injective labels satisfying (1). Permit some entering edges to be paired with equal removed weights, each copy used at most once. Suppose the unpaid entering weights together with all marked internal edge weights are distinct. We show that these local data suffice.

If $m$ entries remain unpaid, $m-1$ removed weights remain. Repeat the [cut-pair and wire construction](multiport.md#a-bounded-degree-unicyclic-replacement) using $m-1$ well-separated internal cut pairs away from all marks and sites of original degree two. There are $k-O_D(t)$ degree-two vertices. Label the two ends of each cut pair $X,W-X$ with its remaining removed weight $W$. Each wire realizes a known unpaid entering weight $B$ using fresh labels $Z,B-Z$ at its anchor and site. For $m=1$ no cut is needed; choose an anchor and a nonneighboring site outside the marked neighborhoods to close the cycle in $U$.

The fresh signed variables of different pairs or wires are independent. In the retained forest no marked edge contains both occurrences of the same variable: cut pairs were removed, and the wire site was nonadjacent to the other marks. The new wires give exactly the unpaid fixed weights. Anchors and cut endpoints are chosen away from the original marks, so all additional retained marked edge expressions have two signed variables, with distinct coefficient vectors on distinct edges. Avoiding the previous labels and weights and the new collisions costs $O_D(t)$ excluded values per variable as in the earlier proof. We obtain a rainbow injection on the closed auxiliary marks.

Let $R$ be the auxiliary graph. On these marks (1) now gives
$$
            \sum (d_R(v)-2)x_v=T+\sum_i a_i-\sum_j W_j=-S .
$$
Paid entering edges and their equal removed weights cancel from this identity. Every vertex of $R$ of degree different from two is marked. Open the designated closing wire, whose ends are also marked. Add six mutually isolated degree-two positions away from the marked vertices and adjust their labels so the entire core sums to $S$. At least six degree-two positions remain outside and every other degree in the cut tree is exhausted. The closed degree-weighted sum on the core is $2S-S=S$; subtracting the closing weight gives the required sum for the cut-tree targets. Lemma 4.9 completes the prescribed embedding. Undoing the cut pairs and wires yields uniform increments. [Müyesser and Pokrovskiy, primary embedding lemma](https://arxiv.org/html/2509.05280v2#S4)

## Choosing the labels in the other cases

With one outside leaf $Y$, let its label be
$$
                    x_Y=\sum_{\delta_v>0}\delta_v X_v-T.
$$
Give every other initial mark its own independent variable. This enforces (1). For $t\ge3$ the positive coefficients have total $t-1\ge2$, so $x_Y$ differs formally from every single-variable label. An induced edge incident to $Y$ has coefficient sum $t$, another marked edge has coefficient sum two, and an entering edge has coefficient sum one since $Y$ is not a port. Within each kind the variable vectors distinguish the edges. Thus all collision comparisons have a nonzero coefficient bounded in terms of $D$. Although the one expression at $Y$ may involve many variables, it and its only edge contribute only $O_D(t)$ comparisons involving any given variable. All other variables have bounded occurrence counts. Greedy choice works. For $t=2$ there is one positive joint $J$ with coefficient one, so $x_Y=X_J-T$. If $T=0$ injection fails. Otherwise the two different labels with coefficient vector $e_J$ are separated by a nonzero constant. Edge sums with identical coefficient vectors can only come from replacing $J$ by $Y$ next to the same marked neighbor, and their difference is also nonzero. The other comparisons work as before.

With no outside leaves and no positive coefficients, (1) requires $T=0$ and arbitrary distinct variables at the ports suffice. With at least two positive coefficients, solvability of the linear congruence in (1) requires the stated gcd condition. Choose one solution $b_v$ on the marks. Fix a positive position $z$, write $d=\delta_z$, and use the affine family
$$
   x_i=b_i+d Z_i\quad(i\ne z),\qquad
   x_z=b_z-\sum_{i\ne z}\delta_i Z_i .
$$
A difference of two expressions is constant on this family as an integer-coefficient form only when its coefficient vector on the original $x_i$ is a rational multiple of $(\delta_i)$. Two distinct vertex labels, two different internal edge sums, or two different entering weights have a nonzero difference vector with coefficient sum zero. A comparison between an internal edge and an entering weight has either mixed signs or just one positive basis vector. None can be parallel to the nonnegative coefficient vector supported at two or more positions. The substituted coefficients are bounded in terms of $D$, and each parameter still occurs in only $O_D(1)$ expressions, including those through $x_z$. Each forbidden equality therefore excludes $O_D(1)$ values at its last nonzero parameter. This constructs all local labels and completes the classification.

## Verification

~~~sh
python3 -B research/bounded-degree/check_sparse_ports.py
python3 -B research/bounded-degree/check_multiport.py
~~~

The [constructor](sparse_ports.py) supplies the affine labels, the paid entering edges, the small cut-tree core and both target moments. The [checker](check_sparse_ports.py) verifies the actual local sums and recounts the full degree-core data in 298 positive cases and exercises 42 moment or short-arm obstructions, on orders through 1,024. These checks concern the prescribed embedding on the marks; the extension over all remaining vertices is the sufficiently-large-order theorem.
