// Independent verification of ranked depth strings, structural reductions, and all sums.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>

namespace {
constexpr int limit = 30;
using List = std::array<int, limit+1>;
using Count = std::uint64_t;
using Matrix = std::array<List, limit+1>;

void require(bool test, const char* message) {
    if (!test) throw std::runtime_error(message);
}

Count rooted_count(int n) {
    std::array<Count, limit+1> t{}, divisor_sum{};
    t[1] = 1;
    for (int i = 1; i < n; ++i) {
        for (int j = i; j < n; j += i) divisor_sum[j] += i*t[i];
        Count value = 0;
        for (int j = 1; j <= i; ++j) value += divisor_sum[j]*t[i+1-j];
        require(value % i == 0, "nonintegral rooted-tree count");
        t[i+1] = value/i;
    }
    return t[n];
}

void tree(int n, const List& depth, List& parent, List& degree) {
    List stack{}, end{}, last;
    last.fill(-1);
    for (int i = 1; i < n; ++i) {
        require(depth[i] > 0 && depth[i] <= depth[i-1]+1, "invalid depth");
        int p = stack[depth[i]-1];
        parent[i] = p;
        ++degree[p];
        ++degree[i];
        stack[depth[i]] = i;
    }
    for (int i = n-1; i >= 0; --i) {
        end[i] = std::max(end[i], i+1);
        if (i) end[parent[i]] = std::max(end[parent[i]], end[i]);
    }
    for (int i = 1; i < n; ++i) {
        int prev = last[parent[i]];
        if (prev >= 0) {
            require(!std::lexicographical_compare(depth.begin()+prev, depth.begin()+end[prev],
                                                  depth.begin()+i, depth.begin()+end[i]),
                    "noncanonical sibling subtrees");
        }
        last[parent[i]] = i;
    }
}

bool structural(int n, const List& parent, List degree) {
    if (n == 1) return true;
    for (int i = 1; i < n; ++i) if (parent[i] == 0 && degree[i] == 1) return true;
    ++degree[0]; // One additional leaf at the root fixes the maximal nonleaf core.
    if (std::count_if(degree.begin(), degree.begin()+n, [](int d) { return d > 1; }) <= 5)
        return true;
    List core_degree{};
    for (int v = 1; v < n; ++v) {
        int p = parent[v];
        if (degree[v] > 1 && degree[p] > 1) { ++core_degree[p]; ++core_degree[v]; }
    }
    if (*std::max_element(core_degree.begin(), core_degree.begin()+n) <= 2) return true;
    // Direct all-pairs distances in the augmented tree.
    Matrix distance{};
    for (int i = 1; i <= n; ++i) {
        int p = i == n ? 0 : parent[i];
        for (int j = 0; j < i; ++j) distance[j][i] = distance[i][j] = distance[p][j]+1;
    }
    for (int i = 0; i <= n; ++i) {
        if (*std::max_element(distance[i].begin(), distance[i].begin()+n+1) <= 2) return true;
    }
    return false;
}

void check(int n) {
    Count shapes = 0, reductions = 0;
    List previous{};
    while (std::cin.peek() != std::char_traits<char>::eof()) {
        List depths{}, parent{}, degree{};
        for (int i = 1; i < n; ++i) depths[i] = std::cin.get();
        int kind = std::cin.get();
        require(kind == 0 || kind == 1, "unexpected or truncated record");
        tree(n, depths, parent, degree);
        require(!shapes || depths < previous, "unordered or duplicated tree");
        previous = depths;
        ++shapes;
        if (!kind) {
            require(structural(n, parent, degree), "unproved reduction");
            ++reductions;
            continue;
        }
        List label{}, vertex_count{}, edge_count{};
        for (int i = 0; i < n; ++i) {
            int x = label[i] = std::cin.get();
            require(0 <= x && x < n && ++vertex_count[x] == 1, "invalid vertex labeling");
        }
        for (int v = 1; v < n; ++v) {
            int x = label[v]+label[parent[v]]-label[0];
            require(1 <= x && x < n && ++edge_count[x] == 1, "invalid edge interval");
        }
    }
    require(!std::cin.bad() && shapes == rooted_count(n), "incomplete rooted-tree stream");
    std::cout << n << " " << shapes << " " << reductions << " " << shapes-reductions << "\n";
}
}

int main(int argc, char** argv) {
    if (argc != 2) return 1;
    int n = std::atoi(argv[1]);
    if (n < 1 || n > limit) return 1;
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    try { check(n); } catch (const std::exception& e) { std::cerr << e.what() << "\n"; return 1; }
}
