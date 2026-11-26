# A cordial labeling need not lift through an even factor

**Proposition.** For every $k\ge2$ and every even $s\ge2$, some $k$-cordial labeling of a tree on $sk$ vertices has no $sk$-cordial lift through reduction modulo $k$.

Make a path of $s$ vertices, each labeled zero. Attach one leaf labeled 1 to each path vertex. For every $j$ with $2\le j<k$, add $s$ leaves labeled $j$ at the first path vertex. Every vertex residue occurs $s$ times. The path gives $s-1$ edges of weight zero and the leaves give $s$ edges of every other weight. Thus the specified labeling is $k$-cordial.

A lift at modulus $sk$ must use each vertex residue once and have distinct edge weights. The possible lifts of zero are $ki$ for $0\le i<s$, and the possible lifts of 1 are $1+ki$ for the same indices. Both sets must be used in full. The $s$ edges joining path vertices to their label-1 leaves form a matching covering both fibers. All their weights reduce to 1, so their weights must also run through the full set $1+ki$. Write $S=0+1+\cdots+(s-1)$. Summing those weights in two ways gives
$$
s+2kS\equiv s+kS\pmod{sk}.
$$
This would require $S\equiv0\pmod{s}$, whereas $S\equiv s/2\pmod{s}$ for even $s$.

For $k=s=2$, the example is the four-vertex path with base labels $1,0,0,1$ in path order. An ordinary 4-cordial labeling in path order is $0,2,1,3$, with weights $2,3,0$.

The obstruction fixes the complete base labeling in advance. It rules out an induction that lifts an arbitrary cordial labeling through an even factor. These trees are caterpillars and hence have ordinary cordial labelings for every modulus. [Hovey, *A-cordial graphs*](https://doi.org/10.1016/0012-365X(91)90254-Y)
