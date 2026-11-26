# Attaching repeated rooted branches

**Theorem.** Let $B$ be any rooted tree of order $n\ge1$, and fix a vertex $a$ of any labeled graph. Attach $k$ disjoint copies of $B$ by joining each copy's root to $a$. For every positive modulus $k$, the old labeling extends so that the new vertices contribute exactly $n$ of each residue and the new edges contribute exactly $n$ of each residue. In particular, this operation preserves $k$-cordiality.

It suffices to construct the new labels when the old vertex has label zero. If its actual label is $b$, add $b$ to every constructed label. The new vertex labels shift by $b$ and every new edge weight shifts by $2b$, including the edges to the old vertex.

For **odd $k$**, number the copies by residues $i$ and label every vertex in copy $i$ with $i$. Each vertex position across the copies uses every residue once. So do the edges to the old vertex, with weight $i$, and each internal edge position, with weight $2i$. This includes $k=1$.

For **even $k$ and odd $n$**, use labels $i+c_w$ at position $w$ in copy $i$. Set the root offset to zero. Pair up the $n-1$ internal edge positions and prescribe the endpoint offset sums 0 and 1 on the two members of each pair. Starting from the root, subtract the parent's offset from the prescribed sum to get each child's offset. Across all copies, the two edges of a pair have weights $2i$ and $2i+1$. Each residue occurs twice. The edges to the old vertex contribute one of each residue and the $n$ vertex positions each contribute one of each.

## Even modulus and even branch order

Write $k=2h$, let $u$ be the root, and take $v\ne u$ whose degree in $B$ has the same parity as the degree of $u$. Such a vertex exists because the number of odd-degree vertices is even, and $n$ is even, so the number of even-degree vertices is even as well.

Construct two lists of offsets, $c^0$ and $c^1$. Use the labels $2i+c^e_w$ at position $w$ of copy $(e,i)$ for $e\in\{0,1\}$ and $0\le i<h$. In both lists make $u$ even and $v$ odd. Give every other vertex opposite parities in the two lists. Of the $2n$ vertex positions across the two lists, exactly $n$ are even and $n$ odd. Adding all $2i$ therefore produces exactly $n$ of each vertex label.

We can choose these parities so that exactly $n$ of the $2(n-1)$ internal edge positions across the two lists have odd endpoint sum. Put $d=\deg_B(u)+\deg_B(v)$ and let $\delta$ be 1 if $uv$ is an edge and 0 otherwise. An edge with exactly one endpoint in $\{u,v\}$ has odd sum in one list. The edge $uv$, when present, has odd sum in both. These edges contribute exactly $d$ odd positions. There are $n-1-d+\delta$ edges disjoint from $\{u,v\}$. Choose $(n-d)/2$ of them. This is possible since $n-d$ is even. If $\delta=1$, the available number is $n-d\ge0$. If $\delta=0$, it is $n-d-1\ge0$, which forces $n-d\ge2$. In the first list prescribe odd sums on the chosen edges and even sums on the other disjoint edges. The vertices outside $\{u,v\}$ induce a forest, so propagation from one vertex of each component realizes these prescriptions. Complementing all their vertex parities in the second list preserves their internal edge parities. The total number of odd internal positions is now $d+(n-d)=n$, and the number of even ones is $n-2$.

For each parity $\pi\in\{0,1\}$, pair the internal edge positions of that parity across the two lists. Within each pair prescribe the integer endpoint sums $\pi$ and $\pi+2$. Starting with $c^0_u=c^1_u=0$, solve separately along the two rooted copies for all integer offsets. The resulting offsets have the specified parities. A paired set of edges across its $h$ translations has weights $4i+\pi$ and $4i+\pi+2$. Together these give $2j+\pi$ for $0\le j<2h$, hence exactly two occurrences of every residue of parity $\pi$, also when $k=2$. Internal edges therefore supply $n$ of every odd residue and $n-2$ of every even residue. The two root positions have offset zero, so their edges to the old vertex supply the remaining two of each even residue. This proves the theorem.

## Consequence and verification

In a minimum-order counterexample at modulus $k$, no vertex has $k$ isomorphic incident rooted branches. Otherwise, removing those branches leaves a smaller tree containing the attachment vertex. Its cordial labeling extends by the theorem. The construction supplies a labeling from any given labeling of the smaller tree, even when a branch itself has no known cordial labeling.

The proof applies to arbitrary orders and moduli. The executable check below reconstructs both histograms directly from the edges for every rooted branch through order nine and every modulus through 24, using up to three attachment labels per case.

~~~sh
python3 -B -m research.repeated_branches
~~~

For odd $k$ the $k$ attached branches may even have different shapes, provided they all have the same order $n$. The constant labeling of each copy uses only its numbers of vertices and edges.
