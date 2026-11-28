// Cover every marked vertex and every prescribed difference to an unused residue.
#include "marked_tree_ranks.hpp"
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>

namespace {
using Word = std::uint64_t;
using Mask = std::uint32_t;
constexpr int k = 27;
constexpr Mask all = (Mask(1)<<k)-1;

Mask rotate(Mask values, int shift) {
    return ((values<<shift)|(values>>(k-shift)))&all;
}

// The pair (old joint color, independent leaf-parent color) is defined up
// to simultaneous multiplication by a unit. Its 53 orbits fit in one word.
struct PairOrbits {
    Word subset[k][3][512]{};
    Word full = 0;

    PairOrbits() {
        Word orbit[k][k]{};
        int count = 0;
        for (int a=0; a<k; ++a) for (int b=0; b<k; ++b) {
            if (orbit[a][b]) continue;
            if (count >= 64) throw std::runtime_error("too many color-pair orbits");
            Word flag = Word(1)<<count++;
            for (int u=1; u<k; ++u) if (std::gcd(u,k)==1)
                orbit[u*a%k][u*b%k] = flag;
            full |= flag;
        }
        for (int a=0; a<k; ++a) for (int block=0; block<3; ++block)
            for (int set=1; set<512; ++set)
                subset[a][block][set] = subset[a][block][set&(set-1)]
                                      | orbit[a][9*block+__builtin_ctz(set)];
    }

    Word covered(int joint, Mask leaf_parents) const {
        return subset[joint][0][leaf_parents&511]
             | subset[joint][1][(leaf_parents>>9)&511]
             | subset[joint][2][leaf_parents>>18];
    }
};

struct Cover {
    int n, budget;
    bool edge_mode;
    std::array<int,k> parent{}, canonical_parent{}, size{}, order{}, label{};
    std::array<Mask,k> neighbors{};
    Mask missing = 0;
    std::array<Mask,3> hits{};
    std::uint32_t seed;

    Cover(int vertices, Word word, bool edge): n(vertices), edge_mode(edge), seed((word^(word>>32))|1U) {
        int height = 0, next = 0, stack[k];
        for (int bit=2*n-1; bit>=0; --bit) {
            if ((word>>bit)&1) {
                parent[next] = height ? stack[height-1] : -1;
                stack[height++] = next++;
            } else --height;
        }
        canonical_parent=parent;
        for (int i=1; i<n; ++i) {
            neighbors[i]|=Mask(1)<<parent[i];
            neighbors[parent[i]]|=Mask(1)<<i;
        }
        size.fill(1);
        for (int i=n-1; i>0; --i) size[parent[i]] += size[i];
        std::iota(order.begin(),order.begin()+n,0);
        std::stable_sort(order.begin(),order.begin()+n,[&](int a,int b){ return size[a]>size[b]; });
    }

    unsigned random() {
        seed ^= seed<<13;
        seed ^= seed>>17;
        return seed ^= seed<<5;
    }

    bool place(int j, Mask vertices, Mask weights) {
        if (j==n) { missing=vertices; return true; }
        if (--budget<0) return false;
        int i=order[j], a=label[parent[i]];
        Mask choices=vertices&rotate(weights,k-a), below=(Mask(1)<<(random()%k))-1;
        for (Mask range : {choices&~below,choices&below}) {
            for (; range; range&=range-1) {
                int x=__builtin_ctz(range);
                label[i]=x;
                if (place(j+1,vertices^(Mask(1)<<x),weights^(Mask(1)<<((a+x)%k)))) return true;
                if (budget<0) return false;
            }
        }
        return false;
    }

    void record(Mask every) {
        auto values=label;
        Mask holes=missing;
        if (edge_mode) {
            holes=all;
            for (int i=1; i<n; ++i) {
                values[i]=(label[i]+label[canonical_parent[i]])%k;
                holes^=Mask(1)<<values[i];
            }
        }
        std::array<Mask,3> residues{};
        for (int d=1; d<k; ++d)
            residues[d%9==0 ? 0 : d%3==0 ? 1 : 2] |= rotate(holes,d);
        const auto previous=hits;
        for (int orbit=0; orbit<3; ++orbit)
            for (Mask left=every^hits[orbit]; left; left&=left-1) {
                int v=__builtin_ctz(left);
                if ((residues[orbit]>>values[v])&1) hits[orbit] |= Mask(1)<<v;
            }
        if (previous!=hits)
            for (int v=0; v<n; ++v) std::putc(label[v],stdout);
    }

    void orient(int root) {
        order[0]=root;
        parent[root]=-1;
        int next=1;
        for (int j=0; j<n; ++j) {
            int v=order[j];
            for (Mask rest=neighbors[v]; rest; rest&=rest-1) {
                int w=__builtin_ctz(rest);
                if (w==parent[v]) continue;
                order[next++]=w;
                parent[w]=v;
            }
        }
        size.fill(1);
        for (int j=n-1; j>0; --j) size[parent[order[j]]]+=size[order[j]];
        std::stable_sort(order.begin(),order.begin()+n,[&](int a,int b){ return size[a]>size[b]; });
    }

    bool swap_witness(int root,int spare) {
        std::array<int,k> sites{}, palette{};
        int count=0;
        for (int i=0; i<k-1; ++i) if (i!=root) sites[count++]=i;
        count=0;
        for (int x=1; x<k; ++x) if (x!=spare) palette[count++]=x;
        // Positions past the tree hold unused colors. The root and the reserved
        // residue stay fixed, so every candidate has the requested difference.
        auto collisions = [&]() {
            Mask bins=0;
            for (int i=0; i<n; ++i) if (i!=root)
                bins|=Mask(1)<<((label[i]+label[parent[i]])%k);
            return n-1-__builtin_popcount(bins);
        };
        label[root]=0;
        for (int trial=0; trial<8; ++trial) {
            for (int j=count-1; j>0; --j) std::swap(palette[j],palette[random()%(j+1)]);
            for (int j=0; j<count; ++j) label[sites[j]]=palette[j];
            int score=collisions();
            for (int step=0; score && step<3500; ++step) {
                int a=sites[random()%count], chosen=-1, best=n, ties=0;
                for (int j=0; j<count; ++j) {
                    int b=sites[j];
                    if (a==b) continue;
                    std::swap(label[a],label[b]);
                    int cost=collisions();
                    std::swap(label[a],label[b]);
                    if (cost<best) { best=cost; chosen=b; ties=1; }
                    else if (cost==best && random()%++ties==0) chosen=b;
                }
                if (best>=score && random()%11==0) chosen=sites[random()%count];
                std::swap(label[a],label[chosen]);
                score=collisions();
            }
            if (!score) {
                missing=all;
                for (int i=0; i<n; ++i) missing^=Mask(1)<<label[i];
                return true;
            }
        }
        return false;
    }

    bool port_swaps(int v, int w, int coefficient) {
        // Add a virtual edge whose adjusted sum has to fill the unique hole.
        auto score=[&]() {
            Mask weights=Mask(1)<<((label[v]+label[w]+k-coefficient)%k);
            for (int i=1; i<k; ++i)
                weights|=Mask(1)<<((label[i]+label[canonical_parent[i]])%k);
            return k-__builtin_popcount(weights);
        };
        for (int trial=0; trial<256; ++trial) {
            std::iota(label.begin(),label.end(),0);
            for (int j=k-1; j>0; --j) std::swap(label[j],label[random()%(j+1)]);
            int conflicts=score();
            for (int step=0; conflicts && step<4000; ++step) {
                int a=random()%k, partner=-1, best=k, ties=0;
                for (int b=0; b<k; ++b) if (b!=a) {
                    std::swap(label[a],label[b]);
                    int candidate=score();
                    std::swap(label[a],label[b]);
                    if (candidate<best) { best=candidate; partner=b; ties=1; }
                    else if (candidate==best && random()%++ties==0) partner=b;
                }
                if (best>=conflicts && random()%10==0) partner=random()%k;
                std::swap(label[a],label[partner]);
                conflicts=score();
            }
            if (!conflicts) return true;
        }
        return false;
    }

    bool certify_ports() {
        std::array<std::array<Mask,3>,k> covered{};
        for (int trial=0; trial<100000; ++trial) {
            if (trial && trial%100==0) orient(random()%k);
            budget=trial<1500 ? 220 : 1400;
            label[order[0]]=0;
            if (!place(1,all^1,all)) continue;
            Mask by3[3]{}, by9[9]{}, at[k]{}, unused=all;
            for (int v=0; v<k; ++v) {
                int x=label[v];
                at[x]=Mask(1)<<v;
                by3[x%3]|=at[x];
                by9[x%9]|=at[x];
                if (v) unused^=Mask(1)<<((x+label[canonical_parent[v]])%k);
            }
            int hole=__builtin_ctz(unused);
            bool finished=true, progress=false;
            for (int v=0; v<k; ++v) {
                int r=(hole-label[v]+k)%k;
                // Offset zero suffices by itself. Otherwise the other port
                // must supply each nonzero orbit, possibly on different rows.
                Mask delta[]={at[r]|(all^by3[r%3]), at[r]|(by3[r%3]^by9[r%9]), by9[r%9]};
                for (int j=0; j<3; ++j) {
                    progress|=(delta[j]&~covered[v][j])!=0;
                    covered[v][j]|=delta[j];
                    finished &= covered[v][j]==all;
                }
            }
            if (progress) for (int v=0; v<k; ++v) std::putc(label[v],stdout);
            if (finished) return true;
        }
        // A scarce coefficient can be targeted by a virtual edge with a bias.
        for (int v=0; v<k; ++v) for (int w=v; w<k; ++w) {
            for (int j=0; j<3; ++j) if (!(covered[v][j]&(Mask(1)<<w))) {
                int coefficient=j==0 ? 1 : j==1 ? 3 : 9;
                if (!port_swaps(v,w,coefficient)) return false;
                for (int i=0; i<k; ++i) std::putc(label[i],stdout);
            }
        }
        return true;
    }

    bool certify_pair() {
        static const PairOrbits pairs;
        std::array<Word,k> need_path, need_siblings;
        need_path.fill(pairs.full);
        need_siblings.fill(pairs.full);
        for (int trial=0; trial<(n == 23 ? 100000 : 5000); ++trial) {
            if (trial>=5000 && trial%200==0) orient(random()%n);
            budget = trial<300 ? 180 : trial<5000 ? 800 : 1600;
            label[order[0]]=0;
            if (!place(1,all^1,all)) continue;
            Mask holes=all, shifted[k];
            for (int i=0; i<n; ++i) if (parent[i]>=0) holes ^= Mask(1)<<((label[i]+label[parent[i]])%k);
            for (int x=0; x<k; ++x) shifted[x]=rotate(holes,(k-x)%k);

            // Before translating away the surplus, collect all second-parent
            // colors for an unordered pair of labels x,y. Either can start a path.
            auto add_pair = [&](int x,int y,Mask& path,Mask& siblings) {
                siblings |= shifted[x]&shifted[y];
                Mask internal = Mask(1)<<((x+y)%k);
                if (holes&internal) {
                    Mask other = holes^internal;
                    path |= rotate(other,(k-x)%k)|rotate(other,(k-y)%k);
                }
            };
            Mask all_paths=0, all_siblings=0, paths_without[k]{}, siblings_without[k]{};
            for (Mask low=missing; low; low&=low-1) {
                int x=__builtin_ctz(low);
                for (Mask high=low&(low-1); high; high&=high-1) {
                    int y=__builtin_ctz(high);
                    Mask path=0, siblings=0;
                    add_pair(x,y,path,siblings);
                    all_paths |= path;
                    all_siblings |= siblings;
                    for (Mask rest=missing^(Mask(1)<<x)^(Mask(1)<<y); rest; rest&=rest-1) {
                        int z=__builtin_ctz(rest);
                        paths_without[z] |= path;
                        siblings_without[z] |= siblings;
                    }
                }
            }

            bool changed=false, unfinished=false;
            for (int v=0; v<n; ++v) if (need_path[v]|need_siblings[v]) {
                int r=label[v];
                Word paths=pairs.covered(0,rotate(all_paths,(k-r)%k));
                Word siblings=pairs.covered(0,rotate(all_siblings,(k-r)%k));
                for (Mask spare=missing; spare; spare&=spare-1) {
                    int z=__builtin_ctz(spare), joint=(k+r-z)%k;
                    Mask path=paths_without[z], leaves=siblings_without[z];
                    for (Mask other=missing^(Mask(1)<<z); other; other&=other-1)
                        add_pair(r,__builtin_ctz(other),path,leaves);
                    paths |= pairs.covered(joint,rotate(path,(k-z)%k));
                    siblings |= pairs.covered(joint,rotate(leaves,(k-z)%k));
                }
                changed |= (paths&need_path[v])!=0 || (siblings&need_siblings[v])!=0;
                need_path[v] &= ~paths;
                need_siblings[v] &= ~siblings;
                unfinished |= (need_path[v]|need_siblings[v])!=0;
            }
            if (changed) for (int i=0; i<n; ++i) std::putc(label[i],stdout);
            if (!unfinished) return true;
        }
        return false;
    }

    bool certify_leaf() {
        static const PairOrbits pairs;
        std::array<Word,k> open;
        open.fill(pairs.full);
        for (int trial=0; trial<3500; ++trial) {
            budget = trial<500 ? 150 : 1200;
            label[0] = 0;
            if (!place(1,all^1,all)) continue;
            Mask edge_holes = all;
            for (int i=1; i<n; ++i)
                edge_holes ^= Mask(1)<<((label[i]+label[parent[i]])%k);

            Mask shifted[k], from_unused = 0, different[k]{};
            for (int t=0; t<k; ++t) shifted[t] = rotate(edge_holes,(k-t)%k);
            for (Mask spare=missing; spare; spare&=spare-1) {
                int z = __builtin_ctz(spare);
                from_unused |= shifted[z];
                // z will translate to the old surplus. The extra leaf can
                // use any different missing vertex color x.
                for (Mask choices=missing^(Mask(1)<<z); choices; choices&=choices-1)
                    different[z] |= shifted[(z+__builtin_ctz(choices))%k];
            }
            bool changed = false, unfinished = false;
            for (int v=0; v<n; ++v) if (open[v]) {
                int r = label[v];
                // When z=r the joint is the surplus and x must be missing.
                Word hits = pairs.covered(0,rotate(from_unused,(k-r)%k));
                for (Mask spare=missing; spare; spare&=spare-1) {
                    int z = __builtin_ctz(spare);
                    // Removing the dummy root makes x=r available as well.
                    Mask leaf_parents = different[z] | shifted[(z+r)%k];
                    hits |= pairs.covered((k+r-z)%k,leaf_parents);
                }
                changed |= (open[v]&hits)!=0;
                open[v] &= ~hits;
                unfinished |= open[v]!=0;
            }
            if (changed) for (int i=0; i<n; ++i) std::putc(label[i],stdout);
            if (!unfinished) return true;
        }
        return false;
    }

    bool edge_witness(int child,int difference) {
        int root=canonical_parent[child];
        orient(root);
        auto where=std::find(order.begin()+1,order.begin()+n,child);
        std::rotate(order.begin()+1,where,where+1);
        for (int trial=0; trial<300; ++trial) {
            int a=1+random()%(k-1);
            int forbidden=(a+difference)%k;
            label[root]=0;
            label[child]=a;
            budget=trial<100 ? 300 : 3000;
            if (place(2,all^1^(Mask(1)<<a),all^(Mask(1)<<a)^(Mask(1)<<forbidden))) return true;
        }
        // The two positions beyond the tree hold unused labels for swaps.
        std::array<int,k> sites{},palette{};
        int count=0;
        for (int i=0; i<k; ++i) if (i!=root && i!=child) sites[count++]=i;
        for (int trial=0; trial<32; ++trial) {
            int a=1+random()%(k-1), forbidden=(a+difference)%k;
            label[root]=0;
            label[child]=a;
            int m=0;
            for (int x=1; x<k; ++x) if (x!=a) palette[m++]=x;
            for (int j=count-1; j>0; --j) std::swap(palette[j],palette[random()%(j+1)]);
            for (int j=0; j<count; ++j) label[sites[j]]=palette[j];
            auto score=[&]() {
                Mask weights=0;
                for (int i=1; i<n; ++i) weights|=Mask(1)<<((label[i]+label[canonical_parent[i]])%k);
                return n-1-__builtin_popcount(weights&~(Mask(1)<<forbidden));
            };
            int conflicts=score();
            for (int step=0; conflicts && step<2500; ++step) {
                int v=sites[random()%count], chosen=-1,best=n,ties=0;
                for (int j=0; j<count; ++j) {
                    int b=sites[j];
                    if (v==b) continue;
                    std::swap(label[v],label[b]);
                    int trial_score=score();
                    std::swap(label[v],label[b]);
                    if (trial_score<best) {best=trial_score;chosen=b;ties=1;}
                    else if (trial_score==best && random()%++ties==0) chosen=b;
                }
                if (best>=conflicts && random()%11==0) chosen=sites[random()%count];
                std::swap(label[v],label[chosen]);
                conflicts=score();
            }
            if (!conflicts) return true;
        }
        return false;
    }

    bool certify() {
        const Mask every=((Mask(1)<<n)-1)^Mask(edge_mode);
        int broad_trials=n<=23 ? 2000 : 60;
        for (int trial=0; trial<broad_trials; ++trial) {
            budget=150;
            label[0]=0;
            if (!place(1,all^1,all)) continue;
            record(every);
            if ((hits[0]&hits[1]&hits[2])==every) return true;
        }
        if (edge_mode) {
            constexpr int differences[]={9,3,1};
            for (int j=0; j<3; ++j) while (hits[j]!=every) {
                int child=__builtin_ctz(every^hits[j]);
                if (!edge_witness(child,differences[j])) return false;
                record(every);
            }
            return true;
        }
        // For a remaining mark, fix its color at zero and reserve a missing
        // color at the desired difference. Rerooting keeps the search parent-first.
        constexpr int difference[]={9,3,1};
        for (int orbit=0; orbit<3; ++orbit) while (hits[orbit]!=every) {
            int v=__builtin_ctz(every^hits[orbit]);
            Mask spare=Mask(1)<<(k-difference[orbit]);
            orient(v);
            label[v]=0;
            bool found=false;
            for (int trial=0; trial<300 && !found; ++trial) {
                budget=trial<100 ? 250 : 3000;
                found=place(1,all^1^spare,all);
            }
            if (!found && !swap_witness(v,k-difference[orbit])) return false;
            missing|=spare;
            record(every);
        }
        return true;
    }
};
}

int main(int argc,char** argv) {
    if (argc==2 && std::string(argv[1])=="--ports") {
        Word word;
        while (std::cin>>word) {
            int height=0;
            if (word>>(2*k)) return 2;
            for (int j=2*k-1; j>=0; --j) {
                height+=(word>>j)&1 ? 1 : -1;
                if (height<0 || (!height && j)) return 2;
            }
            if (height) return 2;
            for (int j=0; j<8; ++j) std::putc((word>>(8*j))&255,stdout);
            Cover cover(k,word,false);
            if (!cover.certify_ports())
                throw std::runtime_error("unresolved port pair on tree "+std::to_string(word));
            std::putc(255,stdout);
        }
        return std::cin.eof() && std::fflush(stdout)==0 ? 0 : 1;
    }
    bool edge=argc==5 && std::string(argv[4])=="--edge";
    bool leaf=argc==5 && std::string(argv[4])=="--leaf";
    bool pair=argc==5 && std::string(argv[4])=="--pair";
    if (argc!=4 && !edge && !leaf && !pair) return 2;
    int n=std::stoi(argv[1]), shard=std::stoi(argv[2]), stride=std::stoi(argv[3]);
    if (n<3 || n>((leaf || pair) ? 23 : 25) || (n%2==0 && !pair) || stride<1 || shard<0 || shard>=stride) return 2;
    MarkedTreeRanks forests(n);
    for (Word rank=shard; rank<forests.count(); rank+=stride) {
        Word word=forests.word(rank);
        for (int j=0; j<8; ++j) std::putc((word>>(8*j))&255,stdout);
        Cover cover(n,word,edge);
        bool done = pair ? cover.certify_pair() : leaf ? cover.certify_leaf() : cover.certify();
        if (!done)
            throw std::runtime_error("unresolved marked tree at rank "+std::to_string(rank));
        std::putc(255,stdout);
    }
    return std::fflush(stdout)==0 ? 0 : 1;
}
