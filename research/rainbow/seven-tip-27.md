# A seven-tip tree at one prescribed boundary, modulo 27

**Theorem (computer-assisted).** Take a prescribed 27-cordial tree whose order is one modulo 27. At any old vertex attach a single rooted tree on at most 26 new vertices with at most seven rooted tips. Its labels can be chosen so that every parent-first ordering of these vertices stays cordial throughout, with all old labels fixed.

For exactly 26 new vertices and exactly seven tips, there are **64,561,161** rooted trees. A verified stream of **187,882,955** explicit labelings covers every tree and every one of the 27 possible old boundary colors, or **1,743,151,347** literal inputs. Labels on the free vertices are distinct and nonzero, and their weights, counting the entering edge, are distinct.

Translate the old surplus label to zero. The stated input for the attachment is the resulting label of its old parent. Each initial segment of a parent-first ordering adds distinct labels to low vertex bins and distinct weights to uniform edge bins. Translate the finished labeling back. For fewer than seven tips use the [six-terminal theorem](few-leaves.md). For fewer than 26 vertices extend one tip by a path, use the larger witness and restrict. These arguments require no size bound on the old tree.

## Enumerating a single rooted component

In a rooted tree with seven tips, follow the unique child until the first vertex with at least two children. Let $a$ count the initial vertices through that branching vertex, inclusive. Including the branching vertex in $a$ gives $a=1$ when the original root branches. Below it is an unordered forest of at least two components, of total order $26-a$ and with exactly seven tips. This decomposition is unique and every such forest reconstructs a valid rooted tree.

For each component record its order and tip count. The [profile enumerator](seven_tip_profiles.py) sums products of multiset binomial coefficients and independently compares their total with the number of rooted 26-vertex trees with exactly seven tips. There are 16,798 stem and component profiles. The [stream generator](spine_generate.cpp) enumerates canonical child forests and wraps each bracket word in $a$ successive roots. The [native verifier](spine_verify.cpp) parses the whole tree again, checks that every path vertex before the designated branching vertex has exactly one child and that all child components have the prescribed orders and tip counts. It verifies the required number of distinct canonical words using its separate bivariate generating function. Every complete rooted tree has one actual entering edge. The verifier checks distinctness of all labels and actual weights and covers all 27 boundary colors under multiplication by units.

The [compressed manifest](seven-tip-27-single.sha256.gz) contains the SHA-256 digest, forest count, witness count, literal boundary count and decomposition for each profile. Its uncompressed SHA-256 is `d5c156e1afd4bd446ebf75e456ac23dbfb2aa205f60a6fdc7ecc9327e10494fa`. The [manifest checker](check_seven_tip_profiles.py) validates the profile set and recomputes all forest and boundary counts.

## Reproduction

Run from the repository root in Bash with Python 3.8 or later and a C++17 compiler. The full replay streams the witnesses directly into the verifier. Temporary disk use consists of the profile list and verification records.

~~~bash
set -euo pipefail
out=$(mktemp -d)
r=research/rainbow
c++ -O3 -std=c++17 -Drainbow_witness=reference_witness -c "$r/search.cpp" -o "$out/reference.o"
c++ -O3 -std=c++17 "$r/spine_generate.cpp" "$r/leaf_search.cpp" "$out/reference.o" -o "$out/generate"
c++ -O3 -std=c++17 -pthread "$r/spine_verify.cpp" -o "$out/verify"
python3 -B -m research.census.check_typed_leaf_streams "$out/generate" "$out/verify"
python3 -B -m research.rainbow.seven_tip_profiles 26 7 > "$out/profiles"
python3 -B research/census/stream_leaf_profiles.py 27 "$out/profiles" "$out/generate" "$out/verify" "$out/single" --workers 2
gzip -dc "$r/seven-tip-27-single.sha256.gz" > "$out/published"
cmp "$out/published" "$out/single/manifest.txt"
python3 -B -m research.rainbow.check_seven_tip_profiles "$r/seven-tip-27-single.sha256.gz"
~~~
