# Two free parents and the leaf count of a smallest counterexample

**Theorem.** For every prime $29\le p\le61$, if a smallest noncordial tree at $p$ has order $mp+s$, $1\le s\le p$, and $L$ leaves, then
$$
L\le 2s-p-3.
$$
This removes the equality case in the [one-parent bound](star-lists.md#a-test-at-the-extremal-leaf-count) at all residues of these nine primes. The statement is conditional on the existence of a counterexample. At 29, a minimum counterexample of order divisible by 29 would have at most 26 leaves. At orders one below a multiple it would have at most 24.

## Coefficient for two disjoint stars

Use the [list grid](star-lists.md#the-list-theorem) with $r$ new vertices and $e$ forbidden edge weights at a prime $p$. Let two distinct new vertices have $j,h$ leaf children respectively. Both centers attach to old vertices and there are $b=r-j-h-2$ other singleton rows. Give each row its own list of size at least $r+e$. Assume $r<p$ and $r+e\le p$. The following field calculation decides if the top grid coefficient certifies the extension, for every choice of lists, boundary labels and additive offsets.

Index rows and columns of each matrix by $I=\{e,\ldots,e+r-1\}$. Put
$$
B(a)_{mn}=\binom nm a^{n-m}\ (m\le n),\qquad C(a)_{mn}=a^{n-m},
$$
with $B(a)_{mn}=0$ below the diagonal and $a$ a unit for $C(a)$. With $t$ a Laurent variable and $D=I_r+zB(1)+wB(t)$ the required coefficient is
$$
(-1)^{\binom r2}j!h!b!\,[z^jw^h u v t^0]\det\big(D+uC(1)+vC(t)\big).
$$

Indeed after expanding the first Vandermonde the required exponents permute $I$. The exponents offered by the edge determinant permute the same set. Temporarily replace the centers as parents by independent parameters $a,t$. A leaf row of the first star that needs power $m$ and offers $n$ contributes $\binom nm a^{n-m}$. The center's row contributes $a^{n-m}$, where its required power must account for transfers from its children. Taking the constant term in $a$ enforces that match exactly. The second star uses $t$ in the same manner. Singletons require $m=n$. In every determinant term the total degree in the two center parameters is zero, so one may set $a=1$ and retain only the constant term in $t$. Expanding a determinant by rows assigns distinct target exponents to each row type. The extra factorials order the children and singletons, and reversal of the first determinant's exponents gives the sign.

The matrices $C(a)=U(a)V(a)^T$ have rank one, with $U(a)_m=a^{-m}$ and $V(a)_n=a^n$. Thus the coefficient of $uv$ is
$$
(1+z+w)^r
\det\left(V(a)^TD^{-1}U(c)\right)_{a,c\in\{1,t\}}.
$$
This equality holds as a formal series at $z=w=0$ by the rank-two determinant identity. For computation, the coefficient of $z^l w^m$ in the inverse is $(-1)^{l+m}\binom{l+m}{l}B(l+mt)$, since the translation matrices satisfy $B(a)B(c)=B(a+c)$. In the constant-term calculation each center can have a negative exponent of magnitude at most $r-1$ because its own row contributes at least $e-(e+r-1)$ and its children contribute nonnegative powers. Total degree zero bounds positive exponents by $r-1$ as well. Hence averaging over all $t\in\mathbb F_p^\times$ selects the constant term exactly. [Coefficient implementation](two_star_lists.py)

## Applying the criterion to trees

Suppose $L=2s-p-2\ge3$ in a smallest counterexample. Delete its original leaves to get a smaller tree $K$. Its order $mp+p+2-s$ is at least two. If only two remain then $m=0,s=p$ and the tree is a caterpillar, so take $|K|\ge3$. Choose two distinct terminals of $K$. They are nonadjacent and deleting both preserves a connected nonempty core. Each had at least one original leaf child. Their populations $j,h$ satisfy $j+h\le L$ and each must lie in the exceptional list from the [single-terminal coefficient](star-lists.md#a-test-at-the-extremal-leaf-count).

Delete both chosen terminals as well. The removed forest has two stars and $L-j-h$ singleton rows. Write $r=L+2=2s-p$. The retained core has order $mp+p-s$. When $s=p$, the single-terminal coefficient already excludes equality. For $s<p$, the number of high vertex bins is $p-s$, and the number of high edge bins is $p-s-1$. There are $s$ available vertex labels per row. We may take the forbidden output size $e=p-s-1$ or enlarge the set by one arbitrarily to use $e=p-s$. In both cases $r+e\le s$. Any certified extension therefore gives the required two balanced histograms on the original tree.

The finite checks used the explicit binomial formulas for every integer $s$ from $(p+5)/2$ through $p$, every surviving pair $1\le j\le h$ with $j+h\le L$, and the two allowable forbidden sizes until one coefficient was nonzero. Smaller $s$ are excluded by the preceding leaf bound and $L\ge3$.

| Prime | 29 | 31 | 37 | 41 | 43 | 47 | 53 | 59 | 61 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Pairs left by the one-terminal test, counted across residues | 3 | 2 | 4 | 3 | 9 | 5 | 9 | 13 | 10 |
| Pairs left by both tests | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

At $p=29$ the three surviving triples $(s,j,h)$ are $(20,1,1)$, $(26,10,10)$ and $(28,9,9)$. At the actual forbidden size their full grid coefficients are respectively $23,10,14$ modulo 29. A separate C++ check evaluates the determinant directly at all triples $(t,z,w)$ of nonzero field elements, extracting $uv$ by the four values obtained at $u,v\in\{0,1\}$. The two rank-one updates make the determinant affine in each marker. After extracting both markers the degree in either $z$ or $w$ is at most $r-2<p-1$, so the averages with factors $z^{-j},w^{-h}$ select the requested coefficient. This computation permits singular $D$. [Independent field-grid determinant](check_two_star_grid.cpp)

## More than two free parents

The determinant construction also gives an exact coefficient algorithm for any rooted forest with a fixed number $d\ge1$ of vertices having children. Keep the same exponent interval $I$. Give each of these vertices $c$ its own center parameter $t_c$, a selector $z_c$ for its leaf children, and a marker $u_c$ for its own row. Treat the parameter of an external parent as zero. The determinant matrix is
$$
I_r+\sum_c z_c B(t_c)+\sum_c u_c M_c,\qquad
(M_c)_{mn}=t_c^{-m}(t_c+t_{p(c)})^n.
$$
The identity term assigns externally attached singletons. Extract each $u_c$ once, each $z_c$ to the number of leaf children of $c$, and the constant term in the $t_c$. Multiply by the reversal sign, the factorial of the number of external singletons, and the factorials of the leaf populations. The same row expansion proves the formula, with the marked row including the linear term from its own parent when that parent is also free. Every $M_c$ has rank one, so inclusion and exclusion on the $d$ markers extracts all their coefficients at once.

For $r+e\le p$, one can evaluate over $\mathbb F_{p^2}$, averaging the selectors and $d-1$ center parameters over its nonzero elements. The remaining center parameter is fixed to one by homogeneity. Each selector degree is at most $r$. Each center parameter has exponent at least $-(e+r-1)$ because only its own marked row contributes negative powers. All center exponents sum to zero. A monomial surviving the averages has every center exponent divisible by $p^2-1$, including the exponent of the normalized center. The lower bound forces every such exponent to be nonnegative, hence zero. This proves exactness, with a number of field operations polynomial in $p$ for each fixed $d$. A zero value in any of these tests leaves the existence of labelings open.

## Reproduction

From the repository root run

~~~sh
out=$(mktemp -d)
c++ -O3 -std=c++17 research/biased/check_two_star_grid.cpp -o "$out/grid"
python3 -B -m research.biased.check_two_star_lists --native "$out/grid"
~~~

The Python checker also compares 39 small coefficients with a direct double-permutation expansion on the actual forests. Four further field-grid checks exercise nested parents on forests with up to three centers. The checker asserts that no terminal pair survives in the nine-prime table. [Proof replay](check_two_star_lists.py) · [Direct exponent-transfer calculation](forest_grid.py)

## Excluding one more residue at every odd prime

**Theorem.** At every odd prime $p\ge5$, a smallest noncordial tree of order $mp+s$, $1\le s\le p$, must satisfy $s\ge(p+9)/2$.

The [four-leaf theorem](../census/four-leaves.md) gives $L\ge5$. The leaf bound $L\le2s-p-2$ therefore gives $s\ge(p+7)/2$. It suffices to exclude equality. The already settled small moduli allow us to assume $p\ge29$. At equality $L=5$. Delete the five leaves. The remainder $K$ has at least three vertices since $s\ge18$. Each terminal of $K$ was adjacent to an original leaf and at least two terminals exist. Some terminal has one or two original leaf children, since a pair of distinct terminals together accounts for at most five.

Delete one terminal of $K$ too. There are $r=6$ free vertices and $e=(p-7)/2$ forbidden edge weights in the [one-star test](star-lists.md#a-test-at-the-extremal-leaf-count). For child counts $j=1,2,3,4,5$, the reduced coefficients $A_{6,j,e}$ at $e=-7/2$ are respectively

$$
7767/256,\quad 8181/128,\quad 9459/128,\quad 5661/128,\quad 2895/256.
$$

Indeed each binomial $\binom{e+i}{i-l}$ in a truncated Pascal entry has degree at most five in $e$ with denominator dividing $5!$. The six integer evaluations $e=0,\ldots,5$ determine each polynomial and reduction modulo $p$ gives its value at $(p-7)/2$. Since $7767=9\cdot863$ and $8181=81\cdot101$, one of the available one-child or two-child terminals certifies the extension unless $p=101$ or $863$.

At 101 only $j=2$ has a zero coefficient. At 863 only $j=1$ does. Choose two terminals of $K$ and remove both, so the new forest on seven vertices has two stars with those populations and the remaining vertices are singletons. The surviving core has $s-7$ high vertex bins and $e=(p-9)/2$ high edge bins. Each input list has $p-(s-7)\ge7+e$ entries. At 101 the full coefficient is $9\pmod{101}$ and at 863 it is $858\pmod{863}$. These are nonzero, so the smaller cordial core extends in both cases. This excludes equality and proves the stated bound.

Run the following check from the repository root. It interpolates the six-row coefficients from integer Pascal sums and computes each seven-row coefficient twice, by the two-star formula and a signed sum over all $(7!)^2$ exponent-permutation pairs. [Verification code](check_five_leaf_residue.py)

~~~sh
python3 -B -m research.biased.check_five_leaf_residue
~~~
