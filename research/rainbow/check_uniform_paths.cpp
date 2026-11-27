// Verify the full vertex and edge permutations independently of the search.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

void require(bool ok, const char* message) {
    if (!ok) throw std::runtime_error(message);
}

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    int k = std::stoi(argv[1]);
    if (k < 2 || k > 63) return 2;
    std::vector<int> previous;
    std::vector<bool> covered(k);
    long long shapes = 0, rows = 0, assignments = 0;
    auto finish = [&]() {
        bool mixed = previous.size() > 1 && previous[0] < previous[1];
        int differences = mixed ? k : 1;
        for (int i = 0; i < differences; ++i) require(covered[i], "uncovered parent pair");
        assignments += k*differences;
        ++shapes;
    };
    std::string line;
    while (std::getline(std::cin, line)) {
        std::istringstream input(line);
        int modulus, x;
        require(bool(input >> modulus >> x) && modulus == k && 0 <= x && x < k, "bad header");
        std::vector<int> lengths;
        int total = 0;
        while (total < k) {
            int n;
            require(bool(input >> n) && n >= 1 && n <= k-total, "bad path length");
            lengths.push_back(n);
            total += n;
        }
        require(std::is_sorted(lengths.begin(), lengths.end()), "unsorted lengths");
        if (lengths != previous) {
            if (!previous.empty()) finish();
            require(previous < lengths, "unordered or repeated partition");
            previous = lengths;
            std::fill(covered.begin(), covered.end(), false);
        }
        std::string word, extra;
        require(bool(input >> word) && int(word.size()) == k && !(input >> extra), "bad labels");
        require(!covered[x], "repeated difference orbit");
        std::vector<bool> vertex(k), edge(k);
        int i = 0;
        for (int n : lengths) {
            int parent = i == 0 ? x : 0;
            for (int j = 0; j < n; ++j) {
                int digit = word[i++]-'!';
                require(0 <= digit && digit < k && !vertex[digit], "repeated vertex label");
                int w = (parent+digit)%k;
                require(!edge[w], "repeated edge weight");
                vertex[digit] = edge[w] = true;
                parent = digit;
            }
        }
        for (int u = 1; u < k; ++u) if (std::gcd(u,k) == 1) covered[(u*x)%k] = true;
        ++rows;
    }
    if (!previous.empty()) finish();
    std::vector<long long> part(k+1);
    part[0] = 1;
    for (int n = 1; n <= k; ++n) for (int v = n; v <= k; ++v) part[v] += part[v-n];
    require(shapes == part[k], "incomplete partition catalog");
    std::cout << k << ' ' << shapes << ' ' << rows << ' ' << assignments << '\n';
}
