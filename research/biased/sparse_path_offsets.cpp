// Find an explicit permutation for each pair of exceptional path offsets up to units.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Mask = std::uint64_t;

class PathSearch {
    int k, budget = 0;
    Mask all;
    std::uint32_t seed = 1991;
    std::vector<int> offsets, labels;

    unsigned random() {
        seed ^= seed << 13;
        seed ^= seed >> 17;
        return seed ^= seed << 5;
    }

    bool visit(int position, Mask vertices, Mask weights) {
        if (!vertices) return true;
        if (--budget <= 0) return false;
        int shift = (labels[position-1] + offsets[position]) % k;
        Mask choices = vertices & ((weights >> shift) | (weights << (k-shift)));
        Mask split = (Mask(1) << (random() % k)) - 1;
        for (Mask side : {choices & ~split, choices & split}) {
            while (side && budget > 0) {
                int x = __builtin_ctzll(side);
                side &= side-1;
                labels[position] = x;
                if (visit(position+1, vertices ^ (Mask(1) << x),
                          weights ^ (Mask(1) << ((shift+x) % k)))) return true;
            }
        }
        return false;
    }

public:
    explicit PathSearch(int n)
        : k(n), all((Mask(1) << n)-1), offsets(n), labels(n) {}

    void emit(int i, int j, int a, int b) {
        std::fill(offsets.begin(), offsets.end(), 0);
        offsets[i] = a;
        offsets[j] = b;
        for (int attempt=0; attempt<1000; ++attempt) {
            budget = 5000;
            if (!visit(1, all ^ 1, all)) continue;
            std::cout << i << ' ' << j << ' ' << a << ' ' << b;
            for (int x : labels) std::cout << ' ' << x;
            std::cout << '\n';
            return;
        }
        throw std::runtime_error("search limit reached without a witness");
    }
};

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    int k = std::stoi(argv[1]);
    if (k < 2 || k > 63) return 2;
    std::vector<std::pair<int,int>> representatives;
    for (int a=0; a<k; ++a) for (int b=1; b<k; ++b) {
        auto pair = std::make_pair(a,b), least = pair;
        for (int u=1; u<k; ++u) if (std::gcd(u,k)==1)
            least = std::min(least, std::make_pair(a*u%k,b*u%k));
        if (pair == least) representatives.push_back(pair);
    }
    PathSearch search(k);
    search.emit(0,0,0,0);
    for (int j=1; j<k; ++j) for (int i=0; i<j; ++i)
        for (auto [a,b] : representatives) if ((a==0) == (i==0))
            search.emit(i,j,a,b);
    return !std::cout;
}
