#pragma once
// Produce explicit bijections on the unicyclic graphs listed on standard input.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using Mask = std::uint32_t;

struct Graph {
    int cycle;
    std::vector<int> parent, degree;
    explicit Graph(const std::string& key) {
        cycle = 1 + std::count(key.begin(),key.end(),'.');
        parent.resize(cycle,-1);
        degree.resize(cycle,2);
        int site = 0;
        std::vector<int> stack;
        for (char token : key) {
            if (token == '.') {
                ++site;
            } else if (token == ')') {
                stack.pop_back();
            } else if (stack.empty()) {
                stack.push_back(site);
            } else {
                int u = stack.back(), v = parent.size();
                parent.push_back(u);
                degree.push_back(1);
                ++degree[u];
                stack.push_back(v);
            }
        }
    }
};

class Search {
    const Graph& g;
    int n, internal, budget;
    Mask all, seed = 1991;
    std::vector<int> order;
    Mask random() {
        seed ^= seed << 13;
        seed ^= seed >> 17;
        return seed ^= seed << 5;
    }
    bool place(int i, Mask unused, Mask weights, int moment) {
        if (--budget < 0) return false;
        if (i == n) return true;
        int v = order[i], u = v < g.cycle ? v-1 : g.parent[v];
        int a = label[u];
        Mask possible = unused & ((weights>>a)|(weights<<(n-a)));
        Mask split = (1U << (random()%n))-1;
        for (Mask choices : {possible & ~split, possible & split}) {
            for (; choices; choices &= choices-1) {
                int x = __builtin_ctz(choices);
                int next = moment + (g.degree[v]-1)*x;
                if (i == internal-1 && next%n) continue;
                Mask rest = weights ^ (1U<<((a+x)%n));
                if (v == g.cycle-1) {
                    if (!(rest & (1U<<x))) continue;
                    rest ^= 1U<<x;
                }
                label[v] = x;
                if (place(i+1,unused^(1U<<x),rest,next)) return true;
                if (budget < 0) return false;
            }
        }
        return false;
    }
public:
    std::vector<int> label;
    Search(const Graph& graph, const std::string& key):
        g(graph), n(g.parent.size()), all((1U<<n)-1), label(n) {
        for (int i = 0; i < n; ++i) if (g.degree[i]>1) order.push_back(i);
        internal = order.size();
        for (int i = 0; i < n; ++i) if (g.degree[i]==1) order.push_back(i);
        for (unsigned char c : key) seed = (seed^c)*16777619U;
        seed |= 1U;
    }
    bool solve() {
        for (int i = 0; i < 10000; ++i) {
            budget = i < 200 ? 1000 : 20000;
            if (place(1,all-1,all,0)) return true;
            if (budget >= 0) return false;
        }
        return false;
    }
};
