// Emit positive root-zero labelings or structural reductions for all rooted trees at one order.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <numeric>

namespace {
constexpr int limit = 30;
using Mask = std::uint64_t;
using List = std::array<int, limit+1>;

class Labeler {
    int n, center;
    std::int64_t budget;
    List order{}, parent{}, degree{}, remaining{}, previous{}, slots{};
    Mask full;

    bool place(int i, Mask free, Mask weights, int target) {
        if (i == n) return target == 0;
        if (--budget < 0) return false;
        if (target < remaining[i]*__builtin_ctzll(free) ||
            target > remaining[i]*(63-__builtin_clzll(free))) return false;
        int offset = slots[parent[i]]-center;
        Mask available = free & (offset >= 0 ? weights >> offset : weights << -offset);
        if (previous[i] >= 0) available &= (~Mask(0)) << (slots[previous[i]]+1);
        while (available && budget >= 0) {
            int x = __builtin_ctzll(available);
            available &= available-1;
            slots[i] = x;
            if (place(i+1, free ^ (Mask(1) << x), weights ^ (Mask(1) << (x+offset)),
                      target-degree[i]*x)) return true;
        }
        return false;
    }

public:
    Labeler(int size, const List& original, const List& children) : n(size), full((Mask(1)<<n)-1) {
        List index, last;
        index.fill(-1);
        last.fill(-1);
        order[0] = index[0] = 0;
        for (int i = 1; i < n; ++i) {
            int best = -1;
            for (int v = 1; v < n; ++v) {
                if (index[v] >= 0 || index[original[v]] < 0) continue;
                if (best < 0 || children[v] > children[best] ||
                    (children[v] == children[best] && original[v] < original[best])) best = v;
            }
            order[i] = best;
            index[best] = i;
            parent[i] = index[original[best]];
            degree[i] = children[best];
            previous[i] = -1;
            if (!children[best]) {
                previous[i] = last[original[best]];
                last[original[best]] = i;
            }
        }
        for (int i = n-1; i >= 1; --i) remaining[i] = remaining[i+1]+degree[i];
    }

    bool solve(int root_degree, List& result) {
        const std::int64_t caps[] = {500, 20000, std::numeric_limits<std::int64_t>::max()};
        for (auto cap : caps) {
            for (int j = 0; j < n; ++j) {
                center = (n-1)/2 + (j%2 ? (j+1)/2 : -j/2);
                if (center < 0 || center >= n-1) continue;
                slots[0] = center;
                budget = cap;
                if (!place(1, full ^ (Mask(1) << center), full ^ 1, (n-root_degree)*center))
                    continue;
                for (int i = 0; i < n; ++i) result[order[i]] = slots[i];
                return true;
            }
        }
        return false;
    }
};

bool reduced(int n, const List& parent, const List& children) {
    if (n == 1) return true;
    for (int i = 1; i < n; ++i) if (parent[i] == 0 && children[i] == 0) return true;
    int nonleaves = 1;
    List incident{};
    for (int i = 1; i < n; ++i) {
        if (!children[i]) continue;
        ++nonleaves;
        ++incident[i];
        ++incident[parent[i]];
    }
    int largest = *std::max_element(incident.begin(), incident.begin()+n);
    return nonleaves <= 5 || largest <= 2 || largest == nonleaves-1;
}

bool emit(int n, const List& depths) {
    List parent{}, children{}, recent{}, result{};
    for (int i = 1; i < n; ++i) {
        parent[i] = recent[depths[i]-1];
        ++children[parent[i]];
        recent[depths[i]] = i;
    }
    bool structural = reduced(n, parent, children);
    if (!structural && !Labeler(n, parent, children).solve(children[0], result)) return false;
    std::array<unsigned char, 2*limit> record{};
    int length = 0;
    for (int i = 1; i < n; ++i) record[length++] = depths[i];
    record[length++] = structural ? 0 : 1;
    if (!structural) for (int i = 0; i < n; ++i) record[length++] = result[i];
    std::cout.write(reinterpret_cast<const char*>(record.data()), length);
    return bool(std::cout);
}
}

int main(int argc, char** argv) {
    if (argc != 2) return 1;
    int n = std::atoi(argv[1]);
    if (n < 1 || n > limit) return 1;
    std::ios::sync_with_stdio(false);
    List depths{};
    std::iota(depths.begin(), depths.begin()+n, 0);
    for (;;) {
        if (!emit(n, depths)) {
            std::cerr << "No witness or write failure at depth sequence";
            for (int i = 0; i < n; ++i) std::cerr << " " << depths[i];
            std::cerr << '\n';
            return 1;
        }
        int i = n-1;
        while (i > 0 && depths[i] == 1) --i;
        if (i == 0) break;
        int j = i-1;
        while (depths[j] != depths[i]-1) --j;
        int period = i-j;
        for (; i < n; ++i) depths[i] = depths[i-period];
    }
}
