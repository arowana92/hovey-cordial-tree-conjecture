# Exact leaf-count and modulus spectra at bounded core order

The [subsequent integer construction](universal-hub.md) proves the rational criterion for every rooted tree. In particular, the conditional obstruction below never occurs, and there are only finitely many exceptional tree–modulus pairs for each bound on the number of nonleaf vertices.

**Theorem.** Fix a tree $H$ and any set $S$ of its vertices. Write $H(\mathbf m)$ for the tree obtained by attaching $m_v\ge0$ leaves at each $v\in S$. Both of the following sets are effectively semilinear:
$$
\{(k,\mathbf m): k\ge1,\ H(\mathbf m)\text{ is }k\text{-cordial}\},\qquad
\{\mathbf m:H(\mathbf m)\text{ is super edge-magic}\}.
$$
A semilinear set is a finite union of translates of finitely generated additive submonoids of $\mathbb N^d$. Equivalently, it can be described in integer arithmetic with addition, comparisons, Boolean operations and quantifiers. This equivalence is effective. [Ginsburg and Spanier, *Semigroups, Presburger formulas, and languages*](https://msp.org/pjm/1966/16-2/pjm-v16-n2-p09-p.pdf)

In particular, there is a computable $D_h$ such that on **any** $h$-vertex core, the second-largest attached leaf count being at least $D_h$ suffices for a super edge-magic labeling. All other counts can be arbitrary, including zero. For any fixed bound on the number of nonleaf vertices, the set of moduli admitting a counterexample is effectively ultimately periodic. If that set is infinite, then every sufficiently large modulus coprime to a single computable integer has a counterexample **of order equal to the modulus**, from one fixed one-hub family.

## Reduction to one unbounded site

Apply the [selected-site threshold](marked-leaf-threshold.md) on $(H,S)$ when $|S|\ge2$. Its upper orthant is entirely super edge-magic. For each count below the threshold, fix the site and value, absorb those leaves into the core, and recurse on the other sites. The recursion tree is finite. All unresolved parts lie on finitely many lines with at most one free population coordinate, or are individual points. This proves the second-largest assertion by taking one more than the largest fixed coordinate on those parts, then maximizing over the finitely many core shapes and site sets at order $h$. An empty collection of exceptions needs no positive bound.

For either labeling property, reconstructing the full success set takes only finite unions of the successful orthants and the spectra of these fixed-core slices. All these operations preserve effective semilinearity. A fixed tree with no free sites needs only a finite search for ordinary cordiality, since sufficiently large moduli allow distinct powers of two on its vertices and distinct edge sums. Its super edge-magic labelings can be tested by permutations.

## Exact ordinary cordiality on a one-site slice

Let $h=|H|$, let $m$ be the remaining leaf count, let $n=h+m$, and set the attachment site's label to zero by translation. Translation moves every edge sum by twice the same amount, preserving both balance conditions. If $n>(h-1)k$, put **all core vertices at zero**. Choose balanced final vertex counts with zero among the largest residues, reserving $h$ zero slots for the core. There are enough since $\lceil n/k\rceil\ge h$. Assign the rest to leaves. The edge histogram is precisely the vertex histogram with one zero removed, which is balanced. This argument even allows the new leaves to have different core parents.

It remains to work inside $n\le(h-1)k$. Here $q_V=\lfloor n/k\rfloor$ and $q_E=\lfloor(n-1)/k\rfloor$ range over a finite set depending only on $h$. Enumerate them as constants and impose their defining linear inequalities. Represent core vertex labels and edge sums in $[0,k-1]$. Each edge value $y$ satisfies either $y=x_u+x_v$ or $y+k=x_u+x_v$. Enumerate equality patterns among the at most $2h-1$ core vertex and edge tokens, allowing repetitions, and require the distinct classes to have different residues. These are finite disjunctions of linear conditions.

For a residue whose core multiplicities are $(v,e)$, the integer number of new leaves labeled there must lie between
$$
l(v,e)=\max(0,q_V-v,q_E-e),\qquad
u(v,e)=\min(q_V+1-v,q_E+1-e).
$$
The root is zero, so every new leaf has its own label as edge weight. These intervals are sufficient as well as necessary. In a fixed equality pattern there are $s$ occupied residues, with known pairs $(v_i,e_i)$. All other $k-s$ residues have pair $(0,0)$. Every occupied interval must be nonempty, and the sum of the lower bounds must be at most $m$, which must be at most the sum of the upper bounds. Every integer between the two sums is attainable by increasing entries individually. The ordinary interval is always nonempty because $q_V-q_E\in\{0,1\}$.

The ordinary contributions $(k-s)l(0,0)$ and $(k-s)u(0,0)$ are linear because the quotients are fixed within this disjunct. The two global totals of vertices and edges enforce the exact numbers of surplus residues, also when one total is divisible by $k$. Existentially project away the class labels to obtain the exact spectrum in $(k,m)$. This uses ordinary labelings at every modulus, including composite moduli.

## Exact super edge-magicness on a one-site slice

Use normalized vertex interval $I=[L,L+n-1]$ and edge interval $J=[L+1,L+n-1]$. For $n\ge2$ normalization is always possible by translating any consecutive-sums labeling. Choose distinct core labels $x_v\in I$, with distinct core sums $y_e\in J$, and put $p=x_o$ at the attachment site. The remaining integer labels must all be leaves and acquire the same shift $p$. The necessary and sufficient test is
$$
\forall z\in\mathbb Z,\quad
\left(z\in J\ \land\ \bigwedge_e z\ne y_e\right)
\quad\Longleftrightarrow\quad
\left(z-p\in I\ \land\ \bigwedge_v z-p\ne x_v\right).
$$
With an empty edge interval the singleton is immediate. Every expression in the test is linear. Projecting the conditions onto $m$ gives an effective ultimately periodic one-site spectrum. A useful bound follows by reflection $x\mapsto1-x$, which preserves the normalized interval form. With this choice $p\ge1$, and the top $p$ positions in $I$ must be occupied by core vertices because their translated weights would exceed its maximum. In the nontrivial case $0,1\in I$, so $p\le h$.

## Consequences for counterexamples

Take complements and project onto $(k,n)$ using $n=h+\sum m_v$, then take the finite union over the possible nonleaf cores up to a prescribed order. This gives the exact semilinear set of pairs for which at least one counterexample exists in that class. Projection onto $k$ gives ultimate periodicity. The same argument for super edge-magicness makes the set of exceptional tree orders effectively ultimately periodic, and decides the super edge-magic tree conjecture on each bounded-nonleaf class.

If the failing moduli are unbounded, a fixed one-site slice in the finite recursion tree must fail at unbounded moduli. Its [rational linear-algebra test](rational.md) must fail, since a rational witness gives all leaf counts at every sufficiently large modulus. For this rooted core $H'$ write $a$ for its number of edges not incident to the hub. At modulus $k\ge |H'|$, an order-$k$ solution yields a permutation assigning each core edge its weight's vertex and assigning the unused vertex to the remaining root position. The core labels are all distinct modulo $k$.

For each candidate permutation, let $A$ be its integer equation matrix with the root coordinate omitted. A failed rational test forces a nontrivial coordinate difference $v$ (possibly a difference from zero) into the rational row span of $A$. Choose a nonsingular rank-size minor of determinant $d$. By solving on the minor's columns, $d v$ is an integer combination of rows of $A$. Thus whenever $\gcd(k,d)=1$, every solution modulo $k$ has the forbidden equality, including for composite $k$. The row-norm determinant bound gives $|d|\le 5^{a/2}$. Taking $G=\operatorname{lcm}(1,\ldots,\lceil5^{a/2}\rceil)$ works simultaneously for all permutations. Every $k\ge|H'|$ coprime to $G$ gives a counterexample of order $k$. This is a conditional obstruction and the computations here do not exhibit a failed rational test.

There is also an exact tail description for the successful **order-equals-modulus** tests at one hub. Their set of moduli is ultimately periodic by the diagonal $m=k-h$. It is closed under passing to multiples. Embed the successful core residues into $\mathbb Z/(tk)$ by multiplication by $t$. Distinctness and containment of the core edge weights in the core vertex set survive. Give all remaining residues to new leaves at zero. For a period $P$ of the tail, one successful residue class $r$ therefore makes every class divisible by $\gcd(r,P)$ successful. Indeed the congruence $tr=s\bmod P$ has positive solutions for each such $s$, and these can be made arbitrarily large. Thus, past a computable threshold, success is a finite union of divisibility conditions by divisors of $P$.

## Independent checks

The one-site code constructs and projects the equality-pattern and interval formulas in the Integer Set Library. Direct checks enumerate actual full-tree labelings and compare both histograms or integer endpoint sums. Two pinned examples test infinite sets of rejected instances as well.

- For the four-vertex path rooted at an endpoint, pin its neighbor to residue one. On the diagonal $m=k-4$, the failed moduli are exactly the even $k\ge4$.
- For the star with center $1$ and leaves $0,2,3,4$, attach the extra leaves at vertex $0$ and fix its normalized integer label to two. The failed leaf counts are exactly $m\equiv3\bmod6$.

The pins in these tests form part of the examples. Both underlying tree families are caterpillars and have ordinary cordial labelings at every modulus. [One-site projections](core_spectra.py) · [Exhaustive checks](check_core_spectra.py) · [Integer Set Library](https://libisl.sourceforge.io/user.html)

~~~sh
python3 -m pip install 'islpy==2026.2.2'
python3 -B -m research.hub.check_core_spectra
~~~
