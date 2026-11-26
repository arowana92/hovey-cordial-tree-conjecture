// Find a permutation of vertex residues whose edge sums are distinct modulo n.
#include <algorithm>
#include <cstdint>
#include <numeric>
#include <random>
#include <vector>

extern "C" int diameter_five_search(int n, const int* parent, int* label,
                                    std::uint32_t seed, int limit) {
    if (n < 2 || parent[0] != -1 || limit <= 0) return 0;
    std::vector<std::vector<int>> neighbors(n);
    for (int i = 1; i < n; ++i) {
        if (parent[i] < 0 || parent[i] >= i) return 0;
        neighbors[i].push_back(parent[i]);
        neighbors[parent[i]].push_back(i);
    }

    std::mt19937 rng(seed);
    std::vector<int> frequency(n), weight(n), conflicts(n);
    std::iota(label, label+n, 0);
    for (int step = 0; step < limit; ++step) {
        if (step % 500 == 0) {
            for (int i = n-1; i > 0; --i)
                std::swap(label[i], label[rng() % (i+1)]);
        }
        std::fill(frequency.begin(), frequency.end(), 0);
        for (int i = 1; i < n; ++i) {
            weight[i] = (label[i] + label[parent[i]]) % n;
            ++frequency[weight[i]];
        }
        int count = 0;
        for (int i = 1; i < n; ++i)
            if (frequency[weight[i]] > 1) conflicts[count++] = i;
        if (!count) return 1;

        const int child = conflicts[rng() % count];
        const int u = (rng() % 3) ? child : parent[child];
        int best = n, partner = u, ties = 0;
        for (int v = 0; v < n; ++v) {
            if (u == v) continue;
            int change = 0;
            auto move = [&](int from, int to, bool undo) {
                for (int w : neighbors[from]) {
                    if (w == to) continue;  // A shared edge keeps its weight.
                    const int old_sum = (label[from]+label[w]) % n;
                    const int new_sum = (label[to]+label[w]) % n;
                    if (undo) {
                        ++frequency[old_sum];
                        --frequency[new_sum];
                    } else {
                        change -= (--frequency[old_sum] > 0);
                        change += (frequency[new_sum]++ > 0);
                    }
                }
            };
            move(u, v, false);
            move(v, u, false);
            move(u, v, true);
            move(v, u, true);
            if (change < best) {
                best = change;
                partner = v;
                ties = 1;
            } else if (change == best && rng() % ++ties == 0) {
                partner = v;
            }
        }
        if (rng() % 25 == 0) partner = rng() % n;
        std::swap(label[u], label[partner]);
    }
    return 0;
}
