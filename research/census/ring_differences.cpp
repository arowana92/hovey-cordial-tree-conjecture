// Emit harmonious bijections realizing all nonzero differences on every vertex pair at 27.
#include "branched_search.hpp"
#include <array>
#include <numeric>

struct Mark {
    int first, second, covered;
};

int main() {
    constexpr int k = 27;
    std::array<int,2*k-1> classes{};
    for (int d = 1-k; d < k; ++d) {
        int divisor = std::gcd(d,k);
        classes[k-1+d] = divisor == 1 ? 1 : divisor == 3 ? 2 : 4;
    }
    std::string key;
    while (std::cin >> key) {
        Graph graph(key);
        if (graph.parent.size() != k || graph.cycle < 3) return 2;
        Search search(graph, key);
        std::vector<Mark> missing;
        for (int i = 0; i < k; ++i)
            for (int j = 0; j < i; ++j) missing.push_back({i,j,0});
        std::cout << key;
        for (int attempt = 0; attempt < 4000 && !missing.empty(); ++attempt) {
            if (!search.solve()) break;
            size_t remaining = 0;
            bool changed = false;
            for (auto mark : missing) {
                int d = search.label[mark.first] - search.label[mark.second];
                int bit = classes[k-1+d];
                changed |= !(mark.covered & bit);
                mark.covered |= bit;
                if (mark.covered != 7) missing[remaining++] = mark;
            }
            missing.resize(remaining);
            if (changed) {
                std::cout << ' ';
                for (int x : search.label) std::cout << char('A' + x);
            }
        }
        if (!missing.empty()) throw std::runtime_error("unresolved vertex pair in " + key);
        std::cout << '\n';
    }
    return std::cin.eof() ? 0 : 2;
}
