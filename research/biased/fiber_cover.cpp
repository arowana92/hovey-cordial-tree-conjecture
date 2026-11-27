// Cover all independent half-turn edge offsets by low-digit labelings.
#include "../rainbow/ranked_forest.hpp"
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <stdexcept>
#include <vector>

extern "C" int fast_offset_witness(int, const int*, const int*, int*);
using Word = std::uint64_t;

namespace {
struct Cover {
    int k,m,n,blocks;
    std::vector<Word> parity;
    std::map<std::vector<int>,std::vector<int>> profiles;
    std::ofstream out;
    Word inputs=0, rows=0, shapes=0;

    Cover(int modulus,const char* path): k(modulus),m(k/2),n(k-1),
        blocks(std::max(1,(1<<(n-1))/64)),parity((1<<(n-1))*blocks),out(path,std::ios::binary) {
        if (!out) throw std::runtime_error("open output");
        out.write("FBL1",4); put(k,1);
        // The high bit of edge zero may be fixed to zero by adding a half-turn
        // to all weights. Bit i of a truth table addresses high-offset word 2i.
        for (int mask=1;mask<(1<<(n-1));++mask) {
            Word low=0;
            for (int i=0;i<64;++i) if (__builtin_parity(mask&i)) low |= Word(1)<<i;
            for (int j=0;j<blocks;++j)
                parity[mask*blocks+j]=__builtin_parity(mask&(64*j)) ? ~low : low;
        }
    }
    void put(Word v,int bytes) {
        for (int i=0;i<bytes;++i) {out.put(static_cast<char>(v&255));v>>=8;}
    }
    const std::vector<int>& colorings(const std::vector<int>& sizes) {
        auto entry=profiles.try_emplace(sizes);
        auto& result=entry.first->second;
        if (!entry.second) return result;
        auto visit=[&](auto& self,int i,int mass,int runs,int last,int raw,int place)->void {
            if (i==int(sizes.size())) {
                for (int u=3;u<m;u+=2) {
                    int image=0;
                    for (int p=1;p<place;p*=m) image+=p*((u*(raw/p%m))%m);
                    if (image<raw) return;
                }
                result.push_back(raw);
                return;
            }
            bool gap=sizes[i]>mass;
            for (int c=0;c<m;++c) {
                if (c!=last && sizes[i]<mass+runs) continue;
                self(self,i+1,mass+sizes[i],runs+(c!=last),c,
                     raw+(gap ? place*c : 0),gap ? place*m : place);
            }
        };
        visit(visit,0,0,0,-1,0,1);
        return result;
    }

    std::vector<Word> witnesses(const std::array<int,16>& par) {
        int total=1<<(n-1);
        std::vector<Word> open(blocks,~Word(0)), answer;
        if (total<64) open[0]=(Word(1)<<total)-1;
        int first=0;
        while (first<blocks) {
            int target=64*first+__builtin_ctzll(open[first]);
            int offset[16]{},x[16]{};
            for (int i=0;i<n;++i) offset[i]=m*((2*target>>i)&1);
            if (fast_offset_witness(k,par.data(),offset,x)!=1)
                throw std::runtime_error("uncovered high assignment "+std::to_string(2*target));
            Word packed=0;
            int prior[8], prior_mask[8]{}, pivots[8]{}, combinations[8]{};
            std::fill_n(prior,m,-1);
            std::vector<int> checks;
            for (int i=0;i<n;++i) {
                int a=x[i]%m, b=par[i]<0 ? -1-par[i] : x[par[i]]%m;
                packed|=Word(a)<<(3*i);
                int w=(a+b)%m, flip=(1<<a);
                if (par[i]>=0) flip^=1<<b;
                flip &= ~1; // the single low-zero free vertex must be the half-turn
                if (prior[w]<0) {prior[w]=i;prior_mask[w]=flip;continue;}
                int mask=flip^prior_mask[w], coeff=(1<<i)|(1<<prior[w]);
                while (mask) {
                    int j=__builtin_ctz(mask);
                    if (!pivots[j]) {pivots[j]=mask;combinations[j]=coeff;break;}
                    mask^=pivots[j];coeff^=combinations[j];
                }
                if (!mask) checks.push_back(coeff>>1);
            }
            answer.push_back(packed);
            for (int j=first;j<blocks;++j) {
                Word hit=open[j];
                for (int mask:checks) {
                    Word p=parity[mask*blocks+j];
                    hit &= __builtin_parity(mask&target) ? p : ~p;
                }
                open[j]^=hit;
            }
            while (first<blocks && !open[first]) ++first;
        }
        return answer;
    }

    void forest(Word word) {
        std::array<int,16> par{},stack{};
        std::vector<int> roots,sizes;
        int depth=0,v=0,leaves=0;bool was_open=false;
        for (int bit=2*n-1;bit>=0;--bit) {
            if (word>>bit&1) {
                if (!depth) roots.push_back(v);
                par[v]=depth ? stack[depth-1] : -1;
                stack[depth++]=v++;was_open=true;
            } else {--depth;leaves+=was_open;was_open=false;}
        }
        for (int j=0;j<int(roots.size());++j)
            sizes.push_back((j+1<int(roots.size()) ? roots[j+1] : n)-roots[j]);
        const std::vector<int> base{0};
        const auto& patterns=3*leaves<=2*(k-2) ? colorings(sizes) : base;
        put(word,8);put(patterns.size(),4);
        for (int raw:patterns) {
            int color=0, digits=raw;
            for (int j=0;j<int(roots.size());++j) {
                if (sizes[j]>roots[j]) {color=digits%m;digits/=m;}
                par[roots[j]]=-1-color;
            }
            auto list=witnesses(par);
            put(raw,2);put(list.size(),4);
            for (auto bits:list) put(bits,8);
            ++inputs;rows+=list.size();
        }
        ++shapes;
    }
};
}

int main(int argc,char** argv) {
    if (argc!=5) return 2;
    int k=std::stoi(argv[1]),i=std::stoi(argv[2]),parts=std::stoi(argv[3]);
    if ((k!=4 && k!=8 && k!=16) || i<0 || i>=parts) return 2;
    RankedForests forests(k-1);
    Cover run(k,argv[4]);
    for (Word j=i;j<forests.count();j+=parts) run.forest(forests[j]);
    run.out.close();
    if (!run.out) return 1;
    std::cout<<run.shapes<<" shapes, "<<run.inputs<<" low inputs, "<<run.rows<<" fiber witnesses\n";
}
