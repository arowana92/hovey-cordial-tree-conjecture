# Arbitrarily many leaves at a prescribed vertex

**Theorem.** Take any rooted tree $H$ on at most twelve vertices, and attach any number of new leaves to its root. The resulting tree is $k$-cordial for every positive $k$. Both the order of the resulting tree and the modulus are unrestricted.

For example, all trees in which at most five edges avoid a single vertex satisfy the theorem. In fact, upon deleting that vertex's leaf neighbors, each surviving branch with $m$ internal edges has $m+1\le2m$ vertices. The remaining core therefore has at most eleven vertices.

Here is the extension criterion used in the proof. Label a finite core over $\mathbb Z/k$ with its root at zero. Suppose all vertex labels are distinct, with set $A$, and all edge weights are distinct and lie in $A$. As the core is a tree, its weights are exactly $A\setminus\{w\}$ for some $w$. The core itself is cordial. It remains cordial after adding any number of leaves at the root if these leaves receive successive entries of the following periodic list. One period consists of

1. all residues outside $A$ in any order,
2. the single residue $w$,
3. all residues in $A\setminus\{w\}$ in any order.

Indeed, each added leaf contributes its label once to each histogram. In the first part, each new label and weight was absent. When this part is complete every vertex residue occurs once and only edge weight $w$ is missing. Adding $w$ makes every edge count one and increases its vertex count to two. In the last part no label repeats, and each of its vertex and edge counts increases from one to two. A completed period adds one of each residue to both histograms, so the same reasoning applies to every prefix of every later period.

## Uniform witnesses for large moduli

For every rooted tree of order twelve, the archive gives distinct integer labels filling an interval of length twelve (width eleven), with the root labeled zero. The eleven edge sums are distinct integers in the same interval. At every $k\ge12$ reduction modulo $k$ is injective on that interval, so the extension criterion applies simultaneously at every such modulus.

For a smaller core, first grow it to order twelve by adding leaves at the root. Delete those extra leaves from the integer witness. Each deletion removes the same integer from the vertex labels and edge weights because the root label is zero. No other edge uses that weight. The surviving edge weights are therefore still distinct and contained in the surviving vertex labels. All remain in the original interval.

For $k\le11$ the all-tree results apply, including the elementary $k=1$ case. [Primary literature for the small moduli](../../README.md#primary-literature) · [Eight labels](../eight/README.md) · [Nine through eleven labels](../rainbow/README.md)

## Reproduction

The independent verifier grows all rooted trees by leaf insertion, checks that each of the 4,766 shapes occurs exactly once, and checks each integer assignment and edge sum directly. Regeneration uses a separate multiset enumeration. Run from the repository root.

~~~sh
python3 -B -m research.hub.certificate 12 --verify research/hub/order12.jsonl.gz
python3 -B -m research.hub.certificate 12 > /tmp/hovey-hub-regenerated.jsonl
gzip -dc research/hub/order12.jsonl.gz | cmp - /tmp/hovey-hub-regenerated.jsonl
~~~

Each record consists of a parent vector followed by the integer labels in vertex order. The root has index zero and parent $-1$. [Archived witnesses](order12.jsonl.gz) · [Generator and independent checks](certificate.py)
