# Every finite tree is 23-cordial

**Theorem.** At modulus 23, every finite tree has a labeling whose vertex frequencies differ pairwise by at most one and whose endpoint-sum frequencies also differ pairwise by at most one. The order of the tree is unrestricted.

The [ordered-cut theorem](ordered-cut.md) needs a bijective rainbow labeling of every order-23 tree and rainbow extensions on certain rooted forests with 22 free vertices. “Rainbow” means all of the relevant edge sums are distinct. After a core of order $1\bmod 23$ has been labeled, translate its unique surplus vertex label to zero. The extension uses distinct nonzero labels and distinct new weights, including the weights of attachment edges. For the forest test one needs at most 14 terminal vertices. In nondecreasing order of component sizes, a new run of boundary colors can begin only at size at least the preceding total order plus the number of preceding runs. The theorem proves by induction that these finite hypotheses suffice.

| Rooted bases | Eligible forests | Base-only shapes | Witness rows | Required boundary assignments |
| ---: | ---: | ---: | ---: | ---: |
| 268,282,855 | 264,416,428 | 3,866,427 | 5,768,438,850 | 701,057,132,194 |

The all-zero boundary on every forest verifies the base after adjoining a root labeled zero. On each witness the independent verifier reconstructs every internal sum and explores the boundary labels by assigning an unused weight to a particular component root in each group. Injectivity and full coverage of all required colorings up to unit multiplication are checked for each shape. Finally, all canonical shape words are sorted, checked for duplicates, and counted against a rooted-tree recurrence. A separate calculation from integer partitions gives the same base, eligible-forest and boundary-assignment totals. The independent [integer census](../census/README.md) also proves the base at this order. [Verifier](spine_verify.cpp) · [Partition count](spine_counts.py) · [Witness format](native-spine.md)

## Generating a shard without storing every rooted branch

Put $s_0=k-1$ and $B=\lfloor s_0/2\rfloor$. Catalogue rooted trees of order at most $B$, sorting by order and canonical opening/closing word. In any forest of order at most $s_0$, at most one component exceeds $B$ and it must come last. Let $W(s,i)$ count forests of order $s$ where only small types of index at least $i$ are allowed. If there are $M$ small types, initialize $W(0,i)=1$. For $s>0$,
$$
W(s,M)=[s>B]W(s-1,0),\qquad
W(s,i)=W(s,i+1)+[s\ge d_i]W(s-d_i,i),
$$
where $d_i$ is the order of type $i$ and an inapplicable term is zero. The last-column term takes a single large tree and removes its root. In the recursion indexed by a small type, take its first occurrence or omit the type.

For fixed $(s,i)$, list completions by their first small component $j\ge i$, in increasing order, then place the single large-component alternative last. The block for $j$ has size $W(s,j)-W(s,j+1)$. Binary search locates a rank's block. Recursing on the remaining forest, or on the children of the single large tree, produces its canonical word. Restricting ranks to one residue class assigns a shard without generating the other shards' shapes. The search for labels and the verifier use the same SPN2 interface as at 22 labels. The verifier has no dependency on the unranking algorithm. At nine labels both generators produced byte-identical witness lists for all 286 individual shape words. [Ranked enumeration](ranked_forest.hpp) · [Generator](spine_generate.cpp) · [Leaf search](leaf_search.cpp)

## Reproduction

Use a C++17 compiler and Python 3. The 128 streams occupy 130,125,049,600 bytes together. Their sizes also satisfy five header bytes per shard, twelve bytes per forest, and 22 bytes per witness. Shards may be generated concurrently within available machine resources.

~~~sh
set -e
src="$PWD/research/rainbow"
out=$(mktemp -d)
c++ -O3 -std=c++17 -c -Drainbow_witness=reference_witness "$src/search.cpp" -o "$out/reference.o"
c++ -O3 -std=c++17 "$src/spine_generate.cpp" "$src/leaf_search.cpp" "$out/reference.o" -o "$out/generate"
c++ -O3 -std=c++17 -pthread "$src/spine_verify.cpp" -o "$out/verify"
cd "$out"
mkdir spine23
for i in $(seq 0 127); do
    ./generate 23 "$i" 128 "spine23/$i.spn" --ranked-cover
done
shasum -a 256 -c "$src/spine23.sha256"
./verify 23 --parallel 8 spine23/*.spn
python3 -B "$src/spine_counts.py" 23
~~~

The [manifest](spine23.sha256) identifies each uncompressed shard. The induction and its two finite hypotheses concern ordinary edge sums with no prescribed offsets.
