# The square-root threshold for repeated tree attachment sites

Fix a bound $D\ge2$ on the internal degrees of a tree $U$ of order $k$. Join $t$ old components to $U$ after removing $t-1$ edges from a prescribed cordial tree. Multiple entries at one free vertex are allowed. Assume the entering old labels are distinct **within each free vertex**. Define $N_D(k)$ to be the largest $n$ such that every such insertion with $1\le t\le n$ preserves the old labels whenever the four [parity obstructions](port-parity.md) do not all hold. Degrees in that test count every entering edge.

**Theorem.** There exists $c_D>0$ such that, for every sufficiently large modulus,
$$
                  c_D\sqrt{k}\ \le\ N_D(k)\ <\ 2\sqrt{2k}+3 .
$$
The lower bound permits unbounded multiplicity at individual free vertices and every possible number of nonport leaves. The upper bound already holds on a path with two internal attachment vertices at every sufficiently large modulus. These are bounds on extending a specified labeling.

## Choose the bins after drawing the joint labels

We strengthen the [repeated-port theorem](repeated-ports.md). Its two-leaf proof excludes at most $O_D((t+1)^2/k)$ of the independent small-quotient lifts. Thus two nonport leaves suffice for $t\le c_D\sqrt{k}$ with a sufficiently small fixed $c_D$, after increasing the lower threshold on $k$. All packing and degree-core bounds continue to hold since $O_D(t)=O_D(\sqrt{k})$. Bounded $t$ is covered by the same theorem. We may now suppose $t\ge5$ and that at most one leaf is outside the ports.

Let $G=\mathbb Z_k$, set $m_v$ equal to the number of entries at $v$, and put $\delta_v=d_U(v)-2+m_v$. Mark every port and every nonzero coefficient. The coefficient sum is $t-2$, and at most one coefficient is negative, in which case its value is $-1$. There are at most $2t$ marks. They include every vertex of degree different from two. The induced internal edges together with the entering edges have at most $3t$ weights.

Write $h=\gcd(k,\delta_v:v\in U)$ and $T=\sum W_j-\sum a_i-\sum G$. In an edge or vertex histogram transfer duplicate an old low bin $B$ and omit an old high bin $F$. Write $E=B_e-F_e$ and $V=B_v-F_v$ for the respective differences, or zero for no transfer. Since $h\le t-1<k$, the [consecutive-count argument](port-parity.md#which-old-bins-can-move) supplies a transfer plan unless all parity conditions hold. It uses at least one genuine transfer and makes $T+E-2V$ a multiple of $h$. Fix the residue classes of the bins in that plan. In one genuine transfer keep one endpoint fixed and vary the other bin $z$ through a set of at least $k/(2h)$ values in its class, using the residue-cycle argument in that proof. Fix all bins in any other transfer. The required moment now takes values
$$
                           R(z)=K+bz, \qquad b\in\{1,-1,2,-2\}.
$$
All these values belong to $hG$, and there are at least $k/(4h)$ different values since each has at most two preimages.

Give **every marked vertex an independent uniform** label $X_v\in G$. The linear form $L=\sum\delta_v X_v$ is uniform on $hG$. Indeed its image is precisely this subgroup by Bézout's identity, and every fiber of a group homomorphism has the same size. Consequently $L$ lies in the available set of moments with probability at least $1/4$. This allows us to exclude collisions in the original independent labels before selecting $z$.

1. Comparing two vertex labels or two different pinned weights costs at most $1/k$ per pair. Different internal edges have different incidence vectors. An entering edge has one variable, and repeated entries on the same variable have distinct constants. The number of tests is $O(t^2)$.
2. A fixed vertex or edge gap conflicts with any one of its pinned values with probability $1/k$. There are $O(t)$ such tests.
3. If the moving bin is an omitted edge color, a conflict with a pinned weight $w$ would require $z=w$, hence $L+w=K$. Its coefficient sum is $t-2+1$ or $t-2+2$, so the form has a nonzero integer coefficient. If the moving bin is an omitted vertex label, a conflict at $i$ would require $L-2X_i=K$, whose coefficient sum is $t-4>0$. In both cases the coefficients have absolute value at most $t+1<k$. Conditioning on all but one variable, each equation therefore has probability at most $(t+1)/k$, even for composite $k$. There are at most $3t$ such equations. A moving duplicated bin has no gap condition.

The probability of any forbidden event is $O(t^2/k)$, which is less than $1/4$ for sufficiently small $c_D$. There is a draw with no collisions and $L=R(z)$ for an available bin $z$. If no edge transfer was used, choose an artificial $B_e=F_e$ outside the pinned weights now. These marks meet the exact moment identity and all palette exclusions. The [degree-two segments](port-parity.md#realizing-both-transfers-at-once) realize these transfers and reduce completion to the prescribed bounded-degree rainbow tree embedding. The segments need $O_D(t)$ space and the degree core has $O_D(t)$ vertices. This proves the lower bound, decreasing $c_D$ if needed for integer rounding. [Müyesser and Pokrovskiy, Lemma 4.9](https://arxiv.org/html/2509.05280v2#S4)

## A path obstruction at every large modulus

Take $m=\lceil\sqrt{k/2}\rceil$, with $2m\le k$, and put
$$
                  A=\{0,\ldots,2m-1\},\qquad
                  B=\{0,m,2m,\ldots,\lfloor(k-1)/m\rfloor m\}.
$$
Every cyclic gap between successive members of $B$ is at most $m$, including the wrap from the last member to zero. Every cyclic interval of $2m$ residues therefore contains at least two different members of $B$, one in each consecutive run of $m$ residues. The [Lean proof](PortCover.lean) proves this for every pair of integers $0<m$ and $2m\le k$, including nondivisible $k$.

At two distinct internal vertices of a $k$-vertex path, enter at the old labels from $A$ and from $B$. Use the [double-star construction](repeated-ports.md#every-prescribed-boundary-list-occurs-on-actual-cordial-trees) to realize uniform old edge bins and only zero removed weights. For every choice $x,y$ at the two sites, the entering weights $x+A$ and $y+B$ have at least two common colors, at least one nonzero. Its old copies survive and at least two new copies enter, contradicting the required uniform increment. Both original path tips are nonport leaves, so the parity obstruction is absent. The number of entries satisfies
$$
                t=2m+\lceil k/m\rceil < 2\sqrt{2k}+3 .
$$
This gives the upper bound for every large $k$. No claim of failure of ordinary cordiality is needed.

## Reproduction

~~~sh
python3 -B research/bounded-degree/check_port_threshold.py
lean research/bounded-degree/PortCover.lean
~~~

The [checker](check_port_threshold.py) samples independent labels with a fixed seed and reconstructs the actual finite embedding targets. It verifies 1,173 successful targets and 27 parity obstructions on five moduli, including instances with many entries at the same joint. It also slides every cyclic window through every modulus from five to 2,000. Lean 4.36.0 checks the two-hit lemma at all orders. The asymptotic lower bound uses the counting argument and the external embedding theorem.
