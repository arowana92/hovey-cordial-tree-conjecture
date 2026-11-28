// A forest type is the multiset of (component order, number of rooted tips).
#pragma once
#include <algorithm>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

struct ForestType {
    std::vector<std::pair<int,int>> parts;
    int mass = 0;
    int tips = 0;
    ForestType(int k, int count, char** names) {
        if (!count) throw std::invalid_argument("empty forest type");
        for (int i = 0; i < count; ++i) {
            std::string name(names[i]);
            std::size_t at = 0, end = 0;
            int size = std::stoi(name,&at);
            if (at >= name.size() || name[at] != ',') throw std::invalid_argument("expected order,tips");
            auto second = name.substr(at+1);
            int leaves = std::stoi(second,&end);
            if (end != second.size() || size < 1 || size >= k || leaves < 1 ||
                leaves > std::max(1,size-1)) throw std::invalid_argument("invalid component type");
            parts.emplace_back(size,leaves);
            mass += size;
            tips += leaves;
            if (mass >= k) throw std::invalid_argument("forest type too large");
        }
        if (tips > 2*(k-2)/3) throw std::invalid_argument("outside ordered-cut tip bound");
        std::sort(parts.begin(),parts.end());
    }
};
