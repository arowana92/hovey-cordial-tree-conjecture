# An exact order test for diameter five

**Theorem.** Fix $k\ge1$. Every tree of diameter at most five is $k$-cordial if and only if every tree of **exact diameter five and order exactly $k$** has a bijective vertex labeling modulo $k$ with distinct edge sums. The diameter-four theorem handles every smaller diameter. [Diameter-four proof](all-radius-two.md)

Two unconditional conclusions hold for every modulus. Let $T$ have exact diameter five, order $n$, and $h$ nonleaf vertices. Then $T$ is $k$-cordial whenever $h\ge k$ or $n\ge 2k-h-1$. In particular, $n\ge2k-5$ always suffices.

**Finite application.** Every finite tree of diameter at most five is $k$-cordial for every $1\le k\le36$. For the moduli $21$ through $36$, the independent verifier checks 3,290,454 order-equals-modulus witnesses. The theorem gives the result at all tree orders. [All-tree results through twenty-one](../../README.md) · [Witness counts and stream digests](diameter-five-counts.txt)

Every tree whose branches at the two centers are single leaves or two-edge paths is super edge-magic. The numbers of branches of either kind at either center are unrestricted. [All partial subdivisions of double stars](subdivided-double-stars.md) · [Earlier matched-arm construction](matched-arms.md)

For equal numbers of branch parents on the two sides, every positive branch child count can be chosen independently. The integer construction also allows direct leaves at a center when their number is less than every branch child count on its side. [Two-center layer theorem](two-center-layers.md)

## Restoring one layer of leaves

At order $0\bmod k$, a cordial tree has uniform vertex counts and one deficient edge residue. Add one leaf with the vertex label that supplies that residue. The order is now $1\bmod k$, with a single surplus vertex residue and uniform edge counts. From this state, up to $k-1$ new leaves with parents already present can be assigned distinct vertex labels avoiding the surplus and distinct edge weights. For a batch of exactly $k$ leaves, do this for the first $k-1$, then fill the resulting edge deficiency with the last leaf. Full batches return to order $1\bmod k$. The partial-batch assertion follows by padding the list of parent shifts to a zero-sum list of length $k$, applying Hall's permutation theorem, then translating the retained leaf labels to avoid the surplus. [Hall, *A combinatorial problem on abelian groups*](https://doi.org/10.1090/S0002-9939-1952-0050579-7) · [Detailed leaf extension](../counterexample-bound.md#removing-leaves)

Delete all leaves of $T$ once, leaving the connected core $H$. Its $h$ vertices consist of the two adjacent centers and the neighbors of the centers with at least one child away from the central edge. Each center has at least one such neighbor on its side. Thus $H$ is a double star with $h-2$ leaves and is a caterpillar. Each of those $h-2$ leaves has at least one neighbor in $T-H$.

First suppose $h\ge k\ge2$. Write $h=ak+r$, $0\le r<k$. At $r=0$, label $H$ and restore the leaves as above. At $r=1$, temporarily remove one leaf of $H$, label the order-$ak$ caterpillar and restore the removed vertex first. All remaining vertices are now leaves at present parents.

For $r\ge2$, temporarily remove $r$ leaves of $H$, which exist since $h-2\ge k$. The remaining caterpillar of order $ak$ is $k$-cordial. Reattach one removed vertex using the deficient edge residue. Of the original leaves of $H$, exactly $h-2-(r-1)=ak-1$ are now present. Each offers at least one exterior leaf. In the next batch take the $r-1$ missing core vertices and $k-r+1$ exterior leaves at already present parents. There are enough since $ak-1\ge k-r+1$. This batch has size $k$ and completes $H$. All remaining vertices can be attached by full batches and a final partial batch. This proves the first unconditional assertion. A separate replay constructs all batches and recomputes both final histograms on 2,106 whole trees across the possible order remainders. [Restoration check](check_diameter_five_order.py)

Suppose $h<k$. If $n\ge k$ and one side of the central edge contains at least $k-h$ exterior leaves, include $k-h$ of them with $H$. Every vertex of this order-$k$ subtree is within distance two of the center on that side. Its diameter is at most four, so it is $k$-cordial. All missing vertices are leaves at parents in the subtree. This applies whenever $n-h\ge2(k-h)-1$ by the pigeonhole principle. Since $h\ge4$, it proves the claimed bound in terms of $n$ alone.

For the equivalence assume the stated order-$k$ test passes. When $h<k\le n$, select any $k-h$ exterior leaves with $H$. The resulting subtree has diameter at most five and thus has a bijective labeling with distinct sums by the test or the diameter-four theorem. Restore the other leaves. When $n<k$, first add leaves at a center up to order $k$. Restrict its labeling to $T$. All vertex labels and all edge weights remain individually distinct, which is sufficient at this order. Necessity of the test follows by taking $n=k$. At $k=1$ the unique residue labels the whole tree.

## A general form of the core argument

Let $T$ have any diameter and let its nonleaf core $H$ have order $h=ak+r\ge k$, $k\ge2$. For $r\ge2$, suppose $H$ has $\ell\ge r$ leaves. Omit the $r-1$ leaves of $H$ with the fewest exterior neighbors, together with any one additional leaf of $H$. If this trimmed core is $k$-cordial and the vertices other than the first $r-1$ omitted leaves of $H$ have at least $k-r+1$ exterior leaves in total, the same two batches label $T$. The additional omitted vertex comes back first. In particular the supply condition is automatic when $\ell\ge k$.

For example, in exact diameter six, $H$ has diameter at most four, so the trimmed core is always cordial. Here $h\le2\ell+1$. Root $H$ at a radius-two center and charge each of its branching neighbors to a different leaf child. It follows that $h\ge2k$ suffices at any order. If $k\le h<2k$, then $n\ge2h-1$ also suffices. Indeed $r=h-k$ and $\ell\ge(h-1)/2\ge r$. At least the fraction $(\ell-r+1)/\ell$ of the exterior leaves are available after the first restoration, because the $r-1$ omitted terminal populations are the smallest and all interior populations remain available. For $n-h\ge h-1$ and $r\ge2$ this gives at least $(h-1)-2(r-1)=k-r+1$ leaves. The cases $r=0,1$ use the simpler restoration above.

## Exhausting the order-$k$ test

Deleting the unique central edge leaves two rooted trees of height exactly two. On each side a child of its center contributes a branch of size $j\ge1$, consisting of that child and $j-1$ leaves. Thus a side is precisely an integer partition containing some part at least two. Conversely every unordered pair of such partitions with total size $k-2$ gives one isomorphism type of exact diameter five.

The generator lists these pairs, keeps a permutation of the $k$ vertex residues, and swaps labels to remove repeated edge sums. A failed search yields no mathematical conclusion. The verifier uses only positive witnesses. It checks the canonical ordering of the two partitions, rejects duplicate or out-of-order records, recomputes every central, branch and leaf edge directly, and requires all $k-1$ sums to be distinct. It obtains the required total without generating any trees. If $P(j)$ is the number of partitions of $j$, there are $P(j)-1$ admissible sides of size $j\ge2$. For unequal sizes multiply the two side counts. For equal sizes with $b$ possible sides use $b(b+1)/2$. This independent count and the strict record order establish completeness. [Generator](diameter_five_generate.py) · [Permutation search](diameter_five_search.cpp) · [Independent verifier](diameter_five_verify.py)

Run the restoration check independently with standard Python.

~~~sh
python3 -B -m research.hub.check_diameter_five_order
~~~

A record contains one byte for the number of parts on side one, one byte per part, the analogous data for side two, then one byte for each vertex residue. Vertex order is the two centers followed by the branches for side one and those for side two, with each branch parent before its children. The witness stream need not be retained. Reproduce the full check from the repository root in Bash or Zsh.

~~~sh
set -o pipefail
c++ -O3 -std=c++17 -shared -fPIC research/hub/diameter_five_search.cpp -o /tmp/hovey-diameter-five.so
for k in $(seq 21 36); do
    python3 research/hub/diameter_five_generate.py "$k" /tmp/hovey-diameter-five.so |
        python3 research/hub/diameter_five_verify.py "$k" || exit 1
done > /tmp/hovey-diameter-five-counts.txt
diff research/hub/diameter-five-counts.txt /tmp/hovey-diameter-five-counts.txt
~~~
