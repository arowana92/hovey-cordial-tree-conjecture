// Exhaust the four distinct spine labels after fixing the first old label to zero.
// Permuting the pendant leaves preserves the entire histogram.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>

void need(bool ok) { if (!ok) throw std::runtime_error("square-port mismatch"); }
int mod(int x,int k) { return (x%k+k)%k; }

// Use the original tree edges, including every pendant edge and both bridges.
bool valid(int k,int a,int b,std::array<int,4> spine,int port) {
    std::vector<int> vertices(k), net(k);
    for (int x : spine) {
        if (vertices[x]++) return false;
    }
    for (int x=0; x<k; ++x) if (!vertices[x]) {
        ++vertices[x];
        ++net[(spine[0]+x)%k];
    }
    if (port>=0) {
        --net[(a+b)%k];
        ++net[(a+spine[port])%k];
        ++net[(b+spine[port+1])%k];
    }
    for (int i=0; i<4; ++i) if (i!=port) ++net[(spine[i]+spine[(i+1)%4])%k];
    return std::count(net.begin(),net.end(),1)==k;
}

bool predicted(int k,int h,int port) {
    if (port<0) return false;
    if (port==1) return k>=6;
    return k%2==0 && h!=0 && h!=k/2 && 2*h%k!=k/2;
}

int main() {
    std::uint64_t direct=0, built=0;
    for (int k=4; k<=16; ++k) {
        std::array<std::vector<int>,3> found;
        for (auto& row : found) row.resize(k);
        for (int u=0; u<k; ++u) for (int x=0; x<k; ++x) if (x!=u)
            for (int y=0; y<k; ++y) if (y!=u && y!=x)
                for (int z=0; z<k; ++z) if (z!=u && z!=x && z!=y) {
                    std::array<int,4> spine{u,x,y,z};
                    found[0][0] |= valid(k,0,0,spine,-1);
                    for (int b=0; b<k; ++b) for (int port=0; port<=1; ++port) {
                        ++direct;
                        found[port+1][b] |= valid(k,0,b,spine,port);
                    }
                }
        need(!found[0][0]);
        for (int b=0; b<k; ++b) for (int port=0; port<=1; ++port)
            need(bool(found[port+1][b])==predicted(k,mod(-b,k),port));
    }
    for (int k=4; k<=128; ++k) for (int h=0; h<k; ++h) for (int port=0; port<=1; ++port) {
        if (!predicted(k,h,port)) continue;
        int x=0,y=0,z=0,a=0,b=0;
        if (port==0) {
            x=k/2; z=h; y=mod(x-z,k); b=mod(-z,k);
        } else if (h==0) {
            x=2; y=1; z=k-3; a=b=k-1;
        } else {
            x=mod(-h,k); a=h;
            for (y=1; y<k; ++y) {
                z=mod(-x-y,k);
                if (z && x!=y && y!=z && z!=x) break;
            }
            need(y<k);
        }
        need(mod(a-b,k)==h);
        int shift=(3*k/5+h)%k;
        need(valid(k,(a+shift)%k,(b+shift)%k,
                   {shift,(x+shift)%k,(y+shift)%k,(z+shift)%k},port));
        ++built;
    }
    std::cout<<direct<<" exhaustive port tests, "<<built<<" constructed replacements\n";
}
