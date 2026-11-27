# A full modular block at a joint with two branching neighbors

**Theorem.** Suppose a given $k$-cordial core has order divisible by $k$. Attach a caterpillar with at most three nonleaf vertices, at any one of its vertices. Its size is unrestricted. The original core labels extend. In the tight case of $k$ new vertices, there are infinitely many rooted caterpillars for which the weight increment must depend on the core's deficient weight.

## The full block at the middle vertex

Normalize the joint's label to zero by translation. Write $d$ for the core's deficient weight after this translation. Give its two spine neighbors $a,b$ leaf children, respectively, and let $p$ ordinary leaves meet the joint directly. Here $k=2+a+b+p$. A full block must use each residue once on the free vertices. Its new weights may use each residue once, or repeat $d$ while omitting another residue. Either possibility gives a cordial extension.

Take $b\le a$ by exchanging the sides. Give the larger center label zero, and the smaller center label $y\in\{1,-1\}$. Outside the smaller center's children, every new edge has its child's label. Give those $b$ children the set
$$
S=\{d-jy:1\le j\le b\}.
$$
If this avoids $0,y$, assign all remaining free labels arbitrarily. The weights on $S$ translate it by $y$, replacing its first position $d-by$ by $d$. For $b=0$ the increment is uniform. For $d=0$ either sign works. Otherwise choose the sign making the representative of $dy$ at least $k/2$. Avoidance holds if that representative is at least $b+2$. Since $2b\le k-2$, the only outstanding case is $k=2s$, $a=b=s-1$, $p=0$ and $d=s$.

For odd $s$, use centers $0,s$ and give the children at $s$ any $(s-1)/2$ pairs $\{i,i+s\}$ outside $\{0,s\}$. Translation by $s$ permutes these child labels. All increments are uniform.

For even $s$, use centers $1,s$. Give the $s-1$ children at $1$ the set
$$
A=\{s+1+j(1-s):0\le j<s-1\}\pmod{2s}.
$$
Give all other available labels to the children at $s$. The step $1-s$ is a unit modulo $2s$. Starting at $s+1$, it reaches $s$ at step $s-1$ and $1$ at step $s$. Hence $A$ avoids both centers. Subtract $s$ from all child-edge weights. This replaces $A$ by $A+(1-s)$ in the full child label set, exchanging $s+1$ for $s$. The resulting child-edge set omits $1$ and $s+1$, as does its translate by $s$. The two center edges weigh $1,s$. In the whole block $s$ repeats and $s+1$ is missing.

## Exactly when uniform increments are possible without direct leaves

Let $p=0$. A labeling with both increments uniform exists **if and only if**
$$
\gcd(a,k)>1\quad\text{or}\quad\gcd(b,k)>1 .
$$
The zero-labeled free vertex must be a center. A zero-labeled grandchild would repeat its parent's weight, already used by the edge to the joint. Give the other center a nonzero label $y$. Only its children's weights differ from their labels, so their set must be invariant under addition of $y$. Its cardinality must be divisible by the additive order of $y$, a divisor of $k$ greater than one.

Conversely, if $g=\gcd(b,k)>1$, use $y=k/g$ and select $b/g$ entire cosets of $\langle y\rangle$ away from the zero coset. These are available since $b<k$, and avoid both centers. The rest of the labels go to the other children. Exchange sides for the other gcd. In particular, at every prime $k\ge5$, every positive split $a+b=k-2$ gives an obstruction to a uniform increment at the joint. The full-block construction still extends over every deficient weight.

## Other joints and arbitrary size

A useful bridge rule works for any two cordial trees. If the core has order divisible by $k$, translate the new tree's labels so the new joining edge fills the core's unique deficient weight. Then the core and bridge contribute uniform edge counts, and the core contributes uniform vertex counts. The union is cordial for any order of the new tree. If instead the **new** tree has order divisible by $k$, its entire increment can be made uniform at any labeled parent $c$. If its root label and its missing weight are $y,m$, translate its labels by $z=c+y-m$. Then the new edge weighs $c+y+z=m+2z$. This rule also holds if an edge has a fixed additive offset, by including that offset in the equation for $z$.

A caterpillar attached at a leaf is covered at every size by the bridge rule, since deleting the shared leaf leaves a caterpillar. A joint at the end of the nonleaf spine has extreme rank. For $t\le k$ edges the [extreme-rank extension](caterpillar-leaf.md#an-extension-at-a-single-shared-vertex) applies there. At any joint with $t<k$ use the [short attachment theorem](caterpillar-joints.md).

For an arbitrary caterpillar with at most three nonleaf vertices and $t\ge k\ge3$, choose a connected $k$-edge subtree containing the joint and every nonleaf vertex. Their connecting subtree uses at most three edges. Enlarge to size $k$ one edge at a time. A nonleaf joint is either at a spine end or at the middle of a three-vertex spine. In the latter case apply the full-block construction, allowing zero children at either retained neighbor. If the prefix has fewer than two neighbors of the joint, the leaf or spine-end rule applies. All omitted vertices are leaves with their parent already present. After the block the labeled tree again has order divisible by $k$. Add a leaf to fill its deficient weight, then up to $k-1$ leaves using Hall's partial permutation extension. Repeat the batches. At $k=2$ one can label any rooted extension in connected order, alternately filling the deficient weight and avoiding the surplus vertex label. The modulus one is immediate. [Leaf batches and Hall's theorem](../counterexample-bound.md#removing-leaves)

## Verification

The checker rebuilds the original tree for each split, verifies the complete permutation on free vertices, and recomputes both histograms including the old deficient bin. It checked 618,332 prescribed full blocks at moduli through 47. It found 568 uniform constructions and 513 arithmetic exclusions for splits with no ordinary leaves. A separate exhaustive subset search confirmed the exact gcd criterion on all 66 splits through modulus 12. [Constructions](two_branch_joint.py) · [Verifier](check_two_branch_joint.py)

~~~sh
python3 -B -m research.census.check_two_branch_joint
~~~
