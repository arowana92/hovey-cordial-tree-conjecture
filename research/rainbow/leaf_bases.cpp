// Bijective order-k bases, enumerated up to unrooted isomorphism.
#include "../census/leaf_centroids.hpp"
#include <array>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>

extern "C" int rainbow_witness(int, const int*, int*);

int main(int argc, char** argv) {
    if (argc != 6) return 2;
    int k=std::stoi(argv[1]), limit=std::stoi(argv[2]);
    int shard=std::stoi(argv[3]), shards=std::stoi(argv[4]);
    if (k<5 || k>30 || limit<2 || limit>k || shard<0 || shard>=shards) return 2;
    std::ofstream out(argv[5],std::ios::binary);
    if (!out) return 1;
    std::uint64_t index=0, rows=0;
    LeafCentroids trees(k,limit);
    trees.each([&](std::uint64_t word) {
        if (index++%shards != static_cast<unsigned>(shard)) return;
        std::array<int,32> stack{}, parents{}, labels{};
        int count=0, depth=0;
        for (int bit=2*k-1; bit>=0; --bit) {
            if ((word>>bit)&1) {
                if (count) parents[count-1]=stack[depth-1]-1;
                stack[depth++]=count++;
            } else --depth;
        }
        // Fix the centroid label to zero. A parent of -1 is the external zero.
        if (rainbow_witness(k,parents.data(),labels.data()+1)!=1)
            throw std::runtime_error("missing modular base for word "+std::to_string(word));
        std::array<unsigned char,40> record{};
        for (int j=0; j<8; ++j) record[j]=word>>(8*j);
        std::copy_n(labels.begin(),k,record.begin()+8);
        out.write(reinterpret_cast<const char*>(record.data()),k+8);
        ++rows;
    });
    out.close();
    if (!out) return 1;
    std::cout << rows << " modular bases in shard " << shard << ", " << index << " total\n";
}
