# Attaching any rooted branch through order 22 at 27 labels

**Theorem (computer-assisted).** Give any tree of order one modulo 27 a 27-cordial labeling. At any prescribed vertex, attach a rooted tree on at most 22 new vertices by one edge. The old labels extend. One labeling works on every prefix of every parent-first order of the branch.

Translate the unique old surplus to zero and write $b$ for the old parent label. The old edge counts are all equal. It suffices to give the branch distinct nonzero labels and distinct weights, counting the entering edge. This condition persists on every parent-first prefix. The [seven-tip theorem](seven-tip-27.md) covers every rooted tree with at most seven tips. At exactly 22 free vertices the [single-branch manifest](single-branches-27.sha256) covers every other tip count, from eight through 21. For any shorter branch, extend a tip by a path to order 22 and restrict a witness.

The new audit has 88,398,176 rooted trees, 170,277,064 witness rows and 2,386,750,752 literal boundary inputs. Together the two certificates cover all 97,055,181 rooted trees of order 22. The [native verifier](spine_verify.cpp) checks the actual tree, entering and internal weights, avoidance of zero, every old boundary color under multiplication by units, and the number of distinct canonical trees at each tip count. A [separate partition recurrence](check_single_branches.py) checks every manifest total. The generator bounds the number of nonleaves in each candidate subtree by the maximum for the requested component types. Every nonleaf of a descendant subtree is a nonleaf in the original tree, so the pruning preserves every requested shape.

Consequently, if a least 27-label counterexample has order $27m+23$, neither side of any edge cut can have any of the exact orders **22 through 27**. For 22, the smaller remaining core has order one modulo 27 and the theorem applies. Orders 23 through 27 follow from the [affine and divisible cut theorems](../prime/four-deficits.md). This excludes particular edge cuts, and the unrestricted order-50 case is still open.

## A unit-orbit test at any modulus

Let $k\ge2$, normalize the surplus to zero and assume $b\ne0$. Write $O$ for the orbit of $b$ under multiplication by units modulo $k$. Let $g(O)$ be the largest clockwise distance between consecutive orbit points, with $g(O)=k$ for a singleton. The following tests apply whenever the indicated integer labelings exist. An integer interval labeling uses consecutive vertex labels and distinct consecutive edge sums. The [integer census](../census/README.md) supplies every tree of order at most 27.

* **One connected branch of order $m<k$.** An interval labeling of the branch suffices whenever $2(k-m)\ge g(O)$. Normalize the free vertex interval to $V=[0,m-1]$ and let $W$ be the interval of its $m-1$ edge sums. Write $r$ for the branch root label. Take $z$ outside $V$ and assign each free vertex of label $x$ the new value $u(x-z)$ for a unit $u$. The entering weight avoids the internal weights exactly when $b/u+r+z$ lies outside $W$. Thus it suffices that $O$ meet $W^c-r-V^c$, a cyclic interval of length $\min(k,2(k-m))$. The asserted inequality guarantees an intersection. For $m=1$ the internal weight set is empty.
* **Any forest at one common parent color.** Give the tree augmented by a common old root an interval labeling on $[0,m]$. Write $r$ for that root's label. An affine map of this tree gives the desired extension whenever $r-d$ is unused for some $d\in O$. Indeed choose a unit sending $d$ to $b$, and a translation sending $r-d$ to zero. This succeeds for every possible $r$ if $m<k-g(O\cup\{0\})$. No cyclic interval of width $m$ can then contain a translate of $O\cup\{0\}$, since the least containing width of a finite cyclic set is the circumference minus its largest gap. For $b=0$ simply translate the augmented root to zero at any $m<k$.

In particular, at any **prime** modulus $p$, the connected-branch test covers every $m\le p-1$ and the common-parent test every $m\le p-2$ for nonzero $b$, subject to the stated interval-labeling hypotheses. For the common-parent result at a prime, any injective rainbow labeling of the augmented tree suffices: when there is an unused residue, a nonzero difference from the root can be scaled to any prescribed $b$.

At $k=27$ the guaranteed maxima are as follows. For zero, use the augmented tree in both columns.

| Difference of parent and old surplus | One branch | Forest at a common parent color |
|---|---:|---:|
| Zero | 26 | 26 |
| A unit | 26 | 24 |
| A multiple of three other than a multiple of nine | 24 | 20 |
| 9 or 18 | 22 with the certificate, 18 by the interval test | 17 |

Thus for a least counterexample of order $27m+1+t$, if an edge cuts off exactly $t=23$ or $24$ vertices, the port in **every** cordial labeling of the remaining core must differ from its surplus by 9 or 18. At $t=25,26$ the difference must be a nonzero multiple of three. The limits in the table give sufficient constructions.

At orders 50 through 54 there is also a test for a union of branches at a single joint. If the other branches at that joint have 27 vertices altogether and at most seven rooted tips, the [common-site period theorem](../bounded-degree/prescribed-pair.md) labels those 27 vertices around the joint with its own label as the surplus. The remaining forest has at most 26 vertices at this common parent. Apply the zero row of the table. This test permits arbitrary branching in the remaining forest.

## Sharp interval width for a marked vertex and a missing residue

Let $p$ be the smallest prime divisor of $k$. Over all nonzero unit orbits $O$ modulo $k$, the **largest possible** $g(O\cup\{0\})$ equals
$$
G(k)=
\begin{cases}
2k/3,&6\mid k,\\
k/p,&6\nmid k.
\end{cases}
$$
Thus an interval labeling of the augmented tree on $m+1$ vertices works at every common parent color whenever $m<k-G(k)$. This bound is sharp for using affine images of an arbitrary given marked interval labeling. For a **connected** branch with its own interval labeling, the corresponding sufficient inequality for nonzero parent difference is $m\le k-k/p$, by the [sharp bound without adjoining zero](../census/marked-ring.md). At zero difference use the augmented tree as above.

To prove the formula, write a nonzero orbit as $g$ times the units modulo $t=k/g$. Here $g$ is the gcd of the difference and $k$; every unit modulo $t$ lifts to a unit modulo $k$. Let $q$ be the smallest prime divisor of $t$ and $r=t/q$. When $t$ is prime, adjoining zero gives every residue. If $q\mid r$, every block of $r$ consecutive integers contains a representative of 1 modulo $r$, which is coprime to $t$. Otherwise an even $r$ is impossible, since then $q=2$. For odd $r\ge5$ the pairs $(1,2)$ and $(-2,-1)$ modulo $r$ are disjoint and consist of units. Listing a block of $r$ consecutive integers can break at most one of these two adjacencies. In the other pair at most one integer is divisible by $q$. Thus the block meets a unit modulo $t$. The only remaining composite case is $r=3,q=2$, when $t=6$ and the points $0,1,5$ have maximum gap four.

After scaling, every nonexceptional divisor $t$ contributes a maximum gap at most $k/q\le k/p$. Taking $t=p$ attains $k/p$. When $6\mid k$, taking $t=6$ attains $2k/3$, larger than $k/2$. This proves the formula. The [finite check](check_single_branches.py) independently computes every orbit gap through modulus 1024.

For sharpness, take the orbit attaining $G(k)$. A translate of $-(O\cup\{0\})$ fits in $[0,m]$ as soon as $m\ge k-G(k)$, for $m<k$. Mark the translated zero. A star with center labeled zero and leaves labeled $1,\ldots,m$ realizes this entire interval with consecutive edge sums. For that mark all potential preimages of the unused residue lie in the given vertex interval, so every affine image fails the two prescriptions. This argument concerns one fixed labeling.

In particular **every common-parent forest of up to 26 new vertices extends a prescribed surplus core at every modulus $k\ge79$**, by the integer census through order 27. At $k=78$, the star labeling on $0,\ldots,26$ with mark 13 cannot be affinely transformed to put 13 at that mark while leaving zero unused: the only possible preimages of zero are 0 and 26. The [modulo-27 marked-tree certificate](common-site-27.md) uses multiple labelings and goes beyond the single-interval bound there.

## Reproduction

The earlier six low-tip streams use the deterministic search, and the final eight use bounded restarts. Generation and verification can be piped without keeping the raw streams. The independent checker counts all shapes and also verifies the gap formulas by enumerating the available residues through modulus 41.

~~~bash
set -euo pipefail
out=$(mktemp -d)
r=research/rainbow
c++ -O3 -std=c++17 -Drainbow_witness=reference_witness -c "$r/search.cpp" -o "$out/ref.o"
c++ -O3 -std=c++17 "$r/spine_generate.cpp" "$r/leaf_search.cpp" "$out/ref.o" -o "$out/make"
c++ -O3 -std=c++17 -pthread "$r/spine_verify.cpp" -o "$out/check"
python3 -B -m research.census.check_typed_leaf_streams "$out/make" "$out/check"
for h in {8..13}; do echo "22,$h"; done > "$out/first"
for h in {14..21}; do echo "22,$h"; done > "$out/last"
python3 -B research/census/stream_leaf_profiles.py 27 "$out/first" "$out/make" "$out/check" "$out/a" --workers 2
python3 -B research/census/stream_leaf_profiles.py 27 "$out/last" "$out/make" "$out/check" "$out/b" --workers 2 --restarts
cat "$out/a/manifest.txt" "$out/b/manifest.txt" | cmp - "$r/single-branches-27.sha256"
python3 -B -m research.rainbow.check_single_branches --manifest "$r/single-branches-27.sha256" --intervals
~~~
