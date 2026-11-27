// Independent exact search using the two possible endpoint sums of each leaf.
// Output records every attainable first-star order for the given boundaries.
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <string>

using Mask = std::uint64_t;

Mask center_orders(int k,int a,int b,int x,int y) {
    int first=(a+x)%k, second=(b+y)%k;
    if (first==second) return 0;
    int h=(x-y+k)%k, orbits=std::gcd(k,h), period=k/orbits;
    Mask totals=1;
    for (int start=0; start<orbits; ++start) {
        // On the cycle z, z+h, ... a left leaf at z conflicts with a right
        // leaf at z+h. A reserved vertex has no leaf edge and breaks the run.
        std::array<int,64> allowed{};
        int z=start;
        for (int j=0; j<period; ++j,z=(z+h)%k) {
            if (z==0 || z==x || z==y) allowed[j]=4;
            else {
                int l=(x+z)%k, r=(y+z)%k;
                allowed[j]=int(l!=first && l!=second)+2*int(r!=first && r!=second);
                if (!allowed[j]) return 0;
            }
        }
        Mask possible=0;
        for (int initial : {1,2,4}) if (initial & allowed[0]) {
            Mask left=initial==1 ? 2 : 0, other=initial!=1;
            for (int j=1; j<period; ++j) {
                Mask all=left|other;
                Mask next=(allowed[j]&1) ? all<<1 : 0;
                other=(allowed[j]&4) ? all : ((allowed[j]&2) ? other : 0);
                left=next;
            }
            possible |= other | (initial==2 ? 0 : left);
        }
        Mask combined=0;
        while (possible) {
            combined |= totals<<__builtin_ctzll(possible);
            possible &= possible-1;
        }
        totals=combined;
        if (!totals) break;
    }
    return totals<<1; // include the first center
}

int main(int argc,char** argv) {
    if (argc<2 || argc>3) return 2;
    int k=std::atoi(argv[1]);
    if (k<3 || k>63 || (argc==3 && std::string(argv[2])!="--surplus-site")) return 2;
    Mask full=(Mask(1)<<(k-1))-2;
    for (int a=0; a<k; ++a) for (int b=0; b<k; ++b) {
        if (argc==3 && a) continue;
        Mask solved=0;
        for (int x=1; x<k && solved!=full; ++x)
            for (int y=1; y<k && solved!=full; ++y)
                if (x!=y) solved |= center_orders(k,a,b,x,y);
        std::cout<<a<<' '<<b<<' '<<solved<<'\n';
    }
}
