// Search for consecutive ordinary sums on the vertex interval [0,n-1].
#include <algorithm>
#include <cstdint>
#include <numeric>

namespace {
using Mask = std::uint64_t;
constexpr int capacity = 31;

Mask reverse_bits(Mask x) {
    x = ((x >> 1) & 0x5555555555555555ULL) | ((x & 0x5555555555555555ULL) << 1);
    x = ((x >> 2) & 0x3333333333333333ULL) | ((x & 0x3333333333333333ULL) << 2);
    x = ((x >> 4) & 0x0f0f0f0f0f0f0f0fULL) | ((x & 0x0f0f0f0f0f0f0f0fULL) << 4);
    return __builtin_bswap64(x);
}

struct Search {
    int n, first_sum, internal = 0, budget;
    std::uint32_t state;
    int parent[capacity]{}, degree[capacity]{}, size[capacity]{}, order[capacity]{};
    int label[capacity]{}, leaves_left[capacity]{}, parent_at[capacity]{};

    std::uint32_t random() {
        state ^= state << 13;
        state ^= state >> 17;
        state ^= state << 5;
        return state;
    }

    bool fill_leaves(Mask vertices, Mask sums) {
        if (!vertices) return true;
        if (--budget < 0) return false;
        Mask parents = 0;
        for (int j = 0; j < internal; ++j)
            if (leaves_left[order[j]]) parents |= Mask(1) << label[order[j]];

        int best = capacity+1, slot = 0;
        bool sum_first = false;
        Mask options = 0;
        const Mask reversed = reverse_bits(vertices);
        for (int pass = 0; pass < 2; ++pass) {
            for (Mask open = pass ? sums : vertices; open; open &= open-1) {
                int p = __builtin_ctzll(open);
                // For a fixed sum h+p, a child x needs parent h+p-x.
                // For a fixed child p, a parent a consumes sum slot p+a-h.
                Mask possible = pass ? reversed >> (63-(first_sum+p))
                    : p >= first_sum ? sums >> (p-first_sum) : sums << (first_sum-p);
                possible &= parents;
                int count = __builtin_popcountll(possible);
                if (!count) return false;
                if (count < best) {
                    best = count;
                    sum_first = pass;
                    slot = p;
                    options = possible;
                }
            }
        }
        for (; options; options &= options-1) {
            int a = __builtin_ctzll(options), p = parent_at[a];
            int x = sum_first ? first_sum+slot-a : slot;
            int y = x+a-first_sum;
            --leaves_left[p];
            if (fill_leaves(vertices ^ (Mask(1)<<x), sums ^ (Mask(1)<<y))) {
                for (int i = 0; i < n; ++i)
                    if (parent[i] == p && degree[i] == 1 && label[i] == -1) {
                        label[i] = x;
                        break;
                    }
                return true;
            }
            ++leaves_left[p];
        }
        return false;
    }

    bool place(int j, Mask vertices, Mask sums, int moment) {
        if (j == internal) return moment == 0 && fill_leaves(vertices,sums);
        if (--budget < 0) return false;
        int v = order[j], p = parent[v], coefficient = degree[v]-1;
        Mask options = vertices;
        if (p >= 0) options &= label[p] >= first_sum ? sums >> (label[p]-first_sum)
                                                     : sums << (first_sum-label[p]);
        if (j+1 == internal && coefficient) {
            if (moment < 0 || moment%coefficient || moment/coefficient >= n) return false;
            options &= Mask(1) << (moment/coefficient);
        }
        if (!options) return false;
        Mask below = (Mask(1) << (random()%n))-1;
        for (Mask choices : {options & ~below, options & below}) {
            for (; choices; choices &= choices-1) {
                int x = __builtin_ctzll(choices);
                if (coefficient*x > moment) continue;
                label[v] = x;
                parent_at[x] = v;
                Mask remaining = p < 0 ? sums : sums ^ (Mask(1)<<(x+label[p]-first_sum));
                if (place(j+1, vertices ^ (Mask(1)<<x), remaining, moment-coefficient*x))
                    return true;
                if (budget < 0) return false;
            }
        }
        return false;
    }

    bool run(int order_n, const int* pp, int* out, std::uint32_t seed) {
        n = order_n;
        if (n < 2 || n >= capacity || pp[0] != -1) return false;
        state = seed|1U;
        std::copy_n(pp,n,parent);
        std::fill_n(size,n,1);
        std::iota(order,order+n,0);
        for (int i = n-1; i > 0; --i) {
            if (parent[i] < 0 || parent[i] >= i) return false;
            ++degree[i];
            ++degree[parent[i]];
            size[parent[i]] += size[i];
        }
        std::stable_sort(order,order+n,[&](int a,int b){ return size[a] > size[b]; });
        while (internal < n && size[order[internal]] > 1) ++internal;
        for (int i = internal; i < n; ++i) ++leaves_left[parent[order[i]]];
        for (int attempt = 0; attempt < 1200; ++attempt) {
            int half = n/2;
            first_sum = attempt%5 ? half+int(random()%5)-2 : 1+int(random()%(n-1));
            if (first_sum < 1 || first_sum >= n) first_sum = half;
            budget = attempt < 80 ? 400 : 3000;
            std::fill_n(label,n,-1);
            if (place(0,(Mask(1)<<n)-1,(Mask(1)<<(n-1))-1,(n-1)*(first_sum-1))) {
                std::copy_n(label,n,out);
                return true;
            }
        }
        return false;
    }
};
}

bool interval_witness(int n, const int* parents, int* output, std::uint32_t seed) {
    Search search{};
    return search.run(n,parents,output,seed);
}
