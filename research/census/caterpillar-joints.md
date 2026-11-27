# Attaching a caterpillar at any prescribed vertex

**Theorem.** Let $T$ have a $k$-cordial labeling and order divisible by $k$. Identify any vertex of $T$ with any vertex of a caterpillar $F$ with $1\le t<k$ edges. The labeling of $T$ extends to a cordial labeling of the union. The joint may lie internally on the spine or on a pendant leaf off the spine.

Write $c$ for its label and $d$ for the unique deficient edge weight of $T$. If the core has order $qk$, all vertex counts are $q$, and the edge counts are $q$ except for $q-1$ at $d$. It therefore suffices that the $t$ new vertices have distinct labels, that $d$ occurs once or twice among the new edges, and that every other weight occurs at most once.

## The interval construction

Enumerate caterpillar edges in spine order, listing each spine vertex's pendant edges between its incoming and outgoing spine edges. Number the vertices of each bipartition class by first appearance, starting at zero. Each edge after the first uses one vertex of the previous edge and the next vertex of its own class. Thus the rank pairs $(i,j)$ visit a monotone unit-step path from $(0,0)$ to $(a-1,b-1)$, one pair per edge. In particular $i+j$ runs from $0$ to $t-1$, where $t=a+b-1$.

Put the joint in the first class, let its rank be $x$, and put $p=c-x$. Give the two classes labels $p+i$ and $p+z+j$ modulo $k$. For $a\le z\le k-b$ even the joint is distinct from all free labels. The normalized weights (subtracting $2p$) occupy $z+[0,t-1]$. Over these starts their union is $[a,k+a-2]$, containing every residue except $a-1$. If $x=0$ we can also take $z=k-b+1$, since the only possible repetition is the joint's label at a free vertex. This covers the last residue as well.

These interval claims use only the distinct rank sums of an $\alpha$-labeling. For any such labeling, the sole possibly uncovered deficit satisfies $d-2c\equiv a-1-2x\pmod{k}$. Reversing both within-class orders changes the right side to its negative. Hence any rooted $\alpha$-labeled tree with $t<k$ admits the extension unless the two right sides coincide and equal $d-2c$. Extreme rank in either direction already suffices, even for $t=k$. [Extreme-rank lemma](caterpillar-leaf.md#an-extension-at-a-single-shared-vertex)

## The remaining residue on a caterpillar

Suppose $x>0$ and $d-2p\equiv a-1$. Start at $z=a$. The vertex representatives before adding $p$ are the integers $[0,t]$. Subtract $2p+a$ from the weights so their positions in edge order are $0,\ldots,t-1$ and the desired deficit is $-1$.

If $t\le k-2$, move the vertex of first-class rank zero from $0$ to $-1$. Its edges form a nonempty initial block of the staircase. Only this block shifts down by one. The resulting positions are strictly increasing in $[-1,t-1]$ and include $-1$. The new vertex residue was free and the joint keeps rank $x$.

If $t=k-1$, swap the labels of the first-class vertex of rank zero and the second-class vertex of rank $b-1$. Their original representatives are $0$ and $k-1$, and neither is the joint. Edges incident **only** to the first vertex form an initial block. Edges incident **only** to the second form a final block. If the two vertices are adjacent, their common edge is the last edge in the first row and the first edge in the last column, and its weight is unchanged. The initial block moves down one position, the final block moves up one modulo $k$, and all middle positions stay fixed. The resulting integer positions are strictly increasing in $[-1,k-1]$. The only possible modular collision is between the endpoints, both equal to the deficient residue after translation. At least one block is nonempty. Otherwise the two extreme vertices would form an isolated edge, impossible in a connected tree with $a\ge2$. Thus $d$ occurs, completing the proof.

**Consequence for a smallest counterexample.** If its order is $qk+r$ with $q\ge1$ and $0<r<k$, it cannot admit a split at one vertex with a caterpillar on exactly $r$ edges on one side. The smaller tree would be cordial by minimality and the theorem would restore that entire side with the prescribed joint label.

**Limitation at $t=k$.** A uniform increment on both vertices and edges can be impossible at an internal joint. Take the four-edge path rooted at its midpoint modulo four. Translate the root to zero. The four free labels must permute the four residues. Call the neighbor labels $a,b$ and the two tip labels $u,v$, with $u$ adjacent to $a$. If the weights are uniform, their sum agrees with the sum of the four free labels modulo four, so $a+b=0$. Their distinctness forces $\{a,b\}=\{1,3\}$ and $\{u,v\}=\{0,2\}$. Then $a+u$ and $b+v$ are odd, just like $a,b$, contradicting uniformity. This concerns a prescribed increment. The path itself is cordial.

## Verification

The checker independently builds the original edge set, keeps the complete supplied core labeling fixed, and adds the new endpoint sums to a histogram with the prescribed deficient bin. Across 207,470 tests the new edges hit that bin once in 202,620 cases and twice in 4,850 cases. Cases include every joint, root label and deficient weight on small caterpillars, including the tight order $t=k-1$. The checker also enumerates all 24 assignments in the path obstruction. Lean verifies strict increase and the only possible modular collision in the two-block step. [Constructor](caterpillar_joint.py) · [Independent checker](check_caterpillar_joint.py) · [Lean lemmas](StaircaseLeaf.lean)

~~~sh
python3 -B -m research.census.check_caterpillar_joint
lean research/census/StaircaseLeaf.lean
~~~
