// Exact-cover search for a fixed interval and two prescribed center labels.
#include <algorithm>
#include <array>
#include <random>
#include <vector>

namespace {
struct Arm {
    int center, parent, tip;
};

// Circular column and row lists for Algorithm X. Each row has four incidences.
struct Incidence {
    int left, right, up, down, column, arm;
};

class Search {
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
    std::vector<Arm> arms, answer;

    Search(int a, int b, int columns, int limit)
        : links(columns+1), sizes(columns+1), remaining{a, b}, budget(limit) {
        for (int i = 0; i <= columns; ++i)
            links[i] = {(i+columns)%(columns+1), (i+1)%(columns+1), i, i, i, -1};
    }

    void add(int arm, std::array<int,4> columns) {
        int first = static_cast<int>(links.size());
        for (int j = 0; j < 4; ++j) {
            int column = columns[j], i = first+j, above = links[column].up;
            links.push_back({first+(j+3)%4, first+(j+1)%4, above, column, column, arm});
            links[above].down = links[column].up = i;
            ++sizes[column];
        }
    }

    bool solve() {
        if (!links[0].right) return true;
        if (--budget < 0) return false;
        int column = links[0].right;
        for (int j = links[column].right; j; j = links[j].right)
            if (sizes[j] < sizes[column]) column = j;
        hide(column);
        for (int i = links[column].down; i != column && budget > 0; i = links[i].down) {
            Arm arm = arms[links[i].arm];
            if (!remaining[arm.center]) continue;
            --remaining[arm.center];
            answer.push_back(arm);
            for (int j = links[i].right; j != i; j = links[j].right) hide(links[j].column);
            if (solve()) return true;
            for (int j = links[i].left; j != i; j = links[j].left) restore(links[j].column);
            ++remaining[arm.center];
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
    Search search(a, b, columns, limit);
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
    std::mt19937 rng(trial);
    for (int j = static_cast<int>(search.arms.size()); j > 1; --j)
        std::swap(search.arms[j-1], search.arms[rng()%j]);
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
