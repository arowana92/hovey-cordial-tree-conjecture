# Keeping a specified leaf in a most-frequent residue class

**Theorem.** In every tree with at most one branching vertex, any specified leaf can receive a most-frequent vertex label for every modulus through 45. With at most two branching vertices, the same holds for every modulus through 39. Both statements hold at every tree order. A branching vertex has degree at least three.

Consequently every such tree with a perfect or near-perfect matching is $2m$-cordial for every odd $m$ through 45 or 39, respectively. The largest moduli given by these two conclusions are **90** and **78**. The proof also covers trees with arbitrarily many branching vertices if their matching contraction, after the completion described below, satisfies the branching bound.

## Retaining or removing the mark

For moduli through 25 the [marked-leaf theorem](../marked-leaves.md) applies to arbitrary trees. For larger moduli use the [terminal-path certificates](terminal-paths.md). Fix a bound on the number of branching vertices and suppose a marked tree is a smallest failure in that class. Every smaller tree in the class has a cordial labeling, since it can be given any leaf mark. A singleton is immediate.

Write the order as $qk+1+t$ with $0\le t<k$. When $t=0$, delete the marked leaf, label the smaller tree, and give the leaf the label that fills the unique deficient edge weight. Its label is now the unique surplus vertex label. When the order is at most $k$, a bijective cordial labeling of an order-$k$ extension restricts to an injective labeling with distinct edge weights. Every used label is then most frequent. Extending a leaf by a path preserves the branching bound.

For $t>0$, suppose the terminal arms of some branching vertex contain at least $t$ vertices. Sort those arms by length and take the last $t$ vertices in their order from the joint outward. The retained tree is connected and has order one modulo $k$. If the marked leaf survives, it is still a leaf or the sole vertex. Label the retained tree so the mark has its unique surplus label. If the mark was removed, use any cordial labeling of the retained tree. The terminal-path certificates give distinct new labels avoiding that surplus, and distinct new edge weights. Thus the surplus stays in a highest-frequency bin and every newly used label reaches a highest-frequency bin. This covers both locations of the mark. On a path use either end as the joint and take a single terminal segment.

## Which divisible cuts can be used

Root the tree at its marked leaf. If a descendant component cut off by an edge has order divisible by $k$, keep the marked side fixed and translate a cordial labeling of the detached component. The [bridge formula](../divisible-cuts.md) gives equal increments in every vertex and edge bin. It preserves the marked label and its rank in the histogram. Minimality consequently forbids every divisible component **on the side away from the mark**.

Root the skeleton of the branching vertices at the branching vertex nearest the marked leaf. Every child connector cuts off a component away from that leaf at each position along the connector. If a child part contains $j$ branching vertices, its descendants below the joint have total order at most $(j-1)k$ by induction. The joint and its own terminal arms add at most $t$ vertices, because $t$ terminal vertices would allow the preceding restoration. The order therefore starts below $jk$. Moving one vertex at a time up the connector, it cannot attain $jk$, a forbidden divisible cut. At the skeleton root this gives $n\le(b-1)k+t$, where $b$ is the number of branching vertices. Substituting $n=qk+1+t$ gives $q\le b-2$ and $n\le(b-1)k$. These are the same [verified arithmetic inequalities](BranchingBound.lean) as for the unmarked bound, now using only outward cuts. For $b=1$ this is impossible. For $b=2$ the order-$k$ bases settle all remaining orders.

## Lifting the marked result

For a near-perfect matching, move the exposed vertex to a leaf by alternating along matched and unmatched edges, and give that leaf a temporary mate. The resulting perfect matching contracts to a tree $Q$. The temporary pair represents a leaf of $Q$, except for a singleton quotient. Give this quotient leaf a most-frequent label. Apply the [matching construction](../matching-expansion.md) and then delete the temporary vertex. Its vertex bin and its odd matching-weight bin each had maximum frequency, so both histograms stay balanced. The perfect case needs only an ordinary quotient labeling. Adding the mate at a leaf preserves the number of branching vertices, and contracting an edge cannot increase it. This proves the two stated matching ranges. [Movement of exposures and the deletion calculation](../near-matching.md)

There is a version at every star size $a\ge2$. Replace each vertex of an $m$-cordial quotient, $m$ odd, by an $a$-vertex star. Join centers to centers or leaves to leaves along quotient edges, as in the [equal-star construction](../matching-expansion.md#equal-stars-in-place-of-vertices). In one star whose quotient vertex has a most-frequent label, delete any set of leaves unused by the joining edges. The result is $am$-cordial. In particular one can prescribe a smaller terminal star of any positive size, provided the specified joining port survives. This applies to arbitrary quotients through odd modulus 25 and to the marked terminal quotients in the larger ranges above.

Indeed, the leaf digits within that star are distinct nonzero residues modulo $a$. Each deleted leaf removes a maximum-frequency vertex entry from its digit class and a maximum-frequency internal edge entry of that same digit. The two histograms repeat the quotient vertex frequencies in those classes, and the digit-zero edge class repeats the quotient edge frequencies. At quotient order divisible by $m$ all vertex entries are equal and the sole lower edge entry is in digit zero. At all other orders a most-frequent quotient vertex entry is also maximal in each complete histogram. Different deleted digits affect different bins, proving simultaneous deletion.

## Reproduction

The [constructor](marked_branches.py) chooses the cut from the input tree, pads small bases and terminal forests, and computes labels using the native solver. The [separate histogram check](check_marked_branches.py) rebuilds the original edge list, tests the leaf frequency and then tests matching and shortened-star expansions at their full moduli. Across moduli 26 through 45 it checked 1,920 marked trees and 7,190 expansions. The constructions included 519 directed divisible cuts and terminal cuts retaining the mark 2,072 times and removing it 1,279 times. These examples test the construction. The exhaustive inputs for the induction are the existing [path and base certificates](terminal-paths.md#reproduction).

~~~bash
set -euo pipefail
src="$PWD/research/rainbow"
out=$(mktemp -d)
c++ -O3 -std=c++17 -fPIC -Drainbow_witness=reference_witness -c "$src/search.cpp" -o "$out/ref.o"
c++ -O3 -std=c++17 -fPIC -shared -DRAINBOW_WIDE_MASK "$src/leaf_search.cpp" "$out/ref.o" -o "$out/search.so"
python3 -B -m research.rainbow.check_marked_branches "$out/search.so" {26..45}
~~~
