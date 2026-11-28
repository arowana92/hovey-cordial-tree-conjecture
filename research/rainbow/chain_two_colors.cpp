// A full rainbow batch with one two-vertex path and 24 singleton leaves.
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <utility>
#include <vector>

namespace {
using Mask=std::uint32_t;
using Choices=std::vector<std::pair<int,Mask>>;
constexpr int k=27;
constexpr Mask full=(1U<<k)-1;

Mask bit(int x) { return 1U<<x; }
Mask shift(Mask x,int delta) { return ((x<<delta)|(x>>(k-delta)))&full; }

// Keep one witnessing set for each possible number of second-parent leaves.
void combine(Choices& previous,const Choices& block) {
    std::array<bool,k> seen{};
    Choices updated;
    for (auto [n,first] : previous) for (auto [j,second] : block) {
        if (!seen[n+j]) {
            seen[n+j]=true;
            updated.emplace_back(n+j,first|second);
        }
    }
    previous.swap(updated);
}

Choices leaves(Mask used,Mask forbidden,int delta) {
    Choices choices{{0,0}};
    if (!delta) {
        if ((full^used)&forbidden) return {};
        Mask second=0;
        for (Mask unused=full^used;unused;unused&=unused-1) {
            second|=unused&-unused;
            choices.emplace_back(__builtin_popcount(second),second);
        }
        return choices;
    }

    int cycles=std::gcd(k,delta),length=k/cycles;
    for (int root=0;root<cycles;++root) {
        int gap=-1;
        Mask cycle=0;
        for (int i=0;i<length;++i) {
            int v=(root+i*delta)%k;
            cycle|=bit(v);
            if (used&bit(v)) gap=i;
        }
        if (gap<0) {
            if (cycle&forbidden) return {};
            combine(choices,{{0,0},{length,cycle}});
            continue;
        }
        std::vector<int> segment;
        Mask occupied=0;
        for (int i=gap+1;i<=gap+length;++i) {
            int v=(root+i*delta)%k;
            if (!(used&bit(v))) {
                segment.push_back(v);
                occupied|=bit(v);
                continue;
            }
            if (segment.empty()) continue;
            Choices local;
            Mask second=0;
            for (int j=0;j<=int(segment.size());++j) {
                if (j) second|=bit(segment[segment.size()-j]);
                if (!(((occupied^second)|shift(second,delta))&forbidden))
                    local.emplace_back(j,second);
            }
            combine(choices,local);
            if (choices.empty()) return {};
            segment.clear();
            occupied=0;
        }
    }
    return choices;
}
}

int main(int argc,char** argv) {
    if (argc!=2) return 2;
    std::ofstream out(argv[1],std::ios::binary);
    std::uint64_t total=0;
    for (int a=0;a<k;++a) for (int b=0;b<k;++b) for (int p=0;p<k;++p) {
        std::array<std::uint64_t,25> witnesses{};
        int missing=25;
        for (int x=1;x<k && missing;++x) for (int y=1;y<k && missing;++y) {
            if (y==x || y==p) continue;
            Mask used=1|bit(x)|bit(y);
            Mask forbidden=bit((p+x+k-a)%k)|bit((x+y+k-a)%k);
            for (auto [j,second] : leaves(used,forbidden,(k+b-a)%k)) {
                if (witnesses[j]) continue;
                witnesses[j]=(std::uint64_t(second)<<10)|(y<<5)|x;
                --missing;
            }
        }
        if (missing) return 1;
        for (auto row : witnesses) {
            for (int i=0;i<5;++i) out.put((row>>(8*i))&255);
            ++total;
        }
    }
    out.flush();
    if (!out) return 1;
    std::cout<<total<<" witnesses\n";
}
