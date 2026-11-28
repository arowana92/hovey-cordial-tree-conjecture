# Prescribing a full progression on a harmonious odd cycle

**Theorem.** Let $k\ge3$ be odd, let $a,d\in\mathbb Z_k$ with $d\ne0$, and write $h$ for the additive order of $d$. There is a cyclic ordering of all $k$ residues in which the consecutive sums, including the closing sum, also run through every residue, and whose first $h$ terms are
$$a,\ a+d,\ \ldots,\ a+(h-1)d.$$
In particular any two distinct residues can be prescribed in either order on a specified edge. The progression can occupy any specified run of $h$ consecutive vertices by rotating the cycle.

The unprescribed rainbow Hamilton cycle in the addition coloring of an odd abelian group is classical. The construction here specifies the consecutive vertices and gives a tree operation that preserves all old labels. [Akbari, Etesami, Mahini and Mahmoody, Theorem 8](https://ajc.maths.uq.edu.au/pdf/37/ajc_v37_p033.pdf)

## Construction

Put $m=\gcd(k,d)$. For $m=1$ take the progression itself as the full cycle. Otherwise $m=2t+1\ge3$ and $k=mh$. First construct the cycle for $(a,d)=(0,m)$. Visit the $m$ cosets of $m\mathbb Z_k$ in the order $i=0,\ldots,m-1$. In coset $i$ list
$$i,\ i+s_i,\ldots,i+(h-1)s_i,\qquad
s_i=\begin{cases}m&i<t,\\2m&i\ge t.\end{cases}$$
Both increments traverse the whole coset since $h$ is odd. In particular the first block contains the required progression. In a single block the successive edge weights have step $2s_i$ and occupy every residue of the weight coset $2i+m\mathbb Z_k$ except $2i-s_i$. These weight cosets are distinct because $m$ is odd.

Let $i'$ be the next coset representative, including the wrap from $m-1$ to zero. The bridge out of block $i$ weighs $i-s_i+i'$. Set
$$j=\begin{cases}i+t+1&i<t,\\i-t&i\ge t.\end{cases}$$
Then $i-s_i+i'=2j-s_j$ as integers. For $i<t$ the two sides equal $2i+1-m$. For $t\le i<m-1$ they equal $2i+1-2m$. At $i=m-1$ both equal $-m-1$. The map $i\mapsto j$ sends the first interval onto $t+1,\ldots,2t$ and the second onto $0,\ldots,t$. Thus the bridges supply every missing weight exactly once. [Lean check of the bridge identity and its unique recipient](CycleBlockEdges.lean)

Choose a unit $u$ modulo $k$ with $um=d$. Indeed $u$ must equal $d/m$ modulo $h$, where that residue is a unit. At any prime dividing $k$ but not $h$, also prescribe $u=1$ modulo that prime. The Chinese remainder theorem supplies $u$. Apply $x\mapsto a+ux$ to the cycle. This transforms both permutations bijectively and gives the prescribed progression.

## Moving branches along a path in a tree

Suppose a cordially labeled tree contains a path whose labels in order are an initial segment of the progression above, of length between two and $h$ vertices. Take a separate copy of the harmonious $k$-cycle with this same length of labeled path. Pick an edge of the old path and its matching edge in the copy. Delete both. Join each old endpoint to the copy of the opposite endpoint. At each vertex of the old path one may also transfer **any selection of its off-path branches** to the copy of that vertex, keeping every label.

The result is a tree. Removing the old edge leaves two components joined by the opened cycle. Each moved branch has a unique attachment and contains no old path vertex. The two joining edges both carry the common weight of the deleted edges. Every moved edge retains the labels at its ends. The inserted cycle therefore adds exactly one to every vertex and edge bin. This construction applies at every old order. In particular, one may start at any edge with unequal old endpoint labels. A properly labeled core stays proper, permitting iteration on any of its edges.

## Odd covers and odd abelian groups

For a harmonious cycle modulo $k$, form a cycle modulo $kD$ by traversing its order once per sheet $i=0,\ldots,D-1$, with $D$ odd. Use $x_v+k((i+b_v)\bmod D)$ at position $v$ of sheet $i$. The $b_v$ are arbitrary. On each base edge the high weight digit runs through $2i$ plus a constant including the carry and the possible sheet change at the closing edge. Thus any prescribed block of distinct low labels in the base cycle can receive **arbitrary chosen lifts** on the first sheet. Place the seam immediately before the block. The same fiber translations work on connected cyclic covers of a unicyclic graph after numbering along a spanning tree and putting its one sheet permutation in cyclic order. [Unicyclic covers](few-leaf-rings.md#odd-numbers-of-sheets)

The progression theorem also holds in every finite abelian group of odd order. For a direct product $A\times B$, suppose $A$ and $B$ have harmonious cyclic orders. Traverse the $A$ order once per element $z$ in the $B$ order, writing $(x_v,z+b_v)$ for the labels. At ordinary edges the second-coordinate sums are $2z$ plus a constant. At the seam they are $z+z_{\rm next}$ plus a constant. Both exhaust $B$. Again, shifts at the base positions allow arbitrary second coordinates along a chosen block in the first row. A trivial factor is allowed.

Decompose the group into cyclic prime-power factors. For each prime dividing the order of $d$, choose one factor on which its projected order has the largest power of that prime. The product $A$ of the chosen factors is cyclic, and the projection of $d$ to $A$ has exactly the order of $d$. The cyclic construction gives the full projected progression with distinct terms. The other factors form $B$, which admits a harmonious order by the ordinary odd-order result or by iterating the preceding direct-product construction on cyclic factors. Choose the shifts to give the desired $B$ coordinates on the entire progression.

The [constructor and independent frequency checks](cycle_progressions.py) test all 15,750 nonzero differences at odd orders through 251, 708 cyclic and direct-product lifts, and 992 complete trees with 884,845 transferred branches. Each tree check recomputes the endpoint sums after moving the branches.

~~~sh
python3 -B -m research.census.cycle_progressions
lean research/census/CycleBlockEdges.lean
~~~
