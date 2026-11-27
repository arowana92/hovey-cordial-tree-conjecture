// Check ordinary integer sums, canonical unrooted encodings, and the free-tree count.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {
using Word = std::uint64_t;
using Child = std::pair<int,Word>;
void require(bool ok, const char* why) { if (!ok) throw std::runtime_error(why); }

Word free_count(int n) {
    // Logarithmic derivative of the rooted-tree multiset product.
    std::vector<Word> rooted(n+1);
    rooted[1] = 1;
    for (int s = 2; s <= n; ++s) {
        Word sum = 0;
        for (int j = 1; j < s; ++j)
            for (int d = 1; d <= j; ++d)
                if (j%d == 0) sum += d*rooted[d]*rooted[s-j];
        require(sum%(s-1) == 0,"nonintegral rooted count");
        rooted[s] = sum/(s-1);
    }
    Word pairs = 0;
    for (int j = 1; j < n; ++j) pairs += rooted[j]*rooted[n-j];
    if (n%2 == 0) pairs -= rooted[n/2];
    require(pairs%2 == 0,"nonintegral edge-root count");
    return rooted[n]-pairs/2;
}

Word leaf_limited_count(int n, int limit) {
    // The logarithmic derivative of the branch multiset product also tracks
    // terminal count. A singleton is one terminal, and an empty forest has none.
    using Row = std::vector<Word>;
    std::vector<Row> trees(n+1,Row(limit+1)), forests(n,Row(limit+1));
    trees[1][1] = forests[0][0] = 1;
    for (int mass=1; mass<n; ++mass) {
        for (int size=1; size<=mass; ++size)
            for (int copies=1; copies*size<=mass; ++copies)
                for (int tips=1; copies*tips<=limit; ++tips)
                    for (int t=copies*tips; t<=limit; ++t)
                        forests[mass][t] += size*trees[size][tips]*forests[mass-copies*size][t-copies*tips];
        for (int t=1; t<=limit; ++t) {
            require(forests[mass][t]%mass==0,"nonintegral planted count");
            forests[mass][t] /= mass;
            trees[mass+1][t] = forests[mass][t];
        }
    }
    Word total = 0;
    for (int t=2; t<=limit; ++t) {
        Word vertex_rooted = trees[n][t]-trees[n-1][t]+trees[n-1][t-1];
        Word oriented = 0;
        for (int a=1; a<n; ++a)
            for (int b=1; b<t; ++b) oriented += trees[a][b]*trees[n-a][t-b];
        Word diagonal = (n%2 || t%2) ? 0 : trees[n/2][t/2];
        require((oriented-diagonal)%2==0,"nonintegral leaf-refined edge count");
        total += vertex_rooted-(oriented-diagonal)/2;
    }
    return total;
}

struct Key {
    bool two = false;
    int count = 0;
    Child entries[32]{};
    bool operator<(const Key& other) const {
        if (two != other.two) return two < other.two;
        return std::lexicographical_compare(entries,entries+count,other.entries,other.entries+other.count);
    }
};

Key check_tree(const unsigned char* record, int n, int limit, bool modular) {
    Word word = 0, vertices = 0, weights = 0;
    for (int i = 7; i >= 0; --i) word = 256*word+record[i];
    require(!(word>>(2*n)),"high bits outside tree");
    int depth = 0, nodes = 0, tips = 0, lo = 2*n, hi = -1;
    struct Frame { int bit, label; Child previous; };
    Frame stack[32];
    Key key;
    for (int bit = 2*n-1; bit >= 0; --bit) {
        if ((word>>bit)&1) {
            require(nodes < n && (depth || nodes == 0),"invalid root or node count");
            int x = record[8+nodes++];
            require(x < n && !(vertices&(Word(1)<<x)),"vertex labels do not form a permutation");
            vertices |= Word(1)<<x;
            if (depth) {
                int y = x+stack[depth-1].label;
                if (modular) y %= n;
                require(!(weights&(Word(1)<<y)),"repeated edge sum");
                weights |= Word(1)<<y;
                lo = std::min(lo,y);
                hi = std::max(hi,y);
            }
            stack[depth++] = {bit,x,{}};
        } else {
            require(depth > 0,"unmatched closing bracket");
            int length = stack[--depth].bit-bit+1;
            if (length == 2) ++tips;
            Child branch = {length/2,(word>>bit)&((Word(1)<<length)-1)};
            if (depth) {
                require(stack[depth-1].previous <= branch,"unsorted children");
                stack[depth-1].previous = branch;
                if (depth == 1) key.entries[key.count++] = branch;
            }
        }
    }
    require(nodes == n && !depth && key.count > 0,"incomplete tree");
    require(tips+(key.count==1) <= limit,"tree exceeds leaf limit");
    require(modular || hi-lo+1 == n-1,"nonconsecutive integer sums");
    auto largest = key.entries[key.count-1];
    require(2*largest.first <= n,"root is not a centroid");
    if (2*largest.first == n) {
        Word left = (word>>(n+1))<<1, right = largest.second;
        require(left <= right,"halves in wrong order");
        key.two = true;
        key.count = 2;
        key.entries[0] = {n/2,left};
        key.entries[1] = {n/2,right};
    }
    return key;
}
}

int main(int argc,char** argv) {
    if (argc < 3) return 2;
    int n = std::stoi(argv[1]);
    if (n < 2 || n > 30) return 2;
    bool modular = std::string(argv[2])=="--modular-leaves";
    bool limited = modular || std::string(argv[2])=="--leaves";
    if (limited && argc<5) return 2;
    int limit = limited ? std::stoi(argv[3]) : n;
    if (limit < 2 || limit > n) return 2;
    std::vector<FILE*> files;
    for (int i = limited ? 4 : 2; i < argc; ++i) {
        files.push_back(std::fopen(argv[i],"rb"));
        require(files.back() != nullptr,"cannot open input");
    }
    Word total = limited ? leaf_limited_count(n,limit) : free_count(n), two = 0;
    Key previous;
    unsigned char record[40];
    for (Word i = 0; i < total; ++i) {
        require(std::fread(record,1,n+8,files[i%files.size()]) == static_cast<unsigned>(n+8),
                "short input");
        Key key = check_tree(record,n,limit,modular);
        require(!i || previous < key,"repeated or out-of-order unrooted shape");
        two += key.two;
        previous = key;
    }
    for (auto file : files) {
        require(std::fgetc(file) == EOF && !std::ferror(file),"trailing data or read failure");
        std::fclose(file);
    }
    std::cout << n << " " << total << " " << total-two << " " << two << "\n";
}
