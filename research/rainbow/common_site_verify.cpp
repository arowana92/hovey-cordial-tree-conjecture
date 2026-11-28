// Check the canonical unrooted tree and prove literal color coverage at every mark.
#include "ranked_forest.hpp"
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

Digits decode(Word word,int n) {
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
                if (height==1) require(length<n,"root is not the unique centroid");
            }
        }
    }
    require(count==n && !height,"incomplete tree");
    return parents;
}

Word coverage(int n,const Digits& parents,const std::array<Mask,k>& orbit) {
    std::array<Mask,k> covered{};
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
        for (int i=0; i<n; ++i) {
            if (covered[i]==full) continue;
            covered[i]|=1;  // Translating the marked vertex to zero always works.
            for (Mask holes=full^vertices; holes; holes&=holes-1)
                covered[i]|=orbit[(labels[i]+k-__builtin_ctz(holes))%k];
        }
        ++rows;
    }
    for (int i=0; i<n; ++i) require(covered[i]==full,"missing an old parent color");
    return rows;
}
}

int main(int argc,char** argv) {
    if (argc!=4) return 2;
    int n=std::stoi(argv[1]), shard=std::stoi(argv[2]), stride=std::stoi(argv[3]);
    if (n<3 || n>25 || n%2==0 || stride<1 || shard<0 || shard>=stride) return 2;
    RankedForests ranks(n-1,true);
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
        auto parents=decode(word,n);
        auto branches=(word>>1)&((Word(1)<<(2*n-2))-1);
        require(ranks.index(branches)==pos,"tree outside shard or out of order");
        witnesses+=coverage(n,parents,orbit);
        ++trees;
    }
    require(std::getc(stdin)==EOF && !std::ferror(stdin),"trailing data or read error");
    std::cout<<trees<<' '<<witnesses<<'\n';
}
