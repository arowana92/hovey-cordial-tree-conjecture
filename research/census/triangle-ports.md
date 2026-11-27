# An eventual periodicity theorem for edge substitution

Fix a connected unicyclic graph $H$, a marked vertex and a chosen cycle edge. For each $k\ge |V(H)|$, add $k-|V(H)|$ leaves at the mark and open the cycle at the chosen edge. The set of moduli for which this gives a uniform insertion **at every pair of old endpoint labels is effectively eventually periodic**. The same holds for the existence of a harmonious labeling of the closed graph. The period, finite exceptional prefix and finite list of residue classes are computable from $H$.

In particular, for each fixed marked graph this decides whether the insertion works at every modulus above a specified threshold. It concerns an infinite family of extensions of arbitrary trees with one fixed inserted shape apart from its leaf population.

## Proof

Use the [fixed integer matrices](square-ports.md#a-fixed-matrix-decision-for-other-marked-graphs) for each partition and each weight matching. On a fixed congruence class modulo the least common multiple of all nonzero diagonal factors, each kernel size $K(M,k)$ is a constant times $k^{v-r}$. Appending the difference row increases the rational rank by zero or one. Thus the image of the old endpoint difference is either a subgroup of **fixed size** $b$ or a subgroup of **fixed index** $d$ on this congruence class. In the second case its size is a rational constant times $k$, and its reciprocal multiplier $d$ is a positive integer because the image is a subgroup for every such $k$.

Partition the possible differences by membership in this finite list of subgroups. On each membership pattern, the number of distinct-core assignments with weight matchings is a fixed polynomial in $k$, the signed sum of the contributing kernel polynomials. Its positivity stabilizes effectively, for instance by bounding the roots of each nonzero polynomial. The zero polynomial is handled separately.

It remains to decide which patterns contain a difference. Apply inclusion–exclusion to the forbidden subgroups along with the required ones. Intersecting index subgroups gives size $k/D$, where $D$ is the least common multiple of their indices, taking $D=1$ for an empty list. Intersecting also with size subgroups gives $\gcd(k/D,B)$, where $B$ is the gcd of their sizes. Refine the modulus of the progression by the products $DB$. The latter size is then constant and the former linear. Thus each pattern's population is affine on each refined progression. Positivity of that population stabilizes effectively too. The all-differences assertion fails precisely when an occupied pattern has zero witness count. This proves the theorem. For a closed graph there is no difference condition and only the sign of one polynomial per progression is needed.

## A triangle attached to the leaf parent

Take a triangle $xyz$, a fourth vertex $v$ adjacent to $x$, and $k-4$ new leaves at $v$. For **every** $k\ge4$ the exact all-differences decisions are as follows.

| Operation | Works at all old endpoint differences exactly when |
|---|---|
| Open $xy$ or $xz$ | $4\mid k$, or $6\mid k$, or $\gcd(k,30)=1$ |
| Open $yz$ | $4\mid k$ |
| Leave the cycle closed and require both bijections | $4\mid k$ |

For example, opening $xy$ gives a uniform insertion at any old edge at **every prime from seven onward**, even though the closed graph has no harmonious labeling at those primes. The construction preserves every old label and increases every count by one.

For the closed graph, normalize $v$ to zero and use $x,y,z$ also for the three labels. Cancel the leaves and the weight $x$. The remaining weights $x+y,y+z,z+x$ must be $0,y,z$. Their sum forces $2x+y+z=0$. The first and last weights are therefore opposites. If both were zero, they would repeat, so $y+z=0$ and $2x=0$. Thus $x=k/2$ is a nonzero involution and $2y=x$. Conversely these conditions with $z=-y$ give both bijections. They are possible precisely for $4\mid k$.

The two open cases follow from a finite symbolic computation. In both cases every fiber kernel has at most one free variable, so on each subgroup membership pattern the count is affine. The [progression checker](triangle_ports.py) splits into periods 60 for $xy$ and 300 for $yz$. It obtains the pattern population by subgroup inclusion–exclusion, and checks its value and slope exactly. On an eventually occupied pattern, the witness count has nonnegative slope; the code verifies this directly. On an increasing occupied pattern the second step has positive witness count whenever the witness slope is positive, since the first step has nonnegative count. Consequently steps zero, one and two decide positivity for the whole progression. The computed truth values equal the displayed divisibility criteria on every progression, including the starting values $k=4,5,6$.

A [second integer-matrix calculation](check_triangle_ports.py) uses inclusion–exclusion over the six forbidden equality pairs and recovers the invariant factors from gcds of minors. It reproduces every signed kernel term for all three cases, independently of the first calculation's row and column elimination. The [square calculation](square-ports.md) gives a different port classification using the same general decision procedure.

~~~sh
python3 -B -m research.census.triangle_ports
python3 -B -m research.census.check_triangle_ports
~~~
