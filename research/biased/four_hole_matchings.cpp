// Emit a matching for each normalized triple of four omitted residues at 27.
#include <algorithm>
#include <array>
#include <cstdint>
#include <string>
#include <iostream>
#include <map>
#include <numeric>
#include <stdexcept>
#include <vector>

using Mask = std::uint32_t;
constexpr int modulus = 27, rows = 23;
constexpr Mask full = (Mask{1} << modulus) - 1;
using Triple = std::array<int, 3>;

Mask bit(int x) { return Mask{1} << x; }

Mask subtract_shift(Mask labels, int s) {
    return (labels >> s) | ((labels & (bit(s) - 1)) << (modulus - s));
}

int first(Mask labels) { return __builtin_ctz(labels); }

struct Search {
    std::array<int, rows> shift{}, label{};
    std::uint32_t state = 1;

    std::uint32_t next() {
        state ^= state << 13;
        state ^= state >> 17;
        state ^= state << 5;
        return state;
    }

    bool complete(Mask remaining, Mask inputs, Mask outputs) {
        if (!remaining) return true;
        int row = -1, best = modulus + 1;
        Mask choices = 0;
        for (Mask left = remaining; left; left &= left - 1) {
            int j = first(left);
            Mask options = inputs & subtract_shift(outputs, shift[j]);
            if (!options) return false;
            int count = __builtin_popcount(options);
            if (count < best) {
                best = count;
                choices = options;
                row = j;
            }
        }
        for (; choices; choices &= choices - 1) {
            int x = first(choices), y = (shift[row] + x) % modulus;
            label[row] = x;
            if (complete(remaining ^ bit(row), inputs ^ bit(x), outputs ^ bit(y))) return true;
        }
        return false;
    }

    void solve(Mask inputs, Mask shifts, Mask outputs) {
        int n = 0;
        for (Mask left = shifts; left; left &= left - 1) shift[n++] = first(left);
        if (n != rows) throw std::logic_error("incorrect number of shifts");
        int start = next() % 243;
        for (int attempt = 0; attempt < 5000; ++attempt) {
            int affine = (start + attempt) % 243;
            int slope = 1 + 3 * (affine / modulus), offset = affine % modulus;
            // For these slopes both x and x+s permute the full group.
            Mask remaining = bit(rows) - 1, v = inputs, e = outputs, release = 0;
            int extra = std::min(attempt / 243, 4);
            while (__builtin_popcount(release) < extra) release |= bit(next() % rows);
            for (int j = 0; j < rows; ++j) {
                if (release & bit(j)) continue;
                int x = (slope * shift[j] + offset) % modulus;
                int y = (x + shift[j]) % modulus;
                if ((v & bit(x)) && (e & bit(y))) {
                    remaining ^= bit(j);
                    v ^= bit(x);
                    e ^= bit(y);
                    label[j] = x;
                }
            }
            if (complete(remaining, v, e)) return;
        }
        throw std::runtime_error("unresolved matching");
    }
};

int main(int argc, char** argv) {
    std::ios::sync_with_stdio(false);
    // Optional first-index interval for independent replays.
    bool requested = argc == 2 && std::string(argv[1]) == "--keys";
    if (!requested && argc != 1 && argc != 3) return 2;
    int low = argc == 3 ? std::stoi(argv[1]) : 0;
    int high = argc == 3 ? std::stoi(argv[2]) : 650;
    if (low < 0 || low > high || high > 650) return 2;

    std::vector<Mask> holes;
    for (int d = 3; d < modulus; ++d)
        for (int c = 2; c < d; ++c)
            for (int b = 1; b < c; ++b)
                for (int a = 0; a < b; ++a)
                    if ((a + b + c + d) % modulus == 0)
                        holes.push_back(bit(a) | bit(b) | bit(c) | bit(d));
    if (holes.size() != 650) return 2;
    std::map<Mask, int> index;
    for (int i = 0; i < 650; ++i) index.emplace(holes[i], i);
    std::vector<std::array<int, 18>> images(650);
    std::vector<Mask> negatives(650);
    for (int i = 0; i < 650; ++i) {
        int col = 0;
        for (int u = 1; u < modulus; ++u) if (std::gcd(u, modulus) == 1) {
            Mask image = 0;
            for (Mask left = holes[i]; left; left &= left - 1)
                image |= bit(u * first(left) % modulus);
            images[i][col++] = index.at(image);
            if (u == modulus - 1) negatives[i] = image;
        }
    }
    auto emit = [&](Triple key) {
        auto [i,j,k] = key;
        Search search;
        search.state = 1 + (i * 650u + j) * 650u + k;
        search.solve(full ^ holes[i], full ^ holes[j], full ^ negatives[k]);
        // Little-endian indices, then input residues in increasing shift order.
        for (int t : key) { std::cout.put(char(t & 255)); std::cout.put(char(t >> 8)); }
        for (int x : search.label) std::cout.put(char(x));
    };
    if (requested) {
        int i,j,k;
        while (std::cin >> i) {
            if (!(std::cin >> j >> k) || i < 0 || i > j || j > k || k >= 650) return 2;
            emit({i,j,k});
        }
        return std::cin.eof() && std::cout ? 0 : 2;
    }
    for (int i = low; i < high; ++i) {
        if (*std::min_element(images[i].begin(), images[i].end()) < i) continue;
        for (int j = i; j < 650; ++j) {
            if (*std::min_element(images[j].begin(), images[j].end()) < i) continue;
            for (int k = j; k < 650; ++k) {
                Triple key{i,j,k};
                bool canonical = true;
                for (int col = 0; col < 18; ++col) {
                    Triple image{images[i][col], images[j][col], images[k][col]};
                    std::sort(image.begin(), image.end());
                    if (image < key) { canonical = false; break; }
                }
                if (!canonical) continue;
                emit(key);
            }
        }
    }
    return std::cout ? 0 : 2;
}
