# Prescribing labels at separated vertices

**Two prescribed vertices.** At eight labels, let two vertices of a tree be at distance at least 121. Any assignment to them extends to an 8-cordial labeling, with one exception: the tree is the path between them, its order is one modulo eight, and the two prescribed residues have opposite parity. At nine labels every assignment extends at distance at least 154. The two labels may coincide.

**Any number of prescribed vertices.** At nine labels, any assignment on a set of pairwise distances at least 307 extends. At eight labels, pairwise distances at least 241 suffice whenever the tree order is different from one modulo eight or the tree has an unprescribed leaf. If the order is one modulo eight and every odd-degree vertex is prescribed, extension is possible exactly when the sum of the prescribed labels on odd-degree vertices is even. The distance bounds are sufficient. The many-vertex statement leaves open the case at eight with all leaves prescribed, some unprescribed odd-degree vertex, and order one modulo eight.

The assertions concern a single labeling of the entire tree with the original endpoint-sum rule. The finite ingredients below also give exact results at short distances.

## Joining two independently labeled trees

Let $k=8$ or $9$. Take two prescribed cordial trees of positive orders divisible by $k$, with missing edge bins $D,E$ (one below the other bins). Join vertices labeled $a,b$ by a path containing $t$ new internal vertices. The following conditions are necessary and sufficient to retain both old labelings.

| Internal vertices | Condition |
|---|---|
| $t=0$ | $a+b$ equals $D$ or $E$ |
| $t=1$ | $b-a=\pm(E-D)$ |
| $t=2$ | All cases except $a=b$ and $D=E=2a$ |
| $t\ge3$, $k=9$ | All cases |
| $t\ge3$, $k=8$ | All cases except $t\equiv1\pmod8$ with $a+b-D-E$ odd |

Subtract the uniform old vertex counts and the uniform part of the old edge counts. The new vertices must themselves have a balanced histogram. The $t+1$ path-edge frequencies, minus one at $D$ and one at $E$, must form a balanced histogram of total $t-1$. This gives the first two rows. In the excluded case at $t=2$, translate $a=b$ to zero. With distinct internal labels $u,v$, at least two of $u,u+v,v$ would have to vanish. That would force $u=v=0$. At $k=8$ and $t=8q+1$, the actual sum of the path-edge weights is $a+b+2\sum x$, summing over internal labels. The required sum is $q\sum\mathbb Z_8+D+E$. Comparing parities proves the stated obstruction.

The [finite constructor](bridge_pins.py) tries each balanced vertex histogram and final edge histogram for $0\le t\le k+2$. It enforces the exact sum identity and searches the remaining multisets in path order. The [checker](check_bridge_pins.py) realizes every possible ordered $(a,b,D,E)$ on two actual trees of order $k$, assembles each supplied walk and recomputes both frequency lists. It checks the short negative cases by direct enumeration. For larger $t$, subdivide one path edge by as many whole periods as needed. This preserves the old labels at both moduli and every old order. [Period subdivision theorem](../census/period-subdivision.md)

## Cutting a tree with prescribed labels

At both moduli any labeling on a connected divisible-order core extends across every outside forest. Thus it suffices to label the smallest subtree $H$ containing the prescribed vertices, enlarged by at most $k-1$ vertices to the next multiple of $k$. Stop at the whole tree if it runs out sooner, and call the resulting tree $C$. With one pin, translate an ordinary cordial labeling. [Eight-label divisible-core theorem](README.md#the-extension-lemma) · [Nine-label divisible-core theorem](../rainbow/surplus-nine.md#divisible-cores)

Put $L=2k^2-k+1$. With two pins, their path has length at least $L$. With more pins at mutual distance at least $2L-1$, the hull $H$ contains a path segment of length at least $L$ with no pin or branching vertex in its interior. If $H$ is a path, take consecutive pins. Otherwise root $H$ at a leaf, and take a farthest branching vertex. Two downward directions are nonbranching paths to leaves, which are prescribed by minimality of the hull. Take the nearest pin in each direction. Their distances from the branching vertex sum to at least $2L-1$, so one is at least $L$. Every edge of the resulting segment separates two nonempty sets of pins.

Write $r=|C|\bmod k$. Use a bridge of length measured in internal vertices $t=k+r$ for $r\in\{0,1,2\}$, and $t=r$ otherwise. In the segment interior, mark each site with an attachment in $C-H$. At divisible order there are at most $k-1$ such sites. If every clean run had length at most $2k-2$, the segment interior would have at most $(k-1)+k(2k-2)=L-2$ vertices. Hence one run has at least $t+k-1$ vertices when $r=0$. At nondivisible order at most $k-2$ vertices have been added to $H$, since the targeted multiple would have required at most $k-1$ additions and was not reached. With at most $k-2$ marked sites, runs of length at most $2k$ would give at most $k-2+(k-1)2k=L-3$ interior vertices. Again one clean run has length at least $t+k-1$.

Among the first $k$ possible starts in this run, choose one with a multiple of $k$ vertices strictly to its left. Moving the start by one adds exactly one vertex to that side. Cut out the next $t$ internal vertices. Both remaining components are nonempty and divisible in order, and both contain fewer pins than before. Their inherited distances are unchanged. This proves the divisible-order result by induction on the number of pins, using the unconditional $t=k$ bridge. The same cut in the nondivisible case uses the proved divisible-order result on its two sides. [Lean proof of the clean-run estimate and alignment](SeparatedPins.lean)

At nine labels every joining profile works. At eight, the only outstanding residue is $r=1$. This can arise only if $C=H$ is the whole original tree: the first order above a smaller multiple of eight is already one modulo eight. Thus all its leaves are pinned. On a divisible side with port label $a$ and deficient weight $D$, the parity of $D$ is the sum of labels at its odd-degree vertices, by counting all edge weights at their endpoints. The connector adds one incidence at each port, and its internal vertices have degree two. Hence $D+E-a-b$ has the parity of the label sum at the original odd-degree vertices. When all these labels are fixed, this proves sufficiency of the parity test. Uniform final edge counts force the same parity to be even, proving necessity. With just two pins the entire hull is their path and they are its only odd-degree vertices.

## Short distances and paths

For the distances below, these are exactly the differences $y-x$ that extend on **every** tree having the two specified vertices at that distance. An empty set means every candidate difference fails on some tree.

| Distance | Eight labels | Nine labels |
|---:|---|---|
| 1 | Empty | Empty |
| 2 | Odd | Units modulo nine |
| 3 | Empty | Units modulo nine |
| 4 | All except 0 and 4 | Units modulo nine |
| 5, 6 | All except 0 and 4 | All nonzero |
| 7 | All nonzero | All nonzero |
| 8 | | All nonzero |

More generally, for any prescribed pattern whose connected hull fits in $k$ vertices, universality is equivalent to extendibility in each tree of order $k$ containing that pattern. Necessity follows by using those trees. For sufficiency, enlarge the hull to order $k$ inside a larger tree and use the divisible-core theorem. For a smaller tree, pad to order $k$ and restrict its injective, rainbow labeling. At both moduli every particular assignment on a specified three-vertex path fails in some order-$k$ tree. These obstructions require fixed labels.

On a path itself, the endpoint differences are all nonzero at orders $2$ through $k$. At every larger order they are arbitrary for nine labels. For eight labels they are arbitrary except at orders $8q+1$, where they must be even. At order nine they must also be nonzero: equal endpoints would be the sole repeated residue $x$ and the actual edge sum would be $2(\sum\mathbb Z_8+x)-2x=0$ modulo eight, against the required sum 4. Complete short witnesses through order $2k+1$ and period subdivision prove sufficiency at all orders. In particular, at distance $7\bmod8$ or $8\bmod9$ the path itself is a divisible-order core, and the path result extends immediately to arbitrary surrounding trees.

## Reproduction

~~~sh
python3 -B -m research.eight.check_bridge_pins
python3 -B -m research.eight.check_separated_pins
lean research/eight/SeparatedPins.lean
~~~

The first calculation enumerates the 23 and 47 unrooted bases by canonicalizing every parent-before-child array. It checks 644 and 1,692 marked pairs and 226 and 545 marked three-vertex paths. For the bridge table it verifies 36,664 positive ordered inputs at eight and 68,355 at nine. The second [independent enumeration and whole-tree check](check_separated_pins.py) starts instead from multisets of rooted trees, fixes the first mark at the root and prunes edge collisions as vertices are assigned. All 115 and 286 rooted bases reproduce the short-distance conclusions. The [whole-tree constructor](separated_pins.py) was also replayed on 112 complete trees totaling 59,426 vertices, including several nonterminal pins, repeated prescribed residues, and branching in the hull. Three additional inputs failed the necessary parity test.
