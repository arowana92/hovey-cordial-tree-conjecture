// Find two cycles with disjoint omitted vertex pairs for each parent difference.
#include "rainbow_cycle.hpp"
#include <iostream>
#include <string>

using rainbow_cycle::Mask;
using rainbow_cycle::Search;

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
                int second_weight = (h + y) % k;
                if (x == y || x == second_weight) continue;
                Mask all = k == 64 ? ~Mask(0) : search.bit(k) - 1;
                Mask vertices = all ^ search.bit(x) ^ search.bit(y);
                Mask weights = all ^ search.bit(x) ^ search.bit(second_weight);
                if (!search.cycle(vertices, weights, 15000)) continue;
                found.push_back(key);
                std::cout << k << ' ' << h << ' ' << x << ' ' << y;
                for (int v : search.path) std::cout << ' ' << v;
                std::cout << '\n';
            }
        }
        if (found.size() != 2) return 1;
    }
}
