// Decode every supplied necklace, its actual cyclic offsets, and its labeling.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>

using Count=std::uint64_t;

Count necklaces(int k) {
    Count total=0;
    int S=k*(k-1)/2;
    for (int j=0;j<k;++j) {
        int d=std::gcd(k,j), t=k/d;
        for (int c=0;c<k;++c) {
            if (t*c%k) continue;
            int target=S-d*c*t*(t-1)/2;
            if (d==1) {
                if (target%k==0) ++total;
            } else if (target%t==0) {
                Count size=t;
                for (int a=0;a<d-2;++a) size*=k;
                total+=size;
            }
        }
    }
    if (total%k) throw std::logic_error("Burnside total");
    return total/k;
}

Count read(const unsigned char* bytes) {
    Count v=0;
    for (int i=7;i>=0;--i) v=v*256+bytes[i];
    return v;
}

int main(int argc,char** argv) {
    if (argc!=3 && argc!=5) return 2;
    int k=std::stoi(argv[1]);
    if (k<3 || k>12) return 2;
    bool affine=argc==5;
    int part=affine?std::stoi(argv[3]):0, parts=affine?std::stoi(argv[4]):1;
    if (parts<1 || part<0 || part>=parts || (affine && k<5)) return 2;
    std::array<int,16> units{};
    int mult[16][16]{},nunits=0;
    for (int u=1;u<k;++u) if (std::gcd(k,u)==1) {
        units[nunits++]=u;
        for (int z=0;z<k;++z) mult[u][z]=u*z%k;
    }
    std::ifstream in(argv[2],std::ios::binary);
    if (!in) return 1;
    Count seen=0,last=0;
    unsigned char row[16];
    while (in.read(reinterpret_cast<char*>(row),16)) {
        Count key=read(row), x=read(row+8);
        if (seen && key<=last) throw std::runtime_error("unordered or duplicate word");
        last=key;
        std::array<int,16> diff{},values{},b{};
        for (int i=k-1;i>=0;--i) {
            diff[i]=key%k; key/=k;
            values[i]=x%16; x/=16;
        }
        if (key || x) throw std::runtime_error("unconsumed high digits");
        for (int j=1;j<k;++j) {
            for (int i=0;i<k;++i) {
                int a=diff[i],other=diff[(j+i)%k];
                if (other<a) throw std::runtime_error("nonminimal rotation");
                if (a<other) break;
            }
            b[j]=(b[j-1]+diff[j-1])%k;
        }
        if (affine) {
            int prefix=0;
            for (int j=0;j<5;++j) prefix=k*prefix+diff[j];
            if (prefix%parts!=part) throw std::runtime_error("record in incorrect shard");
            // The unit-scaled word and its reversal may each be rotated.
            for (int h=0;h<nunits;++h) {
                const int* table=mult[units[h]];
                for (int start=0;start<k;++start) {
                    if (table[diff[start]]<diff[0]) throw std::runtime_error("smaller first digit");
                    if (table[diff[start]]>diff[0]) continue;
                    for (int direction : {-1,1}) {
                        int j=start;
                        for (int i=1;i<k;++i) {
                            j+=direction;
                            if (j<0) j=k-1;
                            if (j==k) j=0;
                            if (table[diff[j]]<diff[i]) throw std::runtime_error("smaller affine word");
                            if (table[diff[j]]>diff[i]) break;
                        }
                    }
                }
            }
        }
        if ((b[k-1]+diff[k-1])%k ||
            (std::accumulate(b.begin(),b.begin()+k,0)-k*(k-1)/2)%k)
            throw std::runtime_error("incorrect offset total or period");
        unsigned verts=0,weights=0;
        for (int i=0;i<k;++i) {
            if (values[i]>=k) throw std::runtime_error("invalid vertex value");
            verts|=1u<<values[i];
            weights|=1u<<((values[(k+i-1)%k]+values[i]+b[i])%k);
        }
        if (verts!=(1u<<k)-1 || weights!=verts) throw std::runtime_error("invalid permutation");
        ++seen;
    }
    if (!in.eof() || in.gcount() || (!affine && seen!=necklaces(k))) throw std::runtime_error("incomplete catalog");
    std::cout<<"k="<<k<<" verified necklaces="<<seen<<"\n";
}
