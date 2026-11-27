#include "branched_search.hpp"

int main() {
    std::string key;
    while (std::getline(std::cin,key)) {
        Graph g(key);
        if (g.cycle < 3 || g.parent.size() != 26) return 2;
        Search s(g,key);
        if (!s.solve()) throw std::runtime_error("unresolved graph "+key);
        std::cout << key;
        for (int x : s.label) std::cout << ' ' << x;
        std::cout << '\n';
    }
}
