// Optional search for lattice interval seeds. The verifier uses only Python.
#include <algorithm>
#include <array>
#include <cstdint>
#include <numeric>

namespace {
using Mask = std::uint64_t;
constexpr int max_vertices = 12;
constexpr int max_band = 63;

struct Search {
    int order, mark_count, radius, attempts;
    std::array<std::array<int, 2>, max_vertices> edges{};
    std::array<int, max_vertices> labels{}, schedule{};
    std::array<bool, max_vertices> assigned{};
    std::array<int, max_band> matched{}, fillers{};
    int lower, upper;
    Mask blocked, visited;

    bool augment(int slot) {
        for (int i = 0; i < mark_count; ++i) {
            int weight = slot + labels[i] - 1;
            if (weight < 0 || weight >= upper-lower) continue;
            Mask bit = Mask(1) << weight;
            if ((blocked | visited) & bit) continue;
            visited |= bit;
            if (matched[weight] < 0 || augment(matched[weight])) {
                matched[weight] = slot;
                return true;
            }
        }
        return false;
    }

    bool fill_interval() {
        int lo = *std::min_element(labels.begin(), labels.begin()+order);
        int hi = *std::max_element(labels.begin(), labels.begin()+order);
        std::array<int, max_vertices> weights{};
        for (int i = 0; i < order-1; ++i) {
            auto [u, v] = edges[i];
            weights[i] = labels[u]+labels[v];
            lo = std::min(lo, weights[i]-1);
            hi = std::max(hi, weights[i]);
        }
        for (int pad = 0; pad <= 2; ++pad) {
            for (int below = 0; below <= pad; ++below) {
                lower = lo-below;
                upper = hi+pad-below;
                if (upper-lower >= max_band-1) continue;
                Mask used = 0;
                blocked = 0;
                for (int i = 0; i < order; ++i) used |= Mask(1) << (labels[i]-lower);
                for (int i = 0; i < order-1; ++i) blocked |= Mask(1) << (weights[i]-lower-1);
                matched.fill(-1);
                bool ok = true;
                for (int x = 0; x <= upper-lower && ok; ++x) {
                    if (used & (Mask(1) << x)) continue;
                    visited = 0;
                    ok = augment(x);
                }
                if (!ok) continue;
                fillers.fill(0);
                for (int y = 0; y < upper-lower; ++y) {
                    if (matched[y] >= 0) fillers[matched[y]] = 1+y-matched[y];
                }
                return true;
            }
        }
        return false;
    }

    bool place(int depth, Mask values, Mask weights) {
        if (depth == order) {
            --attempts;
            return fill_interval();
        }
        const int v = schedule[depth];
        const int choices = depth < mark_count ? 1 : 2*radius+1;
        for (int i = 0; i < choices && attempts > 0; ++i) {
            int x = depth < mark_count ? labels[v] : (i%2 ? -(i+1)/2 : i/2);
            Mask bit = Mask(1) << (x+radius);
            if (values & bit) continue;
            labels[v] = x;
            assigned[v] = true;
            Mask next = weights;
            bool ok = true;
            for (int j = 0; j < order-1 && ok; ++j) {
                auto [a, b] = edges[j];
                int u = a == v ? b : (b == v ? a : -1);
                if (u < 0 || !assigned[u]) continue;
                Mask sum_bit = Mask(1) << (x+labels[u]+2*radius);
                if (next & sum_bit) ok = false;
                next |= sum_bit;
            }
            if (ok && place(depth+1, values | bit, next)) return true;
            assigned[v] = false;
        }
        return false;
    }

    void choose_order() {
        std::iota(schedule.begin(), schedule.begin()+order, 0);
        for (int i = mark_count; i < order; ++i) {
            int best = -1, pick = i;
            for (int j = i; j < order; ++j) {
                int score = 0;
                for (int k = 0; k < order-1; ++k) {
                    for (int side : {0, 1}) {
                        if (edges[k][side] != schedule[j]) continue;
                        ++score;
                        int u = edges[k][1-side];
                        if (std::find(schedule.begin(), schedule.begin()+i, u) != schedule.begin()+i)
                            score += 16;
                    }
                }
                if (score > best) { best = score; pick = j; }
            }
            std::swap(schedule[i], schedule[pick]);
        }
    }
};
}

extern "C" int fit(int h, int marks, int radius, int attempts, const int* edges,
                   const int* marked, int* out) {
    if (h > max_vertices || marks > h || marks < 1 || radius < 1 || radius > 15) return 0;
    Search s{};
    s.order = h;
    s.mark_count = marks;
    s.radius = radius;
    s.attempts = attempts;
    for (int i = 0; i < marks; ++i) {
        if (marked[i] < -radius || marked[i] > radius) return 0;
        s.labels[i] = marked[i];
    }
    for (int j = 0; j < h-1; ++j) s.edges[j] = {edges[2*j], edges[2*j+1]};
    s.choose_order();
    if (!s.place(0, 0, 0)) return 0;
    out[0] = s.lower;
    out[1] = s.upper;
    std::copy_n(s.labels.begin(), h, out+2);
    std::copy_n(s.fillers.begin(), s.upper-s.lower+1, out+2+h);
    return 1;
}
