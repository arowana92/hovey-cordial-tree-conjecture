# Prescribed ten-label cores and a two-star obstruction at infinitely many moduli

A **divisible core** is a tree of order divisible by the modulus with a fixed cordial labeling. Its vertices have uniform counts, and one edge weight $D$ occurs one time fewer than the others. A **surplus core** has order one modulo the modulus. Its edge counts are uniform, and one vertex label occurs one time more than the others. Each new rooted component attaches by an edge from its root to an old vertex. Only that old vertex's label matters.

**Theorem at ten labels.** For a divisible core, every attachment of up to nine vertices works. On exactly ten vertices there is just one exception up to affine symmetry. It consists of a center with seven children at an old parent labeled $b$, and a center with one child at an old parent labeled $b+5$, when $D=2b$. Every other attachment, of any size, works.

For a surplus core translated to have surplus zero, every attachment of at most eight vertices works. On nine new vertices exactly **34** colored forests fail, in 16 unit orbits. On ten new vertices exactly **eight** fail. They have a center with four or five children at a unit-colored parent and all singleton leaves at zero. Every attachment of eleven or more vertices works. This also gives another proof for ordinary ten-label trees, by taking the core to be a singleton. The nine-vertex exceptional list has at least two boundary colors in every row, and the ten-vertex exceptions do too. [Earlier all-tree proof at ten](README.md)

## Finite proof

At nine new vertices on a surplus core the new labels must be precisely the nonzero residues, and the nine edge weights must differ. The generator searches each unit orbit for a witness. The verifier checks each positive witness by summing actual endpoints. For every negative it tries all $9!$ permutations. It checks uniqueness of the isomorphism classes, adds their unit-orbit sizes and compares to the catalog size obtained independently as a multiset generating-function coefficient. In detail, if $r_j$ counts rooted trees of order $j$, then $r_n$ is the coefficient of degree $n-1$ in the product of $(1-x^j)^{-r_j}$ for $j<n$. The boundary-colored forest series has exponents $-10r_j$. The check covers **1,209,660** colored forests in **305,840** orbits. The [16 negative representatives](ten-surplus-obstructions.json) encode an internal parent by its zero-based index and an external parent of color $p$ by $-1-p$.

Any smaller forest can be padded to size nine. Restriction works if that padded forest succeeds. For the failed nine-vertex representatives every deletion of a terminal vertex has a verified rainbow witness (26 deletion orbits). Thus all smaller sizes work by restriction as well.

For a divisible core, choose a new root, color it to produce the old deficient weight and translate the resulting surplus to zero. If nine vertices remain and fail, they occur in the list of 16, up to a unit. Reconstruct the removed root: its label is now zero, its own external parent has color equal to the translated deficit, and any subset of the residual roots at zero could have attached there. The checker enumerates these choices and all ten deficit values. This gives 4,760 parent-array and deficit pairs after literal deduplication. Testing the other roots as first choices leaves 140 pairs for direct search. Witnesses are checked against both histograms; negative cases are independently exhausted up to permutations of leaves at the same parent. The only failed affine orbit has ten elements as stated. Here $f\mapsto uf+t$ sends edge weights to $uw+2t$ and preserves both balance conditions.

For a larger surplus attachment, any ancestor-closed nine-vertex subset with a rainbow witness produces a divisible intermediate core. When at most nine vertices remain that part always extends. Forests avoiding every such good subset can be enumerated by adjoining a child or an externally attached singleton and retaining the result only if deleting **every** terminal vertex gives a previously retained orbit. This enumerates the whole exceptional family: every proper ancestor-closed subset omits some terminal vertex. There are respectively 16, 6, 3 and 0 such orbits at sizes 9, 10, 11 and 12. Direct histogram checks on the six and three cases give precisely the two failed orbits at size ten. The independent negative search across the larger surplus and divisible classifications inspects 18,612 assignments after quotienting by sibling permutations. The same first-root reconstruction from the two failed ten-vertex surplus orbits gives 480 lifts at size eleven on a divisible core. Twenty need a direct witness and all twenty succeed. Finally a divisible attachment of size 12 through 19 starts by filling its deficit, leaving 11 through 18 vertices on a surplus core.

## The nineteen-vertex step

Consider a surplus core and 19 free vertices. Call a free vertex without a free child a tip. An initial set is closed under taking free parents. By the finite proof every forest of size at least twelve contains a good initial nine-vertex set. Giving it a rainbow labeling produces a divisible core. If the ten remaining vertices fail, their two components have respectively seven children and one child at their centers. Thus a failure requires a vertex with at least seven children in the original forest.

**At least nine tips.** It suffices to remove nine tips leaving a good initial ten-vertex set. The labeling of this set gives a surplus core again. The nine terminal leaves can then receive distinct nonsurplus labels and distinct weights, by the nine-vertex classification for singletons.

If there is only one internal vertex, the 18 leaves split into its children and externally attached singletons. Keep the center and nine leaves from one group, which is possible since one group has size at least nine. Neither resulting shape is exceptional. The all-singleton case also works. With at least eleven tips and at least two internal vertices, protect a child of each of two internal vertices. At least nine tips can still be removed. The initial ten then have at least two internal vertices; every ten-vertex surplus exception has just one.

It remains to consider nine or ten tips. Remove any nine. If the resulting set is bad, it has one internal vertex with at most five children. The original forest had at least nine internal vertices, all of which remain in the set. At least eight distinct tips of the set must therefore have lost a child to the nine removals. At most one of the removed leaves can be a child of the retained center, which consequently had at most six children originally. No other vertex can have had more than two children. This contradicts the required seven-child vertex.

**At most eight tips.** Start with a good initial nine-vertex set. If the remainder fails, its two stars already contain eight tips. Every tip of the initial set must therefore be a parent of one of these stars. There are at most two such tips. The remaining finite case is small enough to check on whole trees.

There are 21 possible initial uncolored nine-vertex forests with at most two tips. They consist of a chain, a fork with a positive trunk and two unordered positive arms, or two chains. Coloring their external parents gives 570 distinct inputs. For each input, each of the two additional centers can attach to one of the nine free vertices or at an external parent of one of the ten colors. This gives $570\cdot19^2=205{,}770$ inputs. The checker searches for a rainbow labeling of the nine vertices, then enumerates the three special labels of the two stars. A different rainbow labeling suffices for all 2,544 cases in which the first choice fails. Each resulting labeling is replayed on an actual 30-vertex tree: the old core is the star on eleven vertices with center zero and leaves carrying all ten residues. Every replay has vertex counts all three and edge counts two once and three nine times. The same assignments extend any old surplus core because the boundary colors agree and the old histograms differ only by uniform constants. [Complete join check](check_nineteen_ten.py)

**Induction.** The nineteen-vertex step finishes the small surplus cases. From a divisible core and at least twenty free vertices, first fill the deficient weight at a root. The rest is a smaller surplus-core instance of size at least nineteen. From a surplus core and at least twenty free vertices, label a good initial nine-vertex set. The rest is a smaller divisible-core instance of size at least eleven. Simultaneous strong induction gives both all-size classifications.

## Exact two-star criterion for every even modulus

Let $k=2m\ge4$. Start at a divisible core with $D=0$. Attach a center with $k-3$ leaf children at an old vertex labeled zero, and a center with one leaf child at an old vertex labeled $m$. This prescribed labeling extends **if and only if $3\mid k$ or $4\mid k$**.

The $k$ new labels form a permutation. Call the large center, small center and its leaf labels $a,b,z$. The large center's child edges use all residues except the three distinct holes
$$
H=\{2a,a+b,a+z\}.
$$
The three remaining weights are $a,b+m,b+z$. Every nonzero weight can occur at most once among the new edges. Thus each of these three that is nonzero must occupy a distinct hole. Zero must occur once or twice overall. These conditions are sufficient too: the old zero bin starts one below the rest and the total number of new edges is $k$. If $a\ne0$, membership $a\in H$ forces $a,b$ or $z$ to vanish. Exactly one of the three labels is zero by distinctness.

* If $a=0$, then $b+z$ must vanish, since it cannot equal either $b$ or $z$. The third weight $b+m$ cannot also be zero or equal $b$. Hence $b+m=z=-b$, so $2b=m$. This requires $4\mid k$.
* If $b=0$, the weight $z$ must equal $2a$. The remaining nonzero weight $m$ must occupy the remaining hole $3a$. When $3\nmid k$, the unique solution of $3a=m$ is $a=m$, which would give $z=0$. Thus $3\mid k$.
* If $z=0$, the weight $b$ must equal $2a$. Then $b+m$ can be zero or $3a$. The latter would force $a=m$ and $b=0$. Consequently $2a=m$, which requires $4\mid k$.

For $4\mid k$ choose $a=0,b=k/4,z=-b$. For $3\mid k$ choose $b=0,a=m/3,z=2a$. Direct substitution fills the required holes. This gives a fixed-core obstruction at every $k\equiv2,10\pmod {12}$ with $k\ge4$. An actual example at each such modulus starts with the $k$-vertex star labeled zero at its center and bijectively by the other residues at its leaves. Its deficient weight is zero. The resulting tree is a caterpillar: deleting its leaves gives a path. Hovey's caterpillar theorem supplies a cordial labeling when all vertices may be relabeled. [Hovey (1991)](https://doi.org/10.1016/0012-365X(91)90254-Y)

## Reproduction

Run from the repository root with Python assertions enabled.

~~~sh
set -eu
out=$(mktemp -d)
c++ -O3 -std=c++17 -shared -fPIC research/rainbow/search.cpp -o "$out/search.so"
python3 -B -m research.rainbow.surplus_spectrum 10 --native "$out/search.so" > "$out/ten.jsonl"
shasum -a 256 "$out/ten.jsonl"
python3 -B -m research.rainbow.check_surplus_spectrum 10 "$out/ten.jsonl" "$out/bad.json"
cmp "$out/bad.json" research/rainbow/ten-surplus-obstructions.json
python3 -B -m research.rainbow.surplus_repairs "$out/bad.json"
python3 -B -m research.rainbow.check_star_period
python3 -B -m research.rainbow.check_nineteen_ten
~~~

The witness stream from this native generator has SHA-256 `eff0479873598f208efcd2c813b8cb33a8602c743d8123d22ef9328b58a672cf`. The star-period checker independently enumerates triples of special vertex labels in the two-star example at each even modulus from 4 through 42. [Generator](surplus_spectrum.py) · [Witness and coverage checker](check_surplus_spectrum.py) · [Root choices and direct checks](surplus_repairs.py)
