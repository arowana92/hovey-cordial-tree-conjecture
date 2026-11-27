// Independently parse the rooted decorations, check the matching type and both permutations.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

constexpr int n = 26;
using Mask = std::uint32_t;

void require(bool condition, const char* reason) {
    if (!condition) throw std::runtime_error(reason);
}

struct Check {
    std::array<int,n> labels;
    Mask weights = 0;
    int next;

    void edge(int u, int v) {
        Mask bit = 1U << ((labels[u]+labels[v])%n);
        require(!(weights & bit),"repeated weight");
        weights |= bit;
    }

    // Return true if the root must use a matching edge on its parent side.
    bool subtree(const std::string& word, int& pos, int root) {
        require(pos < int(word.size()) && word[pos++] == '(',"invalid subtree");
        std::string prev;
        int waiting = 0;
        while (pos < int(word.size()) && word[pos] == '(') {
            int start = pos, child = next++;
            require(child < n,"excess vertices");
            edge(root,child);
            waiting += subtree(word,pos,child);
            std::string current = word.substr(start,pos-start);
            require(prev <= current,"unordered siblings");
            prev = current;
        }
        require(pos < int(word.size()) && word[pos++] == ')',"unterminated subtree");
        require(waiting <= 1,"no matching at a decoration");
        return waiting == 0;
    }

    void verify(const std::string& key, int extra) {
        std::vector<std::string> sites;
        std::istringstream fields(key);
        for (std::string site; std::getline(fields,site,'.');) sites.push_back(site);
        int c = sites.size();
        require(c >= 3 && c <= n && key.back() != '.',"invalid cycle");
        for (int i = 0; i < c; ++i) for (int sign : {-1,1}) {
            int j = 0;
            while (j < c && sites[j] == sites[(i+sign*j+c)%c]) ++j;
            require(j == c || sites[j] < sites[(i+sign*j+c)%c],"noncanonical ring");
        }
        next = c;
        int free = 0, anchor = -1;
        std::vector<bool> open(c);
        for (int i = 0; i < c; ++i) {
            edge(i,(i+1)%c);
            int pos = 0;
            open[i] = subtree(sites[i],pos,i);
            require(pos == int(sites[i].size()),"trailing tokens");
            if (open[i]) ++free;
            else anchor = i;
        }
        int run = 0;
        for (int j = 1; j <= c; ++j) {
            if (open[(anchor+j)%c]) ++run;
            else {
                require(run%2 == 0,"odd unmatched run");
                run = 0;
            }
        }
        require(run%2 == 0 && free%2 == 0 && n/2-c+free/2 == extra,
                "wrong number of off-path pairs");
        require(next == n && weights == (1U<<n)-1,"incomplete graph or weight list");
    }
};

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    int extra = std::stoi(argv[1]);
    std::string line, prev;
    long count = 0;
    while (std::getline(std::cin,line)) {
        std::istringstream input(line);
        std::string key, tail;
        require(bool(input >> key) && prev < key,"unordered or repeated record");
        Check record;
        Mask vertices = 0;
        for (int& x : record.labels) {
            require(bool(input >> x) && 0 <= x && x < n,"invalid label");
            vertices |= 1U<<x;
        }
        require(vertices == (1U<<n)-1 && !(input >> tail),"invalid permutation");
        record.verify(key,extra);
        prev = key;
        ++count;
    }
    std::cout << count << '\n';
}
