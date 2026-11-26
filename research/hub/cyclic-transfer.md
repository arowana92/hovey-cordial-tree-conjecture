# Three arbitrary branches at a hub

**Theorem.** Let $H$ have a specified vertex $o$ with at least three incident branches of order at least two. The branches can be arbitrary rooted trees. There are distinct integer labels with $o$ labeled zero for which the edge sums of $H$ are exactly its nonzero vertex labels. For every sufficiently large modulus $k$, the tree obtained by adding any number of leaves at $o$ is therefore $k$-cordial. The threshold is independent of the number of added leaves.

Here are uniform bounds. Discard all singleton branches for the moment. Let $h$ be the remaining order including $o$, and let $b$ be the largest branch order. It suffices that $k>2bhD$, with $D=2^{3b+1}$. For prime $k$ it suffices that $k>\max(D,2bh)$. Thus for any fixed $b$ the threshold grows at most linearly with $h$, with no limit on the number of branches.

## Linking the branches

Index the nonsingleton branches cyclically by $i=1,\ldots,r$, $r\ge3$. Give the root of branch $i$ the vector $(1,0)$ and start a running vector at $(0,1)$. Visit its other vertices in any parent-before-child order. Assign the running vector to the new vertex and then add its parent's vector to the running vector. Write $(A_i,B_i)$ for the terminal value. Both entries are positive. All nonroot vectors form a strictly increasing sequence in the coordinatewise order, in the sense that each step increases one or both coordinates. The second nonroot vector, if present, already has positive first coordinate. [Related single-branch recurrence](branches.md#an-integer-certificate-for-attaching-a-whole-branch)

Use independent variables $Y_1,\ldots,Y_r$ over the rationals. In branch $i$ evaluate a vector $(u,v)$ as $uX_i+vY_i$, where
$$
 X_i=(Y_{i+1}-B_iY_i)/A_i .
$$
The edge at the hub weighs $X_i$, the first nonroot vertex has label $Y_i$, and the terminal sum is $Y_{i+1}$. At each step the edge to the parent weighs the next running value. Thus the internal edges cover all nonroot branch labels other than $Y_i$ and supply $Y_{i+1}$ in its place. Following the indices around the cycle supplies every omitted label exactly once.

It remains to establish that the vertex forms are distinct and nonzero. Within one branch the substitution from $(X_i,Y_i)$ to $(Y_i,Y_{i+1})$ is invertible. The original vectors are distinct and nonzero. A form depending on both coordinates cannot coincide with a form from another branch, since the unordered pairs of adjacent indices in a cycle of length at least three are distinct. The only form of branch $i$ proportional to $Y_i$ alone is its first nonroot label, $Y_i$ itself. A form proportional to $Y_{i+1}$ alone would have $(u,v)=\lambda(A_i,B_i)$ for some $0<\lambda<1$: the root cannot lie on that ray, and each nonroot vector is strictly before the terminal vector. This fraction of $Y_{i+1}$ is distinct from $Y_{i+1}$ itself in the next branch. These exhaust the possible intersections of supports.

A rational specialization avoiding all the finitely many equality hyperplanes exists. Clearing denominators gives the claimed integer labels. Previously omitted singleton neighbors can receive fresh nonzero integers, since each contributes its own label as a weight. Reduction at any modulus larger than the span preserves distinctness. The [periodic leaf extension](README.md) handles any number of further leaves. Equivalently, the construction rules out this entire class of obstructions in the [rational criterion for a fixed hub](rational.md).

## A quantitative specialization

Set $Y_i=A_{i-1}A_i t_i$. The form at $(u,v)$ now has integer coefficients
$$
 (A_i v-B_i u)A_{i-1}t_i+u A_{i+1}t_{i+1}.
$$
All original coordinates, including the terminal ones, are at most $2^b$: the largest coordinate at most doubles at a step. Each displayed coefficient has absolute value at most $2^{3b}$, so the coefficients of pairwise differences have absolute value at most $D$. Include the hub's zero form in these comparisons.

Choose $t_1,\ldots,t_r$ in order modulo $k$. For a difference of two forms, impose its nonvanishing when its last nonzero **integer** coefficient is reached. At that step a congruence $d t_i=c$ excludes at most $\gcd(|d|,k)\le D$ values. Each variable occurs in at most $2b$ vertex forms, and each can be compared to fewer than $h$ others. Thus fewer than $2bhD$ values are forbidden at any step. At a prime larger than $D$, each comparison excludes just one choice. These estimates give the stated thresholds. All edge identities are integral polynomial identities, so they survive reduction even when some $A_i$ are nonunits modulo $k$.

## Verification

The checker generates the sparse integer forms, recomputes each edge sum directly from the tree, and compares the multiset of sums with the vertex forms other than the hub. It also tests explicit cyclic labels, additional hub leaves, and a two-branch example explaining the support condition. The parameter checks use the actual coefficients in each example.

~~~sh
python3 -B -m research.hub.cyclic_transfer
~~~
