# Prescribing a path's surplus and the label of any marked vertex

**Theorem.** Let $k$ be odd and let a path have $qk+1$ vertices with $q\ge1$. Fix any vertex and any two residues $x,y$. There is a labeling with uniform edge counts, a single surplus vertex residue $x$, and label $y$ at the chosen vertex. At every modulus $k\ge2$ the same conclusion holds whenever the path order is at least $12k/p+13$, where $p$ is the least prime divisor of $k$.

**Extension of a fixed core.** Attach such a path by an edge at any vertex of a cordially labeled tree of any order, with any prescribed joining offset $b$. Choose a minimum-frequency vertex bin $x$ and a minimum-frequency edge bin $w$ of the core. If the old parent label is $c$, prescribe path surplus $x$ and marked label $w-b-c$. The old labels stay fixed. Each histogram receives $q$ copies of every residue and one copy of its chosen minimum bin.

More generally, replace each vertex of an arbitrary tree by a path meeting the theorem's hypotheses for the same $k$. For every quotient edge, choose its two attachment sites independently, even when several sites lie in one piece. The resulting tree is $k$-cordial and arbitrary offsets on the joining edges are allowed. In fact the surplus of each piece and the weight of every joining edge can all be prescribed independently. Root the quotient and process parents before children. The known parent label determines the one mark requested from each new path. Taking a balanced sequence of surpluses and another balanced sequence of bridge weights proves the assertion.

## Constructing the path

Use the within-class path ranks of an $\alpha$-labeling in sum form. The rank sums along its edges are consecutive. Stacking its two class intervals gives consecutive integer vertex labels beginning at zero and consecutive edge sums. At an order $1\bmod k$ their residues have surplus zero and uniform edge counts. Translation prescribes the surplus $x$. Multiplication by a unit lets the mark attain every residue with the same gcd with $k$ as its constructed value, before translation. This follows by lifting a unit modulo $k/g$ to a unit modulo $k$, where $g$ is that gcd. The Chinese remainder theorem gives such a lift prime power by prime power. [Path rank constructions and the endpoint lemma](four-leaves.md#paths-with-a-specified-rank)

At order $N\ge12k/p+13$, place the marked class first. For a nonzero target difference $y-x$, prescribe rank $g=\gcd(y-x,k)\le k/p$ at the mark. The exact marked-rank theorem applies because $N\ge12g+13$. For target difference zero prescribe rank zero. Rosa's sole rank-zero exception is the middle of a five-vertex path. These constructions settle the long-path assertion. [Rosa's path theorem, restated as Theorem 2.1 by Panpa, Imnang and Wasuanankul](https://doi.org/10.1155/jama/5826777)

Now let $k\ge3$ be odd. It suffices to treat order $k+1$. If the distances of the mark to the tips are $a,b$, remove multiples of $k$ vertices at each tip until the two remaining distances sum to $k$. When both are divisible by $k$, keep $k$ vertices on a nonempty side. After solving the smaller problem, [uniform endpoint path blocks](../counterexample-bound.md#shortening-paths) restore both tips, leaving the label of the mark and the surplus unchanged.

At order $k+1$ the two classes both have size $B=(k+1)/2$. Putting the marked class below or above realizes rank $z$ as the label $z$ or $B+z$. Rank zero is always available here, giving differences zero and $B$, which is a unit. For any remaining target gcd $g$, write $g=2h+1\ge3$ and $d=k/g\ge3$. A mark of rank $g$ placed below works directly. A mark of rank $h$ placed above gives $B+h=(k+g)/2$, also of gcd $g$ since $d$ is odd. When $k+1\ge12h+13$, the exact rank theorem supplies $h$.

It remains to handle $k+1<12h+13$, equivalently $(d-6)g<6$. Thus $d=3,5$, or $d=7$ and $g=3,5$. The following joins settle all three cases. Assume $a\le b$, $a+b=k$. A path on $n$ vertices has endpoint rank $z$ and opposite endpoint deficiency $z$ whenever $0\le2z<n$ and either $z=0$ or $n\ne4z+1$. Call this condition usable. Joining paths adds the earlier block's two class widths to the later ranks and succeeds when the first endpoint deficiency equals the next starting rank. Write $W_m$ for the staircase with ranks $\lfloor i/2\rfloor$.

- To put rank $z$ at the mark, take the first $a+1$ vertices with endpoint rank $z$ at the mark. Its deficiency there is $\lfloor a/2\rfloor-z$. Join a block of order $b$ starting at that deficiency. The same construction works from the other end.
- Alternatively take $a$ vertices ending with deficiency $z-\lfloor a/2\rfloor$. Join a block of order $b+1$ starting at the same rank. Its first vertex is the mark and its class offset is $\lfloor a/2\rfloor$.
- Start with the reversed staircase of order $m=a+2z+1$ or $a+2z+2$. Its mark has rank $z$ and its final deficiency is $\lfloor(m-1)/2\rfloor$. A usable endpoint at that rank on the remaining $k+1-m$ vertices completes the path.

The [Lean inequalities](SurplusMark.lean) show that for $d=5$ and both remaining $d=7$ cases these joins give $h$ or $g$. For $d=3$ they give $h$ except possibly when $h=3j$ and $a=4j+1$. Here $j\ge1$ and the path order is $18j+4$. Join a path of order $4j$ starting at rank $j$, the reversed staircase of order $2j+2$, and a path of order $12j+2$ starting at rank $j$. Every bridge has matching rank and deficiency $j$. The mark is the second vertex of the middle block. Its local rank $j$ and the first block's class offset $2j$ give $h=3j$. This completes the proof. Modulus one is immediate.

The two prescriptions can conflict at even moduli. When $4\mid k$, take a path with $k+1$ vertices and surplus zero. Write $S=k/2$ for the sum of all residues. Uniform edge counts require the endpoint labels to sum to $S$, by summing the endpoint contributions over all internal edges. Prescribing $k/4$ at one endpoint would force both endpoints to have that same nonzero label, which occurs only once. This is an obstruction to a prescribed labeling of a path. Ordinary paths are cordial.

## Other pieces of order one modulo the modulus

For an ordinary cordial piece of order $qk+1$, let $u$ be its surplus residue and let its joining vertex have label $a$. The possible differences after affine changes are exactly the unit orbit of $a-u$. Translation then permits any requested surplus.

At a prime $p$, if $a\ne u$, this piece extends any cordially labeled core by one edge. When the old order is $r\ne0\bmod p$ there are $p-r$ possible minimum vertex bins and $p-r+1$ minimum edge bins. Thus a pair $x,w$ with $w-c-b-x\ne0$ exists. At order zero there are $p$ possible vertex bins. If $a=u$, the piece has exactly the effect of an ordinary leaf upon translation, apart from uniform increments. Consequently a minimum ordinary counterexample at a prime has **no edge separating a proper component of order $1\bmod p$ larger than one**. For $a\ne u$ extend the smaller complement. For $a=u$ first replace the component by a single leaf, label the smaller tree and expand that leaf. [Divisible components](../divisible-cuts.md)

More generally, a unit difference $a-u$ suffices at any $k$ when the core order residue $r$ satisfies $0\le r\le k-k/p$. For $r>0$ the possible vertex choices $X$ and the translated edge choices $Y$ have sizes $k-r,k-r+1$. Sets of cardinalities at least $k/p$ and greater than $k/p$, respectively, contain a cross-pair of unit difference. To see this, average a function over the neighbors at unit difference. Modulo a prime power $v^j$ this operator averages over all the other residue classes modulo $v$. It has eigenvalue one on constants, $-1/(v-1)$ on centered functions of the class, and zero on functions of mean zero inside each class. By the Chinese remainder theorem the operator at $k$ is a tensor product, so its norm on mean-zero functions is at most $1/(p-1)$. If the two sets have no unit cross-pair, applying Cauchy–Schwarz to their centered indicators gives $(p-1)^2AB\le(1-A)(1-B)$ for their densities $A,B$. The stated sizes contradict this inequality. For $r=0$ one can choose any vertex bin.

## Reproduction

~~~sh
lean research/census/SurplusMark.lean
python3 -B -m research.census.check_prescribed_path_surplus
~~~

The [constructor](prescribed_path_surplus.py) builds the path. A [separate check](check_prescribed_path_surplus.py) recomputes both histograms and the marked label for 74,892 pairs, including every mark and target difference at order $k+1$ for every odd $k$ through 73. It also checks 172,595 neighbor sets, 2,000 full-tree joins and 400 trees assembled with independent bridge offsets at arbitrary attachment sites.
