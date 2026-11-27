// Independently minimize the arm excess needed for each exact branch order.
#include <algorithm>
#include <array>
#include <iostream>
#include <map>
#include <utility>
#include <vector>

using Costs = std::map<int,int>; // order -> minimum excess
using Corridors = std::array<Costs,20>;

void update(Costs& table, int order, int cost) {
    auto [it, inserted] = table.emplace(order,cost);
    if (!inserted) it->second=std::min(it->second,cost);
}

struct Bound {
    int s, z;
    int mass() const { return s-2; }
    int budget() const { return mass()-4*z; }
    bool cut(int n) const { return n%26!=0 && n%26!=s%26; }

    std::vector<Corridors> branches(int small_cap) const {
        int limit=mass()-7;
        std::vector<Corridors> open(limit+1), child(limit+1);
        std::vector<Costs> single(limit+1), many(limit+1);
        const Costs empty{{0,0}};
        for (int leaves=2; leaves<=limit; ++leaves) {
            // Split a collection containing at least two child joints.
            for (int l=2; l<=leaves-2; ++l)
                for (auto [a,x] : single[l])
                    for (const Costs* tail : {&single[leaves-l],&many[leaves-l]})
                        for (auto [b,y] : *tail)
                            if (x+y<=budget()) update(many[leaves],a+b,x+y);

            for (int arms=0; arms<=leaves; ++arms) {
                int rest=leaves-arms;
                for (int w=arms; w<=std::min(mass(),arms*std::min(20,small_cap)); ++w) {
                    auto attach=[&](const Costs& children, int last) {
                        for (auto [order,cost] : children) {
                            int used=cost+std::max(0,w-arms*z);
                            if (used>budget()) continue;
                            int base=1+w+order;
                            for (int e=0; e<=std::min(last,19) && cut(base+e); ++e) {
                                if ((leaves<=6 && base+e>mass()) ||
                                    (leaves<=3 && base+e>small_cap)) break;
                                update(open[leaves][e],base,used);
                            }
                        }
                    };
                    if (!rest && arms>=2) attach(empty,arms==2 ? 25-w : 19);
                    if (arms && rest>=2) {
                        if (arms==1) {
                            for (int e=0; e<=19; ++e) attach(child[rest][e],24-w-e);
                        } else attach(single[rest],19);
                    }
                    if (rest>=4) attach(many[rest],19);
                }
            }
            for (int e=0; e<=19; ++e)
                for (auto [base,cost] : open[leaves][e]) {
                    update(child[leaves][e],base+e,cost);
                    update(single[leaves],base+e,cost);
                }
        }
        return open;
    }

    int maximum() const {
        std::vector<std::vector<Corridors>> tables;
        for (int c=0; c<=mass(); ++c) tables.push_back(branches(c));
        int best=s+26*((1+6*mass()-s)/26);
        for (int a=s-13; a<=mass(); ++a) {
            int b=a==s-13 ? a : mass()-a;
            for (int left=7; left+7<=mass(); ++left)
                for (int right=7; left+right<=mass(); ++right)
                    for (int e=0; e<=19; ++e)
                        for (auto [u,x] : tables[a][left][e])
                            for (auto [v,y] : tables[b][right][e]) {
                                int total=u+v+e;
                                if (x+y<=budget() && total%26==s%26)
                                    best=std::max(best,total);
                            }
        }
        return best;
    }
};

int main() {
    for (int s=23; s<=26; ++s) {
        int best=0;
        for (int z=1; 4*z<=s-2; ++z)
            best=std::max(best,Bound{s,z}.maximum());
        std::cout<<s<<' '<<best<<std::endl;
    }
}
