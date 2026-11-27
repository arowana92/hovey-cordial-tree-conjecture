# One extra leaf at any vertex of a caterpillar

**Theorem.** Add a leaf at any chosen vertex of any caterpillar. Every resulting tree is $k$-cordial for every positive integer $k$. In particular the new leaf may be attached to an old leaf in the middle of the caterpillar. Spine length, degrees and modulus are unrestricted. The proof gives a direct construction at the order-equals-modulus and harmonious orders as well as at all other orders.

## A labeling at every multiple of the modulus

Represent the original caterpillar $C$ by its spine and its pendant leaves. List the edges in spine order, taking the leaves of each spine vertex between the incoming and outgoing spine edges. The first edge uses a new vertex in each bipartition class. Each subsequent edge keeps one endpoint of the preceding edge and introduces the next vertex of the other class. Number each class by order of first occurrence, starting at zero. The resulting edge pairs form a monotone lattice path from $(0,0)$ to $(a-1,b-1)$ with unit steps, where $a,b$ are the class sizes. This also covers a path or star. [Hovey's caterpillar theorem](https://doi.org/10.1016/0012-365X(91)90254-Y) · [Staircase construction](../hub/all-radius-two.md#1-removing-the-dependence-on-branch-sizes)

Call the selected vertex's class $B$ and its rank $y$. Put $n=a+b+1$, including the new leaf. Choose a position
$$
r=\begin{cases} b-y,&2y<b,\\ b-1-y,&2y\ge b.\end{cases}
$$
Insert the new leaf into the *numeric* block of $B$ at $r$. This puts its parent at rank $y'=y+[y\ge r]$, and $r+y'=b$. Give $A$ the integer labels $0,\ldots,a-1$ and the enlarged block the labels $a,\ldots,n-1$. These are a bijection on the actual tree.

After subtracting $a$ from the weights, the original edges had sums $0,1,\ldots,a+b-2$ in order. Inserting the slot increases precisely a suffix of these sums by one. Thus the old weights occupy $[0,n-2]$ with one integer missing, allowing the empty or full suffix. The new edge has normalized weight $a+r+y'=n-1$. Together the normalized weights occupy **$[0,n-1]$ with one hole**. If $k\mid n$, reduction gives uniform vertex counts and exactly one deficient weight. If $k\ge n$, all the vertex labels and all the edge weights are individually distinct. A one-vertex starting caterpillar is immediate.

## An extension at a single shared vertex

**Lemma.** Let a cordial core have order divisible by $k$ and deficient edge residue $d$. Attach a tree $F$ with $1\le t\le k$ edges at one shared vertex. Suppose $F$ has an $\alpha$-labeling in which the shared vertex has extreme rank in its own class. The labeling extends cordially for its actual prescribed label $c$ in the core.

Use within-class ranks with all edge rank sums $0,\ldots,t-1$. Reverse both rank lists if necessary to put rank zero at the shared vertex. Write $a,b$ for the two class sizes with that vertex in the first class. Give the classes labels $c+i$ and $c+z+j$ modulo $k$ respectively. Let $D$ be the representative of $d-2c$ in $[a,k+a-1]$ and put $z=\min(D,k-b+1)$. Since $a+b-1=t\le k$, the free vertex representatives after subtracting $c$ occupy the disjoint intervals $[1,a-1]$ and $[z,z+b-1]\subseteq[a,k]$. They are distinct modulo $k$, including if the representative $k$ occurs. The $t$ new weights form the cyclic interval $2c+z+[0,t-1]$. It contains $d$ since $0\le D-z<t$. Adding these two injective histograms balances both totals. At $t=k$ both increments are uniform, so this particular attachment preserves any cordial core regardless of its order.

An endpoint of the spine of a caterpillar has extreme rank in its class, even with leaves attached there. Use the staircase ordering above. Thus this lemma applies whenever a pendant caterpillar can be cut off at such an endpoint. In particular, at order $n>k$ with $t=n\bmod k>0$, a minimum counterexample cannot have a pendant caterpillar from which one can take exactly $t$ edges in this way.

## Cutting at an arbitrary order

An extra leaf at a spine vertex keeps the tree a caterpillar. In the remaining case the tree consists of a spine, ordinary leaves on that spine, and a two-edge arm $v,w,u$ off a spine vertex $v$. Include neither of the two arm edges among the ordinary leaves. Let $L,R$ be the edge counts strictly allocated to the left and right arms from $v$, counting the first edge to the adjacent spine vertex and all ordinary leaves at other spine vertices on that side. Write $p$ for the number of ordinary leaves at $v$. Then $n=L+R+p+3$.

Every edge count from zero through $L+p$ can be removed from the left as a caterpillar sharing one spine endpoint with the remainder. Start at the far end and take that vertex's ordinary leaves, then the next spine edge. Repeat, taking only the requested number of leaves at the last vertex reached. At $v$ take only ordinary leaves. The last vertex is retained in the remainder, which is again a caterpillar with the one extra leaf. The right side gives every count through $R+p$.

For $n>k$ with $t=n\bmod k>0$, take such a tail with $t$ edges if possible. The remainder has order $n-t$ divisible by $k$, so the integer construction above labels it. The single-vertex lemma restores the actual tail at its actual joint.

If neither side suffices, then $L+p,R+p\le t-1$. Thus $k+t\le n\le2t+1-p$ with $t<k$, forcing $t=k-1$, $p=0$, $L=R=k-2$, and $n=2k-1$. For $k\ge3$, add a twin to an ordinary leaf of $C$ different from $w$. Such a leaf exists in this case. Order it and its twin consecutively among the leaves at their parent, using the nonleaf path as the spine if needed. Apply the integer construction at order $2k$. These two leaves have ranks differing by one before the insertion, and by at most two afterwards. They therefore have distinct weights modulo $k$. At least one avoids the sole deficient weight. Remove that one, interchanging the indistinguishable leaves if necessary. Uniform vertex counts drop in just one bin. The edge histogram loses one from a full bin, so it too remains balanced. At $k=2$ the exceptional order is three, a path. This completes the proof.

## Checks

The direct checker recomputes frequencies from the original spine, its stated leaf populations and the extra two-edge arm, including every unused residue. It checked 28,409 whole-tree instances across all four construction cases. It also verified 4,556 single-joint extensions with independently prescribed root label and deficient weight. Lean checks the image of inserting a slot into an integer interval, the reflected choice of $r$, the translation interval and the exceptional-order arithmetic. [Constructor](caterpillar_leaf.py) · [Whole-tree verifier](check_caterpillar_leaf.py) · [Lean lemmas](StaircaseLeaf.lean)

~~~sh
python3 -B -m research.census.check_caterpillar_leaf
lean research/census/StaircaseLeaf.lean
~~~
