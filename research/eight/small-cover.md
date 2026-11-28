# A 3,639-byte certificate for eight labels

**Every finite tree is 8-cordial.** The ordered-cut proof needs just 322 stored permutations across 115 rooted shapes at this modulus. Each permutation may be multiplied by an odd unit when selecting it for an actual boundary. The number 322 is the minimum for this certificate format with those cut conditions. [Download the certificate](small-cover.spn) · [General cut lemma](../rainbow/ordered-cut.md)

## What the certificate proves

Remove a root from each possible eight-vertex tree. On the resulting seven-vertex forest, the all-zero boundary must admit a permutation of $1,\ldots,7$ such that the seven edge sums are distinct, including the attachment edges. Restoring the zero root gives the required order-eight base. For a forest with at most four terminal vertices, the same requirement applies to every boundary coloring that can occur in a size-ordered cut. In order of nondecreasing component size, the boundary color can change only once. Two changes would require at least one free vertex in the first run, two in the second and five in the third. A single change is permitted when the next component size exceeds the total size of its predecessors.

The general induction deletes leaves or retains a connected core of order one modulo eight with such an exterior. Its surplus vertex label is translated to zero, and its edge counts are uniform. The selected permutation keeps the new vertex labels distinct from one another and from zero, while the new weights are distinct. Short exteriors can be padded to seven and the labeling restricted. This proves balance at every order. [Cut, padding and induction](../rainbow/ordered-cut.md) · [Leaf-batch case](../counterexample-bound.md#removing-leaves)

The file contains every one of the 115 forest shapes. Of these, 87 require a total of 3,216 boundary inputs. The other 28 need only the all-zero base, giving 3,244 actual inputs. Independent native and Python checkers validated every record and every required input.

## Why 322 rows are necessary

For each shape, regard its allowed boundary colorings modulo multiplication by $1,3,5,7$ as a finite set. A vertex permutation covers a boundary orbit when it gives distinct edge sums for at least one member. Unit multiplication then gives the corresponding labeling for every member. The program exhausts permutations, records their covered sets and discards sets contained in another. It searches in increasing order of the number of permutations. Choosing an uncovered orbit and trying all sets containing it preserves every possible solution.

| Minimum stored permutations on one shape | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Number of shapes | 28 | 43 | 2 | 21 | 11 | 7 | 3 |

A separate C++ program generates all color tuples, tests the cut inequalities, evaluates all $7!$ literal vertex permutations and collects unit-equivalent permutations. It verifies that the stored rows cover the required set, then branches on inclusion or exclusion to rule out one fewer row on each shape. The minimum concerns the number of stored rows in this reduction. Other inductions and other encodings have their own size measures.

## Reproduce the proof

Run the following from the repository root using Python 3 and a C++17 compiler. The Python generator requires only the standard library. The certificate's SHA-256 is `785648c9cf8c750a0efbd3768510d7760ee3f6cd948955585a61cdfd886f5720`.

~~~sh
set -e
e="$PWD/research/eight"
r="$PWD/research/rainbow"
out=$(mktemp -d)
python3 -B "$e/small_cover.py" "$out/eight.spn"
cmp "$out/eight.spn" "$e/small-cover.spn"
c++ -O3 -std=c++17 -pthread "$r/spine_verify.cpp" -o "$out/coverage"
"$out/coverage" 8 "$out/eight.spn"
python3 -B "$r/check_spine_samples.py" "$out/eight.spn" --stride 1
c++ -O3 -std=c++17 "$e/check_small_cover.cpp" -o "$out/minimum"
"$out/minimum" "$out/eight.spn"
~~~

The Python checker evaluates all 3,244 actual inputs by excluding collisions. The native coverage verifier independently checks completeness of the rooted catalog. The [Lean proof](README.md#the-complete-eight-label-theorem-in-lean) uses the separate divisible-core certificate.
