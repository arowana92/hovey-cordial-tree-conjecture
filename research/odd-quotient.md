# Joining cordial pieces through an odd quotient

**Theorem.** Partition a tree into $q$ connected pieces of the same order $s$, for odd $q\ge3$. Suppose the quotient tree has a bijection onto $\mathbb Z_q$ with distinct edge sums. There is a positive integer $D$ determined by that labeled quotient, with $q\mid D$ and $D\le2^{q-1}$. If each piece is $m$-cordial and $\gcd(D,m)=1$, the whole tree is $qm$-cordial. The connecting edges may use arbitrary vertices of the pieces. More generally the same conclusion holds whenever
$$
(s-1)\bmod m < m/\gcd(D,m).
$$
In particular, if $s\equiv1\pmod m$ the conclusion holds for every $m$. When $s=m$, the coprime case gives a bijection on $qm$ vertices with distinct edge sums.

At $q=3$, the determinant is always 3. Consequently three equally large $m$-cordial trees joined in any tree pattern give a $3m$-cordial tree whenever $3\nmid m$. A sharper condition at multiples of three is given below.

## The directed graph supplied by the quotient

Name each piece by its quotient label $i$. Its internal edges will lie in residue class $2i$ modulo $q$. A connecting edge $ij$ must use class $2c$ for the unique midpoint $c$ with $2c=i+j\pmod q$. These midpoints are distinct and different from their own edge endpoints. Exactly one residue $r$ is missing as a midpoint. Draw two arrows from each midpoint $c$ to $i$ and $j$.

Every vertex reaches $r$ along arrows. Otherwise the nonempty set of vertices unable to reach $r$ would be closed under both arrows. For every $c$ in this set there would be a different quotient edge inside it, an impossibility for an induced forest. Form the matrix $M$ with rows and columns indexed by the residues other than $r$: in row $c$ put 2 on the diagonal and $-1$ at each of its two arrow targets still present. Set $D=\det M$.

The directed matrix-tree theorem identifies $D$ with the number of ways to choose one arrow at every $c\ne r$ so all chosen paths lead to $r$. There is at least one choice, for instance by decreasing distance to $r$, and at most $2^{q-1}$. Alternatively expand the determinant by multilinearity in its rows. Each row is a sum of its two possible single-arrow rows $e_c-e_j$ with $e_r=0$. A chosen cycle makes the rows dependent; a choice leading to $r$ is triangular with diagonal 1 in distance order. Finally the column vector of residues $c-r$ is killed by $M$ modulo $q$. One entry is 1, so multiplying by the adjugate proves $q\mid D$. [De Leenheer, *An elementary proof of a matrix tree theorem for directed graphs*](https://arxiv.org/abs/1904.12221)

## Solving for translations within the pieces

Choose an $m$-cordial labeling $f_i$ on each piece. With the usual representatives $0\le i<q$, label its vertex $v$ by
$$
i+q(f_i(v)+t_i)\pmod{qm}.
$$
Each vertex coset has balanced counts because every piece has size $s$. The internal edge counts within coset $2c$ are balanced as well. Choose a residue $w_c$ occurring at the lower frequency in the internal edges of piece $c$, allowing any weight if all frequencies coincide. The connecting edge $ij$ at endpoints $u,v$ supplies that low slot, after translation, exactly when
$$
2t_c-t_i-t_j=\frac{i+j-2c}{q}+f_i(u)+f_j(v)-w_c\pmod m.
$$
The fraction on the right is an integer. Take $t_r=0$. These are exactly the rows of $M$. A determinant coprime to $m$ lets us solve them simultaneously for any chosen low slots.

More generally let $g=\gcd(D,m)$. The image of $M$ modulo $m$ contains all vectors with entries multiples of $g$, by $M\operatorname{adj}(M)=D I$ and Bézout's identity. Each residue class modulo $g$ contains $m/g$ choices for $w_c$. Only $(s-1)\bmod m$ weights occur at the higher frequency; under the displayed strict inequality there is a low choice making each right-hand side divisible by $g$.

Each used edge coset now contains $s$ weights with balanced frequencies. The omitted midpoint's coset contains $s-1$ balanced weights. If $s$ is divisible by $m$, the latter has just one deficiency from uniformity. Otherwise both local histograms have counts in $\{\lfloor s/m\rfloor,\lceil s/m\rceil\}$. This proves the global edge balance.

The same proof permits unequal piece orders $s_i$ in the coprime case. It suffices that all $s_i$ lie in one interval $[jm,(j+1)m]$, and that the row totals $s_i-\mathbf1_{i=r}$ all lie in one such interval, possibly with a different $j$. These are exactly the capacity conditions for balanced counts inside each vertex and edge coset to be globally balanced. In the singular case use the low-slot inequality at each active midpoint with its own $s_c$.

## What happens when three divides the factor?

Call the central piece $A$ and the end pieces $B,C$. Normalize their low labels to $0,1,2$, respectively. Write $a_B,a_C$ for the high labels at the two endpoints in $A$, and $b,c$ for the high labels at the connecting vertices in $B,C$. The appropriate internal low slots are $w_B,w_C$. The reduced matrix has diagonal entries 2 and off-diagonal entries $-1$.

At $3\mid m$, its two equations are solvable exactly when their right-hand sides agree modulo 3. Elimination gives a single equation with coefficient 3 and then one with coefficient 1. Since the carry at the edge $AB$ is $-1$ and at $AC$ is zero, the test is
$$
(a_B-a_C)+(b+w_B)-(c+w_C)=1\pmod3.
$$
One may negate each complete high labeling independently, including its chosen low slot, and exchange the low labels of $B$ and $C$. Thus translations, independent signs, choice of low slots and exchange of ends succeed if and only if one can make at least one of $a_B-a_C$, $b+w_B$, $c+w_C$ nonzero modulo 3. Indeed, changing one nonzero summand's sign permits a nonzero total, and exchanging the ends changes the total's sign. This implies the unconditional bound $(s-1)\bmod m<2m/3$ when $3\mid m$, since then a low-slot set cannot be confined to a single class modulo 3.

The obstruction can occur for this lift. Take three $m$-vertex stars, joining their centers along a three-vertex path, with $3\mid m$. In a bijective internal labeling of a star whose center is $z$, its missing weight is $2z$. Both center attachments in the middle coincide, and $z+2z=0\pmod3$ on either end. Thus no lift making each star monochromatic in a different low coset can be cordial. Any such lift at order $3m$ would induce bijective internal vertex labels and distinct internal weights on the three fibers. The resulting ordinary tree is a caterpillar. This identifies a limit of the partition construction, alongside the [obstructions for prescribed base labelings](cyclic-lifts.md).

## Checks

The checker compares the integer determinant to an independent enumeration of arrow choices, constructs the high translations, and tests the two full histograms, including zero counts. For one labeling of each of the 59 rooted quotient shapes on 3, 5 and 7 vertices, it verifies the arborescence count directly. It checks 2,944 equal-order and 2,901 variable-order lifts. At factors 3, 6 and 9 it independently tries translations, signs and end exchanges on 144 triples, finding 137 feasible and seven obstructed, in exact agreement with the three-piece criterion.

~~~sh
python3 -B -m research.check_odd_quotient
~~~
