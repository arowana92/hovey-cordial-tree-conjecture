# A rank for independently checking every rooted forest

The streaming verifier can track one bit for each unordered rooted forest of mass $k-1$. This gives an alternative completeness test for the binary certificates and reduces the global shape storage by a factor of 64. At $k=25$ the bit array takes 258,396,832 bytes. Both modes check the actual vertex permutations, edge sums and boundary-color coverage in every record. [Verifier](spine_verify.cpp) · [Rank implementation](shape_rank.hpp)

## Bijection

Let $F(s,t)$ count forests of total order $s$ whose component orders are at least $t$. The empty forest gives $F(0,t)=1$. Write $T_t=F(t-1,1)$ for the number of rooted trees on $t$ vertices, by deleting their root. If $s>0$ then $F(s,t)=0$ for $t>s$. For $1\le t\le s$,
$$
F(s,t)=\sum_{q=0}^{\lfloor s/t\rfloor}
   \binom{T_t+q-1}{q}F(s-qt,t+1).
$$
Indeed $q$ is the multiplicity of components of order $t$. The two factors choose their multiset and the forest of larger components.

Order these choices by increasing $q$. For fixed $q$, let $0\le r_0\le\cdots\le r_{q-1}<T_t$ be the component ranks. Their multiset index is
$$
h=\sum_{i=0}^{q-1}\binom{r_i+i}{i+1}.
$$
Adding $i$ gives a strictly increasing $q$-subset of $[0,T_t+q-2]$. In colexicographic order all subsets with largest member below $a$ contribute $\binom{a}{q}$ positions. Recursing on the remaining $q-1$ members gives the displayed index. Consequently $h$ takes each value from zero through $\binom{T_t+q-1}{q}-1$ exactly once.

To rank a forest, skip the terms in the recurrence with multiplicity smaller than its $q$, add $hF(s-qt,t+1)$, then add the rank of the remaining forest among the larger components. Absent size classes simply take their $q=0$ block. Each individual tree uses the rank of its own child forest. Induction on mass, and backwards on the minimum size for fixed mass, proves a bijection with the integers from zero to $F(s,t)-1$. The verifier computes it from the parent array, independently of the generator's ordering of parenthesis words.

The verifier atomically sets the corresponding bit and rejects a second occurrence even in another worker. The number of accepted distinct records must equal the independent rooted-tree count. These two conditions prove coverage.

## Checks

The checker compared the rank with sorted bracket strings on 409,113 named parent arrays through mass nine. It also checked 2,732,469 forest words exhaustively through mass 17 and 400,565 sampled words at masses 18 through 25. An additional exhaustive pass assigned distinct ranks in range to **all 2,067,174,645 forests of mass 24**, the entire shape catalog at modulus 25. At modulus 26, the same independent ranker assigned distinct ranks in range to **all 5,759,636,510 forests of mass 25**. These exhaustive passes check the complete catalogs of tree shapes. A labeling theorem also requires verified witnesses and boundary coverage. [Rank checker](check_shape_ranks.cpp)

On four complete modulus-16 shards, the original and bit-array verifiers returned identical counts of 235,381 bases, 217,251 eligible forests, 4,970,751 witness rows and 109,930,416 boundary assignments. Both modes rejected seven deliberate faults on data from modulus 25. The tests exercise a missing catalog, duplicates within and across files, an out-of-range vertex, truncation, an empty record and incomplete boundary coverage. [Fault tests](check_spine_faults.py)

~~~sh
src="$PWD/research/rainbow"
out=$(mktemp -d)
c++ -O3 -std=c++17 -pthread "$src/check_shape_ranks.cpp" -o "$out/ranks"
"$out/ranks"
"$out/ranks" --mass 24 4
"$out/ranks" --mass 25 3
"$out/ranks" --mass 26 3
c++ -O3 -std=c++17 -pthread "$src/spine_verify.cpp" -o "$out/verify"
~~~

To run a full certificate with this mode, append `--rank-bits` to the documented `stream_spine.py` command. With a retained, nontrivial SPN2 shard, run the following from the same shell after setting `shard` to its path.

~~~sh
python3 -B "$src/check_spine_faults.py" "$out/verify" "$shard"
python3 -B "$src/check_spine_faults.py" "$out/verify" "$shard" --rank-bits
~~~

## A 27-label pilot

The complete ordered-cut test at modulus 27 asks for 16,083,734,329 rooted bases, of which 15,825,505,189 have eligible forests. The latter require 92,009,660,290,353 boundary assignments before unit symmetry. The partition recurrence gives these inventory counts. A separate complete run of the topology checker at mass 26 decoded each generated forest word into its parent array, recomputed its independent rank and rejected any repeated or out-of-range rank. It terminated successfully with **16,083,734,329 unique ranks**. This establishes coverage of the entire 27-label shape catalog. The unrestricted audit of labeling witnesses and boundary coverage is still in progress.

One reproducible shard contains 7,670 shapes and 451,990 witness rows. The independent Python checker examined every record, recomputed the distinct weights, and checked all 44,779,592 required boundary inputs across the pilot, including the all-zero inputs for base-only shapes. A separate SSH checkout rebuilt the generator and reproduced the pilot byte for byte. The ranker comparison now includes 450,566 sampled forest words at masses 18 through 26. The native rank verifier rejected each of the seven deliberate faults on this shard. These checks give finite evidence for 27. [Independent partition counts](spine_counts.py) · [Pilot checker](check_spine_samples.py)

Use the build commands from the [25-label reproduction](twenty-five.md#reproduction), then run the following.

~~~sh
"$out/generate" 27 89 2097152 "$out/pilot-27.spn" --ranked-cover
echo "efa34e4fe40468726418bd14afdf6d43bb8605963219f2d7e34b6523a2c905ac  $out/pilot-27.spn" | shasum -a 256 -c -
python3 -B "$src/check_spine_samples.py" "$out/pilot-27.spn" --stride 1
python3 -B "$src/check_spine_faults.py" "$out/verify" "$out/pilot-27.spn" --rank-bits
python3 -B "$src/spine_counts.py" 27
~~~

The full run uses a rank bit array of approximately 1.87 GiB, plus worker memory. It streams witnesses directly through the independent verifier. Successful completion writes the global totals and the hash manifest in the audit directory.

~~~sh
python3 -B "$src/stream_spine.py" 27 8192 10 "$out/generate" "$out/verify" "$out/audit27" --pipe-witnesses --rank-bits
~~~

Shard 271 at the full stride of 8,192 was regenerated separately from a public SSH checkout. Its 1,963,347 shapes and 115,350,817 witness rows matched that shard's generation log in the full run. The native verifier accepted the local records and reached the expected incomplete-catalog check. On 70 sampled forests the independent checker covered 1,263,306 actual boundary inputs using all 6,331 stored permutations in those records. The file has 3,022,681,411 bytes. These checks establish a finite milestone at 27.

~~~sh
"$out/generate" 27 271 8192 "$out/271.spn" --ranked-cover
echo "9ba5238a0b8cc1e8dfe4f122e8305c51322b897cf61eeb31282786c3f0c0f386  $out/271.spn" | shasum -a 256 -c -
python3 -B "$src/check_spine_samples.py" "$out/271.spn" --stride 30000
~~~

## Verifying a single ranked shard and resuming a run

A canonical forest word now has a directly computable position in the stream order. Let the remaining forest have mass $m$ and let $i$ be the first allowed small component type. The table $A(m,i)$ counts completions after that restriction. If the first component has small type $j$, the number of earlier choices is $A(m,i)-A(m,j)$. Add this to the position and continue on the suffix with lower bound $j$. If the first component is larger than half the original mass, it is the sole remaining component. Skip all small-first completions and continue inside its root with no sibling restriction. These rules depend only on the actual bracket word. [Index and decoding routines](ranked_forest.hpp)

For shard $a$ at stride $d$, the verifier recomputes the position of every parsed canonical word and requires the successive values $a,a+d,a+2d,\ldots$ below the independently counted number $N$ of rooted bases. It checks both ends of this sequence and every labeling and boundary orbit. A repeated word would have the same position twice. Consequently the full set of accepted shards contains $N$ distinct valid words, which proves completeness even without assuming that the generator's enumeration is correct. The independent shape-rank bijection above supplies an additional check.

The driver saves each successful verifier report and stream hash by atomic rename after both producer and verifier exit successfully. Run the same command with the same output directory and binaries after an interruption. The final report reconciles all shard counts with the separate partition recurrence. At eight labels an independent full-catalog replay matched all seven shard hashes and both former verification modes. Removing one report and its generator summary required regenerating just that shard. Nine malformed inputs were rejected, including a stream assigned to the wrong shard and missing, transposed or duplicated records. At 27 labels the pilot above matched its published hash and passed the positional check on all 7,670 forests and 451,990 rows. The unrestricted 27-label witness audit remains open. [Restartable driver](stream_ranked_shards.py) · [Regression checks](check_ranked_shards.py)

~~~sh
python3 -B "$src/check_ranked_shards.py" "$out/generate" "$out/verify"
"$out/verify" 27 --ranked-shard 89 2097152 "$out/pilot-27.spn"
python3 -B "$src/stream_ranked_shards.py" 27 8192 10 "$out/generate" "$out/verify" "$out/ranked27"
~~~
