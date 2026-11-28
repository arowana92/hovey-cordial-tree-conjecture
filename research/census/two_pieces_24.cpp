// Fit two pairs of interval histograms around a shared neighbor and three more vertices.
#include <array>
#include <cstdint>
#include <cstdio>
#include <iostream>
#include <string>
#include <utility>

namespace {
constexpr int k=27;
using Mask=std::uint32_t;
Mask bit(int x) { return Mask(1)<<x; }

struct Holes {
    Mask first, second;
    bool take(int x) {
        Mask v=bit(x);
        if (first&v) { first^=v; return true; }
        if (second&v) { second^=v; return true; }
        return false;
    }
};
Mask vertex[k][k], edge[k][k][k];

struct Search {
    bool fork;
    std::array<unsigned char,7> row{};
    bool finish(int i,Holes v,Holes w) {
        if (i==3) return !(v.first&v.second) && !(w.first&w.second);
        int parent=0;
        if (i>0) {
            int parent_index=fork ? 0 : i-1;
            parent=row[4+parent_index];
        }
        for (Mask left=v.first|v.second;left;left&=left-1) {
            int y=__builtin_ctz(left);
            Holes vs=v,ws=w;
            vs.take(y);
            if (ws.take((parent+y)%k)) {
                row[4+i]=y;
                if (finish(i+1,vs,ws)) return true;
            }
        }
        return false;
    }
    bool orient(int a,int f,int b,int g) {
        // Normalize the common neighbor to zero and the first piece's unit to one.
        // Its length-24 vertex interval must then omit zero in this orientation.
        for (int d=1;d<=3;++d) {
            int first_root=(a+d)%k;
            for (int u=1;u<k;++u) if (u%3) {
                for (int e=0;e<k;++e) {
                    Holes w{edge[1][d][f],edge[u][e][g]};
                    if (!w.take(first_root) || !w.take((u*b+e)%k)) continue;
                    Holes v{vertex[1][d],vertex[u][e]};
                    if (!v.take(0) || !finish(0,v,w)) continue;
                    row[1]=u; row[2]=d; row[3]=e;
                    return true;
                }
            }
        }
        return false;
    }
};
}

int main(int argc,char** argv) {
    if (argc!=2) return 2;
    std::string shape=argv[1];
    if (shape!="path" && shape!="fork") return 2;
    for (int u=1;u<k;++u) if (u%3) for (int d=0;d<k;++d) {
        for (int x=24;x<k;++x) vertex[u][d]|=bit((u*x+d)%k);
        for (int f=0;f<k;++f) for (int x=23;x<k;++x)
            edge[u][d][f]|=bit((u*(x+f)+2*d)%k);
    }
    Search search{shape=="fork"};
    for (int a=0;a<k;++a) for (int f=0;f<k;++f)
        for (int b=0;b<k;++b) for (int g=0;g<k;++g) {
            search.row[0]=0;
            if (!search.orient(a,f,b,g)) {
                search.row[0]=1;
                if (!search.orient(b,g,a,f)) {
                    std::cerr<<"unresolved "<<a<<" "<<f<<" "<<b<<" "<<g<<"\n";
                    return 1;
                }
            }
            if (std::fwrite(search.row.data(),1,7,stdout)!=7) return 1;
        }
    return std::fflush(stdout)!=0;
}
