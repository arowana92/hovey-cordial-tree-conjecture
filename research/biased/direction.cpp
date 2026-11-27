// Exhaust a single bias vector directly, accumulating signed first moments.
#include <algorithm>
#include <cstdint>

namespace {
struct Count {
    int p;
    const int* parent;
    const int* bias;
    int label[16]{};
    std::int64_t moments[16]{};
    unsigned all;
    bool found = false;

    std::int64_t visit(int i, unsigned used_v, unsigned used_w, int parity, int mode) {
        if (i == p) {
            found = true;
            return parity ^ (__builtin_ctz(all^used_w)&1) ? -1 : 1;
        }
        int shift = (label[parent[i]]+bias[i-1])%p;
        unsigned free_w = all^used_w;
        unsigned choices = (all^used_v) & ((free_w>>shift)|(free_w<<(p-shift)));
        if (mode == 2 && i == 1) choices &= 2U;
        std::int64_t sum = 0;
        for (; choices; choices &= choices-1) {
            int a = __builtin_ctz(choices), w = a+shift;
            if (w >= p) w -= p;
            label[i] = a;
            int sign = parity ^ __builtin_parity(used_v>>(a+1)) ^ __builtin_parity(used_w>>(w+1));
            auto count = visit(i+1,used_v|(1U<<a),used_w|(1U<<w),sign,mode);
            if (mode == 1 && found) return 1;
            sum += count;
            moments[i] += a*count;
        }
        return sum;
    }
};
}

// mode 0 counts moments, mode 1 finds a witness, mode 2 counts only the
// zero-bias scalar and uses scaling to fix the first nonroot label at one.
extern "C" int direction(int p, const int* parents, const int* biases, int* out, int mode) {
    if (p < 2 || p > 13) return 0;
    Count c{p,parents,biases};
    c.all = (1U<<p)-1;
    auto z = c.visit(1,1,0,0,mode);
    if (mode == 1) {
        if (c.found) std::copy_n(c.label,p,out);
    } else {
        if (mode == 2) z *= p-1;
        out[0] = (z%p+p)%p;
        for (int i = 1; i < p; ++i) out[i] = (c.moments[i]%p+p)%p;
    }
    return c.found;
}
