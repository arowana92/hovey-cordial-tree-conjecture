// Store the least arm excess for each exact order of a branch or side forest.
#include <algorithm>
#include <tuple>
#include <cstdint>
#include <iostream>
#include <map>
#include <utility>
#include <vector>

using Costs = std::vector<std::uint8_t>;
constexpr int absent = 255;
void add(Costs& table, int order, int cost) {
    if (order >= int(table.size())) table.resize(order+1, absent);
    table[order] = std::min<int>(table[order], cost);
}
using Corridors = std::vector<Costs>;
using Branches = std::vector<Corridors>;

void merge(Costs& out,const Costs& in) {
    if (out.size()<in.size()) out.resize(in.size(),absent);
    for (size_t i=0;i<in.size();++i) out[i]=std::min(out[i],in[i]);
}
// Leaf count and mass beside the chosen direction, and the following corridor.
using Tag=std::tuple<int,int,int>;
using Types=std::map<Tag,Costs>;
struct Bound {
    int k, s, z, paths, ring_leaves;
    int mass() const { return s-2; }
    int budget() const { return mass()-paths*z; }
    int pruning_limit() const { return k==27 ? 7 : 6; }
    bool two_site() const { return k==27 && s==24; }
    bool excluded_union(int w) const { return two_site() && (w==21 || w==22); }
    int run() const { return k-7; }

    Branches branches(int cap, int four_cap) const {
        int limit=mass()-pruning_limit()-1;
        Branches joined(limit+1, Corridors(run()+1));
        std::vector<Costs> single(limit+1);
        std::vector<std::vector<Types>> types(limit+1,std::vector<Types>(run()+1));
        // One complete group of terminal arms and any count of nonterminal branches.
        std::vector<std::vector<Costs>> bushes(limit+1,std::vector<Costs>(limit+1));
        int limb=std::min(run()+1,cap);
        for (int q=0; q<=limit; ++q) for (int w=q; w<=std::min(mass(),q*limb); ++w) {
            int cost=std::max(0,w-q*z);
            if (cost<=budget() && !excluded_union(w)) add(bushes[1][q],w,cost);
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
                            if (cost<=budget() && !excluded_union(i+j) && (q>pruning_limit() || i+j<=mass()))
                                add(rows[q],i+j,cost);
                        }
            }
            auto put=[&](int base,int used,int last,Tag tag) {
                for (int e=0; e<=std::min(run(),last); ++e) {
                    int n=base+e;
                    if (n%k==0 || n%k==s%k || (tips<=pruning_limit() && n>mass()) ||
                        (two_site() && 21<=n && n<=27) || (tips<=3 && n>cap) ||
                        (tips==4 && n>four_cap)) break;
                    add(joined[tips][e],n,used);
                    add(single[tips],n,used);
                    add(types[tips][e][tag],n,used);
                }
            };
            // Follow a child direction with the most leaves. When all directions
            // are terminal arms, follow a longest arm instead.
            for (int largest=1; largest<tips; ++largest) {
                int q=tips-largest;
                const auto& bush=bushes[largest][q];
                for (int m=0; m<int(bush.size()); ++m) if (bush[m]<=budget()) {
                    bool ring=q<=ring_leaves && k-m>=3;
                    if (largest==1) {
                        for (int d=1; d<=limb && m+d<=mass(); ++d) if (m<=q*d) {
                            int cost=std::max(0,m+d-tips*z);
                            Tag tag=q<ring_leaves ? Tag{q,m,d-1} : Tag{ring_leaves,0,0};
                            if (cost<=budget()) put(1+m+d,cost,ring ? k-1-m-d : run(),tag);
                        }
                    } else for (int g=0; g<=run(); ++g) {
                        int last=ring ? k-2-m-g : run();
                        if (last<0) continue;
                        auto use=[&](const Costs& child,int emax,Tag tag) {
                            for (int n=0; n<int(child.size()); ++n) {
                                int cost=bush[m]+child[n];
                                if (cost<=budget()) put(1+m+n,cost,emax,tag);
                            }
                        };
                        if (q>=ring_leaves) {
                            use(joined[largest][g],last,{ring_leaves,0,0});
                            continue;
                        }
                        auto tag=Tag{q,m,g};
                        Corridors choices(run()+1);
                        for (const auto& item : types[largest][g]) {
                            auto [other,f,h]=item.first;
                            int end=std::min(last,run());
                            int low=2+m+g+f;
                            if (q+other<=ring_leaves && low<=k && k-m-f>=3) end=std::min(end,k-1-low-h);
                            if (end>=0) merge(choices[end],item.second);
                        }
                        for (int end=0;end<=run();++end) use(choices[end],end,tag);
                    }
                }
            }
        }
        return joined;
    }

    int maximum() const {
        int first=s+1-k/2;
        std::map<std::pair<int,int>,Branches> tables;
        int groups=pruning_limit()==7 ? mass()/4 : 6;
        int best=s+k*((1+groups*mass()-s)/k);
        int min_half=pruning_limit()+1;
        for (int a=first-1; a<=mass(); ++a) {
            int b=a<first ? a : mass()-a;
            int four_cap=two_site() ? a : mass();
            for (int cap : {a,b}) {
                auto key=std::make_pair(cap,four_cap);
                if (!tables.count(key)) tables.emplace(key,branches(cap,four_cap));
            }
            for (int l=min_half; l+min_half<=mass(); ++l) for (int r=min_half; l+r<=mass(); ++r) {
                for (int e=0; e<=run(); ++e) {
                    const Costs& left=tables.at({a,four_cap})[l][e];
                    const Costs& right=tables.at({b,four_cap})[r][e];
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
    int paths=argc>=2 ? std::stoi(argv[1]) : 6;
    int rings=argc==3 ? std::stoi(argv[2]) : 6;
    if (argc>3 || paths<4 || paths>6 || rings<4 || rings>6) return 2;
    for (int k : {26,27}) for (int s=23; s<=k; ++s) {
        int best=0;
        for (int z=1; paths*z<=s-2; ++z) best=std::max(best,Bound{k,s,z,paths,rings}.maximum());
        std::cout<<k<<' '<<s<<' '<<best<<std::endl;
    }
}
