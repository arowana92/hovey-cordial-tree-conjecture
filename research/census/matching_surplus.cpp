// Construct uniform attachments on rooted matching quotients and their exceptions.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>

#include "../rainbow/tip_forests.hpp"

using Word = std::uint64_t;

std::vector<int> parents(Word forest, int k) {
    std::vector<int> parent{-1}, stack{0};
    for (int bit = 2*k-1; bit >= 0; --bit) {
        if ((forest >> bit) & 1) {
            parent.push_back(stack.back());
            stack.push_back(static_cast<int>(parent.size())-1);
        } else {
            stack.pop_back();
        }
    }
    return parent;
}

class Search {
    int k, internal = 0;
    std::vector<int> parent, degree, order, previous;
    std::uint32_t state = 1991;
    int budget = 0;
    bool bounded = false;

    bool place(int at, std::uint32_t used, std::uint32_t weights, int moment) {
        if (bounded && --budget < 0) return false;
        if (at == k) return true;
        int v = order[at], first = previous[v] ? labels[previous[v]]+1 : 0;
        int start = 0;
        if (bounded) {
            state = state*1664525U+1013904223U;
            start = state%k;
        }
        for (int t = 0; t < k; ++t) {
            int x = (start+t)%k, y = (x+labels[parent[v]])%k;
            if (x < first || ((used >> x) & 1) || ((weights >> y) & 1)) continue;
            int sum = moment+degree[v]*x;
            if (at+1 == internal && sum%k != 0) continue;
            labels[v] = x;
            if (place(at+1, used|(1U<<x), weights|(1U<<y), sum)) return true;
            if (bounded && budget < 0) return false;
        }
        return false;
    }

public:
    std::vector<int> labels;

    explicit Search(std::vector<int> tree):
        k(static_cast<int>(tree.size())-1), parent(std::move(tree)),
        degree(k+1), previous(k+1), labels(k+1) {
        for (int v = 1; v <= k; ++v) ++degree[parent[v]];
        for (int v = 1; v <= k; ++v) if (degree[v]) order.push_back(v);
        internal = static_cast<int>(order.size());
        for (int u = 0; u <= k; ++u) {
            int last = 0;
            for (int v = 1; v <= k; ++v) {
                if (parent[v] != u || degree[v]) continue;
                previous[v] = last;
                last = v;
                order.push_back(v);
            }
        }
    }

    bool solve(bool retries) {
        bounded = retries;
        if (!bounded) return place(0,0,0,0);
        for (int i = 0; i < 200; ++i) {
            budget = i < 12 ? 8000 : 100000;
            if (place(0,0,0,0)) return true;
        }
        return false;
    }
};

Word expansion_code(const std::vector<int>& p, unsigned choices) {
    // The edge arriving at a pair always enters its first endpoint.
    std::vector<int> expanded{-1};
    for (int i = 1; i < static_cast<int>(p.size()); ++i) {
        int u = p[i];
        expanded.push_back(u ? 2*u-1+static_cast<int>(choices & 1) : 0);
        expanded.push_back(2*i-1);
        if (u) choices >>= 1;
    }
    std::vector<std::vector<std::string>> children(expanded.size());
    for (int i = static_cast<int>(expanded.size())-1; i >= 0; --i) {
        auto& row = children[i];
        std::sort(row.begin(),row.end());
        std::string contents;
        for (const auto& s : row) contents += s;
        if (i == 0) return std::stoull(contents,nullptr,2);
        children[expanded[i]].push_back("1"+contents+"0");
    }
    throw std::logic_error("missing root");
}

void record(char type, Word code, const std::vector<int>& labels) {
    std::cout << type << ' ' << code;
    for (std::size_t i = 1; i < labels.size(); ++i) std::cout << ' ' << labels[i];
    std::cout << '\n';
}

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    int m = std::stoi(argv[1]);
    if (m < 3 || m > 15 || m%2 == 0) return 2;
    TipForests quotient(m,m);
    std::set<Word> expanded;
    quotient.each(m,[&](Word code) {
        auto p = parents(code,m);
        Search search(p);
        if (search.solve(false)) {
            record('Q',code,search.labels);
        } else {
            record('Q',code,{});
            unsigned splits = 1U << std::count_if(p.begin(),p.end(),[](int x){ return x > 0; });
            for (unsigned mask = 0; mask < splits; ++mask) expanded.insert(expansion_code(p,mask));
        }
    });
    for (Word code : expanded) {
        Search search(parents(code,2*m));
        if (!search.solve(true)) throw std::runtime_error("missing expansion witness "+std::to_string(code));
        record('E',code,search.labels);
    }
    return !std::cout;
}
