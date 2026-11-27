# Three-edge paths at adjacent centers

**Theorem.** Join two centers by an edge. At each center attach any number of direct leaves and any number of disjoint three-edge paths. The resulting tree is super edge-magic and cordial at every positive modulus. The two path counts and the two direct leaf counts vary independently. When both centers have a three-edge path, the diameter is seven.

With at most one long path the tree is a caterpillar. Otherwise we give its centers the labels 0 and 1, with vertex interval $[L,U]$ and edge-sum interval $[L+1,U]$. From such a labeling each additional direct leaf at 0 takes the next upper label and each one at 1 takes the next lower label. We can therefore omit direct leaves in the construction. Reducing the two intervals gives cordiality. [Caterpillar labeling](all-radius-two.md) · [Youssef's interval implication](https://ajc.maths.uq.edu.au/pdf/43/ajc_v43_p031.pdf)

## Two orientations of a labeled path

For an integer $d>0$ define the speed in row $i$ to be $-1$ for $i\le-d$, $+1$ for $i\ge d$, and zero otherwise. Write vertex labels as $3i+c$ with $c\in\{0,1,2\}$. Write edge sums as $3i+c$ with $c\in\{1,2,3\}$. A seed is expandable if each column of each interval contains rows $1-d$ through $d-1$ and on each edge the two vertex speeds add to the weight speed.

Choose $s\ge2d-1$ and move every old label and weight by $9s$ times its speed. In each column this moves the outer rows by $3s$. In each enlarged interval precisely the rows $S=\pm[d,d+3s-1]$ are available in every column. Both ends grow by $9s$. The integer interval identity works even when an outer segment of the old interval was empty. [Formal row interval identity](RadiusTwoIntervals.lean)

There is a permutation $v$ of $S$ for which $u\mapsto u+v(u)$ is also a permutation of $S$. The signed Langford theorem gives a partition of $S$ into triples $(u,v,w)$ of sum zero. Cycling each triple gives the permutation, since $u+v=-w$ and $S=-S$. [Jordon and Mitchell, *Signed Langford sequences*](https://doi.org/10.1016/j.disc.2021.112719) · [Derivation of the triple partition](subdivided-double-stars.md#placing-new-branches-in-groups-of-three)

For each $u\in S$, take a path on the three new labels, in order,
$$
3u+1,\qquad 3v(u)+2,\qquad 3u .
$$
Attach its first vertex at center 0 or its last vertex at center 1. The incoming sum is $3u+1$ in either orientation. Its other sums are $3(u+v(u))+3$ and $3(u+v(u))+2$. The vertex slots run through $S$ in columns $1,2,0$, and the weights run through $S$ in columns $1,3,2$. Every new path can switch centers independently. This adds exactly $6s$ paths in any desired split. [Lean check of the three sums](ThreePathFrame.lean)

## Covering every pair of path counts

Write $a\ge b$ for the counts after naming the sides. At $n=a+b\ge24$, choose the unique $m\in[6,11]$ congruent to $n$ modulo six. The certificate gives a defect-two seed with $m$ paths at 0 and none at 1. Since $a\ge12$ and $n-m\ge18$, use $s=(n-m)/6\ge3$ and attach exactly $b$ of the new paths at 1. This proves the theorem for arbitrarily large $n$.

For $2\le n<24$ the verifier exhausts the pairs. It checks a seed directly or checks that a certified seed expands to the requested counts. The archive holds 131 seeds, including eight expandable ones. The verifier recovers the branches from the actual graph and compares its sorted vertex labels and edge sums with the two intervals. It also constructs 240 enlarged trees, covering every split size at the smallest allowed enlargement of each seed, every individual path reversal, and additional direct leaves at both centers. [Certificate](three-path-seeds.jsonl) · [Independent verifier](check_three_path_frames.py)

~~~sh
python3 -B -m research.hub.check_three_path_frames
lean research/hub/ThreePathFrame.lean
lean research/hub/RadiusTwoIntervals.lean
~~~

The exact-cover generator selects one row per path, consuming three distinct vertex slots and three distinct sum slots. Regenerate from the repository root. [Generator](three_path_generate.py) · [Native row search](double_arm_search.cpp)

~~~sh
out=$(mktemp -d)
c++ -O3 -std=c++17 -shared -fPIC research/hub/double_arm_search.cpp -o "$out/search.so"
python3 -B -m research.hub.three_path_generate "$out/search.so" > "$out/seeds.jsonl"
cmp "$out/seeds.jsonl" research/hub/three-path-seeds.jsonl
~~~
