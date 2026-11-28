// A forest type is the multiset of (component order, number of rooted tips).
#pragma once
#include <algorithm>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

struct ForestType {
    std::vector<std::pair<int,int>> parts;
    int stem = 0; // vertices on the path ending at the first branching vertex
    int mass = 0;
    ForestType(int k, int count, char** names) {
        if (!count) throw std::invalid_argument("empty forest type");
        std::string first(names[0]);
        int start = 0;
        if (first.rfind("stem=",0) == 0) {
            std::size_t end = 0;
            stem = std::stoi(first.substr(5),&end);
            if (end+5 != first.size() || stem < 1 || stem >= k-1 || count < 3)
                throw std::invalid_argument("expected a positive stem and at least two branches");
            mass = stem;
            start = 1;
        }
        for (int i = start; i < count; ++i) {
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
            if (mass >= k) throw std::invalid_argument("forest type too large");
        }
        std::sort(parts.begin(),parts.end());
    }
};
