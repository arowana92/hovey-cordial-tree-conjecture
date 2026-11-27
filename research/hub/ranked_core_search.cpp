// Find one interval labeling for specified leaf counts and allowed core prefixes.
#include <algorithm>
#include <array>
#include <cstdint>

namespace {
using Mask = std::uint64_t;
constexpr int max_core = 12;
constexpr int max_order = 62;

struct Search {
    int h, n, attempts, lower;
    const int* edges;
    const int* count;
    std::array<int, max_core> f{}, coefficient{}, left{};
    std::array<int, max_order> assignment{};

    bool fill(Mask rows, Mask columns) {
        if (!rows) return true;
        if (--attempts < 0) return false;

        int best_size = h+1, best_slot = -1;
        bool column_first = false;
        std::array<int, max_core> best{}, support{};
        for (int pass = 0; pass < 2; ++pass) {
            for (Mask open = pass ? columns : rows; open; open &= open-1) {
                const int slot = __builtin_ctzll(open);
                std::array<int, max_core> options{};
                int size = 0;
                for (int p = 0; p < h; ++p) {
                    if (!left[p]) continue;
                    int other = pass ? slot+1-f[p] : slot+f[p]-1;
                    int limit = pass ? n : n-1;
                    Mask targets = pass ? rows : columns;
                    if (other < 0 || other >= limit || !(targets & (Mask(1) << other))) continue;
                    options[size++] = p;
                    if (pass) ++support[p];
                }
                if (!size) return false;
                if (size < best_size) {
                    best_size = size;
                    best_slot = slot;
                    best = options;
                    column_first = pass != 0;
                }
            }
        }
        for (int p = 0; p < h; ++p) if (support[p] < left[p]) return false;
        for (int i = 0; i < best_size; ++i) {
            int p = best[i];
            int x = column_first ? best_slot+1-f[p] : best_slot;
            int y = x+f[p]-1;
            --left[p];
            assignment[x] = p;
            if (fill(rows ^ (Mask(1) << x), columns ^ (Mask(1) << y))) return true;
            ++left[p];
        }
        return false;
    }

    bool try_interval(int lo) {
        if (lo > 0 || lo+n-1 < 1) return false;
        Mask rows = (Mask(1) << n)-1, columns = (Mask(1) << (n-1))-1;
        for (int i = 0; i < h; ++i) {
            int x = f[i]-lo;
            if (x < 0 || x >= n) return false;
            rows ^= Mask(1) << x;
        }
        for (int i = 0; i < h-1; ++i) {
            int y = f[edges[2*i]] + f[edges[2*i+1]] - lo - 1;
            if (y < 0 || y >= n-1 || !(columns & (Mask(1) << y))) return false;
            columns ^= Mask(1) << y;
        }
        std::copy_n(count, h, left.begin());
        attempts = 15000;
        if (!fill(rows, columns)) return false;
        lower = lo;
        return true;
    }

    std::array<int, max_core> known_weights{};
    std::array<unsigned, max_core> earlier_neighbors{};

    bool add_weights(int i, int& lo, int& hi, int& used) {
        for (auto neighbors = earlier_neighbors[i]; neighbors; neighbors &= neighbors-1) {
            const int w = f[i] + f[__builtin_ctz(neighbors)];
            if (std::find(known_weights.begin(), known_weights.begin()+used, w)
                != known_weights.begin()+used) return false;
            known_weights[used++] = w;
            lo = std::min(lo, w-1);
            hi = std::max(hi, w);
        }
        return hi-lo < n;
    }

    bool place(int i, int lo, int hi, int sum, int used) {
        if (i == h) return try_interval(sum);
        for (int x = hi-n+1; x <= lo+n-1; ++x) {
            if (std::find(f.begin(), f.begin()+i, x) != f.begin()+i) continue;
            f[i] = x;
            int low = std::min(lo, x), high = std::max(hi, x), length = used;
            if (add_weights(i, low, high, length)
                && place(i+1, low, high, sum+coefficient[i]*x, length))
                return true;
        }
        return false;
    }
};
}

extern "C" int solve(int h, const int* edges, const int* counts, int rank,
                     const int* prefixes, int number, int* result) {
    if (h < 2 || h > max_core || rank < 0 || rank > h) return -1;
    Search s{};
    s.h = h;
    s.n = h;
    s.edges = edges;
    s.count = counts;
    for (int i = 0; i < h; ++i) {
        if (counts[i] < 0) return -1;
        s.n += counts[i];
        s.coefficient[i] = 1-counts[i];
    }
    if (s.n > max_order) return -1;
    for (int j = 0; j < 2*(h-1); ++j) --s.coefficient[edges[j]];
    for (int j = 0; j < h-1; ++j) {
        const int a = edges[2*j], b = edges[2*j+1];
        s.earlier_neighbors[std::max(a, b)] |= 1U << std::min(a, b);
    }
    for (int b = 0; b < number; ++b) {
        int lo = 0, hi = 1, sum = 0;
        for (int i = 0; i < rank; ++i) {
            int x = s.f[i] = prefixes[b*rank+i];
            lo = std::min(lo, x);
            hi = std::max(hi, x);
            sum += s.coefficient[i]*x;
        }
        int used = 0;
        bool valid = true;
        for (int i = 0; valid && i < rank; ++i) valid = s.add_weights(i, lo, hi, used);
        if (!valid || !s.place(rank, lo, hi, sum, used)) continue;
        result[0] = s.lower;
        std::copy_n(s.f.begin(), h, result+1);
        std::copy_n(s.assignment.begin(), s.n, result+1+h);
        return 1;
    }
    return 0;
}
