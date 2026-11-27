// Search dense prescribed vertex and weight sets, modulo affine symmetry of vertices.
#include "rainbow_cycle.hpp"
#include <iostream>
#include <numeric>
#include <set>
#include <string>

using rainbow_cycle::Mask;
using rainbow_cycle::Search;

int moment(Mask sites, int k) {
    int total = 0;
    for (; sites; sites &= sites - 1) total += __builtin_ctzll(sites);
    return total % k;
}

Mask affine(Mask sites, int k, int u, int shift) {
    Mask result = 0;
    for (; sites; sites &= sites - 1)
        result |= Mask(1) << ((__builtin_ctzll(sites) * u + shift) % k);
    return result;
}

void choose(int k, int start, int count, Mask prefix, std::vector<Mask>& sets) {
    if (!count) {
        sets.push_back(prefix);
        return;
    }
    for (int i = start; i <= k - count; ++i)
        choose(k, i + 1, count - 1, prefix | (Mask(1) << i), sets);
}

int main(int argc, char** argv) {
    if (argc != 3 && argc != 5) return 2;
    int k = std::stoi(argv[1]), h = std::stoi(argv[2]);
    if (k < 5 || k >= 64 || h < 1 || h > k - 3) return 2;
    Mask all = (Mask(1) << k) - 1;
    Search search{k, 0, 0, std::mt19937(unsigned(1000*k+h)), {}};
    if (argc == 5) {
        Mask x = std::stoull(argv[3]), y = std::stoull(argv[4]);
        if ((x | y) > all || __builtin_popcountll(x) != h || __builtin_popcountll(y) != h)
            return 2;
        for (int trial = 0; trial < 400; ++trial) {
            if (!search.cycle(all ^ x, all ^ y, 5000 + 30*trial)) continue;
            for (int a : search.path) std::cout << a << ' ';
            std::cout << '\n';
            return 0;
        }
        return 1;
    }
    std::vector<Mask> sets;
    choose(k, 0, h, 0, sets);
    std::vector<std::vector<Mask>> by_sum(k);
    for (Mask y : sets) by_sum[moment(y,k)].push_back(y);
    std::set<Mask> seen;
    long long rows = 0, shapes = 0;
    for (Mask x : sets) {
        if (seen.count(x)) continue;
        ++shapes;
        for (int u = 1; u < k; ++u) if (std::gcd(u,k) == 1)
            for (int t = 0; t < k; ++t) seen.insert(affine(x,k,u,t));
        int target = (2*moment(x,k) + k - (k*(k-1)/2)%k) % k;
        for (Mask y : by_sum[target]) {
            bool found = false;
            for (int trial = 0; trial < 200 && !found; ++trial)
                found = search.cycle(all ^ x, all ^ y, 5000 + 30*trial);
            if (!found) {
                std::cerr << "search exhausted on " << k << ' ' << h << ' ' << x << ' ' << y << '\n';
                return 1;
            }
            std::cout << x << ' ' << y;
            for (int a : search.path) std::cout << ' ' << a;
            std::cout << '\n';
            ++rows;
        }
    }
    std::cerr << k << ' ' << h << " representatives " << shapes << " cycles " << rows << '\n';
}
