# Prescribing an independent offset on every edge

**Theorem.** Let $p\in\{2,3,5,7,11,13\}$. Given any finite tree and any assignment $b_e\in\mathbb F_p$ to its edges, there are vertex labels $f(v)$ such that the vertex labels and the edge weights
$$
f(v)+f(w)+b_{vw}
$$
both have residue counts differing pairwise by at most one. The offsets on adjacent edges may differ. Setting every offset to zero gives ordinary cordiality.

## Reduction to one order

At every modulus $k\ge2$, the assertion with arbitrary edge offsets at **order exactly $k$** implies the same assertion at all orders. At order $k$ it asks for a vertex bijection and distinct edge weights. A smaller tree can be padded to order $k$ and the labeling restricted.

For larger orders use strong induction. At order $1\bmod k$, remove a leaf. Its core has uniform vertex counts and one deficient edge weight. The unique leaf label that gives this weight, after including the prescribed offset, completes the tree.

Otherwise retain a connected subtree of order $1\bmod k$ with $1\le t\le k-1$ vertices outside it. Such a subtree is obtained by successive leaf removals until reaching that order. Label it by induction and translate all its vertex labels so its unique surplus vertex residue is zero. Its edge weights remain uniform because they all translate by the same amount. Each exterior component has a unique edge to the retained core. Join the roots of these components to a single new dummy vertex. Retain the internal offsets, and on a dummy edge put the old offset plus the label of the original parent in the core. Pad this tree of order $t+1$ to order $k$. Use a bijective rainbow labeling and translate it to put the dummy at zero. Its $t$ exterior labels are distinct and nonzero. Its $t$ exterior weights are distinct and agree with those obtained on attaching it to the real core. This restores balance and proves the reduction.

The prime assumption matters for this stronger question. For every composite $k$ take a proper divisor $1<s<k$. Join two vertices, give one $k-1-s$ leaf neighbors and the other $s-1$ leaf neighbors. Prescribe offset 1 on the joining edge and zero elsewhere. Normalize the first central label to zero, and call the other $x$. In a rainbow labeling $x$ would be the missing weight. Summing the weights once by their residues and once by their endpoints gives $sx=-1\pmod k$, impossible. The ordinary zero-offset instance is a caterpillar. [Full divisibility calculation](../rainbow/pinned-star.md)

## Signed counts and first moments

Root an order-$p$ tree at vertex 0. Normalize its label to zero, and index the other $r=p-1$ vertices so parents precede children. Write $x_0=0$, $D=\mathbb F_p^\times$, and $y_i=x_i+x_{\mathrm{parent}(i)}+b_i$. For a bijection $x$ of the nonroot vertices onto $D$ whose $y_i$ are distinct, let $w$ be its missing edge weight and $\epsilon$ the sign of the permutation $0\mapsto w,\ x_i\mapsto y_i$. For a polynomial $g$ in the vertex labels, define
$$
M_g(b)=\sum_{\text{such }x}\epsilon g(x)\quad\text{in }\mathbb F_p.
$$

**Degree lemma.** $M_g$ is represented by a polynomial in all the offsets of total degree at most $\deg(g)$.

Put $V(z)=\prod_{i<j}(z_j-z_i)$, $Q(z)=\prod_{v\in D}(z-v)$ and apply the grid sum
$$
L(F)=\sum_{x\in D^r}F(x)\Big/\prod_i Q'(x_i)
$$
to $F=V(x)V(y)g(x)$. Terms with repeated labels or repeated weights vanish. On every remaining term the denominator and $V(x)^2$ are fixed nonzero field elements. Prepending $0$ to the $x$ tuple or $w$ to the $y$ tuple multiplies each Vandermonde by the same product of all elements of $D$. The ratio of the enlarged Vandermondes is $\epsilon$, hence $L(F)$ is a fixed nonzero multiple of $M_g(b)$.

Univariate Lagrange interpolation gives $\sum_{v\in D} v^a/Q'(v)=0$ for $0\le a<r-1$. Every monomial in the $x$ variables of total degree below $r(r-1)$ has at least one such exponent. As $V(x)V(y)g(x)$ has total degree at most $r(r-1)+\deg(g)$ in $x,b$, each coefficient of a bias monomial above degree $\deg(g)$ is annihilated. This proves the lemma. [Boundary-only antecedent and grid formula](../rainbow/prime-star.md#a-signed-count-independent-of-the-boundary-modulo-p) · [Schauz, *Algebraically Solvable Problems*](https://www.combinatorics.org/ojs/index.php/eljc/article/view/734)

In particular the scalar $N=M_1$ is constant. For odd $p$, the first moments $M_{x_i}$ are homogeneous linear forms because at zero offsets negating all labels preserves the permutation sign and negates the moment. Let $A$ be their matrix. Outside $\ker A$, or for any tree with $N\ne0$, at least one rainbow labeling must exist. Subtracting a common constant from every offset translates all the edge weights. Multiplying all offsets and labels by one unit preserves distinctness. Thus one may first fix $b_1=0$, then test zero and one representative of each line in the remaining kernel. If this kernel has dimension $d$, the number of representatives including zero is $1+(p^d-1)/(p-1)$.

| Prime | Unrooted trees of order $p$ | Trees with zero scalar | Dimensions after fixing $b_1=0$ (dimension × number of trees) | Explicit witnesses |
| ---: | ---: | ---: | :--- | ---: |
| 2 | 1 | 0 | | 0 |
| 3 | 1 | 0 | | 0 |
| 5 | 3 | 0 | | 0 |
| 7 | 11 | 0 | | 0 |
| 11 | 235 | 30 | 0 × 24, 1 × 3, 2 × 3 | 69 |
| 13 | 1,301 | 96 | 0 × 77, 1 × 14, 2 × 4, 4 × 1 | 2,546 |

## Independent arithmetic check

The generator enumerates injective labels directly at zero and, when necessary, at each unit vector of offsets. It computes signs from inversions. The checker recomputes the moments by a different enumeration. It fixes one nonroot label to one, works entirely at **zero offsets**, and retains assignments with either distinct edge weights or a single pair of equal edge weights. Only these assignments can become rainbow when one weight changes. It obtains permutation signs by counting cycles.

For a rainbow assignment with missing weight $h$, changing edge $j$ of weight $a$ can only send it to $h$. After dilation by $(h-a)^{-1}$, offset one does exactly that. The output transposition reverses the sign, giving first-moment column contribution $-\epsilon x/(h-a)$. For the zero-offset scalar, the full dilation orbit contributes $(p-1)\epsilon$.

For a repeated weight $a$ on edges $j,l$ and missing weights $h,g$, let $s$ be the sign after moving edge $j$ to $h$ and sending zero to $g$. Moving it to $g$ interchanges two outputs. Repairing $l$ instead of $j$ interchanges two inputs. The combined contribution in column $j$ is $s x((h-a)^{-1}-(g-a)^{-1})$, with its negative in column $l$. These cases compute all unit-vector first moments without enumerating any biased tree.

The checker compares every recorded scalar and matrix entry, computes rank by elimination, and checks actual labels, parent sums and distinct projective representatives for every remaining kernel case. To verify unrooted coverage, it independently roots each input at every vertex, takes the least recursively sorted rooted representation, rejects duplicates and compares the total to the free-tree multiset/dissymmetry count. Together with the order reduction, these finite checks prove the theorem. [Direct counter](direction.cpp) · [Independent orbit counter](orbit_check.cpp) · [Certificate checks](verify.py)

## Consequences at other primes

* At **every prime**, every double star with arbitrary edge offsets is cordial. At order $p$, root it at one of its centers. The zero-offset signed scalar is $(p-1)(-1)^j j!(p-2-j)!$, where $j$ leaves are attached to the other center. This is nonzero, so the degree lemma covers all offsets. Smaller double stars can be padded with leaves. For larger ones retain an order-$p$ subtree containing the two centers. Add the other leaves in batches as in the census corollary, using each parent label plus its edge offset as the prescribed shift. Stars are included. [Star scalar calculation](../rainbow/prime-star.md#evaluating-the-star) · [Leaf batches](../census/README.md#an-unbounded-order-consequence)
* More generally, let all but at most four edges of a tree meet one vertex. At every prime except possibly $17,19,61$, arbitrary edge offsets are possible at every order. For $p\le13$ use the main theorem. At $p>13$ with $p\notin\{17,19,61\}$ the previously checked finite template theorem gives a nonzero **scalar** at zero offsets for every order-$p$ shape rooted at that vertex, after removing the root and recognizing at most four internal edges. The degree lemma applies to arbitrary offsets on all its edges. For larger orders, the union of the hub and its nontrivial off-hub components has at most nine vertices, so retain them all and enough hub leaves to reach $p$, then restore the remaining leaves in batches. Smaller orders can be padded at the hub. [Template integers and exceptional primes](../prime/README.md#finite-verification-for-four-edges)
* There is a simpler one-edge argument for larger primes. Suppose an order-$n$ tree has distinct vertex labels and distinct edge weights modulo a prime $p\ge n$. Given a nonzero offset $b$ at one prescribed edge with original weight $a$, choose any absent weight $w$. Scale all labels by $b/(w-a)$. The offset now sends the scaled edge weight to the scaled missing weight and all weights are distinct. This applies to every tree of order $n\le26$ at every prime $p\ge n$ by the integer census. [Census](../census/README.md)

## Reproduction

Use Python 3.8 or newer in normal assertion-enabled mode and a C++17 compiler. The verifier needs only the following shared library and the six compressed JSON-lines certificates in this directory. Each record gives the parent list, scalar, matrix by columns when needed, and explicit offset/label pairs.

~~~bash
set -e
src="$PWD/research/biased"
out=$(mktemp -d)
c++ -O3 -std=c++17 -fPIC -shared "$src/orbit_check.cpp" -o "$out/orbit.so"
python3 -B "$src/verify.py" "$out/orbit.so"
~~~

To regenerate all records independently of the distributed certificate files, continue in Bash from the repository root:

~~~bash
c++ -O3 -std=c++17 -fPIC -shared "$src/direction.cpp" -o "$out/direct.so"
c++ -O3 -std=c++17 research/census/{generate,interval}.cpp -o "$out/trees"
for p in 2 3 5 7 11 13; do
    "$out/trees" "$p" 0 1 "$out/tree$p.bin"
    python3 -B "$src/generate.py" "$p" "$out/direct.so" "$out/tree$p.bin" > "$out/p$p.jsonl"
    gzip -dc "$src/p$p.jsonl.gz" | cmp - "$out/p$p.jsonl"
done
~~~
