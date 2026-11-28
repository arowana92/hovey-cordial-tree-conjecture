// Emit a literal witness for each pair of parent choices and first path label.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <tuple>
#include <vector>

using Mask = std::uint64_t;

bool finish(int k, int last, Mask vertices, Mask weights, std::vector<int>& row) {
    int previous = row.back();
    if (!vertices) {
        if (!(weights & (Mask(1) << ((previous+last)%k)))) return false;
        row.push_back(last);
        return true;
    }
    for (Mask rest = vertices; rest; rest &= rest-1) {
        int next = __builtin_ctzll(rest);
        Mask edge = Mask(1) << ((previous+next)%k);
        if (!(weights & edge)) continue;
        row.push_back(next);
        if (finish(k,last,vertices ^ (Mask(1)<<next),weights ^ edge,row)) return true;
        row.pop_back();
    }
    return false;
}

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    int k = std::atoi(argv[1]);
    if (k < 3 || k > 40) return 2;
    Mask all = (Mask(1)<<k)-1;
    int sum = k%2 ? 0 : k/2;
    for (int x=1; x<k; ++x) for (int b=0; b<k; ++b) for (int c=b+1; c<k; ++c) {
        int z=(x+sum+b+c)%k;
        if (!z || z==x) continue;
        // Unit scaling acts on all labels. Select the least triple in the orbit.
        auto canonical = std::make_tuple(x,b,c);
        for (int u=2; u<k; ++u) if (std::gcd(u,k)==1) {
            int f=(u*b)%k, g=(u*c)%k;
            canonical=std::min(canonical,std::make_tuple(u*x%k,std::min(f,g),std::max(f,g)));
        }
        if (canonical!=std::make_tuple(x,b,c)) continue;
        Mask free=all ^ 1 ^ (Mask(1)<<x) ^ (Mask(1)<<z);
        Mask palette=all ^ (Mask(1)<<((x+b)%k)) ^ (Mask(1)<<((x+c)%k));
        std::vector<int> row{x};
        std::cout << x << ' ' << b << ' ' << c;
        if (finish(k,z,free,palette,row)) for (int a : row) std::cout << ' ' << a;
        std::cout << '\n';
    }
}
