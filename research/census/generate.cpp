// Enumerate unrooted trees at their one or two centroids.
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
#include "../rainbow/ranked_forest.hpp"
#include "leaf_centroids.hpp"

bool interval_witness(int, const int*, int*, std::uint32_t);
namespace {
using Code = std::uint64_t;
struct Rooted { int size; Code code; };

class Census {
    int n, shard, shards;
    FILE* out;
    std::uint64_t index = 0, written = 0;
    std::vector<Rooted> catalog;

    template<class Emit>
    void forests(int remaining, std::size_t start, int max_size, Code word, Emit& emit) {
        if (!remaining) { emit(word); return; }
        for (std::size_t i = start; i < catalog.size(); ++i) {
            auto t = catalog[i];
            if (t.size > remaining || t.size > max_size) break;
            forests(remaining-t.size,i,max_size,(word<<(2*t.size))|t.code,emit);
        }
    }

    void certify(Code word) {
        int stack[32], parents[32], labels[32], depth = 0, count = 0;
        for (int j = 2*n-1; j >= 0; --j) {
            if ((word>>j)&1) {
                parents[count] = depth ? stack[depth-1] : -1;
                stack[depth++] = count++;
            } else --depth;
        }
        std::uint32_t seed = 42+word+(word>>32);
        bool found = false;
        for (unsigned trial = 0; trial < 32 && !found; ++trial)
            found = interval_witness(n,parents,labels,seed+0x9e3779b9U*trial);
        if (!found) throw std::runtime_error("missing witness at "+std::to_string(word));
        unsigned char record[40];
        for (int i = 0; i < 8; ++i) record[i] = (word>>(8*i))&255;
        std::copy_n(labels,n,record+8);
        if (std::fwrite(record,n+8,1,out) != 1) throw std::runtime_error("write failed");
        ++written;
    }
public:
    Census(int order, int part, int total, FILE* file): n(order),shard(part),shards(total),out(file) {}
    void limited(int leaves) {
        LeafCentroids trees(n,leaves);
        trees.each([&](Code word) {
            if (index++%shards == static_cast<unsigned>(shard)) certify(word);
        });
        std::cerr << written << " certified in shard " << shard << ", " << index
                  << " shapes with at most " << leaves << " leaves\n";
    }
    void run(bool ranked) {
        if (ranked) {
            // Removing a unique centroid leaves no component above (n-1)/2.
            RankedForests centered(n-1,true);
            index = centered.count();
            for (Code r = shard; r < index; r += shards)
                certify((Code(1)<<(2*n-1))|(centered[r]<<1));
        }
        for (int s = 1; (!ranked || n%2 == 0) && s <= n/2; ++s) {
            std::vector<Rooted> layer;
            auto add = [&](Code f){ layer.push_back({s,(Code(1)<<(2*s-1))|(f<<1)}); };
            forests(s-1,0,s-1,0,add);
            std::sort(layer.begin(),layer.end(),[](auto a,auto b){ return a.code < b.code; });
            catalog.insert(catalog.end(),layer.begin(),layer.end());
        }
        if (!ranked) {
            auto centered = [&](Code f){
                if (index++%shards == static_cast<unsigned>(shard))
                    certify((Code(1)<<(2*n-1))|(f<<1));
            };
            forests(n-1,0,(n-1)/2,0,centered);
        }
        if (n%2 == 0) {
            for (std::size_t i = 0; i < catalog.size(); ++i) if (catalog[i].size == n/2) {
                const Code skip = (shard+shards-index%shards)%shards;
                for (std::size_t j = i+skip; j < catalog.size(); j += shards)
                    certify(((catalog[i].code>>1)<<(n+1))|(catalog[j].code<<1));
                index += catalog.size()-i;
            }
        }
        std::cerr << written << " certified in shard " << shard << ", " << index << " shapes total\n";
    }
};
}

int main(int argc,char** argv) {
    if (argc < 5 || argc > 7) return 2;
    bool ranked = argc == 6;
    if (ranked && std::string(argv[5]) != "--ranked") return 2;
    int n = std::stoi(argv[1]), shard = std::stoi(argv[2]), shards = std::stoi(argv[3]);
    if (n < 2 || n > 30 || shards < 1 || shard < 0 || shard >= shards) return 2;
    if (argc == 7 && std::string(argv[5]) != "--leaves") return 2;
    int leaves = argc == 7 ? std::stoi(argv[6]) : 0;
    if (argc == 7 && (leaves < 2 || leaves > n)) return 2;
    FILE* output = std::fopen(argv[4],"wb");
    if (!output) return 1;
    Census census(n,shard,shards,output);
    if (leaves) census.limited(leaves);
    else census.run(ranked);
    return std::fclose(output) != 0;
}
