# Every tree of matching number at most six is super edge-magic

**Theorem.** Every finite tree with at most six edges in a maximum matching has a bijection onto consecutive integers under which all edge sums are consecutive. It is $k$-cordial for every positive $k$. Both the number of leaves and the tree order can be arbitrarily large. [Consecutive-sums implication](https://ajc.maths.uq.edu.au/pdf/43/ajc_v43_p031.pdf)

## Reducing to a finite list of marked cores

In a tree the minimum vertex cover size equals the maximum matching size $d$. One elementary proof chooses a leaf edge in a maximum matching by exchanging its neighbor's matched edge if necessary. Put that neighbor in the cover and delete both vertices, then continue on the remaining forest. Isolated vertices need no cover. At orders at least three a minimum cover can be chosen entirely among nonleaf vertices by replacing any selected leaf by its neighbor. Write $S$ for this cover.

Remove all leaves once to obtain a tree $H$ on $h$ vertices. The stars and smaller trees are covered directly. Every removed leaf is adjacent to $S$. Every vertex of $H-S$ has at least two neighbors, all in $S$, and has no exterior leaves. Thus with $u=h-d$ we have $2u\le h-1$, or $h\le2d-1$. The [seven-nonleaf theorem](seven-nonleaf.md) covers $h\le7$, in particular all $d\le4$. The remaining possibilities have $d=5,6$ and $8-d\le u\le d-1$.

Rank just the $d$ sites by their extra leaf counts after reserving one leaf at each degree-one vertex of $H$. Number the other $u$ vertices after the sites. The core consists of direct edges between sites and $u$ unmarked junctions, each specified by its subset of neighboring sites. Two different junctions cannot have identical neighborhoods since their degrees are at least two and $H$ is acyclic. We identify cores up to permutations of these junctions, keeping every site rank fixed.

For a given core use the same ranked leaf layers and integer interval seeds as in the seven-nonleaf proof. Only the first $d$ ranks can receive extra leaves. The verifier requires zeros in the remaining base and step coordinates and checks exact coverage in the $d$ varying coordinates. It reconstructs every seed and checks new vertex labels, leaf populations, and actual edge sums when applying the bands. The induction from these checks permits unbounded counts at the marked sites. [Seed and layer verification](ranked_core_verify.py)

## Independently counting the marked trees

Suppose $v$ edges are direct. Put $m_i$ for the number of unmarked junctions of degree $i+1$. Then $\sum m_i=u$ and $v+\sum i m_i=d-1$. Subdivide each direct edge once temporarily. This gives a bipartite tree on $d$ labeled sites and $u+v$ incidence vertices, with the $v$ new degree-two vertices distinguished as a type. For these multiplicities the number of ranked cores is
$$
\frac{d^{u+v-1}(d-1)!}{v!\prod_{i\ge1}m_i!(i!)^{m_i}}.
$$
Indeed, when all incidence vertices have names, the bipartite tree code consists of a word of length $u+v-1$ on the sites and a word of length $d-1$ on the incidence vertices. The second word contains each incidence vertex its degree minus one times. The first word is unrestricted. Forgetting the names within each incidence type divides by the indicated factorials. The action is free because the site labels distinguish each neighborhood. Subdividing or suppressing the distinguished direct-edge vertices are inverse operations. [Bacher's bipartite tree enumeration](https://arxiv.org/abs/1102.2708)

| Cover size | Ranked geometries by increasing junction count | Witnessed cells | Largest seed order | Coverage representatives |
| ---: | --- | ---: | ---: | ---: |
| 5 | $u=3,4$: 650, 125 | 1,388 | 26 | 36,060 |
| 6 | $u=2,3,4,5$: 20,790, 20,340, 8,640, 1,296 | 88,394 | 34 | 4,713,408 |

The verifier recognizes each connected simple marked tree, rejects repeated neighborhood descriptions, and compares the separate totals for each $u$ to the formula. The generator constructs direct edges and junction neighborhoods by joining separate components. No matching-number computation or graph-isomorphism oracle is required in the verifier. [Five-site certificate](vertex-cover-5.jsonl.gz) · [Six-site certificate](vertex-cover-6.jsonl.gz) · [Independent verifier](check_vertex_cover.py)

~~~sh
python3 -B -m research.hub.check_vertex_cover 5
python3 -B -m research.hub.check_vertex_cover 6
~~~

To regenerate both certificates, run the following from the repository root. The native search prunes a partial assignment when two completed edges already have the same sum or the interval cannot contain all completed labels and sums. These are necessary conditions and do not change the order of successful witnesses. The decompressed SHA-256 digests are `4c463658030d663a0dbf729ed89bf0a0244021b9c43b306dfa90ae812c2fce8d` and `3d2fbf8ddb4ae8eb68cd945f49ecbc1fafc14b0ca6e17b205918e46af5fe45b8`, respectively. [Generator](vertex_cover_generate.py)

~~~sh
out=$(mktemp -d)
c++ -O3 -std=c++17 -shared -fPIC research/hub/ranked_core_search.cpp -o "$out/search.so"
for d in 5 6; do
    python3 -B -m research.hub.vertex_cover_generate "$d" "$out/search.so" > "$out/$d.jsonl" || exit 1
    gzip -dc "research/hub/vertex-cover-$d.jsonl.gz" | cmp - "$out/$d.jsonl" || exit 1
done
~~~
