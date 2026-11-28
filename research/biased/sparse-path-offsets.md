# Two exceptional edge offsets on a path

**Theorem (computer-assisted).** At every modulus from 2 through 32 except 4, a path of any order has a cordial labeling when all edge offsets have one common value with up to two exceptions. The two exceptional positions may be adjacent and their values may coincide. More generally, partition the path in its given order into a nonempty first block of at most $k$ vertices and subsequent blocks of $k$ vertices. It suffices that within each block all but at most two internal offsets share a value. The offsets between blocks are arbitrary.

Subtracting the common offset within an isolated block permutes its edge bins. For a path of order $k$ it therefore suffices to give a permutation of the residues with $k-1$ distinct adjusted weights when at most two offsets are nonzero. The [generator](sparse_path_offsets.cpp) does this for each ordered pair of positions and each simultaneous unit orbit of nonzero values, with separate rows for one or zero exceptions. The [verifier](check_sparse_path_offsets.py) checks the permutation and each actual weight. It expands every orbit at its specified positions, rejects overlaps and compares their total size to
$$
1+(k-1)^2+\binom{k-1}{2}(k-1)^2 .
$$
These are all possible literal path inputs. Across the thirty moduli, 264,039 permutations cover 2,986,162 inputs. At 27 labels the respective counts are 15,029 and 220,377. At modulus four a direct enumeration of all 24 vertex permutations finds exactly four failing triples with at most two nonzero entries, namely $(0,1,0),(0,3,0),(1,0,1),(3,0,3)$.

Pad the first block to $k$ with ordinary edges and restrict its labeling. Its original vertices and adjusted edges remain injectively labeled. Label each subsequent block in isolation, restore its common offset, and let $w$ be its single missing weight. If its entering port has label $p$, the preceding endpoint has label $a$ and their joining edge has offset $b$, translate this block by $a+p+b-w$. The entering weight now fills its translated hole. Each new block contributes exactly one to every vertex and edge bin. This proves the arbitrary-order assertion. Separate results treat arbitrary offsets at primes and at the composite moduli 6, 8, 9, 10 and 12. [Prime path theorem](prime-paths.md) · [Composite path theorem](composite-paths.md)

## Compressing a tree between two ports

At any modulus let a cordially labeled tree of order $qk$ have low edge residue $w$ and two marked vertex labels $p,r$. The two marks may be the same vertex. Insert this tree between old vertices labeled $a,b$, joining the first to port $p$ and the second to port $r$. The effective offset on the old edge is
$$
                       c=p+r-w \pmod k.
$$
Indeed, translate the inserted labels by $d=a+p-w$. Its internal edges and the first joining edge then contribute exactly $q$ copies of each weight. The last joining edge weighs $r+d+b=a+b+c$. Its vertices likewise contribute $q$ copies of each residue. Fixed internal offsets on the inserted tree are allowed when its given labeling is cordial with those offsets. Offsets on the two joining edges add to $c$ by the same calculation.

Consecutive pieces on the same edge have effective offset equal to the sum of their individual offsets. After each piece the label available at the outgoing port is the entering old label plus that piece's effective offset when joins are ordinary. Thus a path in which up to two edges are replaced by any chains of such trees has a cordial labeling throughout the certified range. The blockwise hypothesis of the theorem also permits more replaced edges. In particular, at 27 labels the [integer tree census](../census/README.md) supplies every possible 27-vertex ordinary tree for these insertions. The [sixteen-leaf reduction](../census/sixteen-leaf-corridor.md) uses this for trees of orders 79 through 81.

The independent checker expands two actual labeled trees on short paths, including repeated edge choices and coincident ports, and recounts the resulting vertices and ordinary edges. It checks 2,880 such expansions. The [manifest](sparse-path-offsets.sha256) identifies the uncompressed witness streams. Reproduce all rows from the repository root in Bash.

~~~bash
set -euo pipefail
src="$PWD/research/biased"
out=$(mktemp -d)
c++ -std=c++17 -O3 "$src/sparse_path_offsets.cpp" -o "$out/generate"
for k in {2..3} {5..32}; do
    "$out/generate" "$k" > "$out/sparse-path-$k.txt"
done
(cd "$out" && shasum -a 256 -c "$src/sparse-path-offsets.sha256")
python3 -B "$src/check_sparse_path_offsets.py" "$out" {2..3} {5..32}
~~~
