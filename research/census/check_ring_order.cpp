// Store the least arm excess for each exact order of a branch or side forest.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <map>
#include <string>
#include <vector>

using Costs = std::vector<std::uint8_t>;
constexpr int absent = 255;
void add(Costs& table, int order, int cost) {
    if (order >= int(table.size())) table.resize(order+1, absent);
    table[order] = std::min<int>(table[order], cost);
}
using Corridors = std::vector<Costs>;
using Branches = std::vector<Corridors>;

struct Bound {
    int k, s, z, paths;
    int mass() const { return s-2; }
    int budget() const { return mass()-paths*z; }
    int run() const { return k-7; }

    Branches branches(int cap) const {
        int limit=mass()-7;
        Branches joined(limit+1, Corridors(run()+1));
        std::vector<Costs> single(limit+1);
        // One complete group of terminal arms and any count of nonterminal branches.
        std::vector<std::vector<Costs>> bushes(limit+1,std::vector<Costs>(limit+1));
        int limb=std::min(run()+1,cap);
        for (int q=0; q<=limit; ++q) for (int w=q; w<=std::min(mass(),q*limb); ++w) {
            int cost=std::max(0,w-q*z);
            if (cost<=budget()) add(bushes[1][q],w,cost);
        }
        for (int tips=2; tips<=limit; ++tips) {
            // Admit branches with one more leaf into the side-forest catalog.
            int new_size=tips-1;
            if (new_size>=2) {
                auto& rows=bushes[new_size];
                rows=bushes[new_size-1];
                for (int q=new_size; q<=limit; ++q)
                    for (int i=0; i<int(single[new_size].size()); ++i) if (single[new_size][i]<=budget())
                        for (int j=0; j<int(rows[q-new_size].size()); ++j) {
                            int cost=single[new_size][i]+rows[q-new_size][j];
                            if (cost<=budget() && (q>6 || i+j<=mass())) add(rows[q],i+j,cost);
                        }
            }
            auto put=[&](int base,int used,int last) {
                for (int e=0; e<=std::min(run(),last); ++e) {
                    int n=base+e;
                    if (n%k==0 || n%k==s%k || (tips<=6 && n>mass()) ||
                        (tips<=3 && n>cap)) break;
                    add(joined[tips][e],n,used);
                    add(single[tips],n,used);
                }
            };
            // Follow a child direction with the most leaves. When all directions
            // are terminal arms, follow a longest arm instead.
            for (int largest=1; largest<tips; ++largest) {
                int q=tips-largest;
                const auto& bush=bushes[largest][q];
                for (int m=0; m<int(bush.size()); ++m) if (bush[m]<=budget()) {
                    bool ring=q<=4 && (q>=2 || k%2==0) && k-m>=3;
                    if (largest==1) {
                        for (int d=1; d<=limb && m+d<=mass(); ++d) if (m<=q*d) {
                            int cost=std::max(0,m+d-tips*z);
                            if (cost<=budget()) put(1+m+d,cost,ring ? k-1-m-d : run());
                        }
                    } else for (int g=0; g<=run(); ++g) {
                        int last=ring ? k-2-m-g : run();
                        if (last<0) continue;
                        const auto& child=joined[largest][g];
                        for (int n=0; n<int(child.size()); ++n) {
                            int cost=bush[m]+child[n];
                            if (cost<=budget()) put(1+m+n,cost,last);
                        }
                    }
                }
            }
        }
        return joined;
    }

    int maximum() const {
        int first=s+1-k/2;
        std::map<int,Branches> tables;
        int best=s+k*((1+6*mass()-s)/k);
        for (int a=first-1; a<=mass(); ++a) {
            int b=a<first ? a : mass()-a;
            for (int cap : {a,b}) if (!tables.count(cap)) tables.emplace(cap,branches(cap));
            for (int l=7; l+7<=mass(); ++l) for (int r=7; l+r<=mass(); ++r) {
                for (int e=0; e<=run(); ++e) {
                    const Costs& left=tables.at(a)[l][e];
                    const Costs& right=tables.at(b)[r][e];
                    for (int i=0; i<int(left.size()); ++i) if (left[i]<=budget()) {
                        int residue=(s-i+e)%k;
                        if (residue<0) residue+=k;
                        for (int j=residue; j<int(right.size()); j+=k)
                            if (left[i]+right[j]<=budget()) best=std::max(best,i+j-e);
                    }
                }
            }
        }
        return best;
    }
};

int main(int argc,char** argv) {
    int paths=argc==2 ? std::stoi(argv[1]) : 5;
    if (argc>2 || (paths!=4 && paths!=5)) return 2;
    for (int k : {26,27}) for (int s=23; s<=k; ++s) {
        int best=0;
        for (int z=1; paths*z<=s-2; ++z) best=std::max(best,Bound{k,s,z,paths}.maximum());
        std::cout<<k<<' '<<s<<' '<<best<<std::endl;
    }
}
