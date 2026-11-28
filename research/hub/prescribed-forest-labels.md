# Assigning a prescribed set of labels to a rooted forest

**Theorem.** Fix any modulus $k$, any rooted forest and a boundary residue for the parent of each root. Prescribe a multiset of vertex labels of the same size as the forest, with maximum multiplicity $D$. One can assign exactly those labels so that each edge weight occurs at most $2D$ times, counting every entering edge. This holds for forests of arbitrary size. In particular, any set of distinct inputs gives at most two edges per weight.

A factor of two can be necessary for distinct inputs at every $k\ge2$. Take $k$ singleton roots, with one parent of label 1 and all other parents of label 0. Use all $k$ residues as inputs. The sum of weights differs from the sum of all residues by one, so some weight repeats.

## Ordering the available vertices

At each residue $b$ place the total number $A_b$ of vertices in components entering from $b$. Let $B_b$ count the requested copies of $b$. The two totals agree. Rotate the cyclic order to start just after a minimum partial sum of the list $A_b-B_b$. In the rotated ranks $0,\ldots,k-1$, every initial interval has at least as much component mass as requested input multiplicity. Indeed a partial sum after rotation is the difference between an old partial sum and the minimum, including after wraparound since the old total is zero.

Initially all component roots are waiting, keyed by the rotated rank of their prescribed parent. Process requested ranks $x$ in nondecreasing order. Give $x$ to a waiting vertex with minimum parent rank $p$, and add its children with key $x$.

A vertex with $p\le x$ is always available. At the step for $x$, the components entering at ranks through $x$ have at least as many vertices as the number of requested labels through $x$. Fewer than that many vertices have been processed. In one such component choose a first unprocessed vertex on a path from its root. Its parent is either the prescribed boundary of rank at most $x$ or an already processed vertex of rank at most $x$. The selected minimum meets the same bound. Since every newly added key is $x\ge p$, the selected parent ranks never decrease.

The integer sums $x+p$ are therefore nondecreasing in $[0,2k-2]$. Repetition of an integer sum requires identical $x$ values and hence occurs at most $D$ times. Each modular weight has at most two representatives in the interval. Undoing the rank rotation translates every weight by the same constant. This gives the claimed assignment and a priority-queue algorithm.

## Keeping a fixed cordial core

Let a prescribed cordial tree have order $ak$, $a\ge1$. Attach a rooted forest of $r<k$ vertices at arbitrary old parents, and also provide pendant leaves. At **every modulus**, two available leaves per old parent label suffice to extend the original labeling, regardless of the shape or boundary labels of the forest. The two leaves at a given label may have the same physical parent. All of them may attach to the old core. All extra leaves can be retained.

If $r=0$, apply the usual divisible-order leaf extension. For $0<2r\le k$, choose a parent-first order of the forest. Use the first edge to fill the deficient old weight. At the $i$th subsequent assignment with $i$ forest vertices already labeled, avoid their $i$ inputs and the $i$ choices repeating a forest weight. Since $2i<k$, every step succeeds. The resulting core is cordial. Two leaves per shift suffice by the [prescribed-core pairing](sparse-leaf-sites.md#pairing-prescribed-vertex-and-edge-counts). At odd modulus even one per shift suffices in this range.

For $2r>k$, give the forest the input set $R=[0,r-1]$ by the theorem. Subtract $a-1$ from every core vertex and edge bin in the augmented core. The normalized vertex bins are two on $R$ and one on $X=[r,k-1]$. The normalized edge bins $M$ are nonnegative, at most three, and positive at all but at most one residue because of the old core. Each bin of size three uses at least two forest edges, so fewer than $r$ bins have that size. The [restricted-sum argument](two-private-leaves.md#completing-a-core-with-at-most-three-edges-per-weight) chooses $t=k-r$ distinct helper weights $Y$ avoiding all size-three bins. It places the forced deficiency $d=3\sigma-\sum_w wM_w-\sum Y$ at a bin of size at most one, where $\sigma$ is the sum of all residues. In unnormalized counts this equals $(a+2)\sigma-\sum(\text{weights before the helpers})-\sum Y$.

Pair each $x\in X$ with a $y\in Y$ and request one leaf at shift $y-x$. The residues $-x$ as $x$ ranges over $[r,k-1]$ are exactly $1,\ldots,t$. Apply the theorem of Kézdy and Snevily to the list $Y$ and these consecutive positions. Its hypothesis $2t\le k+1$ holds since $2r>k$. Thus the shifts $y-x$ can be made distinct at every modulus. Two leaves per old shift cover these helpers and leave a reserved batch of one leaf per shift. [Kézdy and Snevily, Theorem 2.5](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Kezdy/kezdy.pdf)

After assigning helpers, every vertex bin has size $a+1$. Every edge bin has size at most $a+2$, with strict inequality at $d$. The [uniform-parent criterion](breadth-first-leaves.md#an-exact-criterion-with-uniform-parent-colors) assigns the reserved batch, reaching order $(a+2)k$. Remaining leaves extend from that divisible order.

## Reduction to the modulus-sized tree case

**Corollary.** At any fixed $k$, assume that every tree on $k$ vertices has a bijective labeling with distinct weights modulo $k$. Then attaching at least two leaves at every vertex of **any** tree gives a $k$-cordial tree. In particular the [integer tree census](../census/README.md) gives the conclusion at 27, where the unrestricted conjecture is still open.

Write $h$ for the order of the original tree. For $h<k$ and final order at least $k$, keep the original tree and enough leaves to reach order $k$, then restore all other leaves. If the final order is below $k$, pad by leaves to order $k$ and restrict a bijective rainbow labeling. For $k\le h<2k$ take a connected $k$-vertex seed. Its rainbow labeling is cordial, and two leaves per original site meet the forest-extension hypotheses. In this range it is enough that one available seed have such a labeling. Only its $k$ vertices need the two leaves each. The other $r$ ordinary vertices may all have zero private leaves. For $h\ge2k$ the [unconditional breadth-first theorem](breadth-first-leaves.md) already applies. Consequently a smallest counterexample of order greater than $k$ cannot consist of a core with two or more leaves at every site. For such a counterexample all smaller trees already satisfy the needed base hypothesis.

## Verification

The [Lean file](ForestLabelQueue.lean) checks the rotation inequality, existence of a ready job under prefix dominance, preservation of dominance when its root is replaced by its children, and the impossibility of three distinct integer sums in the allowed range with the same residue. The mass of a waiting subtree is its number of unprocessed vertices. The forest interpretation and the cordial extension are proved above.

The [constructor and checker](prescribed_forest_labels.py) test 260,408 instances with distinct inputs, exhausting all parent-first forest descriptions with one through four vertices, up to the modulus, all boundary labels and all input sets through modulus seven. They also test 288 multiset instances, including sizes greater than the modulus. A further 117 constructions keep fixed divisible cores and use only two leaves per old shift at odd and even moduli. Another 152 start with interval-labeled prefixes of order $r+1$ and assign the remaining $k-1$ ordinary vertices by the forest theorem. Both checks attach actual leaves and recount all final bins, including zeros.

~~~bash
lean research/hub/ForestLabelQueue.lean
python3 -B -m research.hub.prescribed_forest_labels
~~~
