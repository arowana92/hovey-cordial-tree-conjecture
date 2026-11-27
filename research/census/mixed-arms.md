# Preserving a prescribed core under mixed one- and two-edge arms

**Theorem.** At every positive modulus $k$, a prescribed cordial labeling of a tree of order zero or one modulo $k$ extends across any number of leaves and any number of two-edge paths attached at one vertex. The joint label and the surplus label of an order-one-residue core may differ arbitrarily.

**Local consequence.** In a smallest counterexample of order $qk+s$, $2\le s\le k$, at each branching vertex at most $s-2$ vertices lie on its terminal arms of lengths one and two combined. If every terminal arm has length at most two and there are $B$ branching vertices, this smallest unrestricted counterexample has at most $(B-1)k$ vertices. These bounds hold at every modulus.

## One specified missing label

Translate the joint label to zero. This translates every edge weight by twice the same constant and preserves cordiality. Write an arm as $(a,z)$ with intermediate vertex $a$, tip $z$ and weights $a,a+z$. For any $2b+e=k-1$ we construct $b$ arms and $e$ direct leaves using precisely the vertex residues other than a specified $y$ and giving $k-1$ distinct edge weights. For $y=0$ use the [short interval at the hub](subdivided-star-mark.md#fewer-than-half-a-period-of-two-edge-arms). If $e=0$, then $k$ is odd and the [prescribed-hole theorem](surplus-arms.md) applies. Negating every label allows us to take $1\le y\le k/2$ in the remaining cases.

Write $h=\lfloor b/2\rfloor$. If $b$ is even, index $b$ consecutive tip slots by $j=1,\ldots,b$ and double the indices modulo $b+1$. The displacements are $\pm[1,h]$. If $b$ is odd, use $j=0,\ldots,b-1$ and double modulo $b$, giving displacements $[-h,h]$. Put label $S+j$ on tip $j$ and use its displacement as intermediate label. The internal weights permute the tip slots. Whenever the slots avoid the intermediates, both histograms thus occupy the same $2b$ bins. In either parity, positive displacement $y\le h$ occurs at index $j=y$.

1. **A hole in the intermediate labels.** Take $S=h+1$ and leave $v=-S\pmod k$ vacant. This bin lies strictly past the highest tip and below the negative intermediates if $b$ is odd or $k>2b+2$. Fill the remaining free bins with direct leaves. On the arm $(y,S+y)$ change the intermediate label from $y$ to $v$. Its two weights change from $y,S+2y$ to $v,y$. Thus the vertex hole moves to $y$, and all weights stay distinct.
2. **A hole between intervals.** Place the $b$ tips as high as possible, from $k-h-b$ through $k-h-1$. If $h<y<k-h-b$, leave $y$ empty and fill the rest with direct leaves.
3. **A hole removed from a tip.** Put $q=b+1$, $t=\lfloor q/2\rfloor$. Build a neutral collection on $q$ arms and fill its complementary bins with leaves. If $y$ is a tip, delete it. Its intermediate vertex becomes a direct leaf and only the internal weight disappears. To make $y$ a tip, place $q$ consecutive slots in $[t+1,k-t-1]$ using the same index permutation. Their first slot may be $\max(t+1,y-q+1)$. This works whenever $t<y<k-t$ and the interval contains at least $q$ slots.

If $2q<k$, steps 1 and 2 cover the small values, and every remaining value meets the conditions in step 3. Indeed failure of step 2 with $y>h$ gives $y\ge k-h-b$. If $2q=k$ and $b$ is odd, steps 1 and 2 already cover $y\le q/2+1$. At $k=4$ these are all values. Otherwise $q$ is even and at least four. The [full even-center block](regular-joints.md#an-even-number-of-centers) has intermediate labels $0,1,2,-3$ and $\pm[4,q/2+1]$. Every remaining $y$ is a tip. Apply the deletion in step 3.

Finally suppose $2q=k$ and $b$ is even, so $q$ is odd. Every odd $y$ is a tip in the following full row at modulus $2q$. Put the odd label $2j+1$ at tip $j$ and use intermediate $2((2j\bmod q)-j)$ for $0\le j<q$. The intermediates fill the even bins and the tip weights permute the odds. For even $y\ne0$ let $g=\gcd(k,y)$ and $m=k/g$. Its additive order $m$ is odd and at least three. The residue $z=g(m-1)/2$ has gcd $g$ with $k$ and lies between $k/3$ and $k/2$. Step 3 applies since $q$ is odd and $z>\lfloor q/2\rfloor$. Multiply all labels by a unit carrying $z$ to $y$. Such a unit exists since units modulo $m$ lift to units modulo $k$. This completes the packet construction. [Lean verification of the vacancy and interval placement](MixedArms.lean)

## Arbitrary numbers of arms and leaves

From a core of order one modulo $k$, choose $y$ as its surplus in the translated coordinates. Its old edges are uniform. At odd $k$ the case without leaves is the [pure-arm extension](surplus-arms.md). Otherwise remove neutral groups of $k$ arms, using $(j,j)$ for each residue $j$. If the remainder has more than $(k-1)/2$ arms, put $(k-1)/2$ of them and one leaf in a [neutral coincident-parent block](two-site-arms.md). At even $k\ne4$, remove neutral groups of $k/2$ arms by the full blocks above. These reductions leave $2b<k$ and preserve every difference between frequencies.

Construct the packet with $e=k-1-2b$ leaves. If fewer are required, retain the desired number. All added vertex labels are distinct and avoid the old surplus, and all added weights are distinct. If more are required, take the whole packet. The vertices are now uniform and there is one deficient edge weight $D$. Cycle the extra singles through $D$ followed by the other residues. Every prefix is balanced in both histograms. Undo the translation.

At four, four arms $(0,1),(0,2),(1,2),(3,3)$ add two in every bin of both histograms. Four direct leaves are also neutral. After removing these groups only 64 cases remain: four surplus labels, zero through three arms and zero through three leaves. The [constructor](mixed_arms.py) searches the multisets of arms and leaves and the [independent checker](check_mixed_arms.py) verifies all 64 resulting labelings. Modulus one is immediate.

From a divisible core with at least one direct leaf, first give it the unique label filling the deficient edge bin. The preceding construction finishes. With at least three pure arms use the [regular-joint theorem](regular-joints.md). For one or two pure arms at $k\ge6$, normalize the joint to zero and write $D$ for the deficient weight. Use $(0,x)$ with $x=D$ if $D\ne0$ and $x=1$ otherwise. For a second arm choose $a\notin\{0,x\}$ and $z\notin\{0,x,a,-a,x-a\}$. Both histograms gain distinct entries and the deficient bin is hit. At $k\le5$ the [terminal-path theorem](../rainbow/terminal-paths.md) already handles all populations, including the four-label case.

## A restriction on the local shape of a smallest counterexample

Let $A,B$ count the leaves and two-edge paths at a branching vertex. If $A+2B\ge s-1$ and $A>0$, some selection of whole arms and leaves has size $s-1$. Indeed the intervals $[2j,2j+A]$ for $0\le j\le B$ cover all integer sizes up to $2B+A$. Removing that selection leaves a smaller tree of order one modulo $k$, and its labeling extends back. If $A=0$, remove $s-1$ vertices when this is even, or $s$ when it is odd. In the latter case the smaller tree is divisible. Hence $A+2B\le s-2$. When all terminal arms have length at most two, each branching vertex and its terminal arms together contain at most $s-1$ vertices. The [connector argument using divisible cuts](../rainbow/terminal-paths.md#bounding-a-smallest-counterexample-by-its-branching-vertices) then bounds the order by the claimed multiple of $k$.

The checker verifies 170,857 packets, including every prescribed hole and admissible arm count through modulus 100 and selected cases through 65,536. It also recomputes both histograms on 15,250 whole trees with prescribed path and star cores and checks all 64 four-label tails.

~~~bash
python3 -B -m research.census.check_mixed_arms
lean research/census/MixedArms.lean
~~~
