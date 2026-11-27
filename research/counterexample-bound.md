# A size bound for a smallest counterexample

**Theorem.** Fix $k\ge 5$. If there is a tree with no $k$-cordial labeling, there is one on at most

$$
1+(k-2)(k-1)+2k(k-5)=3k^2-13k+3
$$

vertices. The bound concerns ordinary trees with freely chosen vertex labels. It gives a finite necessary and sufficient test at each fixed modulus. A proof uniform in $k$ still requires a way to exclude all the surviving trees or exhibit an obstruction.

### Removing leaves

Let $1\le t<k$ and give each of $t$ new leaves a prescribed parent label $b_i$. For any forbidden vertex residue $u$, the leaves can receive distinct labels different from $u$ while their new edge weights are all distinct.

To see this, pad the list of parent residues to length $k$ with sum zero. At least one padding position is available, so its value can cancel the sum of the others. Hall's theorem gives an enumeration $x_1,\ldots,x_k$ of the group such that $x_i+b_i$ also enumerate it. Keep the first $t$ entries. Choose an unused vertex residue $v$ and translate just the retained leaf labels by $u-v$. The omitted residue moves to $u$, and every retained edge weight moves by the same amount. This works because each new edge has exactly one new endpoint. [Marshall Hall Jr., *A combinatorial problem on abelian groups* (1952), pp. 584–587](https://doi.org/10.1090/S0002-9939-1952-0050579-7)

Now choose a counterexample of minimum order $n$. It has at least two vertices. If $n\equiv1\pmod k$ and $n>1$, delete a leaf. The smaller cordial core has a multiple of $k$ vertices and a unique deficient edge weight. Giving the leaf the unique label that produces that weight preserves cordiality. This excludes the residue class $1$.

Otherwise let $t$ be the least nonnegative residue of $n-1$ modulo $k$, so $1\le t\le k-1$. If the tree has at least $t$ leaves, delete $t$ original leaves simultaneously. Their parents survive since the retained core has positive order and the two-vertex case deletes only one leaf. The core has $mk+1$ vertices for some $m\ge0$. Its cordial labeling uses one vertex residue $m+1$ times and all others $m$ times. Every edge weight occurs $m$ times. Take the exceptional vertex residue as $u$ in the preceding construction. Adding the leaves preserves both balance conditions. Thus the number of leaves $L$ in a minimum counterexample satisfies

$$
L < (n-1)\bmod k \le k-1.
$$

At any modulus, writing $n=mk+s$ with $1\le s\le k$, the total leaf count at the two busiest parents must be less than $2s-k$. At primes $p$ the entire leaf count must be less than $2s-p-1$. [Leaf-list extension on a prescribed core](biased/spare-lists.md#restoring-leaves-on-a-cordial-core-of-arbitrary-order)

For any odd prime $p\ge5$ the order residue must satisfy $s\ge(p+7)/2$. A four-vertex forest excludes the first residue left by the leaf bound, with a five-vertex certificate at the exceptional prime 211. [List-coefficient proof and restrictions at 29](biased/star-lists.md)

### Shortening paths

All labels below are taken modulo $k$. A pendant path of $k$ new vertices extends any labeled core while adding one to every vertex and edge count. Write $a$ for its old endpoint label and set $b=a+\lfloor k/2\rfloor+1$. Along the path, starting at the old endpoint, label positions $2i$ by $a+i$ and positions $2i+1$ by $b+i$. The new even and odd positions together receive the residues $a+1,\ldots,a+k$ once each. The $j$-th edge, with positions numbered from zero and endpoints $j,j+1$, weighs $a+b+j$. It covers each residue once as $j$ runs from 0 to $k-1$. This is the endpoint-rooted path instance of the caterpillar construction. [Driscoll, Krop and Nguyen, Proposition 2.1](https://www.ejgta.org/index.php/ejgta/article/download/231/pdf_33)

An edge with arbitrarily prescribed endpoint labels $a,b$ can also be subdivided by $2k$ new vertices, adding two to every vertex and edge count. On the replacement path use the same alternating formula, now with $a,b$ taken directly from the original endpoints. Its last position $2k+1$ receives $b+k=b$. Its internal even positions receive $a+1,\ldots,a+k$, and its internal odd positions receive $b,\ldots,b+k-1$. The edge weights run from $a+b$ to $a+b+2k$. After subtracting the old edge of weight $a+b$, the net change is two of every residue.

For even $k$, a subdivision adding only $k$ vertices cannot give the same exact increment of one per residue to both histograms. Put $S=\sum_{x\in\mathbb Z/k\mathbb Z}x=k/2$ in the group. Summing the new edge weights counts endpoints once and internal labels twice, giving $a+b+2S$. The prescribed edge histogram would sum to $a+b+S$. Their equality would require $S=0$.

### Counting the remaining vertices

The [four-leaf construction](census/four-leaves.md) proves that a minimum counterexample has $L\ge5$ at every modulus. Suppress its vertices of degree two to form a tree with $L$ leaves and $B$ branching vertices. The degree-sum identity gives $\sum_{\deg(v)\ge3}(\deg(v)-2)=L-2$, hence $B\le L-2$. The suppressed tree has $L$ pendant edges and $B-1\le L-3$ edges between branching vertices.

Each pendant edge represents a path of length at most $k-1$ in the original tree. Otherwise delete its last $k$ vertices and use the first path construction to extend a labeling of the smaller tree. Each edge between branching vertices represents a path of length at most $2k$. A longer path has at least $2k$ internal vertices of degree two. Suppress $2k$ consecutive such vertices and apply the subdivision construction to restore them. Both reductions contradict minimality.

The number of edges is at most $L(k-1)+(L-3)2k$. Substituting $L\le k-2$ gives the stated bound. For example, at nine labels a smallest counterexample would have at most seven leaves and 129 vertices. Combining the four-leaf construction with $L\le k-2$ also excludes minimum counterexamples at every modulus from three through six.

### Odd moduli

For any odd $k$, subdivide an edge by $k$ vertices. If the first endpoint has label $a$, insert $a+1,\ldots,a+k$ in that order. The last new vertex has label $a$, so the last edge has the original edge weight. The first $k$ edges have weights $2a+2i+1$ for $0\le i<k$. Multiplication by two permutes the residues, so the net increment is one of each vertex label and one of each edge weight. Thus an internal segment of a minimum counterexample has length at most $k$ for these moduli.

For odd $k\ge5$ the order bound improves to $1+L(k-1)+(L-3)k\le 2k^2-8k+3$. At odd primes a star extension further improves the leaf bound. [Prime-modulus argument](rainbow/prime-star.md)
