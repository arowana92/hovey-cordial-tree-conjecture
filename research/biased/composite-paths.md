# Arbitrary path offsets at six, eight, nine, ten and twelve labels

**Theorem (computer-assisted).** For each $k\in\{6,8,9,10,12\}$, every finite path has a $k$-cordial labeling for arbitrary independent additive offsets on its edges. With these same offsets allowed, the assertion also holds for every tree in which each original edge is replaced by a path of length at least $k-1$. For a cycle of length $qk$, vertex and edge histograms can both be uniform exactly when the sum of its offsets is $qS$ modulo $k$, where $S=k(k-1)/2$.

These offset results do not require the offsets at neighboring edges to agree in any quotient. On general trees the composite moduli have [independent-offset obstructions](prime-powers.md). The unrestricted-tree ordinary results use zero offsets. [Eight-label theorem](../eight/README.md)

## One finite path test for all lengths

On the cycle of length $k$ ask for a permutation $x$ of the residues such that
$$
y_i=x_{i-1}+x_i+b_i\pmod k
$$
is also a permutation. Necessarily $\sum b_i=-S=S\pmod k$. Conversely an arbitrary path of order $k$ can be closed by choosing its extra offset to give this total. A rainbow path has $k-1$ distinct weights and the closing edge gives the missing weight by summation. Thus the cycle test at the specified total is equivalent to the full path test.

A positive result for every such cycle at a fixed $k$ gives all the conclusions by the [path block and two-arm arguments](prime-paths.md#paths-cycles-and-prescribed-terminals). Those arguments only require the full path test at order $k$. In particular a path adding $k$ vertices and $k$ edges uniformly from a parent $c$ ends at $c+\sum b_i-S$. Subdividing an edge by $k$ vertices replaces its effective offset by a list with total equal to that offset plus $S$. Contracting down to one $k$-cycle gives sufficiency of the stated $qS$ condition. Summation over the original cycle gives necessity.

## Orbit certificates

Adding a common constant to all offsets keeps distinctness. Normalize $b_0=0$ and record cyclic first differences $d_i=b_{i+1}-b_i$. A rotation of the offsets rotates this word. A reflection reverses the word and negates its entries. Simultaneous multiplication of offsets and vertex labels by any unit preserves both permutations. At $6,8,9,10$ the verifier uses just common offset translation and rotation. At twelve it also uses units and reflection. Every representative has an explicit witness checked by recalculating all $k$ actual edge sums on the cycle, including the closing edge.

| Modulus | Offset vectors with $b_0=0$ and the required total | Witness records | SHA-256 of uncompressed stream |
| ---: | ---: | ---: | --- |
| 6 | 1,296 | 222 | `bb847cd0f90584c30badfe4f5ac1090f44c5396327d35df2964fb8ea23df3f0a` |
| 8 | 262,144 | 32,806 | `7e2010009ea66f42e559f89e63b4800e48473a1362495052fb37304f3f2b4461` |
| 9 | 4,782,969 | 531,465 | `9b7d9203384d39c8717add7f4611d0079354cec4080b2fb376c757c38ce933f0` |
| 10 | 100,000,000 | 10,000,212 | `5e8f2a8ad49bc5bbbb0a975727a371544d3704b463d22aed2184919845cb1cb5` |
| 12 | 61,917,364,224 | 645,857,061 | [64-shard SHA-256 manifest](path-offset12.sha256) |

The generator builds cyclic words and solves for the final two differences from periodicity and the sum condition. It backtracks on actual vertex values. Each record has two eight-byte little-endian integers: the first-difference word in base $k$ and the vertex-label word in base 16, each written from left to right with its first digit most significant. Leading zeros are restored to length $k$. The verifier requires sorted, nonrepeating, least representatives and checks the sum constraint and both permutations. At twelve the first five digits interpreted in base twelve determine the shard modulo 64; the verifier checks this assignment too. An earlier build on a finer stride of 4,096 regenerated 277,678 records of shard 17 byte for byte.

**Independent completeness count.** For the rotation-only calculation, consider a rotation by $j$, set $d=\gcd(j,k)$ and $t=k/d$. A fixed normalized offset word has $b_{i+j}=b_i+c$ for some $c$ with $tc=0$. Each orbit on positions has length $t$. Take initial values on its $d$ orbits, using zero on the orbit of position zero. The total offset equals $t$ times the sum of these initial values plus $dc\,t(t-1)/2$. If $d=1$ check the total directly. Otherwise there are $tk^{d-2}$ choices exactly when subtracting the constant from $S$ leaves a multiple of $t$. Summing the fixed counts over all rotations and dividing by $k$ gives the required number of records.

At twelve, a separate Burnside calculation works directly on **unnormalized offsets**. For each dihedral permutation $\sigma$ of positions, each unit $u$ and translation $c$, require $b_{\sigma(i)}=u b_i+c$. On each orbit try all starting values, keep the ones that close, and compute their sums. Convolve these lists modulo $k$ and take the entry at $S$. Average over $2k^2\varphi(k)$ transformations. This independently gives precisely 645,857,061 orbits and uses no necklace enumeration. Distinct valid representatives numbering the entire orbit count prove coverage. [Generator](path_offset_generate.cpp) · [Record verifier](path_offset_verify.cpp) · [Independent orbit count and shard audit](verify_path_shards.py)

## Reproduction

Use a C++17 compiler and Python 3. The twelve-label streams total 10,333,712,976 bytes. All work files in the following commands use a fresh directory.

~~~sh
set -e
src="$PWD/research/biased"
out=$(mktemp -d)
c++ -O3 -std=c++17 "$src/path_offset_generate.cpp" -o "$out/generate"
c++ -O3 -std=c++17 "$src/path_offset_verify.cpp" -o "$out/verify"
for k in 6 8 9 10; do
    "$out/generate" "$k" "$out/$k.bin"
    "$out/verify" "$k" "$out/$k.bin"
    shasum -a 256 "$out/$k.bin"
done
mkdir "$out/twelve"
for i in $(seq 0 63); do
    "$out/generate" 12 "$out/twelve/$i.bin" "$i" 64
done
python3 -B "$src/verify_path_shards.py" 12 64 "$out/twelve" "$out/verify" "$out/manifest" --workers 4
cmp "$out/manifest" "$src/path-offset12.sha256"
~~~
