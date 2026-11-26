// Search cyclic labelings, then cut the cycle to obtain a short integer witness.
#include <algorithm>
#include <cstdint>
#include <vector>

namespace {
using Mask = std::uint64_t;

struct Search {
    int h, k, cap;
    const int* parents;
    int* labels;
    std::vector<int> order, earlier_twin;

    bool interval_witness() {
        std::vector<int> sorted(labels, labels+h);
        std::sort(sorted.begin(), sorted.end());
        std::vector<int> ranks(h), gaps(h), carries(h), blocked(h, -1);
        for (int i = 0; i < h; ++i)
            ranks[i] = std::lower_bound(sorted.begin(), sorted.end(), labels[i]) - sorted.begin();
        for (int i = 1; i < h; ++i) {
            int raw = labels[i] + labels[parents[i]];
            carries[i] = raw > k;
            int w = raw - k*carries[i]; // weight zero is represented by k
            int gap = std::lower_bound(sorted.begin(), sorted.end(), w) - sorted.begin() - 1;
            if (gap < 0 || blocked[gap] >= 0) return false;
            blocked[gap] = w;
            gaps[i] = gap;
        }
        // Cut at the sole gap containing no original weight. Keep hubs 0 and 1.
        int cut = std::find(blocked.begin(), blocked.end(), -1) - blocked.begin();
        if (cut == 0 || cut == h) return false;
        for (int i = 1; i < h; ++i) {
            int shift = (ranks[i] > cut) + (ranks[parents[i]] > cut) - carries[i];
            if (shift != (gaps[i] > cut)) return false;
        }
        int at_zero = 0, at_one = 0;
        for (int j = 0; j < h; ++j) {
            if (j == cut) continue;
            int upper = j+1 < h ? sorted[j+1] : k;
            at_zero += blocked[j] - sorted[j] - 1;
            at_one += upper - blocked[j];
        }
        if (at_zero > cap || at_one > cap) return false;
        for (int i = 0; i < h; ++i)
            if (ranks[i] > cut) labels[i] -= k;
        return true;
    }

    bool assign(int step, Mask used, Mask weights) {
        if (step == h) return interval_witness();
        int v = order[step];
        int previous = labels[v];
        int first = previous >= 0 ? previous : 0;
        int last = previous >= 0 ? previous+1 : k;
        if (earlier_twin[v] >= 0) first = std::max(first, labels[earlier_twin[v]]+1);
        for (int value = first; value < last; ++value) {
            Mask bit = Mask(1) << value;
            if (used & bit) continue;
            Mask next = weights;
            bool collision = false;
            for (int j = 0; j < step; ++j) {
                int u = order[j];
                if (parents[u] != v && parents[v] != u) continue;
                Mask w = Mask(1) << ((value + labels[u]) % k);
                if (next & w) { collision = true; break; }
                next |= w;
            }
            if (collision) continue;
            labels[v] = value;
            if (assign(step+1, used | bit, next)) return true;
            labels[v] = previous;
        }
        return false;
    }
};
}

// All arguments are read from the generator's parent-before-child trees.
extern "C" int two_hub_seed(int h, int a, int b, int k, int cap,
                            const int* parents, int* labels) {
    if (h < 2 || k < h || k > 63 || cap < 0 || a == b ||
        a < 0 || b < 0 || a >= h || b >= h || parents[0] != -1) return -1;
    for (int i = 1; i < h; ++i) if (parents[i] < 0 || parents[i] >= i) return -1;
    std::fill(labels, labels+h, -1);
    labels[a] = 0;
    labels[b] = 1;
    Search s{h, k, cap, parents, labels, {a, b}, std::vector<int>(h, -1)};
    std::vector<int> size(h, 1), last_leaf(h, -1);
    for (int i = h-1; i > 0; --i) size[parents[i]] += size[i];
    for (int i = 0; i < h; ++i) if (i != a && i != b) s.order.push_back(i);
    std::stable_sort(s.order.begin()+2, s.order.end(),
                     [&](int i, int j) { return size[i] > size[j]; });
    for (int j = 2; j < h; ++j) {
        int v = s.order[j];
        if (v && size[v] == 1) {
            s.earlier_twin[v] = last_leaf[parents[v]];
            last_leaf[parents[v]] = v;
        }
    }
    return s.assign(0, 0, 0) ? 1 : 0;
}
