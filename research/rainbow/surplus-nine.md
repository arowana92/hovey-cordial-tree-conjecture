# Nine-label extensions with fixed old labels

**Theorem.** Any prescribed 9-cordial labeling on a tree of order divisible by nine extends across every attached forest. Starting from order one modulo nine, the same is true with precisely **12 exceptions**, all on eight new vertices. Every exception consists of one new center with $c=2$ or $c=5$ children, and $7-c$ singleton leaves. The singleton parents all carry the old surplus color. The center parent differs from it by a unit modulo nine. Thus there are two cases up to unit symmetry. Other sizes, including arbitrarily large forests, always extend.

## The eight-vertex test

Translate the old unique surplus to zero. At eight new vertices the new labels must be the eight nonzero residues and all eight new weights must differ. The [checker](surplus_nine.py) considers all **213,057** eight-vertex boundary-colored forests up to rooted isomorphism. For each parent array it evaluates all $8!$ permutations simultaneously, discarding those with any pair of equal edge weights. The separate multiset enumeration and vertex-by-vertex search cover **37,127** unit orbits. They give the same twelve failures. The [pinned-star criterion](pinned-star.md) also proves each failure arithmetically, since neither 3 nor 6 times a residue can be a unit modulo nine.

Every smaller forest has a witness. An all-singleton packet can be padded by singletons. Otherwise extend a path from a child of an internal vertex, if necessary, to ensure that at least two vertices have children, then pad to eight. No listed failure has two internal vertices. Restrict the labeling to the original forest.

## Divisible cores

Let $D$ be the deficient edge weight in the old divisible core. Attach up to nine vertices at a time. Give one new component root at old parent $p$ the label $D-p$. The enlarged core has uniform edge weights and its new vertex supplies the unique surplus. If the rest of the batch has fewer than eight vertices the preceding result finishes the step.

For a full batch it remains to select that first root. With at least three internal vertices, removing a root leaves at least two internal vertices, so the remaining forest works. With none it consists of singletons. With just one, take that internal vertex, which must be a root. With two internal vertices, take a singleton root if available. If the forest is connected, take its unique root; all newly exposed components have that root as parent, so their common boundary color is its surplus and the exceptions are impossible.

The remaining case consists of two stars with respective child counts $c_1+c_2=7$, both positive. Remove a center so the other star has a child count outside $\{2,5\}$ whenever possible. This leaves just the pair of counts 2 and 5. For these two stars the checker constructs a permutation of all nine labels for every one of the $9^3=729$ ordered choices of the two old parent colors and $D$. It recomputes all nine actual edge sums, adds them to the old profile, and finds one low edge bin and eight high bins in every case. Iterating complete batches followed by a partial one proves the divisible-core theorem. Taking the surplus core to be a singleton also gives a proof for every ordinary tree.

## Larger attachments on a surplus core

A forest of order at least nine contains an ancestor-closed set of eight vertices outside the exceptional shapes. If a path from a root has three vertices, or two roots both have children, keep these vertices and fill to eight; at least two vertices have children. Otherwise the forest consists of singletons and at most one star. If there are $s$ singletons and $c$ children, with $s+c\ge8$, the number of children retained with the center can range from $\max(0,7-s)$ to $\min(7,c)$. This interval contains 0 or 7, or contains two consecutive integers, so one value avoids both 2 and 5. An all-singleton forest is immediate. Label the resulting eight-vertex packet, then use the divisible-core theorem for the rest.

~~~sh
python3 -B -m research.rainbow.surplus_nine
~~~
