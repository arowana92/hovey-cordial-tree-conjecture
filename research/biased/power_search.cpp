// Cover all high-digit edge offsets for one prescribed low-boundary forest.
#include <cstdint>
#include <iostream>
#include <vector>

namespace {
struct Forest {
    int k, p, stride, n;
    int parent[8]{}, labels[8]{}, bias[8]{}, baseline[8]{};
    std::vector<bool> covered;
    std::vector<std::uint32_t> witnesses;

    int parent_label(int i) const {
        return parent[i] < 0 ? -1-parent[i] : labels[parent[i]];
    }

    bool find(int i, unsigned used_labels, unsigned used_weights) {
        if (i == n) return true;
        int shift = parent_label(i)+bias[i];
        for (int x = 1; x < k; ++x) {
            if (used_labels&(1U<<x)) continue;
            int weight = (x+shift)%k;
            if (used_weights&(1U<<weight)) continue;
            labels[i] = x;
            if (find(i+1,used_labels|(1U<<x),used_weights|(1U<<weight))) return true;
        }
        return false;
    }

    void mark(int i, unsigned weights, int code, int place) {
        if (i == n) {
            covered[code] = true;
            return;
        }
        for (int digit = 0; digit < p; ++digit) {
            int weight = (baseline[i]+stride*digit)%k;
            if (!(weights&(1U<<weight)))
                mark(i+1,weights|(1U<<weight),code+digit*place,place*p);
        }
    }

    bool run() {
        n = k-1;
        stride = k/p;
        int total = 1;
        for (int i = 0; i < n; ++i) total *= p;
        covered.assign(total,false);
        for (int code = 0; code < total; ++code) {
            if (covered[code]) continue;
            int value = code;
            for (int i = 0; i < n; ++i) {
                bias[i] = stride*(value%p);
                value /= p;
            }
            if (!find(0,1,0)) {
                std::cerr << "no witness for high-digit code " << code << '\n';
                return false;
            }
            std::uint32_t word = 0;
            for (int i = 0; i < n; ++i) {
                baseline[i] = (labels[i]+parent_label(i))%k;
                word |= std::uint32_t(labels[i])<<(4*i);
            }
            witnesses.push_back(word);
            mark(0,0,0,1);
        }
        return true;
    }
};
}

int main() {
    int k,p;
    while (std::cin >> k >> p) {
        if (!((k == 4 && p == 2) || (k == 8 && p == 2) || (k == 9 && p == 3))) return 2;
        Forest forest{k,p};
        for (int i = 0; i < k-1; ++i)
            if (!(std::cin >> forest.parent[i]) || forest.parent[i] >= i || forest.parent[i] < -k/p)
                return 2;
        if (!forest.run()) return 1;
        for (auto word : forest.witnesses) std::cout << word << ' ';
        std::cout << std::endl;
    }
}
