#include "branched_search.hpp"

int main(int argc, char** argv) {
    if (argc > 2) return 2;
    int order = argc == 2 ? std::stoi(argv[1]) : 26;
    if (order < 3 || order > 31) return 2;
    std::string key;
    while (std::getline(std::cin,key)) {
        Graph g(key);
        if (g.cycle < 3 || int(g.parent.size()) != order) return 2;
        Search s(g,key);
        if (!s.solve()) throw std::runtime_error("unresolved graph "+key);
        std::cout << key;
        for (int x : s.label) std::cout << ' ' << x;
        std::cout << '\n';
    }
}
