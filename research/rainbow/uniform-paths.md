# Uniform increments from paths at a single joint

**Theorem.** At every modulus through 43, fix any vertex labeling on any tree and choose a joint. Attach any number of paths there, of arbitrary lengths. If their total number of new vertices is $qk$, both histograms can gain exactly $q$ at every residue. The unique exception is $k=4$ with exactly two paths of length two. A cordial core stays cordial for every old order. The identity also holds for a core whose counts are unbalanced.

For example, one can attach such path families repeatedly at different vertices and still preserve every old label. At every modulus $k\ne4$ in the certified range, the center of any spider can receive a most-frequent vertex label at every tree order. At orders one modulo $k$ it can receive the unique surplus.

## A block of one period

Sort the paths by nondecreasing length and list each from the joint to its tip. Remove the last $k$ vertices. The removed pieces are paths at the joint, with at most one exception whose parent is a retained vertex on its own arm. If there are other removed paths, this exceptional path is strictly shorter than all of them. The retained arms still meet only at the original joint. Induct on $q$.

For each partition of $k$, it suffices to assign all $k$ residues once to the free vertices and see each residue once on the $k$ entering edges. The common parent and the parent of a unique shortest path may have any prescribed labels. A single path has one prescribed parent. Translate so the common parent label is zero. Write $x$ for the first parent's difference, using zero in the common-parent case. Multiplication by units takes $x$ through precisely the residues of the same gcd with $k$. Conversely every unit modulo $k/\gcd(x,k)$ lifts to a unit modulo $k$, by avoiding the remaining primes. One verified labeling per difference orbit suffices. Translation back leaves uniform counts uniform.

For the center assertion at order $qk+1+t$, $0\le t<k$, keep the joint and remove the last $t$ arm vertices in the same sorted order. The smaller spider has a uniform labeling of its $qk$ free vertices and $qk$ edges relative to its center. Thus the center carries the unique vertex surplus. The [short terminal-path certificate](terminal-paths.md#removing-ends-of-paths) restores the $t$ vertices using distinct labels avoiding that surplus and distinct weights. The center stays in a most-frequent bin.

## Four labels

For one period the finite assertion passes except for $(2,2)$ at a common parent. Normalize the parent to zero. The sum of all entering weights minus all free labels is the sum of the intermediate labels. The two permutations force this to be zero. The intermediates must be 1 and 3, and the zero tip then repeats a boundary weight.

For two periods the [four-label enumeration](check_uniform_grafts.py) verifies all 22 partitions of eight at a common parent. It also covers six two-edge arms at a common parent. For a larger multiple of four, remove a four-vertex suffix in the usual order unless it consists of two whole two-edge arms. In that case all arms have lengths at most two. If any singleton arms remain, there are at least two by parity. Take two singletons and one two-edge arm. Otherwise take four whole two-edge arms, using the order-eight row. When the total was twelve and all arms have length two, use the six-arm row directly. Thus every step from a total of at least twelve leaves at least eight, or finishes outright. The only failure is the original single-period exception, inside the five-vertex path. Modulus one is immediate.

## Chains of matched pairs

At $2m$ with odd $m$, replace each free vertex by a pair and allow each incident edge to choose either endpoint. Write the two labels of each pair with equal residue modulo $m$ and opposite parities. Given a uniform path-forest assignment modulo $m$, orient each entering endpoint to match its actual parent's parity. The entering edges hit each even weight $q$ times. The matched edges hit the odd weights $q$ times since doubling permutes the low residues. Both vertex parities also cover every low residue $q$ times. Thus **chains of matched pairs** with a total of $qm$ pairs attach at any joint to any old labeling, through odd $m=43$. One arbitrarily long chain with a whole number of periods has this property at **every** odd $m$, using the ordinary [uniform path block](../counterexample-bound.md#shortening-paths) on its contraction.

There is a second result for **every odd $m\le45$**. If the old tree has order divisible by $2m$ and its labeling is cordial, an arbitrary number of these chains of arbitrary lengths extends the fixed labeling, even with a partial last batch. Remove the final $t$ pairs in sorted arm order, taking $1\le t\le m$ so the retained number of added pairs is divisible by $m$. Induct on the number of added pairs. The retained tree has one deficient edge residue $D$ and uniform vertex counts. Choose the first pair on the shortest removed path, choosing the exceptional path if present. Force its entering edge to have weight $D$. This fixes its low residue $z$ and orientation.

After this pair, every remaining path begins at the common joint except possibly the shortened tail. If nonempty, that tail is strictly shorter than the other paths. Normalize $z$ to zero in the low coordinates, pad a longest path to bring the remaining free order to $m-1$, and apply the short terminal-path theorem. Restriction and translation back give distinct low labels avoiding $z$ and distinct low weights on all subsequent entering edges. Orient the remaining pairs so those weights are even. After filling $D$, the matching edges add distinct odd weights and the remaining entering edges add distinct even weights. Each new vertex label occurs at most once in the batch. This proves the partial batch and the induction. At $m=1$ a single pair per batch already supplies both vertex labels and fills the deficit before its odd matching edge.

For every odd $m$, uniformity also transfers from any proven uniform rooted quotient forest by the same parity argument. For example, any mixture of one- and two-pair chains with total divisible by $m$ works at a common joint at all odd $m$. The [regular-branch integer theorem](../census/regular-joints.md) handles at least three two-pair chains, or use the elementary interval construction when there is a singleton. With one two-pair chain alone or two alone the number of free pairs is two or four, whose only odd divisor is one. [Two independently prescribed sites at every odd modulus](../census/two-site-arms.md)

## Certificates and reproduction

The [generator](uniform_paths.cpp) writes the path lengths, normalized parent difference and actual permutation in every row. The [independent verifier](check_uniform_paths.cpp) directly counts endpoint sums, checks unit-orbit coverage, and verifies that distinct sorted partitions reach the target given by the integer partition recurrence. The [counts](uniform-paths.counts) give the full number of parent assignments before normalization, and the [hashes](uniform-paths.sha256) pin the streams. Modulus four has its separate checker. Failed searches play no role in the positive assertions.

The [whole-tree checker](check_uniform_grafts.py) preserves arbitrary old labels, applies each batch and counts the actual added labels and weights. It checked 3,024 whole trees and 8,880 batches through modulus 43. For odd moduli it also checked the uniform matching lift on those trees, with arbitrary ports. The [partial-batch checker](check_matched_chains.py) verified another 1,870 complete matched grafts in 6,100 batches through modulus 90, using divisible cores and actual endpoint sums throughout.

~~~bash
set -euo pipefail
src="$PWD/research/rainbow"
out=$(mktemp -d)
c++ -O3 -std=c++17 -fPIC -Drainbow_witness=reference_witness -c "$src/search.cpp" -o "$out/ref.o"
c++ -O3 -std=c++17 -fPIC -DRAINBOW_WIDE_MASK -c "$src/leaf_search.cpp" -o "$out/leaf.o"
c++ -O3 -std=c++17 "$src/uniform_paths.cpp" "$out/leaf.o" "$out/ref.o" -o "$out/make"
c++ -O3 -std=c++17 "$src/check_uniform_paths.cpp" -o "$out/check"
for k in 2 3 {5..43}; do
    "$out/make" "$k" > "$out/neutral$k"
    "$out/check" "$k" < "$out/neutral$k"
done
(cd "$out" && shasum -a 256 -c "$src/uniform-paths.sha256")
python3 -B -m research.rainbow.check_uniform_grafts "$out" {2..43}
c++ -shared "$out/leaf.o" "$out/ref.o" -o "$out/search.so"
python3 -B -m research.rainbow.check_matched_chains "$out/search.so" {3..45..2}
~~~
