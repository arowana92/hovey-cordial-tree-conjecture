// Enumerate trees of the given order with exactly two branching vertices.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>

using Mask=std::uint64_t;
extern "C" int rainbow_witness(int,const int*,int*);

struct Side {
    Mask ends;
    std::vector<int> legs;
    int size;
};

void partitions(int total,int at,int first,Mask ends,
                std::vector<int>& legs,std::vector<Side>& sides) {
    if (at==total) {
        if (legs.size()>=2) sides.push_back({ends,legs,total});
        return;
    }
    for (int length=first; at+length<=total; ++length) {
        legs.push_back(length);
        partitions(total,at+length,length,ends|(Mask(1)<<(at+length-1)),legs,sides);
        legs.pop_back();
    }
}

int main(int argc,char** argv) {
    if (argc!=2) return 2;
    int k=std::stoi(argv[1]);
    if (k<4 || k>63) return 2;
    std::vector<Side> sides;
    std::vector<int> legs;
    for (int n=2; n<=k-4; ++n) partitions(n,0,1,0,legs,sides);
    std::sort(sides.begin(),sides.end(),[](const Side& a,const Side& b){return a.ends<b.ends;});
    long long count=0;
    for (size_t i=0; i<sides.size(); ++i) {
        const auto& a=sides[i];
        if (2*a.size>k-2) break;
        for (size_t j=i; j<sides.size(); ++j) {
            const auto& b=sides[j];
            int gap=k-1-a.size-b.size;
            if (gap<1) break;
            int parents[64],labels[64],n=0;
            auto path=[&](int root,int length) {
                for (int h=0; h<length; ++h) {
                    parents[n]=root;
                    root=n++;
                }
            };
            path(-1,gap);
            for (int length : a.legs) path(-1,length);
            for (int length : b.legs) path(gap-1,length);
            if (rainbow_witness(k,parents,labels)!=1)
                throw std::runtime_error("unresolved two-center base");
            std::cout << a.ends << ' ' << b.ends << ' ';
            for (int v=0; v<n; ++v) std::cout << char('!'+labels[v]);
            std::cout << '\n';
            ++count;
        }
    }
    std::cerr << k << ' ' << count << '\n';
}
