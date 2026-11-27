// Exact-cover search for a fixed interval and two prescribed center labels.
#include <algorithm>
#include <array>
#include <random>
#include <vector>

namespace {
template <std::size_t Length>
using Arm = std::array<int, Length+1>;

// Circular column and row lists for Algorithm X.
struct Incidence {
    int left, right, up, down, column, arm;
};

template <std::size_t Length>
class Search {
    static constexpr int width = 2*Length;
    std::vector<Incidence> links;
    std::vector<int> sizes;
    int remaining[2];
    int budget;

    void hide(int column) {
        auto &c = links[column];
        links[c.left].right = c.right;
        links[c.right].left = c.left;
        for (int i = c.down; i != column; i = links[i].down) {
            for (int j = links[i].right; j != i; j = links[j].right) {
                auto &x = links[j];
                links[x.down].up = x.up;
                links[x.up].down = x.down;
                --sizes[x.column];
            }
        }
    }

    void restore(int column) {
        auto &c = links[column];
        for (int i = c.up; i != column; i = links[i].up) {
            for (int j = links[i].left; j != i; j = links[j].left) {
                auto &x = links[j];
                ++sizes[x.column];
                links[x.up].down = links[x.down].up = j;
            }
        }
        links[c.left].right = links[c.right].left = column;
    }

public:
    std::vector<Arm<Length>> arms, answer;

    Search(int a, int b, int columns, int limit)
        : links(columns+1), sizes(columns+1), remaining{a, b}, budget(limit) {
        for (int i = 0; i <= columns; ++i)
            links[i] = {(i+columns)%(columns+1), (i+1)%(columns+1), i, i, i, -1};
    }

    void add(int arm, std::array<int,2*Length> columns) {
        int first = static_cast<int>(links.size());
        for (int j = 0; j < width; ++j) {
            int column = columns[j], i = first+j, above = links[column].up;
            links.push_back({first+(j+width-1)%width, first+(j+1)%width, above, column, column, arm});
            links[above].down = links[column].up = i;
            ++sizes[column];
        }
    }

    void shuffle(unsigned trial) {
        std::mt19937 rng(trial);
        for (int j = static_cast<int>(arms.size()); j > 1; --j)
            std::swap(arms[j-1], arms[rng()%j]);
    }

    bool solve() {
        if (!links[0].right) return true;
        if (--budget < 0) return false;
        int column = links[0].right;
        for (int j = links[column].right; j; j = links[j].right)
            if (sizes[j] < sizes[column]) column = j;
        hide(column);
        for (int i = links[column].down; i != column && budget > 0; i = links[i].down) {
            auto arm = arms[links[i].arm];
            if (!remaining[arm[0]]) continue;
            --remaining[arm[0]];
            answer.push_back(arm);
            for (int j = links[i].right; j != i; j = links[j].right) hide(links[j].column);
            if (solve()) return true;
            for (int j = links[i].left; j != i; j = links[j].left) restore(links[j].column);
            ++remaining[arm[0]];
            answer.pop_back();
        }
        restore(column);
        return false;
    }
};
}

extern "C" int armsearch(int a, int b, int lower, int cutoff, unsigned trial, int limit, int* out) {
    const int n = 2*(a+b+1), upper = lower+n-1;
    auto speed = [&](int x) {
        int relative = x + (x%2 != 0);
        return cutoff ? (relative >= cutoff) - (relative <= -cutoff) : 0;
    };
    if (lower > 0 || upper < 1 || (cutoff && (lower > -cutoff || upper < cutoff-2))) return 0;
    std::vector<int> vertex(n), weight(n);
    int columns = 0;
    for (int x = lower; x <= upper; ++x)
        if (x != 0 && x != 1) vertex[x-lower] = ++columns;
    for (int y = lower+1; y <= upper; ++y)
        if (y != 1) weight[y-lower] = ++columns;
    Search<2> search(a, b, columns, limit);
    for (int c : {0, 1}) for (int p = lower; p <= upper; ++p) {
        int y = c+p;
        if (!vertex[p-lower] || y <= lower || y > upper || !weight[y-lower]) continue;
        for (int x = lower; x <= upper; ++x) {
            int z = p+x;
            if (p == x || !vertex[x-lower] || y == z || z <= lower || z > upper || !weight[z-lower])
                continue;
            if (speed(p) == speed(y) && speed(p)+speed(x) == speed(z))
                search.arms.push_back({c, p, x});
        }
    }
    search.shuffle(trial);
    for (int i = 0; i < static_cast<int>(search.arms.size()); ++i) {
        auto [c, p, x] = search.arms[i];
        search.add(i, {vertex[p-lower], vertex[x-lower], weight[c+p-lower], weight[p+x-lower]});
    }
    if (!search.solve()) return 0;
    for (auto [c, p, x] : search.answer) {
        *out++ = c;
        *out++ = p;
        *out++ = x;
    }
    return 1;
}

extern "C" int pathsearch(int a, int b, int lower, int d, unsigned trial, int limit, int* out) {
    const int n = 2+3*(a+b), upper = lower+n-1;
    if (lower > 0 || upper < 1 || (d && (lower > 3*(1-d) || upper < 3*d))) return 0;
    auto speed = [&](int x, int origin) {
        return d ? (x >= 3*d+origin) - (x < 3*(1-d)+origin) : 0;
    };
    std::vector<int> vertex(n), weight(n);
    int columns = 0;
    for (int x = lower; x <= upper; ++x)
        if (x != 0 && x != 1) vertex[x-lower] = ++columns;
    for (int y = lower+1; y <= upper; ++y)
        if (y != 1) weight[y-lower] = ++columns;
    Search<3> search(a, b, columns, limit);
    auto available = [&](int parent, int child) {
        const int sum = parent+child;
        return vertex[child-lower] && sum > lower && sum <= upper && weight[sum-lower]
            && speed(parent,0)+speed(child,0) == speed(sum,1);
    };
    for (int c : {0, 1}) for (int p = lower; p <= upper; ++p) {
        if (!available(c,p)) continue;
        for (int q = lower; q <= upper; ++q) {
            if (p == q || !available(p,q)) continue;
            for (int x = lower; x <= upper; ++x)
                if (x != p && x != q && available(q,x) && c+p != q+x)
                    search.arms.push_back({c,p,q,x});
        }
    }
    search.shuffle(trial);
    for (int i = 0; i < static_cast<int>(search.arms.size()); ++i) {
        auto [c,p,q,x] = search.arms[i];
        search.add(i, {vertex[p-lower], vertex[q-lower], vertex[x-lower],
                       weight[c+p-lower], weight[p+q-lower], weight[q+x-lower]});
    }
    if (!search.solve()) return 0;
    for (const auto& arm : search.answer)
        for (int x : arm) *out++ = x;
    return 1;
}
