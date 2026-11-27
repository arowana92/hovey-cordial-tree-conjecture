// Independent signed counts from unbiased assignments with at most one collision.
#include <algorithm>
#include <cstdint>
#include <numeric>

namespace {
struct Orbits {
    int p;
    const int* parent;
    bool matrix;
    int label[16]{}, weight[16]{}, order[16]{}, inverse[16]{}, image[16]{};
    std::int64_t scalar = 0, columns[16][16]{};
    unsigned all;

    int sign() const {
        unsigned seen = 0;
        int cycles = 0;
        for (int i = 0; i < p; ++i) if (!(seen&(1U<<i))) {
            ++cycles;
            for (int x = i; !(seen&(1U<<x)); x = image[x]) seen |= 1U<<x;
        }
        return (p-cycles)%2 ? -1 : 1;
    }
    void add(int j, int factor) {
        for (int i = 1; i < p; ++i) columns[j][i] += factor*label[i];
    }
    void tally(unsigned holes, int duplicate) {
        int h = __builtin_ctz(holes);
        if (duplicate < 0) {
            image[0] = h;
            int s = sign();
            scalar += (p-1)*s;
            if (matrix) for (int j = 1; j < p; ++j)
                add(j,-s*inverse[(h-weight[j]+p)%p]);
            return;
        }
        int g = __builtin_ctz(holes&(holes-1));
        int first = 0, second = 0;
        for (int j = 1; j < p; ++j) if (weight[j] == duplicate) {
            if (first) second = j;
            else first = j;
        }
        image[label[first]] = h;
        image[0] = g;
        int factor = sign()*(inverse[(h-duplicate+p)%p]-inverse[(g-duplicate+p)%p]);
        image[label[first]] = duplicate;
        add(first,factor);
        add(second,-factor);
    }
    void visit(int j, unsigned vertices, unsigned weights, int duplicate) {
        if (j == p) { tally(all^weights,duplicate); return; }
        int v = order[j];
        unsigned choices = j == 1 ? 2U : all^vertices;
        int shift = label[parent[v]];
        if (!matrix || duplicate >= 0) {
            unsigned free = all^weights;
            choices &= (free>>shift)|(free<<(p-shift));
        }
        for (; choices; choices &= choices-1) {
            int a = __builtin_ctz(choices), w = a+shift;
            if (w >= p) w -= p;
            label[v] = a;
            image[a] = weight[v] = w;
            visit(j+1,vertices|(1U<<a),weights|(1U<<w),weights&(1U<<w) ? w : duplicate);
        }
    }
    void run() {
        all = (1U<<p)-1;
        for (int a = 1; a < p; ++a)
            for (int b = 1; b < p; ++b) if (a*b%p == 1) inverse[a] = b;
        int size[16];
        std::fill_n(size,p,1);
        for (int i = p-1; i > 0; --i) size[parent[i]] += size[i];
        std::iota(order,order+p,0);
        std::stable_sort(order,order+p,[&](int a,int b){ return size[a] > size[b]; });
        visit(1,1,0,-1);
    }
};
}

extern "C" void orbit_check(int p, const int* parents, int matrix, int* out) {
    if (p < 2 || p > 13) return;
    Orbits c{p,parents,static_cast<bool>(matrix)};
    c.run();
    *out++ = (c.scalar%p+p)%p;
    if (matrix) for (int j = 1; j < p; ++j) for (int i = 1; i < p; ++i)
        *out++ = (c.columns[j][i]%p+p)%p;
}
