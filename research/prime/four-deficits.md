# Sharp modulus thresholds for joining up to four missing residues

Fix an ordinary cordially labeled piece of order $-h\pmod k$ and a cordially labeled core of order $-a\pmod k$, with $a,h\ge1$. The piece's $h$ low vertex residues and $h+1$ low edge residues must each be consecutive with the same unit step modulo $k$. Their starts may differ, and either port may be any vertex. Write $H=a+h$.

| Total deficit $H$ | Every modulus from this value onward admits the join |
|---:|---:|
| 2 | 7 |
| 3 | 13 |
| 4 | 25 |

**Theorem (computer-assisted).** At the indicated moduli, an affine permutation of the piece's labels makes the joined tree cordial, preserving every core label. The core may have fixed edge offsets and the joining edge may have any prescribed offset. Each threshold is sharp for this guarantee on the two given labelings.

At **27 labels**, suppose a least ordinary counterexample has order $27m+s$ with $23\le s\le27$. Neither side of any edge cut can have any of the exact orders $s,s+1,\ldots,27$. The two endpoints are excluded by the [divisible-cut theorem](../divisible-cuts.md). For an interior size, use an integer labeling with consecutive vertex labels and edge sums on that piece and a cordial labeling on the smaller remaining tree. The [integer census](../census/README.md) supplies all required pieces. In particular any tree on 50 through 54 vertices with an edge separating it into two parts of at most 27 vertices is 27-cordial, directly applying the same argument to these two parts. More generally the interval exclusion works at the thresholds above whenever the relevant small piece admits such a labeling. At 28 labels all interior sizes are still at most 27. The unrestricted 27-label conjecture remains open.

## A small divisor can certify every multiple

Normalize the old port plus its bridge offset to zero. Normalize the unit step on the piece to one and its low vertex set to $V=[0,h-1]$. Write $W=f+[0,h]$ for its low edge set and $b$ for its port. An affine map $x\mapsto ux+d$ gives the bridge weight $z=ub+d$, vertex holes $uV+d$ and edge holes $uW+2d$. Write $V_0,W_0$ for the old holes. The final histograms are balanced precisely when the two vertex-hole sets are disjoint, the bridge belongs to at least one edge-hole set, and the two edge-hole sets intersect only possibly at the bridge. This follows by subtracting the holes from complete periods. [Frequency criterion](sparse-deficit-profiles.md)

Let $M\mid k$ with $M>h$, and project all four sets and the port modulo $M$. The core vertex set may shrink to any size at most $a$ and the nonempty core edge set to any size from 1 to $a+1$. The piece's edge holes still project to distinct points. Suppose the projected test accepts some unit and translation. Lift the unit to a unit $U$ modulo $k$ using the surjection of unit groups. This surjection follows by choosing a lift coprime to each prime dividing $k$ but absent from $M$, by the Chinese remainder theorem.

* If the projected bridge fills a projected piece hole, take its unique source $j\in W$ and use $d=U(b-j)$. This makes the actual bridge equal to the actual transformed hole from $j$. All other transformed edge holes project away from any old hole.
* Otherwise lift any old hole $w\in W_0$ at the projected bridge, and use $d=w-Ub$. The two projected edge-hole sets are disjoint in this case. The actual bridge fills $w$.

Both translations reduce to the accepted one modulo $M$. Disjoint vertex holes downstairs imply disjoint vertex holes upstairs. This proves that a projected certificate covering all input supports proves the assertion at every multiple of $M$. Distinct old holes may have the same projection, including at the bridge. The [Lean proof](QuotientBridge.lean) verifies the lifting implication with this asymmetry and the two anchor identities.

## Finite verification of the quotients

| $H$ | Prime divisors handled by the earlier analytic bound | Further sufficient divisors $M$ |
|---:|---|---|
| 2 | $p\ge5$ | 8, 9, 12 |
| 3 | $p\ge11$ | 7, 10, 15, 16, 18, 24, 25, 27 |
| 4 | $p\ge13$ | 11, 14, 20, 21, 25, 27, 30, 32, 35, 36, 45, 48, 49 |

For the prime column, $p>3h$ and $p-1>\max(h(2a+1),a(2h+1))$ for each deficit split in that row. The earlier [prime-power factor bound](interval-deficit-cut.md) therefore works at any $k$ divisible by such a prime. Without such a prime or a listed prime or prime power, $k$ divides 12, 360, or 5040 respectively. Every divisor of that number at or above the stated threshold has one of the displayed sufficient divisors.

The [native checker](check_four_deficits.cpp) enumerates every nonempty projected old edge set of size at most $a+1$, up to multiplying it by a unit. This symmetry fixes the normalized old port. Applying it after the tested affine maps simply permutes the available maps of the piece. For every piece port, starting edge hole and old edge set, keep all maps which pass the edge test. A set of at most $a$ old vertex holes could block them all exactly if it meets every transformed piece vertex-hole set. A family containing $a+1$ pairwise disjoint sets has no such blocker. Otherwise the checker branches on the elements of the first unhit set until it proves the same conclusion. The three totals of projected profiles are 6,315, 683,795 and 92,489,900.

A [second checker](check_four_deficits.py) independently proves all three rows by growing both old low sets from the empty set. At a partial input, choose a map whose bridge already lies in the piece holes or an already chosen old hole. This map can only be spoiled by adding one of its transformed vertex holes to the old vertex set or one of its transformed edge holes other than the bridge to the old edge set. Recurse on each possible addition within the two capacities. If no usable map exists while the old edge set is still empty, try every possible first old hole. Both checkers cover every input. The second also replays 696 joins of actual trees in larger multiples, including cases with all old edge holes projecting to one residue.

## Examples one modulus below each threshold

The old port has label zero. Here $V=[0,h-1]$ and $W=f+[0,h]$ are on the piece.

| $k$ | $V_0$ | $W_0$ | $h$ | $f$ | $b$ |
|---:|---|---|---:|---:|---:|
| 6 | 3 | 2, 4 | 1 | 0 | 3 |
| 12 | 4, 8 | 0, 2, 10 | 1 | 1 | 6 |
| 24 | 8, 16 | 0, 4, 20 | 2 | 2 | 12 |

Realize each side with frequency two outside its holes and one inside. Start with a star containing each vertex residue once. Every remaining vertex of desired label $x$ and desired entering weight $w$ can be attached at an existing vertex of label $w-x$. The checker constructs the six labeled trees and rejects all 252 affine images by counting actual vertices and edges. The obstruction concerns the specified labelings and their affine changes.

~~~bash
set -e
out=$(mktemp -d)
c++ -O3 -std=c++17 research/prime/check_four_deficits.cpp -o "$out/check"
"$out/check"
python3 -B -m research.prime.check_four_deficits
lean research/prime/QuotientBridge.lean
~~~
