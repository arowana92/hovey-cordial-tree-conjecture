# Cutting the tree in order of subtree size

At modulus $k$, the finite forest test can use at most $\lfloor\log_2 k\rfloor$ independent boundary residues on $k-1$ free vertices. The permissible places for these residues are determined by the component sizes. We prove this for every $k\ge5$ and give a sharper characterization of which colored forests occur at a cut.

## The finite test

Use the existing base hypothesis on all $k$-vertex trees. For the extension hypothesis take rooted forests of order $k-1$ with at most $\lfloor2(k-2)/3\rfloor$ terminal vertices. List the component orders $s_1\le\cdots\le s_c$, and put $p_i=\sum_{j<i}s_j$. Assign boundary colors in this order, allowing a change only at an index with $s_i>p_i$. Equal-sized components therefore have equal boundary colors. Require, for each such assignment, a bijection onto the nonzero residues with pairwise distinct edge sums, including all boundary edges.

**Theorem.** These two finite hypotheses imply that every finite tree is $k$-cordial.

Take a minimum counterexample. The [leaf deletion and base arguments](README.md#why-the-hypotheses-suffice) give order $n=mk+1+t$ with $m\ge1$, $1\le t<k$, and fewer than $t$ original leaves. Use the [leaf centroid](README.md#choosing-the-core-with-a-leaf-centroid) to take a seed subtree consisting of a vertex $v$ and whole components of $T-v$. Its order is at most $mk+1$, and at most $\lfloor2(k-2)/3\rfloor$ original leaves lie outside it.

The exterior together with $v$ is a rooted tree at $v$. Visit it in preorder, sorting each vertex's child subtrees by nondecreasing order. Break ties arbitrarily. Grow the seed by that preorder until its order is $mk+1$. Its complement has exactly $t$ vertices. Each complement component is a whole unvisited child subtree. Its parent is either the last visited exterior vertex (possibly $v$) or one of that vertex's ancestors.

List the distinct boundary parents from deepest to shallowest. At an outer parent, the child on the path toward the cut was visited before each of its unvisited children. This path child's subtree contains **all** components contributed by the deeper parents and at least the deeper parent nearest to it. Each component at the outer parent is therefore larger than the sum of all earlier component orders. Within one parent's group sort by size. This gives the displayed size order and allows a boundary-color change only at $s_i>p_i$.

A terminal vertex in the complement is an original leaf. If $t<k-1$, extend a terminal vertex of a largest component by a path to reach order $k-1$. This preserves the number of terminals and the permitted boundary coloring: every largest component belongs to the last color group, and only its size increases. Label the core by minimality, translate the unique surplus residue to zero, apply the finite hypothesis and restrict to the actual complement. The distinct new vertex labels avoid the surplus and the distinct new edge weights extend uniform edge counts. This contradicts minimality.

If there are $d$ indices with $s_i>p_i$, the accumulated order after the $j$-th such index is at least $2^j-1$, by induction. Thus $d\le\lfloor\log_2 k\rfloor$. Each required shape has just $k^d$ boundary colorings before unit symmetry. In particular, if $R_k$ is the number of rooted trees of order $k$, the whole test has at most $R_k(1+k^{\lfloor\log_2 k\rfloor})$ base and colored instances. The tree order in the conclusion is unrestricted.

## Which colored forests actually occur?

There is a sharper, exact test for the traversal itself. Group consecutive components with the same boundary color into runs, still in order of nondecreasing component size. Tied sizes must have the same color. Write $M_j$ for the total order of the first $j$ runs, with $M_0=0$.

**Characterization.** A nonempty colored forest can occur as the suffix of a nonempty preorder prefix with child subtrees visited by nondecreasing order, for a suitable rooted tree, tie order and boundary coloring, exactly when every component in run $j\ge2$ has order at least $M_{j-1}+j-1$.

For necessity, the path child at a change of boundary color contains not only the $M_{j-1}$ earlier free vertices but also at least $j-1$ distinct boundary parents in the prefix. For sufficiency, build a path of new vertices $v_r,\ldots,v_1$, rooted at $v_r$, and attach the components in run $j$ to $v_j$. Give $v_j$ that run's color. The path-child subtree at $v_j$ has order exactly $M_{j-1}+j-1$. It can be visited first, breaking any ties in its favor. Stop after visiting $v_1$. The exterior is exactly the prescribed colored forest. The converse constructs a traversal; it does not require the prefix coloring to be cordial.

For $r$ nonempty runs, $M_1\ge1$ and $M_j\ge2M_{j-1}+j-1$. Thus $M_r\ge3\cdot2^{r-1}-r-1$. Taking one component of the minimum allowed size in each run attains equality with alternating colors. In particular, four runs require at least 19 free vertices. The same padding argument works for the exact test. The option `--spine` verifies this smaller sufficient family. The certificates below use the larger `--ordered` family.

## Independent checks

The generator chooses an independent color at each size gap and identifies assignments related by multiplying every label by a unit. The verifier independently grows every rooted tree by one-leaf insertion, removes its root to enumerate forest shapes, and checks every witness's actual vertex residues and edge sums. It checks that each actual change of boundary color is permitted and counts its unit orbit once. Separately, it enumerates all subsets of change positions on every shape. A valid choice of $r-1$ actual changes contributes $k(k-1)^{r-1}$ colorings, since adjacent runs differ. Equality of the covered and required counts proves coverage. With `--grouped`, repeated nonconsecutive shape groups are rejected.

The [Lean proof](OrderedCut.lean) formalizes the cut along the active child, including completed sibling vertices and empty boundary groups. It proves the mass and separation inequalities at every step and the coarse power-of-two bound. The [traversal check](../bounded-degree/check_prefix.py) independently checks the sharp inequalities on 362,879 concrete cuts. The tree induction and its link to the certificates are proved above.

~~~sh
lean research/rainbow/OrderedCut.lean
python3 -B research/bounded-degree/check_prefix.py
~~~

## Verified moduli

**Corollary.** Every finite tree is $k$-cordial for $k=14,15,16,17$. Each row below verifies both finite hypotheses of the theorem. The forest witness column excludes the base witnesses.

| Modulus | Rooted base trees | Terminal limit | Forest shapes | Forest witness rows | Boundary colorings covered |
|---:|---:|---:|---:|---:|---:|
| 14 | 32,973 | 8 | 30,486 | 2,015,760 | 11,547,550 |
| 15 | 87,811 | 8 | 76,178 | 4,610,330 | 32,824,530 |
| 16 | 235,381 | 9 | 217,251 | 23,827,919 | 158,004,816 |
| 17 | 634,847 | 10 | 607,544 | 32,555,217 | 511,770,312 |

The repository includes the compressed certificates at 14 and 15. The larger certificates at 16 and 17 were generated, hashed and independently checked in a pipeline. Recreate them with the commands below. All digests refer to the uncompressed ASCII JSON Lines in generation order.

| Modulus | SHA-256 |
|---:|---|
| 14 | `a41670c71a7eb347bfd888eb35c595f46a55118ba57f15fbe2ca07fef87de026` |
| 15 | `302c2f3cfd9f1b7d342350849b2b19b17f13982596d2e389c5776c19b76880b1` |
| 16 | `a8de65e7c8b7163fb84c810b7804894b91b37009517f304925ef9331a400cad3` |
| 17 | `4a966cd40561beac56ef0c9669c272b49cef5125c98e5b488d196d6ca507b797` |

Run in Bash from the repository root with Python 3.8 or newer. The generator at 14 uses the Python search. The other three digests use the deterministic C++ search. The independent verifier uses only the Python standard library in every case.

~~~sh
set -e -o pipefail
for k in 14 15; do
  python3 -B -m research.rainbow.verify "$k" "research/rainbow/k$k.jsonl.gz" --ordered --grouped
done

out=$(mktemp -d)
c++ -O3 -std=c++17 -shared -fPIC research/rainbow/search.cpp -o "$out/search.so"
for k in 14 15 16 17; do
  search=()
  if (( k >= 15 )); then search=(--native "$out/search.so"); fi
  python3 -B -m research.rainbow.generate "$k" --ordered "${search[@]}" |
    gzip -1 -n > "$out/k$k.jsonl.gz"
  gzip -dc "$out/k$k.jsonl.gz" | shasum -a 256
  python3 -B -m research.rainbow.verify "$k" "$out/k$k.jsonl.gz" --ordered --grouped
done
~~~

The two searches may choose different valid labelings for the same input. The verifier accepts either when its explicit witnesses satisfy the same hypotheses.
