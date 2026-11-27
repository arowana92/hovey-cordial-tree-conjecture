# Which offsets may be assigned independently on every tree?

Let $A$ be a nonempty set of residues modulo $k$. Give every edge an independent choice $b_e\in A$, and give it weight $f(u)+f(v)+b_e$. Call $A$ admissible if every finite tree has a cordial labeling for every such assignment. Translating all of $A$ by a constant preserves admissibility because every edge weight translates by that constant.

**Theorem.** The following table characterizes all admissible sets for $1\le k\le15$.

| Modulus | Necessary and sufficient condition on $A$ |
| :--- | :--- |
| 1, 2, 3, 5, 7, 11, 13 | Every nonempty set works |
| 4 | All elements agree modulo 2 |
| 8 | All elements agree modulo 4 |
| 9 | All elements agree modulo 3 |
| 6, 10, 12, 14, 15 | $A$ has one element |

In particular, at eight labels a different choice between $0$ and $4$ can be prescribed on **every edge of every tree**. At nine labels the choices are $0,3,6$. Ordinary cordiality is the single-offset case. The nonconstant positive results at prime powers use the finite checks below.

## Obstructions at every composite modulus

Take two offsets in $A$ whose difference is $b$, and subtract the first from every edge. For every proper divisor $1<s<k$, the order-$k$ double star with $s-1$ leaves on one side and $k-1-s$ on the other can accommodate offset $b$ on its central edge and zero elsewhere only if $s\mid b$. Indeed, normalize the label at the second center to zero and let $x$ be the other central label. When $b\ne0$, $x$ must be the missing weight. Summing the $k-1$ distinct weights gives $sx=-b\pmod k$. [Double-star calculation](../rainbow/pinned-star.md)

Consequently every difference in $A-A$ must be divisible by the least common multiple of the proper divisors of $k$. For $k=p^a$, $a\ge2$, this is $k/p$. For $k$ with at least two distinct prime factors, the proper divisors $k/p$ as $p$ varies over those factors already have least common multiple $k$. Thus at any such mixed modulus a nonconstant set fails, with an explicit ordinary tree and a single changed edge. A singleton works exactly when ordinary Hovey cordiality holds at that modulus. The ordinary proofs cover the mixed moduli in the table. For prime moduli in the table use the [arbitrary-offset theorem](README.md).

## A sufficient finite test for cosets of a subgroup

Normalize the coset to the subgroup $m\mathbb Z/k\mathbb Z$ with $k=mp$. The argument here only needs $p$ integral. Encode a forest of $k-1$ free vertices by its rooted components and by a low boundary label in $\mathbb Z/m\mathbb Z$ for each root, represented by an integer in $[0,m-1]$. On an internal edge start with the sum of the free endpoints. On a root edge start with the root label plus its prescribed low boundary label. Test a bijection of the free vertices to the nonzero residues modulo $k$ with distinct weights, after adding arbitrary independent multiples of $m$ to **all** $k-1$ edges.

Use the following low boundary inputs for each shape.

1. Include the all-zero low boundary on every shape. This supplies the order-$k$ base for every allowed edge-offset vector, by labeling its root zero.
2. If the forest has at most $\lfloor2(k-2)/3\rfloor$ terminals, sort components by order. Allow a change of boundary label at a component when its size is at least the total preceding size plus the number of preceding constant-color runs. Equivalently this condition holds at the start of every run after the first. Tied sizes cannot change color.

These hypotheses suffice at all orders for $k\ge4$. To see this, consider a smallest failing tree with allowed offsets. Below order $k$, pad and restrict a base labeling. At order $1\bmod k$, restore one leaf to fill the uniquely deficient weight. Otherwise write the order $ak+1+t$, $1\le t<k$. If there are at least $t$ leaves, delete $t$ simultaneously and restore them with distinct labels avoiding the core surplus and distinct new edge weights. The prescribed shifts in Hall's leaf lemma incorporate their edge offsets, so a smallest counterexample has fewer than $t$ leaves. [Leaf lemma](../counterexample-bound.md#removing-leaves)

As in the [ordered-cut argument](../rainbow/ordered-cut.md), split at a leaf centroid. Take the smaller of two seed subtrees that share only the centroid and each contain at least one third of the leaves. Extend it to order $ak+1$ by a preorder with child subtrees in nondecreasing order of size. At most $\lfloor2(k-2)/3\rfloor$ terminals remain outside. The exterior components attach to the visited ancestor path. When a new group starts farther up the path, its smallest component has at least the preceding component mass plus the number of preceding boundary parents, by the child-size order. This implies the run condition for any coloring of those parents, including their labels reduced modulo $m$.

Translate the core labeling to make its sole surplus vertex label zero. Edge weights stay uniform under the common translation. Every exterior parent edge has effective shift equal to the core parent label plus its prescribed offset; its low digit is exactly the specified boundary color. All other freedom at the boundaries is covered by the independent multiples of $m$. When $t<k-1$, extend a largest component at a terminal by a path to order $k-1$, keeping the terminal count and run conditions. Restrict the tested labeling to the actual exterior. Its $t$ distinct nonzero labels extend the core vertex counts, and its $t$ distinct weights extend the uniform edge counts. This contradicts failure.

## Certificates at four, eight and nine labels

| $k$ | $m$ | Rooted shapes | Shape/low-boundary inputs | Inputs including all high offsets | Witness rows |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 4 | 2 | 4 | 5 | 40 | 13 |
| 8 | 4 | 115 | 916 | 117,248 | 17,881 |
| 9 | 3 | 286 | 1,190 | 7,807,590 | 188,842 |

The generator tries uncovered high-offset vectors, obtains a labeling by injective depth-first search and marks every high-offset vector on which that labeling gives distinct weights. A certificate row stores the parents and a list of vertex permutations packed in four-bit digits. A negative parent $-1-c$ denotes an external parent of low color $c$.

The independent checker reconstructs canonical unordered forest shapes. It verifies validity of the low runs, excludes duplicated low patterns, and uses multiset recurrences both for the total number of rooted shapes and, separately, the number of low patterns needed per shape. Each witness must be a permutation of $1,\ldots,k-1$. For its baseline edge weights $w_i$, a pair of edges can collide only when $m\mid w_j-w_i$. In that event, with independent digits $d_i,d_j\in\mathbb Z/p\mathbb Z$, the collision is exactly
$$
d_i-d_j=(w_j-w_i)/m\pmod p.
$$
The checker removes each of those digit assignments using bit sets and requires the union over the stored permutations to be the entire set of $p^{k-1}$ assignments. It uses no search code. Negative controls rejected a repeated vertex label, a missing cover and a deleted low input. [Generator](power_generate.py) · [Witness search](power_search.cpp) · [Independent checker](power_verify.py)

Run from the repository root with assertion-enabled Python 3. Verification needs only the committed archives.

~~~sh
python3 -B -m research.biased.power_verify
~~~

To reproduce every record with a C++17 compiler, run

~~~sh
set -e
src="$PWD/research/biased"
out=$(mktemp -d)
c++ -O3 -std=c++17 "$src/power_search.cpp" -o "$out/search"
for k in 4 8 9; do
    python3 -B "$src/power_generate.py" "$out/search" "$k" > "$out/$k.jsonl"
    gzip -dc "$src/power$k.jsonl.gz" | cmp - "$out/$k.jsonl"
done
~~~
