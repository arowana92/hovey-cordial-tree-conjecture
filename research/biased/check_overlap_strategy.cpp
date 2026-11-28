// Read the policy in increasing state order and test every literal old parent color.
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <set>
#include <stdexcept>
#include <string>

namespace {
constexpr int k=27;
using Mask=std::uint32_t;
using Key=std::uint64_t;
Key key(Mask x,Mask w) { return Key(x)|(Key(w)<<k); }
void require(bool test,const char* message) { if (!test) throw std::runtime_error(message); }

bool all_multiplicities(Mask x,Mask w,int delta,int r) {
    // Start with every available edge of shift zero. Its size equals r here.
    // Follow a shifted edge, then a matched identity edge, from each unmatched source.
    constexpr Mask full=(1U<<k)-1;
    Mask reached=0,front=w&~x;
    while (front) {
        reached|=front;
        Mask destinations=((front<<delta)|(front>>(k-delta)))&full&~w;
        if (destinations&x) return true;
        front=destinations&~reached;
    }
    // Both pure matchings are maximum. Intact cycles contribute zero or d;
    // all other components contribute an uninterrupted interval of counts.
    int cycles=std::gcd(k,delta), length=k/cycles, intact=0;
    for (int root=0;root<cycles;++root) {
        bool touched=false;
        for (int i=0;i<length;++i) touched|=((x|w)>>((root+i*delta)%k))&1U;
        if (!touched) ++intact;
    }
    return !intact || r-intact*length>=length-1;
}

Mask read_mask(std::istream& in) {
    Mask result=0;
    for (int i=0;i<4;++i) {
        int digit=in.get();
        require(digit>=0,"incomplete mask");
        result|=Mask(digit)<<(8*i);
    }
    require((result>>k)==0,"residue outside the group");
    return result;
}
}

int main(int argc,char** argv) {
    if (argc!=5) return 2;
    int steps=std::stoi(argv[1]),delta=std::stoi(argv[2]),target=std::stoi(argv[3]);
    if (steps<1 || steps>7 || delta<0 || delta>=k || target<1 || target>3) return 2;
    std::ifstream in(argv[4],std::ios::binary);
    std::set<Key> reachable{key(1,0)};
    std::uint64_t states=0;
    while (!reachable.empty()) {
        Mask x=read_mask(in),w=read_mask(in);
        require(key(x,w)==*reachable.begin(),"missing or unexpected state");
        reachable.erase(reachable.begin());
        int old=__builtin_popcount(w);
        require(old<steps && __builtin_popcount(x)==old+1,"wrong size of high bins");
        Mask translated=0;
        for (int v=0;v<k;++v) if (x&(1U<<v)) translated|=1U<<((v+delta)%k);
        for (int p=0;p<k;++p) {
            int y=in.get();
            require(y>=0 && y<k,"invalid new label");
            int z=(p+y)%k;
            require(!(x&(1U<<y)) && !(w&(1U<<z)),"incremented a high bin");
            Mask nx=x|(1U<<y), nw=w|(1U<<z);
            int a=__builtin_popcount(nx&nw);
            int b=__builtin_popcount((translated|(1U<<((y+delta)%k)))&nw);
            if (a>=target && b>=target && (delta==0 || a>target || b>target)) continue;
            if (old+1==steps) {
                int r=k-2*steps-1+target;
                require(delta && a==target && b==target && all_multiplicities(nx,nw,delta,r),
                        "missing leaf multiplicity at last step");
            } else {
                reachable.insert(key(nx,nw));
            }
        }
        ++states;
    }
    require(in.peek()==std::char_traits<char>::eof() && !in.bad(),"trailing bytes or read error");
    std::cout<<states<<" states, "<<k*states<<" parent choices\n";
}
