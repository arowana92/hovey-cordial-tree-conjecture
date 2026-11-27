// Exchange two free vertex labels while retaining their permutation. Only
// incident edge weights change, so their collision count can be updated locally.
#pragma once
#include <algorithm>
#include <cstdint>
#include <numeric>

namespace {
bool swap_search(int k, const int* parents, int* labels, std::uint32_t seed) {
    int n = k-1;
    int degree[64]{}, incident[64][64], weight[64], count[64];
    for (int i=0; i<n; ++i) {
        incident[i][degree[i]++] = i;
        if (parents[i]>=0) incident[parents[i]][degree[parents[i]]++] = i;
    }
    auto random = [&]() {
        seed ^= seed<<13;
        seed ^= seed>>17;
        seed ^= seed<<5;
        return seed;
    };
    auto edge_weight = [&](int i) {
        int a = parents[i];
        int w = labels[i] + (a<0 ? -a-1 : labels[a]);
        return w<k ? w : w-k;
    };
    for (int trial=0; trial<16; ++trial) {
        std::iota(labels,labels+n,1);
        for (int i=n-1; i>0; --i) std::swap(labels[i],labels[random()%(i+1)]);
        std::fill_n(count,k,0);
        int score = 0;
        for (int i=0; i<n; ++i) {
            weight[i] = edge_weight(i);
            score += count[weight[i]]++>0;
        }
        for (int step=0; step<1500*k && score; ++step) {
            int v = random()%n;
            while (count[weight[v]]==1) v=(v+1)%n;
            if (parents[v]>=0 && (random()&1)) v=parents[v];

            auto measure = [&](int w, bool apply) {
                int edges[64], used=0;
                for (int j=0; j<degree[v]; ++j) edges[used++]=incident[v][j];
                for (int j=0; j<degree[w]; ++j) {
                    int e=incident[w][j];
                    if (e!=v && parents[e]!=v) edges[used++]=e;
                }
                int delta=0;
                for (int j=0; j<used; ++j) delta-=--count[weight[edges[j]]]>0;
                std::swap(labels[v],labels[w]);
                for (int j=0; j<used; ++j) {
                    int e=edges[j], value=edge_weight(e);
                    delta += count[value]++>0;
                    if (apply) weight[e]=value;
                }
                if (!apply) {
                    for (int j=0; j<used; ++j) --count[edge_weight(edges[j])];
                    std::swap(labels[v],labels[w]);
                    for (int j=0; j<used; ++j) ++count[weight[edges[j]]];
                }
                return delta;
            };

            int best=2*k, chosen=v, ties=0;
            int start=random()%n;
            for (int j=0; j<n; ++j) {
                int w=(start+j)%n;
                if (w==v) continue;
                int delta=measure(w,false);
                if (delta<best) {
                    best=delta;
                    chosen=w;
                    ties=1;
                } else if (delta==best && random()%++ties==0) {
                    chosen=w;
                }
            }
            if (best>=0 && random()%11==0) chosen=(v+1+random()%(n-1))%n;
            score+=measure(chosen,true);
        }
        if (score==0) return true;
    }
    return false;
}
}
