// Cover every marked vertex and every prescribed difference to an unused residue.
#include "ranked_forest.hpp"
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

struct Cover {
    int n, budget;
    bool edge_mode;
    std::array<int,k> parent{}, size{}, order{}, label{};
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
                values[i]=(label[i]+label[parent[i]])%k;
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
        if (edge_mode) return false;
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
    bool edge=argc==5 && std::string(argv[4])=="--edge";
    if (argc!=4 && !edge) return 2;
    int n=std::stoi(argv[1]), shard=std::stoi(argv[2]), stride=std::stoi(argv[3]);
    if (n<3 || n>(edge ? 23 : 25) || n%2==0 || stride<1 || shard<0 || shard>=stride) return 2;
    RankedForests forests(n-1,true);
    for (Word rank=shard; rank<forests.count(); rank+=stride) {
        Word word=(Word(1)<<(2*n-1))|(forests[rank]<<1);
        for (int j=0; j<8; ++j) std::putc((word>>(8*j))&255,stdout);
        if (!Cover(n,word,edge).certify())
            throw std::runtime_error("unresolved marked tree at rank "+std::to_string(rank));
        std::putc(255,stdout);
    }
    return std::fflush(stdout)==0 ? 0 : 1;
}
