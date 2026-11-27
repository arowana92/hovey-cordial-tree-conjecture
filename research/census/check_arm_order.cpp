// Independent maximum-order calculation. Close the tree across an internal
// connector, gluing two rooted branches that exclude that connector.
#include <algorithm>
#include <array>
#include <iostream>
#include <map>
#include <utility>
#include <vector>

constexpr int k=26, run=19;
using Table = std::map<std::pair<int,int>,int>; // (excess, order residue) -> largest order
using ByLength = std::array<Table,run+1>;

void record(Table& table, int cost, int order) {
    int& previous=table[{cost,order%k}];
    previous=std::max(previous,order);
}
struct Bound {
    int s, threshold, budget;
    void join(Table& result, const Table& a, const Table& b) const {
        for (const auto& [ka,ma] : a) for (const auto& [kb,mb] : b)
            if (ka.first+kb.first<=budget) record(result,ka.first+kb.first,ma+mb);
    }
    bool cut(int order) const { return order%k!=0 && order%k!=s%k; }

    int maximum() const {
        int leaves=s-2, best=0;
        // An open branch excludes its connector but records how many internal
        // vertices it can accept on that connector. Ready children include it.
        std::vector<ByLength> open(leaves+1), ready(leaves+1);
        std::vector<Table> single(leaves+1), multiple(leaves+1);
        Table empty;
        record(empty,0,0);
        for (int l=2; l<=leaves-2; ++l) {
            for (int child=2; child<=l-2; ++child) {
                join(multiple[l],single[child],single[l-child]);
                join(multiple[l],single[child],multiple[l-child]);
            }

            for (int arms=0; arms<=l; ++arms) {
                int rest=l-arms;
                for (int mass=arms; mass<=std::min(leaves,20*arms); ++mass) {
                    int extra=std::max(0,mass-arms*threshold);
                    auto extend=[&](const Table& children, int max_length) {
                        for (const auto& [key,order] : children) {
                            int cost=key.first+extra, base=order+mass+1;
                            if (cost>budget) continue;
                            for (int e=0; e<=std::min(run,max_length) && cut(base+e); ++e)
                                record(open[l][e],cost,base);
                        }
                    };
                    if (rest==0 && arms>=2)
                        extend(empty,arms==2 ? 25-mass : run);
                    if (rest>=2 && arms>=1) {
                        if (arms==1) {
                            for (int child=0; child<=run; ++child)
                                extend(ready[rest][child],24-mass-child);
                        } else {
                            extend(single[rest],run);
                        }
                    }
                    if (rest>=4) extend(multiple[rest],run);
                }
            }
            for (int e=0; e<=run; ++e)
                for (const auto& [key,base] : open[l][e]) {
                    record(ready[l][e],key.first,base+e);
                    record(single[l],key.first,base+e);
                }
        }
        // Every branching skeleton with at least two joints has such an edge.
        for (int left=2; left<=leaves-2; ++left)
            for (int right=2; left+right<=leaves; ++right)
                for (int e=0; e<=run; ++e)
                    for (const auto& [ka,a] : open[left][e])
                        for (const auto& [kb,b] : open[right][e]) {
                            int order=a+e+b;
                            if (ka.first+kb.first<=budget && order%k==s%k)
                                best=std::max(best,order);
                        }
        return best;
    }
};
int main() {
    for (int s=23; s<=26; ++s) {
        int best=0;
        for (int z=1; 4*z<=s-2; ++z)
            best=std::max(best,Bound{s,z,s-2-4*z}.maximum());
        std::cout<<s<<' '<<best<<std::endl;
    }
}
