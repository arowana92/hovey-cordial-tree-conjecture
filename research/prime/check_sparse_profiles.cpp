// Check every affinely inequivalent pair of rooted deficit profiles for the listed sizes.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <map>
#include <numeric>
#include <stdexcept>
#include <utility>
#include <vector>

using Mask = std::uint32_t;
using Profile = std::pair<Mask,Mask>;
using Count = std::uint64_t;

Mask transform(int k, Mask mask, int u, int t) {
    Mask result = 0;
    while (mask) {
        int i = __builtin_ctz(mask);
        result |= Mask(1) << ((u*i+t)%k);
        mask &= mask-1;
    }
    return result;
}

std::map<Profile,Count> catalogue(int k, int loss, const std::vector<int>& units) {
    std::vector<Mask> vertices, edges;
    for (Mask m = 0; m < (Mask(1)<<k); ++m) {
        int n = __builtin_popcount(m);
        if (n == loss) vertices.push_back(m);
        if (n == loss+1) edges.push_back(m);
    }
    std::map<Profile,Count> result;
    for (Mask v : vertices) for (Mask w : edges) {
        Profile key{v,w};
        for (int u : units)
            key = std::min(key,Profile{transform(k,v,u,0),transform(k,w,u,0)});
        ++result[key];
    }
    return result;
}

bool rigid(int k, Profile p) {
    auto [v,w] = p;
    return (v & w & 1) && !(transform(k,w & ~v,2,0) & ~w);
}

struct Image {
    Mask vertices, edges, bridge;
    bool fits(Profile old) const {
        auto [v,w] = old;
        return !(v & vertices) && !((w & edges) & ~bridge) && ((w | edges) & bridge);
    }
};

void audit(int k, int a, int h) {
    std::vector<int> units;
    for (int u = 1; u < k; ++u) if (std::gcd(k,u)==1) units.push_back(u);
    auto cores = catalogue(k,a,units), pieces = catalogue(k,h,units);
    Count total = 0, failed = 0;
    for (const auto& [piece, m] : pieces) {
        std::vector<Image> images;
        for (int u : units) for (int t = 0; t < k; ++t)
            images.push_back({transform(k,piece.first,u,t), transform(k,piece.second,u,2*t),
                              Mask(1)<<t});
        bool piece_rigid = rigid(k,piece);
        for (const auto& [core, n] : cores) {
            bool works = std::any_of(images.begin(),images.end(),
                                     [old = core](Image image) { return image.fits(old); });
            if (works == (piece_rigid && rigid(k,core)))
                throw std::logic_error("direct affine search contradicts the criterion");
            total += m*n;
            if (!works) failed += m*n;
        }
    }
    std::cout << "k=" << k << " old deficit=" << a << " new deficit=" << h
              << " profile pairs=" << total << " blocked=" << failed << '\n';
}

int main() {
    for (int p : {7,11,13}) audit(p,1,1);
    for (int p : {11,13}) audit(p,1,2);
    audit(13,2,2);
}
