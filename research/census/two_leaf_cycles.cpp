// Find two cycles with disjoint omitted vertex pairs for each parent difference.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <random>
#include <vector>

using Mask = std::uint64_t;

struct Search {
    int k;
    int budget = 0;
    int first = 0;
    std::mt19937 random;
    std::vector<int> path;

    Mask bit(int x) const { return Mask(1) << x; }

    bool extend(int last, Mask vertices, Mask weights) {
        if (--budget < 0) return false;
        if (!vertices) return weights == bit((first + last) % k);
        int choices[64];
        int count = 0;
        for (Mask remaining = vertices; remaining; remaining &= remaining - 1) {
            int x = __builtin_ctzll(remaining);
            if (weights & bit((last + x) % k)) choices[count++] = x;
        }
        for (int j = count - 1; j > 0; --j)
            std::swap(choices[j], choices[random() % (j + 1)]);
        for (int j = 0; j < count && budget > 0; ++j) {
            int x = choices[j];
            path.push_back(x);
            if (extend(x, vertices ^ bit(x), weights ^ bit((last + x) % k))) return true;
            path.pop_back();
        }
        return false;
    }

    bool find(int other_parent, int x, int y) {
        int second_weight = (other_parent + y) % k;
        if (x == y || x == second_weight) return false;
        Mask all = k == 64 ? ~Mask(0) : bit(k) - 1;
        Mask vertices = all ^ bit(x) ^ bit(y);
        first = __builtin_ctzll(vertices);
        budget = 15000;
        path.assign(1, first);
        return extend(first, vertices ^ bit(first), all ^ bit(x) ^ bit(second_weight));
    }
};

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    int k = std::stoi(argv[1]);
    if (k < 10 || k > 64 || k % 2) return 2;
    Search search{k, 0, 0, std::mt19937(88882u + k), {}};
    for (int h = 0; h < k; ++h) {
        if (h && k % h) continue;
        std::vector<int> found;
        for (int trial = 0; trial < 200 && found.size() < 2; ++trial) {
            for (int x = 0; x < k && found.size() < 2; ++x) {
                int y = (h + k / 2 - x + 2 * k) % k;
                int key = std::min(x, y);
                if (std::find(found.begin(), found.end(), key) != found.end()) continue;
                if (!search.find(h, x, y)) continue;
                found.push_back(key);
                std::cout << k << ' ' << h << ' ' << x << ' ' << y;
                for (int v : search.path) std::cout << ' ' << v;
                std::cout << '\n';
            }
        }
        if (found.size() != 2) return 1;
    }
}
