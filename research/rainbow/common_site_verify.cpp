// Check the canonical unrooted tree and prove literal color coverage at every mark.
#include "marked_tree_ranks.hpp"
#include <array>
#include <cstdint>
#include <cstdio>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <utility>

namespace {
using Word = std::uint64_t;
using Mask = std::uint32_t;
constexpr int k=27;
constexpr Mask full=(Mask(1)<<k)-1;
using Digits=std::array<int,k>;

void require(bool valid,const char* message) {
    if (!valid) throw std::runtime_error(message);
}

Digits decode(Word word,int n,bool& central_edge) {
    require((word>>(2*n))==0,"bits outside tree");
    Digits parents{}, stack{}, start{};
    std::array<std::pair<int,Word>,k> previous{};
    int count=0, height=0;
    for (int j=2*n-1; j>=0; --j) {
        if ((word>>j)&1) {
            require(count<n && (height || !count),"invalid opening");
            parents[count]=height ? stack[height-1] : -1;
            start[count]=j;
            stack[height++]=count++;
        } else {
            require(height>0,"unexpected closing bracket");
            int v=stack[--height], length=start[v]-j+1;
            std::pair<int,Word> branch{length/2,(word>>j)&((Word(1)<<length)-1)};
            if (height) {
                int p=parents[v];
                require(previous[p]<=branch,"noncanonical children");
                previous[p]=branch;
                if (height==1) {
                    require(length<=n,"root is not a centroid");
                    if (length==n) {
                        require(!central_edge && j==1,"invalid second centroid");
                        central_edge=true;
                    }
                }
            }
        }
    }
    require(count==n && !height,"incomplete tree");
    return parents;
}

Mask rotate(Mask values,int shift) {
    return ((values<<shift)|(values>>(k-shift)))&full;
}

void check_leaf_row(int n,const Digits& labels,Mask vertices,Mask weights,
                    std::array<std::array<Mask,4>,k>& pending,
                    std::array<std::array<Mask,4>,k>& sibling,bool pair) {
    constexpr int anchors[] = {0,1,3,9};
    for (int unit=1; unit<k; ++unit) if (std::gcd(unit,k)==1) {
        Mask spare = 0, unused = 0;
        for (Mask rest=full^vertices; rest; rest&=rest-1)
            spare |= Mask(1)<<(unit*__builtin_ctz(rest)%k);
        for (Mask rest=full^weights; rest; rest&=rest-1)
            unused |= Mask(1)<<(unit*__builtin_ctz(rest)%k);
        for (int v=0; v<n; ++v) {
            int mark = unit*labels[v]%k;
            for (int j=0; j<4; ++j) if (pending[v][j] || sibling[v][j]) {
                int translation = (k+anchors[j]-mark)%k;
                // Apply x -> unit*x + translation to the whole augmented tree.
                // After its root is removed, its color is also a spare source.
                Mask sources = rotate(spare|(Mask(1)<<mark),translation);
                if (!(sources&1)) continue;
                Mask destinations = rotate(unused,2*translation%k);
                for (sources^=1; sources; sources&=sources-1) {
                    int leaf = __builtin_ctz(sources);
                    if (!pair) {
                        pending[v][j] &= ~rotate(destinations,k-leaf);
                        continue;
                    }
                    for (Mask others=sources&(sources-1); others; others&=others-1) {
                        int other=__builtin_ctz(others);
                        sibling[v][j] &= ~(rotate(destinations,k-leaf)&rotate(destinations,k-other));
                        Mask internal=Mask(1)<<((leaf+other)%k);
                        if (internal&destinations) {
                            Mask outside=destinations^internal;
                            pending[v][j] &= ~(rotate(outside,k-leaf)|rotate(outside,k-other));
                        }
                    }
                }
            }
        }
    }
}

Word coverage(int n,const Digits& parents,const std::array<Mask,k>& orbit,bool edge,bool leaf,bool pair) {
    std::array<Mask,k> covered{};
    std::array<std::array<Mask,4>,k> pending{}, sibling{};
    if (leaf || pair) for (int i=0; i<n; ++i) pending[i].fill(full);
    if (pair) for (int i=0; i<n; ++i) sibling[i].fill(full);
    Word rows=0;
    for (int lead=std::getc(stdin); lead!=255; lead=std::getc(stdin)) {
        Digits labels{};
        Mask vertices=0, weights=0;
        for (int i=0; i<n; ++i) {
            int x=i ? std::getc(stdin) : lead;
            require(x>=0 && x<k,"invalid or truncated vertex label");
            require(!((vertices>>x)&1),"repeated vertex label");
            vertices|=Mask(1)<<x;
            labels[i]=x;
            if (i) {
                int weight=(x+labels[parents[i]])%k;
                require(!((weights>>weight)&1),"repeated edge weight");
                weights|=Mask(1)<<weight;
            }
        }
        if (leaf || pair) check_leaf_row(n,labels,vertices,weights,pending,sibling,pair);
        else for (int i=edge ? 1 : 0; i<n; ++i) {
            if (covered[i]==full) continue;
            covered[i]|=1;
            int value=edge ? (labels[i]+labels[parents[i]])%k : labels[i];
            for (Mask holes=full^(edge ? weights : vertices); holes; holes&=holes-1)
                covered[i]|=orbit[(value+k-__builtin_ctz(holes))%k];
        }
        ++rows;
    }
    if (leaf || pair) {
        for (int v=0; v<n; ++v) for (int j=0; j<4; ++j)
            require(!(pending[v][j]|sibling[v][j]),"missing an independent leaf-parent color");
    } else for (int i=edge ? 1 : 0; i<n; ++i)
        require(covered[i]==full,"missing a prescribed residue");
    return rows;
}
}

int main(int argc,char** argv) {
    bool edge=argc==5 && std::string(argv[4])=="--edge";
    bool leaf=argc==5 && std::string(argv[4])=="--leaf";
    bool pair=argc==5 && std::string(argv[4])=="--pair";
    if (argc!=4 && !edge && !leaf && !pair) return 2;
    int n=std::stoi(argv[1]), shard=std::stoi(argv[2]), stride=std::stoi(argv[3]);
    if (n<3 || n>((edge || leaf || pair) ? 23 : 25) || (n%2==0 && !pair) || stride<1 || shard<0 || shard>=stride) return 2;
    MarkedTreeRanks ranks(n);
    std::array<Mask,k> orbit{};
    for (int d=0; d<k; ++d) for (int u=1; u<k; ++u)
        if (std::gcd(u,k)==1) orbit[d]|=Mask(1)<<((d*u)%k);
    Word trees=0, witnesses=0;
    for (Word pos=shard; pos<ranks.count(); pos+=stride) {
        Word word=0;
        for (int j=0; j<8; ++j) {
            int byte=std::getc(stdin);
            require(byte>=0,"truncated tree word");
            word|=Word(byte)<<(8*j);
        }
        bool central_edge=false;
        auto parents=decode(word,n,central_edge);
        require(ranks.index(word,central_edge)==pos,"tree outside shard or out of order");
        witnesses+=coverage(n,parents,orbit,edge,leaf,pair);
        ++trees;
    }
    require(std::getc(stdin)==EOF && !std::ferror(stdin),"trailing data or read error");
    std::cout<<trees<<' '<<witnesses<<'\n';
}
