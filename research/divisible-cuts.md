# Divisible edge cuts bound the size of a smallest counterexample

**Theorem.** Fix $k\ge5$ and write the order of a smallest noncordial tree as $n=mk+s$ with $1\le s\le k$. If it has $L$ leaves, then
$$
m+2\le L\le s-2,\qquad n\le k(L-1)\le k(k-3).
$$
The same bound holds if each edge carries an arbitrary additive offset, when minimality is taken among trees with such offsets. In particular, an exhaustive test through order 598 would suffice at $k=26$.

## Cutting and rejoining

Suppose an edge of the tree separates a component of order $qk$. By minimality both components have cordial labelings with their original offsets. In the divisible component every vertex residue occurs $q$ times and there is a unique edge residue $w$ occurring $q-1$ times. Let $c$ be the label at the other component's port, $a$ the port label on the divisible side, and $b$ the edge offset. Add $d=c+a+b-w$ to every label in the divisible component. Its edge deficit moves to $w+2d$ and the joining edge now has residue $c+a+b+d=w+2d$. The divisible component and the bridge together add $q$ copies to every vertex and edge bin. The two components thus give a cordial labeling of the entire tree. Consequently both sides of **every** edge cut of a minimum counterexample have order nonzero modulo $k$. [Divisible-block extension](binary-fibers.md)

## Counting a tree with no divisible cut

Root the tree at an original leaf. The rooted tree has $L-1$ terminal vertices, since the root has one child. We claim that any descendant subtree with $h$ terminals has at most $kh$ vertices. This holds for a terminal. At a nonterminal, let $h_i$ be the terminal counts of its child subtrees. Every child subtree has nondivisible order, so the inductive bound $kh_i$ improves to $kh_i-1$. With $d\ge1$ children the order of the subtree is therefore at most
$$
1+\sum_i (kh_i-1)=k\sum_i h_i+1-d\le k\sum_i h_i.
$$
At the root this is $n\le k(L-1)$. As $s>0$, it implies $m\le L-2$. The [leaf-deletion argument](counterexample-bound.md#removing-leaves) gives $L<s-1$, including with offsets by treating the parent label plus its edge offset as the prescribed leaf shift. Combining the two inequalities gives the theorem. In particular, the test restricted to any family closed under connected subtrees and having at most $L$ leaves only needs orders at most $k(L-1)$.

The cut inequality itself is sharp. Fix $k\ge3$ and $2\le L\le k+1$. Choose $L$ integers $1\le d_i\le k-1$ summing to $k+1$. This is possible since $L\le k+1\le L(k-1)$. Attach to a center $L$ paths of lengths $k-d_i$. The order is $k(L-1)$, and every edge cuts off a terminal segment of length between one and $k-1$. Its complement also has nondivisible order. These examples establish sharpness of the structural inequality.

## Verification

The [Lean proof](DivisibleCut.lean) formalizes the well-founded bottom-up construction from nondivisible child subtrees, the tree and forest inequalities, and their consequence for $m$ and $n$. The [independent checker](check_divisible_cut.py) inspects both component orders at every edge in rooted tree catalogs through order 12, checks the equality examples through $k=40$, and recomputes both full histograms on joined trees with independently prescribed offsets.

~~~sh
lean research/DivisibleCut.lean
python3 -B -m research.check_divisible_cut
~~~
