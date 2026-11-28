# Extending one branch by permuting leaves at its root

Fix a $k$-cordial labeling of a tree of order one modulo $k$, with $k\ge2$. Attach a nonempty rooted tree $A$ by a single edge. Let $n=|A|<k$, put $q=k-n$, and let $j$ count the leaf children of the root of $A$. Add $q$ temporary leaves at this root. Assume the resulting $k$-vertex tree admits a bijective labeling with distinct edge sums modulo $k$.

Translate the old surplus to zero and let $b$ be the color of the old parent of $A$. If $b=0$, the labeling extends. For $b\ne0$, put $m=k/\gcd(b,k)$ and let $p$ be the least prime factor of $m$. **Either of the following suffices** for an extension.

* $q+j\ge k-\varphi(m)$.
* $q\ge2$ and $q+j\ge k/p$.

In each case one labeling of $A$ works for every parent-first prefix. At a prime modulus the first condition always holds, including at $n=k-1$. This uses only a bijective rainbow labeling of the single padded tree. At 27 labels the census supplies this hypothesis for every shape. Hence a branch of at most 25 vertices extends across every boundary color whenever **at most 18 of its vertices remain after removing the root's leaf children**. In particular, a least counterexample of order $26\bmod 27$ cannot contain a 25-vertex side whose entering root has seven or more leaf children. Removing that side would leave a smaller tree of order one modulo 27. [Integer census](../census/README.md) · [Interval criteria for a single branch](single-branches-27.md)

## The construction

Translate the padded labeling so that the branch root has label zero. Let $S$ be the labels of the $q+j$ interchangeable leaf children, including the temporary leaves. Let $h$ be the unique missing edge weight of the padded tree. Every element of $S$ is a weight of a root-to-leaf edge, so $h\notin S$.

Suppose $z\in S$, and either $w=h$ or $w$ is a different element of $S$ with $q\ge2$. Designate $q$ children for deletion, including the child labeled $z$ and also the child labeled $w$ if $w\in S$. Permuting these leaf children gives the original rooted shape after deletion. Its vertex labels omit $z$ and its internal edge weights omit $w$. Choose a unit $u$ with $u(w-z)=b$. Apply $x\mapsto u(x-z)$ to the retained vertices. Their labels are distinct and avoid zero. The entering edge weighs $b-uz=u(w-2z)$, exactly an unused transformed weight. All new edge weights are distinct. This also proves the prefix claim since the old edge counts were uniform and the old vertex counts away from zero were equally low.

When $b=0$, choose one of the temporary leaves and translate its label to zero. Its incident edge has the same weight as the entering edge that replaces it. Discarding the other temporary leaves preserves distinctness and all retained vertices avoid zero.

## Finding two labels

Let $O$ be the residues with gcd $\gcd(b,k)$ with $k$. Two residues of this gcd are unit multiples of each other. Indeed, after division by the gcd they are units modulo $m$, and every unit modulo $m$ lifts to a unit modulo $k$ by the Chinese remainder theorem. In particular $|O|=\varphi(m)$. For the first condition, $S$ and $h-O$ both avoid $h$. Their sizes sum to at least $k$, so they intersect in the other $k-1$ residues. Use $w=h$.

For the second condition the largest subset of $\mathbb Z_k$ containing no pair with difference in $O$ has size exactly $k/p$. To see this, partition into cosets modulo $g=\gcd(b,k)$ and divide the coordinates in each coset by $g$ after subtracting the coset representative. In $\mathbb Z_m$ partition the representatives $0,\ldots,m-1$ into consecutive blocks of size $p$. Every nonzero difference within a block is coprime to $m$, since its absolute value is less than the least prime factor of $m$. An avoiding set contains at most one entry per block. The multiples of $p$ in each reduced coset attain this bound. The set $S\cup\{h\}$ has more than $k/p$ elements. Choose a pair with difference in $O$, orient it so that $z\in S$, and apply the construction. Negation preserves $O$.

On a fixed core of order zero modulo $k$, one additional leaf may attach at an independently chosen old vertex before the branch. Give that leaf the label filling the unique deficient edge weight $D$. If its old parent is colored $c$ and the branch's old parent is colored $a$, the new surplus is $D-c$, so the tests above apply with $b=a+c-D$. At a prime, this gives a branch of any order through $k-1$ together with the independently attached leaf whenever the indicated padded tree has a bijective rainbow labeling.

The verifier independently enumerated the 4,094 subsets containing zero at moduli 2 through 12 to check every maximum avoiding-set size. It also counted actual endpoint sums on 14,587 joined trees through modulus 40, including 1,090 prime cases with $q=1$ and nonzero $b$, and 2,329 cases covered only by the second size bound. The theorem for arbitrary moduli follows from the construction. [Verifier](check_sibling_branches.py)

~~~sh
python3 -B -m research.rainbow.check_sibling_branches
~~~
