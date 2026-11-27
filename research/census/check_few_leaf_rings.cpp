// Independently parse the graph, count its leaves, and check its two bijections.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

void require(bool condition, const char* reason) {
    if (!condition) throw std::runtime_error(reason);
}

struct Ring {
    int order, cycle, next, tips = 0;
    std::vector<std::pair<int,int>> edges;

    void tree(const std::string& word, size_t& pos, int root) {
        require(pos < word.size() && word[pos++] == '(', "invalid subtree");
        std::string previous;
        bool leaf = true;
        while (pos < word.size() && word[pos] == '(') {
            leaf = false;
            size_t start = pos;
            int child = next++;
            require(child < order, "too many vertices");
            edges.emplace_back(root, child);
            tree(word, pos, child);
            std::string current = word.substr(start, pos-start);
            require(previous <= current, "unordered children");
            previous = current;
        }
        require(pos < word.size() && word[pos++] == ')', "unterminated subtree");
        tips += leaf && root >= cycle;
    }

    Ring(const std::string& key, int k): order(k) {
        std::istringstream parts(key);
        std::vector<std::string> sites;
        for (std::string word; std::getline(parts, word, '.');) sites.push_back(word);
        cycle = sites.size();
        require(cycle >= 3 && cycle <= order && key.back() != '.', "invalid cycle");
        next = cycle;
        for (int i = 0; i < cycle; ++i) {
            for (int sign : {-1, 1}) {
                int j = 0;
                while (j < cycle && sites[j] == sites[(i+sign*j+cycle)%cycle]) ++j;
                require(j == cycle || sites[j] < sites[(i+sign*j+cycle)%cycle], "noncanonical cycle");
            }
            edges.emplace_back(i, (i+1)%cycle);
            size_t pos = 0;
            tree(sites[i], pos, i);
            require(pos == sites[i].size(), "trailing subtree data");
        }
        require(next == order && int(edges.size()) == order, "wrong graph size");
    }
};

// Test the surgery on an actual single-edge core. A common translation covers
// all possible labels of the first old endpoint. Test both port orientations.
void check_operations(const Ring& ring, const std::vector<int>& x) {
    int k=ring.order;
    for (int i=0; i<ring.cycle; ++i) for (int sign : {1,-1}) {
        int u=i, v=(i+sign+ring.cycle)%ring.cycle;
        std::vector<int> label(k), vertices(k);
        for (int j=0; j<k; ++j) {
            label[j]=(x[j]+k-x[v])%k;
            ++vertices[label[j]];
        }
        require(std::count(vertices.begin(),vertices.end(),1)==k, "vertex increment");
        for (int b=0; b<k; ++b) {
            std::vector<int> net(k);
            --net[b];
            ++net[label[u]];
            ++net[(label[v]+b)%k];
            for (auto [p,q] : ring.edges)
                if (!((p==u && q==v) || (p==v && q==u))) ++net[(label[p]+label[q])%k];
            require(std::count(net.begin(),net.end(),1)==k, "edge increment");
        }
    }
    for (int d : {3,5}) {
        std::vector<int> vertices(d*k), edges(d*k);
        for (int j=0; j<d; ++j) {
            for (int a : x) ++vertices[a+k*j];
            for (auto [u,v] : ring.edges) {
                int next=(u==ring.cycle-1 && v==0) ? (j+1)%d : j;
                ++edges[(x[u]+k*j+x[v]+k*next)%(d*k)];
            }
        }
        require(std::count(vertices.begin(),vertices.end(),1)==d*k &&
                std::count(edges.begin(),edges.end(),1)==d*k, "odd cover");
    }
}

int main(int argc, char** argv) {
    if (argc != 4) return 2;
    int k = std::stoi(argv[1]), leaves = std::stoi(argv[2]);
    require(k >= 3 && k <= 31, "unsupported order");
    std::vector<int> counts(k+1);
    std::unordered_set<std::uint64_t> seen;
    std::uint32_t all = (1U<<k)-1;
    for (std::string line; std::getline(std::cin, line);) {
        std::istringstream row(line);
        std::string key, tail;
        require(bool(row >> key), "missing key");
        Ring ring(key, k);
        require(ring.tips == leaves, "wrong leaf count");
        // Balanced components identify the missing separators uniquely.
        std::uint64_t id = 0;
        for (char c : key) if (c != '.') id = 2*id + (c == '(');
        require(seen.insert(id).second, "duplicate shape");
        ++counts[ring.cycle];
        std::vector<int> labels(k);
        std::uint32_t vertices = 0, weights = 0;
        for (int& x : labels) {
            require(bool(row >> x) && x >= 0 && x < k, "invalid label");
            vertices |= 1U<<x;
        }
        require(!(row >> tail) && vertices == all, "invalid vertex permutation");
        for (auto [u,v] : ring.edges) weights |= 1U<<((labels[u]+labels[v])%k);
        require(weights == all, "invalid edge permutation");
        if (counts[ring.cycle] == 1) check_operations(ring, labels);
    }
    std::ifstream expected(argv[3]);
    for (int c = 3; c <= k; ++c) {
        int length, want;
        require(bool(expected >> length >> want) && length == c && counts[c] == want,
                "cycle count differs from independent enumeration");
    }
    std::string tail;
    require(!(expected >> tail), "extra count data");
    std::cout << k << ' ' << leaves << ' ' << seen.size() << '\n';
}
