# A rainbow connected prefix that scattered two-edge arms cannot complete

**Theorem.** For every $r\ge1$ there is one fixed tree prefix with distinct integer vertex labels and distinct integer edge sums with the following property at all sufficiently large moduli $k$. Attach one two-edge arm at each of $r$ distinct prescribed vertices and add leaves at the zero root until the order is $k$. No $k$-cordial labeling extends that prefix.

The resulting trees have only one vertex of unbounded degree. They are themselves $k$-cordial at all sufficiently large moduli by the [one-exceptional-degree theorem](one-exceptional-degree.md). The obstruction concerns keeping the specified prefix. In the [positive repair using pendant stars](pendant-stars.md), several arms share a parent and its label enters several boundary-edge equations.

## Construction and the matching equations

Give the root label zero, put labels $p_1,\ldots,p_r$ on $r$ of its children, and add another child of label $a=t-s$ with one child of label $s$. Choose $0,p_1,\ldots,p_r,a,s,t$ pairwise distinct. The actual prefix edge sums are $p_1,\ldots,p_r,a,t$. Thus both histograms are already balanced. Write $x_i,y_i$ for the two future labels below $p_i$, in that order. The number of direct leaves to add at zero is $k-3r-3$.

At order $k$ the vertex labels must be a bijection, and every edge weight occurs once apart from one omitted residue $g$. Direct leaves at zero contribute identical labels and weights. Subtracting the prefix histograms gives the required multiset equality
$$
\{p_i+x_i,\ x_i+y_i:1\le i\le r\}\mathbin{\uplus}\{t,g\}
=
\{x_i,y_i:1\le i\le r\}\mathbin{\uplus}\{s,0\}.
$$
We prove that generically even this equality is impossible, allowing any values for the new labels and the omission.

Fix one of the $(2r+2)!$ bijections between positions in these lists. It gives an integer matrix of $2r+2$ equations in the $2r+1$ unknowns $(x_i,y_i,g)$, with right hand side linear in $(p_i,s,t)$. There is a nonzero rational relation among its rows on the unknown side. Clear denominators, obtaining integer multipliers $\lambda_j$. Their linear combination on the data side is a **nonzero** integer linear form.

Indeed, if it vanished identically, the multipliers on the rows $p_i+x_i$ and $t$ would all vanish, since each has its own data coordinate. The multiplier at $g$ vanishes because $g$ occurs in just that row of the unknown side. Only rows $x_i+y_i$ can remain. If $b>0$ of them have nonzero multipliers, their left entries involve $2b$ distinct unknowns with nonzero coefficients. Their matched right entries can use at most $b$ of these unknowns. They cannot cancel. This contradicts the choice of a nonzero relation and proves the claim. The argument applies to every matching, including ones that match constants to constants.

## One fixed prefix for all sufficiently large moduli

There is an explicit choice. Put $H=(2r+1)!$ and $B=2H+3$, and take $(p_1,\ldots,p_r,s,t)=(1,B,\ldots,B^{r+1})$. For each matrix choose a maximal independent set of rows and one further dependent row. On a nonsingular minor of the independent rows, the cofactor dependence on these rows has nonzero coefficient at the extra row. It annihilates all columns since the extra row lies in the span of the independent ones. All matrix entries belong to $\{-1,0,1\}$, so the determinant expansion bounds each multiplier by $H$ in absolute value (use multiplier one at rank zero). Each data coordinate appears in only one equation, so the resulting nonzero linear form also has coefficients of absolute value at most $H$.

On the chosen powers of $B$ this form is a nonzero integer. Reducing successively modulo $B$ proves nonvanishing, and the geometric sum bounds its magnitude strictly below $B^{r+2}$. At every $k>B^{r+2}$ it remains nonzero modulo $k$, which contradicts the required matching. The prefix labels and sums are distinct there as well. In addition, over a prime field of order $q$ the same row-count and disjoint-variable argument works directly over the field. The fraction of all data vectors admitting the histogram equality is at most $(2r+2)!/q$ by the union bound over proper hyperplanes.

## Explicit certificates and an eight-label example

For the following smaller prefixes the checker generates an integer multiplier vector for every matching, multiplies it back against the original matrix, and obtains a nonzero integer from the data. Its largest absolute value is the threshold displayed.

| $r$ | $(p_i)$ | $s$ | $t$ | All $k$ greater than |
|---:|---|---:|---:|---:|
| 1 | $(1)$ | 7 | 19 | 39 |
| 2 | $(1,7)$ | 24 | 61 | 259 |
| 3 | $(1,11,127)$ | 1601 | 19013 | 152635 |

Already at $k=8$, take $r=1,p_1=1,s=2,t=5$. The prefix uses vertex labels $0,1,3,2$ and sums $1,3,5$. There are twelve injections of two of the remaining labels on the arm. For each injection the other two labels are forced as a set on the direct leaves, and in every case an edge weight repeats. On the **same tree** change $t$ to 7, so $a=5$, and give the arm labels $7,3$ and the direct leaves $4,6$. Its edge weights are $1,5,7,0,2,4,6$. The independent direct search also checks failed and successful prefixes at modulus 13 with two and three scattered arms.

~~~sh
python3 -B -m research.hub.check_scattered_arms
~~~
