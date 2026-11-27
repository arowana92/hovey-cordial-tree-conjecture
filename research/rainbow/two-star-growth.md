# Exactly when two stars can grow cordially at two prescribed sites

**Theorem.** Fix $k\ge2$, a cordial core of order divisible by $k$, and its unique deficient edge weight $D$. Attach two stars of orders $s,t\ge1$ at their centers to prescribed old vertices with labels $a,b$. Their parent vertices may coincide. Ask for one extension and a parent-before-child growth order keeping **every prefix cordial**, including the last one.

If $s+t<k$, such an extension always exists. If $s+t\ge k$, it exists **if and only if** the integer interval
$$
               [\max(1,k-t),\ \min(k-1,s)]
$$
contains some $j$ with $\gcd(j,k)\mid a+b-D$. The criterion is independent of all other features of the core.

At a prime modulus every input works. For composite $k$, let $J(k)$ be the least length of an interval of consecutive integers guaranteed to contain an integer coprime to $k$ (Jacobsthal's function, with this convention). The largest total size allowing any obstruction is exactly $k+J(k)-2$. Every total size from $k$ up to this bound occurs. Thus all sufficiently large two-star attachments extend with every prefix cordial, at **every** modulus.

At 26 the last possible size is **28**. Two stars of order 14 each at old labels 0 and 1 with deficit zero attain it. A core realizing those data is the 26-vertex star centered at zero with all other residues on its leaves. Attaching at its center and its leaf labeled 1 gives a caterpillar, which is ordinarily cordial at every modulus by Hovey's theorem. [Hovey (1991)](https://doi.org/10.1016/0012-365X(91)90254-Y)

## The first period decides all larger sizes

An ancestor-closed first batch can take $j$ vertices of the first star and $k-j$ of the other, including both centers, exactly in the displayed interval. On those vertices the [two-star first-period criterion](../eight/growth-orders.md#two-stars-at-any-modulus) is $\gcd(j,k)\mid a+b-D$. Once both centers are present, everything remaining is a leaf at an already labeled vertex. At each divisible order let one leaf fill the edge deficit. The next at most $k-1$ leaves have a simultaneous assignment of distinct labels avoiding its surplus and distinct weights for any prescribed parent labels. Every prefix of this batch works. This follows by padding the parent shifts to a zero-sum list of $k$ elements, applying Hall's prescribed-differences theorem and translating to put the surplus in a padding position. [Leaf extension proof](../counterexample-bound.md#removing-leaves) · [Hall (1952)](https://doi.org/10.1090/S0002-9939-1952-0050579-7)

If the interval contains no suitable value, both stars have order below $k$. Indeed $s\ge k$ would allow $j=k-1$ and $t\ge k$ would allow $j=1$. Consequently every potential first period must include both centers. The two-star necessity rules out every possible split, proving the converse.

When $s,t<k$ the interval has $s+t-k+1$ elements. For composite $k$, the longest run of nonunits in $1,\ldots,k-1$ has length $J(k)-1$. A run through a multiple of $k$ consists just of that multiple, and at least one nonunit occurs inside the stated range. Every interval of length $J(k)$ therefore works for every deficit. Conversely choose any interval $[L,R]$ of nonunits and set $s=R$, $t=k-L$, $a=0$, $b=1$, $D=0$. The available splits are precisely that interval, and none works. At 26 the even nonunits are isolated from one another except for the run $12,13,14$ containing the sole odd nonunit.

## Below one period

Take the first center with its forced label $x=D-a$ and translate this surplus to zero. Its remaining $s-1$ children are singletons at zero. The other center attaches at $P=b-x$ and has $c=t-1$ children. We need distinct nonzero labels and distinct entering weights. At $P=0$ use the full pinned-star construction and discard unused singletons. If $c=0$, give the second center $-P$ for $P\ne0$ and give the singletons distinct remaining nonzero labels.

Suppose $P\ne0$ and $c>0$. Set $y=-P$ on the second center. Its edge has weight zero. Choose the $c$ labels $B$ of its children so that both $B$ and $B+y$ avoid $0,y$, and $(B+y)\setminus B$ has at most one element. To do this, take whole orbits of addition by $y$ outside its generated subgroup, followed if necessary by a segment of one more such orbit. If that supply is too small, use all outside orbits. In the subgroup of order $h$, the remaining $u$ labels can be $2y,3y,\ldots,(u+1)y$. Here $u\le h-3$ since $c\le k-3$. Thus the segment and its translate avoid both reserved labels.

There are at least $k-c-3$ labels outside $\{0,y\}\cup B\cup(B+y)$. Use any $s-1$ of them on the singleton vertices, whose weights equal their labels. The inequality $s+t<k$ supplies the required room. All edges after the first are distinct and all vertices after the first avoid the surplus. This works for either choice of first center.

## Reproduction

~~~sh
python3 -B -m research.rainbow.check_two_star_growth
~~~

The [constructor](two_star_growth.py) returns the ordered labels for both stars, including any subsequent leaf batches. The [independent replay](check_two_star_growth.py) counts every residue after each vertex. Through eight labels it exhausts permutations of the first period as a separate existence oracle. It checks the extremal interval sizes and positive constructions through 64 labels.
