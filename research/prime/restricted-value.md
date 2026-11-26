# A four-variable obstruction to a proposed polynomial lemma

Hegde and Srinivasa Murthy report a prime-modulus result in *A Partial Solution to Cordial Tree Conjecture*. The publisher's abstract states the range $n<p$. The author-posted manuscript gives $n\le p$ in Corollary 2.10 and invokes its Lemma 2.6 in the proof of Theorem 2.8. The following calculation concerns the numbered lemma in that manuscript. [Publisher's abstract](https://doi.org/10.1080/09720529.2013.867698) · [Authors' manuscript, pp. 3–6](https://www.researchgate.net/profile/Suresh-Hegde/publication/265390236_A_Partial_Solution_to_Cordial_Tree_Conjecture/links/54ed5dd10cf28f3e6535861f/A-Partial-Solution-to-Cordial-Tree-Conjecture.pdf)

For an injective tuple over $\mathbb F_p$, write
$$
F(a,b,c,d)=1+(a-b)(c-d)^{p-2}.
$$
Since $c\ne d$, this factor vanishes exactly when $a+c=b+d$. Lemma 2.6 asserts that for any proper subset of permutations the product of the corresponding factors can take a nonzero value on an injective tuple. All coordinate domains are the whole field.

Take $n=4$, $p=5$, and use the three permutations in one-line notation $1324,1234,1243$. These form a proper subset of $S_4$ and test all three partitions of four positions into two unordered pairs. Given four distinct field elements, their six unordered sums of two different elements take values in a field of size five. Two sums coincide. Their pairs cannot share an element, by cancellation. Hence one of the three factors is zero for **every** injective tuple. The restricted nonzero value set in the lemma is empty. This example already satisfies the strict inequality $n<p$.

More generally, taking one permutation for each partition of every four positions into two pairs tests whether **all** unordered sums from distinct positions are distinct. This uses only $3\binom n4<n!$ permutations for $n\ge4$. Thus the unrestricted choice of permutation set in the lemma imposes a condition much stronger than distinct sums along the edges of a given tree. The example identifies a gap in the manuscript's derivation of its prime-modulus corollary. Hovey's five-label tree theorem applies to the trees at this modulus. For instance the four-vertex path labeled $0,1,3,2$ has distinct weights $1,4,0$. [Hovey (1991)](https://doi.org/10.1016/0012-365X(91)90254-Y)

[Lean verification](RestrictedValue.lean) evaluates the original cubic factors and proves that their product vanishes for all four distinct residues. It uses kernel evaluation with `decide`. The six-sums argument proves the obstruction independently.

~~~sh
lean research/prime/RestrictedValue.lean
~~~
