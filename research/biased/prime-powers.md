# Which offsets may be assigned independently on every tree?

Let $A$ be a nonempty set of residues modulo $k$. Give every edge an independent choice $b_e\in A$, and give it weight $f(u)+f(v)+b_e$. Call $A$ admissible if every finite tree has a cordial labeling for every such assignment. Translating all of $A$ by a constant preserves admissibility because every edge weight translates by that constant.

**Theorem.** The following table characterizes all admissible sets for $1\le k\le16$ and at $k=18,20,21,22$.

| Modulus | Necessary and sufficient condition on $A$ |
| :--- | :--- |
| 1, 2, 3, 5, 7, 11, 13 | Every nonempty set works |
| 4 | All elements agree modulo 2 |
| 8 | All elements agree modulo 4 |
| 9 | All elements agree modulo 3 |
| 16 | All elements agree modulo 8 |
| 6, 10, 12, 14, 15, 18, 20, 21, 22, 24 | $A$ has one element |

In particular, at eight labels a different choice between $0$ and $4$ can be prescribed on **every edge of every tree**. At nine labels the choices are $0,3,6$, and at sixteen they are $0,8$. Ordinary cordiality is the single-offset case. The nonconstant positive results at prime powers use the finite checks below.

## Obstructions at every composite modulus

Take two offsets in $A$ whose difference is $b$, and subtract the first from every edge. For every proper divisor $1<s<k$, the order-$k$ double star with $s-1$ leaves on one side and $k-1-s$ on the other can accommodate offset $b$ on its central edge and zero elsewhere only if $s\mid b$. Indeed, normalize the label at the second center to zero and let $x$ be the other central label. When $b\ne0$, $x$ must be the missing weight. Summing the $k-1$ distinct weights gives $sx=-b\pmod k$. [Double-star calculation](../rainbow/pinned-star.md)

Consequently every difference in $A-A$ must be divisible by the least common multiple of the proper divisors of $k$. For $k=p^a$, $a\ge2$, this is $k/p$. For $k$ with at least two distinct prime factors, the proper divisors $k/p$ as $p$ varies over those factors already have least common multiple $k$. Thus at any such mixed modulus a nonconstant set fails, with an explicit ordinary tree and a single changed edge. A singleton works exactly when ordinary Hovey cordiality holds at that modulus. The ordinary proofs cover the mixed moduli in the table, including [24 labels](../rainbow/twenty-four.md). For prime moduli in the table use the [arbitrary-offset theorem](README.md).

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

## A binary certificate for sixteen labels

At $k=16$, every edge of every finite tree may independently receive offset $0$ or $8$. For the finite test above, a forest has 15 free vertices and each external parent has a prescribed low digit modulo 8. Multiplication by an odd unit permutes the low boundary inputs. If the chosen representative for the product changes by 8 on a root edge, absorb this into that edge's independent offset. Thus a full cover at one low input proves the claim on its entire orbit.

| Rooted forests | Low boundary inputs | Unit orbits | Inputs including all high offsets | Low-label witnesses |
| ---: | ---: | ---: | ---: | ---: |
| 235,381 | 18,027,946 | 5,773,126 | 590,739,734,528 | 74,646,543 |

Fix a low-label witness on the free vertices. Low digit zero occurs once and must lift to 8. Each other digit occurs twice, so its two possible high digits must occur once each. There are $2^7$ possible vertex permutations above this witness. The low edge weights have seven pairs and one singleton. For a pair of edges $e,e'$ let $z_e,z_{e'}$ denote their prescribed high offset bits. Their final weights differ just when
$$
z_e+z_{e'}=1+h_e+h_{e'}\quad\text{in }\mathbb F_2,
$$
where the $h$'s are the high bits of the ordinary full endpoint sums before these offsets. Swapping the two high digits at a given vertex fiber changes the seven right-hand sides by a fixed vector regardless of other swaps. This follows because adding 8 to an endpoint toggles the high bit of its sum. The possible right-hand sides form the affine span of the baseline and seven single swaps. Membership is therefore equivalent to all binary linear characters orthogonal to the seven differences taking their baseline values.

The generator finds a full permutation at the first uncovered offset word. It eliminates the vertex flip variables to mark the assignments covered by that permutation's low digits. The independent verifier starts from the packed low digits alone. It constructs a baseline permutation and the seven single swaps, recomputes their actual endpoint sums, and intersects explicit tables of orthogonal characters. It checks the union of the resulting sets against the entire high-offset cube, fixing the last bit by common translation. Separately it parses every canonical forest, checks the permitted runs and unit orbit sizes, and counts the exact sets of change positions. It excludes duplicate shapes and compares the final number with the rooted-tree multiset product. The separate partition recurrence gives the same 18,027,946 low inputs. [Generator](fiber_cover.cpp) · [Full independent verifier](fiber_verify.cpp) · [Partition recurrence](../rainbow/spine_counts.py)

A third check enumerates all $2^7$ actual lifts for each row in 32 sampled low-boundary inputs, with both values of every edge offset. It recomputed 56,704 vertex lifts and checked 1,048,576 offset vectors. At eight labels the same check tested every row and all 604 unit orbits of the binary certificate. Negative controls rejected a repeated low label, an empty cover, a missing low input, a repeated shape and a truncated row. [Direct lift checker](check_fiber_samples.py)

The 64 little-endian streams occupy 634,635,992 bytes. Each starts with the four ASCII bytes FBL1 and a one-byte modulus. For each forest an eight-byte parenthesis word and four-byte profile count precede its profiles. Each profile has a two-byte low-boundary code, a four-byte row count and one eight-byte low labeling per row. The vertex low digits occupy three bits each, first vertex least significant. The low-boundary code uses base eight at the component positions where size exceeds the preceding mass, first such position least significant. [SHA-256 manifest](fiber16.sha256)

~~~bash
set -e
src="$PWD/research"
out=$(mktemp -d)
c++ -O3 -std=c++17 -c -Drainbow_witness=reference_witness "$src/rainbow/search.cpp" -o "$out/reference.o"
c++ -O3 -std=c++17 "$src/biased/fiber_cover.cpp" "$src/rainbow/leaf_search.cpp" "$out/reference.o" -o "$out/generate"
c++ -O3 -std=c++17 "$src/biased/fiber_verify.cpp" -o "$out/verify"
cd "$out"
mkdir fiber16
for i in {0..63}; do ./generate 16 "$i" 64 "fiber16/$i.fbl"; done
shasum -a 256 -c "$src/biased/fiber16.sha256"
./verify 16 fiber16/{63..0}.fbl
python3 -B "$src/biased/check_fiber_samples.py" 16 fiber16/43.fbl --limit 32
~~~
