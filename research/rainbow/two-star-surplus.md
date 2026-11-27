# Two stars on a core with one surplus vertex label

**Theorem.** At every prime modulus, take a fixed cordial labeling of a core of order zero or one modulo the prime. Attach two stars by their centers at any prescribed old vertices. For **every prescribed parent-first order** of the added vertices, one labeling extending the core is cordial on every prefix.

At every modulus, two stars attached at sites carrying the **same label** extend an old labeling of either of those two orders. Any number of direct leaves at sites of the same label may also be included. From order one modulo the modulus, some parent-first order keeps every prefix cordial. From divisible order the same holds if there is a direct leaf in addition to the stars. For two stars alone at divisible order the [previous prefix criterion](two-star-growth.md) decides whether such an order exists.

At composite moduli a one-surplus core can obstruct even the final labeling. A divisor test settles **every modulus** when one parent carries the surplus. At odd prime powers all those inputs extend. The complete classification for arbitrary parents is also available at **twice every odd prime**. [General surplus-site criterion](surplus-site.md) [Classification and concrete obstructed sizes at 26](surplus-antipodes.md)

## A quadratic decision procedure

Let the modulus be $k$, normalize the surplus vertex label to zero, and consider star orders $s,t\ge1$ with $s+t=k-1$. Denote the old parent labels by $a,b$, the respective new centers by $x,y$, and let $h=x-y$. The new vertices must use exactly the nonzero residues. The new edge sums must be distinct, omitting one residue $W$. Summing them gives
$$
W=-a-b-(s-1)x-(t-1)y .
$$
The weight $x+y$ cannot occur on a leaf edge because the opposite center already uses the required leaf label. Unless $y=a$ or $x=b$, it follows that $W=x+y$, hence $y=a+b+sh$. Thus each nonzero $h$ has at most three candidates for $y$. The [Lean theorem](TwoStarPacket.lean) checks the missing-weight and moment implication on lists of actual labels and endpoint sums.

Let $B$ be the $s-1$ labels on the first star's leaves. The condition on actual edge weights is equivalent to
$$
 (\tau^h-1)1_B=e_0+e_x+e_y-e_{a+h}-e_b-e_{W-y},\qquad
 B\cap\{0,x,y\}=\varnothing . \tag{1}
$$
Indeed, subtract $y$ from each weight. Begin with all residues, remove $0,x,y$, translate the leaves in $B$ by $h$, and insert the two entering weights $a+h,b$. Requiring the result to omit $W-y$ gives (1). Integrate the right side along the cycles of adding $h$. Each cycle must sum to zero. Its successive indicator values are fixed up to a constant, which is constrained by the prescribed zeros and the range $\{0,1\}$. Any optional increase adds the entire cycle. All cycles have the same length, so their attainable total sizes form an arithmetic progression. This takes $O(k)$ arithmetic operations per candidate and $O(k^2)$ in total. An accepted indicator gives both stars' labels directly.

## Two intervals supply the prime construction

For a unit $h$ take $y=a$, $x=a+h$ and write all positions in units of $h$. Put $A=a/h$ in $[1,k-2]$. Use as first-star leaves the last $l$ positions before $A$ and the last $r$ before zero, with $l+r=s-1$. These intervals avoid $0,A,A+1$ provided
$$
 0\le l\le A-1,\qquad 0\le r\le k-A-2 .
$$
The two translates end at $A,0$ and remove the starting positions $A-l,-r$, with empty intervals cancelling their endpoints. Equation (1) therefore holds if $b/h$ equals either start. The other start is the normalized missing weight after subtracting $y$. This reasoning works at every modulus where the chosen $h$ is a unit.

* If $a,b$ are nonzero, distinct, and $a-b$ is a unit, first suppose $s,t\ge2$. Take $h=a-b$, so $b/h=A-1$ and $2\le A\le k-1$. Use $l=1$, $r=s-2$ whenever $A\le k-s$. Otherwise interchange the stars and negate $h$. The new position is $k+1-A\le k-t$, since $s+t=k-1$, and the same choice works. For a singleton first star use $x=b-a,y=b$. Its edge supplies $y$ and the other center edge supplies $x+y$, both holes in the remaining leaf weights. This singleton construction works for any distinct nonzero $a,b$.
* If $a\ne0$, $b=0$ and both $a,s$ are units, take $h=a/s$, giving $A=s$. Choose $l=s-1,r=0$. Exchange the stars if the zero parent occurs first.
* If $a=b\ne0$, take the smaller star first. Choose $h=1$ or $-1$ so that $1\le A\le\lfloor k/2\rfloor$. Take $l=0,r=s-1$; the bound on $s$ ensures enough room. If $a=b=0$, adjoin a virtual parent zero to both centers. This tree is a caterpillar. Its consecutive vertex labels and consecutive edge sums give a rainbow labeling modulo $k$; translate its virtual parent to zero and delete it. [Caterpillar rank construction](../hub/all-radius-two.md#1-removing-the-dependence-on-branch-sizes)

These cases cover every input at an odd prime. A shorter pair can be padded by leaves at either center to size $k-1$, then restricted. For a prescribed order, first fill the deficient edge bin if the core has divisible order. Starting at order one modulo the prime, each batch of up to $k-1$ vertices gets distinct labels avoiding the surplus and distinct entering weights. If a batch contains both fresh centers and both have children in it, they and their children form precisely the two stars just handled. Indeed neither center arrived earlier, and every vertex of the original attachment belongs to one of these stars. In every other case at most one fresh vertex has children in the batch. The [one-center prime theorem](prime-star.md) handles the resulting star and singleton leaves with any prescribed parents. Follow each completed batch with the single forced deficit-filling vertex and repeat. Every prefix of a rainbow batch is cordial. At two labels a rainbow batch has at most one vertex, so the same conclusion follows directly.

## Common labels, arbitrary modulus and arbitrary sizes

Start on a one-surplus core. In a batch of $k-1$ vertices include both centers if available and $k\ge3$. Other vertices may be direct leaves at the common old label. At a nonzero normalized site treat these leaves as children of the larger star, keeping its center at $y=a$, as in the equal-parent interval construction. Moving the leaves back leaves all their weights unchanged. At the zero site the virtual-parent caterpillar already includes these direct leaves. Pad a short batch at one star and restrict. For a larger attachment, choose the first batch to include both centers. Every remaining vertex is a leaf with a prescribed parent. At divisible order fill the edge deficit on the first leaf, then apply [Hall's partial permutation lemma](../counterexample-bound.md#removing-leaves) to the following at most $k-1$ leaves and repeat. This gives the claimed prefix growth. Modulus one is immediate, and two uses one-vertex batches.

From a divisible core with a direct leaf, put that leaf first and use the preceding construction. For two stars alone the [divisible-core theorem](two-star-extension.md) covers sizes with $s+t\ne k$. To cover $s+t=k$, normalize the common old parent to zero and let $D$ be the deficient edge weight. If $\gcd(s,k)\mid D$ the prefix construction already applies. Otherwise take $s\le k/2$ and choose $h=1$ or $-1$ so $D/h>s$ in coordinates $0,\ldots,k-1$. This choice can fail only for $D=0$ or $D=s=k/2$, both already covered. Put the centers at $h,0$, and take the $s-1$ first-star leaf positions immediately before $D/h$ in units of $h$. They avoid positions zero and one. Their translate difference is $e_D-e_{D-(s-1)h}$, exactly the required [divisible-core identity](two-star-extension.md#one-full-period) at equal parents.

## Verification

The [constructor](two_star_surplus.py) uses the explicit formulas above and solves (1) on remaining inputs. An [independent exact search](check_surplus_pairs.cpp) tries every ordered pair of centers. It blocks their two actual entering weights and assigns each remaining label to either star. With step $h=x-y$, putting label $z$ on the first star and $z+h$ on the second causes the only possible cross-star leaf collision. A cyclic two-choice recurrence computes all attainable first-star sizes while enforcing the entering-edge exclusions. This search uses neither the moment nor equation (1). The [whole-tree replay](check_two_star_surplus.py) compares the two decisions, checks all labels on actual stars attached to a cordial core, tests the antipodal divisor criterion, and exhausts small inputs by literal subsets. The two decisions agree on 494,323 inputs, including 1,085 failures. The replay also checks 1,456 literal searches, 930 antipodal inputs, 81,313 inputs with one parent at the surplus, and 122,760 common-site packets with direct leaves. A further replay checks 29,010 intermediate prefixes of 2,280 prescribed interleavings at primes through 97.

~~~sh
out=$(mktemp -d)
c++ -std=c++17 -O3 research/rainbow/check_surplus_pairs.cpp -o "$out/check"
python3 -B -m research.rainbow.check_two_star_surplus "$out/check"
python3 -B -m research.rainbow.check_two_star_extension
lean research/rainbow/TwoStarPacket.lean
~~~
