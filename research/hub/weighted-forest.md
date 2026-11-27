# Simultaneous integer moment control on a forest

**Lemma.** In a forest of at most $n$ free vertices, prescribe the actual integer parent of each component root and a fixed occupied set of size and magnitude $O(n+1)$ containing the boundary labels. Give the free vertices any nonnegative integer weights $r_v$ with total at most $h$. There is an injection outside the fixed set with labels and targets of magnitude $O((n+1)^2)$ and at most an absolute constant number of [guarded discrepancy pairs](integer-forest.md) on the actual entering edges, such that
$$
 \left|\sum_v r_v f(v)\right|=O((h+1)(n+1)).
$$
The constants can absorb those in the bound for the fixed set. In particular $r_v$ can count terminal children deliberately left for a final walk. There is no bound on any individual $r_v$. A bounded number of other weight systems can be controlled simultaneously, with constants depending on their number.

## Grouping a vector of weights

Consider a level with $u\le n$ vertices carrying prescribed vectors $w_v$ of nonnegative weights in dimension $d$. Only their linear span matters; project to independent coordinate rows, retaining rank $r\le d$. The projection is injective on their span. We partition the vertices **before their parent jumps need to be known**.

Let $Z=\{\sum_v a_v w_v: |a_v|\le1\}$. Choose $r$ signed sums $z_i=\sum_v\sigma_{iv}w_v$, $\sigma_{iv}=\pm1$, with maximal absolute determinant in the projected coordinates. Such sums span: the all-positive sum and the sums obtained by changing one sign recover each $2w_v$ by a difference. For any $z\in Z$, all coordinates of $z$ in this basis have absolute value at most one. Indeed Cramer's rule compares a one-column replacement determinant to the original, and a linear form on the coefficient cube achieves its extremum at signs. Rank zero uses the empty basis. For an effective alternative, replace a single column whenever its maximum signed determinant is larger. Integral determinants strictly increase and are bounded, and the same Cramer argument holds at termination.

Group vertices by their sign pattern $(\sigma_{1v},\ldots,\sigma_{rv})$, in at most $2^r$ groups. In each group separately choose $c_v\in[-1,1]$ satisfying $\sum c_v w_v=0$, with at most $r$ coefficients strictly between the endpoints. Start with all zero. As long as the vectors with interior coefficients are dependent, move their coefficients along a rational dependence up to the first box boundary. This preserves the equation and decreases the interior count. Split this group into one subgroup per occurring endpoint sign and a singleton for each interior coefficient. The number of final subgroups is at most $2^r(r+2)$ and they each have a common coefficient $c_H$. They can all be selected from the topology and weights alone.

## Translation while preserving all moments

Suppose every final subgroup's total parent jump and each individual jump has magnitude at most $K$. In each subgroup run the signed walk, erase cycles and translate their offsets as in the [integer forest proof](integer-forest.md#the-integer-construction). Within each subgroup the offsets $a_v$ are distinct, exclude the terminal jump sum, and have magnitude at most $K+u(u+1)$. Set $A=\max_v |a_v|$. Express $-\sum a_v w_v=\sum_i d_i z_i$. The basis bound gives $|d_i|\le A$, also when $A=0$. A sign group $j$ receives baseline $y_j=\sum_i d_i\sigma_{ij}$, with $|y_j|\le rA$. Then $\sum_v(a_v+y_{j(v)})w_v=0$ exactly, including in the original coordinates.

Use an independent integer $z_j'$ for each sign group and an independent integer $e_H$ for each subgroup. Translate the offsets of subgroup $H$ of group $j$ by
$$
 X_H=\lfloor y_j+c_H z_j'\rfloor+e_H .
$$
For box lengths $L,D$ use $0\le z_j'<L$, $0\le e_H<D$. The terms with $z_j'$ have **zero** vector moment by construction. Hence in any original coordinate $i$ the final moment has absolute value at most $(D+1)\sum_v w_{vi}$. This bound holds for every parameter choice.

There is an admissible choice with $L=O_d((n+1)^2)$ and $D=O_d(n+1)$ if the already blocked set has size $O(n+1)$. Within an endpoint-sign subgroup its translation is an integer variable of unit slope in $z_j'$, after fixing the other coordinates. All the [ordinary and guarded tests](integer-forest.md#the-integer-construction) within it or against the preexisting labels and reservations exclude at most one value per equality. Ordinary arrivals in different endpoint-sign subgroups either depend on different $z_j'$ or have opposite unit slopes in the same $z_j'$. Altogether these lists have $O_d((n+1)^2)$ comparisons of probability at most $1/L$. Within a singleton all remaining tests against old and new values cost $O_d(n+1)$ comparisons per singleton. Between two subgroups, tests involving a target, its negative, or any of the forbidden multiples also cost only $O_d(n+1)$ in total because the number of subgroups is bounded. For each such equality fix all coordinates except the relevant subgroup's $e_H$. Its coefficient is nonzero. Within a subgroup the only identical-slope exclusions are the same ones already settled by the walk offsets. Thus these last tests have probability at most $1/D$ each. Increasing the box constants makes the union smaller than one. The code can enumerate the box after independent trials. Each subgroup adds at most one guarded pair. Every label and target has magnitude $O_d(K+(n+1)^2)$.

## Planning levels from the tips back towards the roots

First use the [linear-magnitude neutral partial forest](polynomial-two-hubs.md#a-partially-labeled-forest-with-its-incoming-edges). Its contribution to the requested terminal moment is at most $O(h(n+1))$. The rest has at most 432 levels. Plan their subgroups from deepest to shallowest. At the deepest level use weight $r_v$. At each earlier level take the vector consisting of $r_v$ and, for **each final subgroup of the next level**, the number of children of $v$ in that subgroup. Apply the grouping construction just proved to this vector. Its required dimension is one plus the next subgroup count. Iterating $d\mapsto1+2^d(d+2)$ at most 432 times gives a finite absolute bound on all dimensions and counts. This bound is very large. In actual finite instances the rank never exceeds the number of vertices on the level.

Place levels in the forward order. Each first-level subgroup's total parent jump has magnitude $O((n+1)^2)$, since the initial parents have magnitude $O(n+1)$. At any later level the total for a subgroup is exactly the preceding level's specified child-count moment. It is at most $O((n+1)^2)$ since that coordinate's mass is at most $n$. The baseline and box bound therefore keeps all individual labels $O((n+1)^2)$ by induction through a bounded number of levels, allowing a constant multiplier on the old maximum at each step. The terminal-count moment on each level costs $O(n+1)$ times its own terminal mass. Adding those bounds and the neutral seed contribution proves the lemma. Previously reserved guards are retained throughout and cost only a constant per accumulated pair. No tree degree enters the number of pairs.

## Checks

The verifier checks the null equations and the lifted baseline cancellation against every **original** coordinate, including dependent columns with sizes above $10^{12}$. On 129 forests it computes all 2,709 entering weights independently, checks guard exclusions, and compares actual terminal moments to the rounding allowance. A deep forest adds 1,491 entering edges, exercising the neutral seed before the weighted levels. Six full-tree checks use these labels in subsequent window repairs. [Rational constructor](weighted_forest.py) · [Vector identities, forest and actual-edge checks](check_weighted_forest.py)

~~~sh
python3 -B -m research.hub.check_weighted_forest
~~~
