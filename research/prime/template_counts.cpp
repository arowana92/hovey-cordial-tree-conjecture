// Input rows: prime, number of active vertices, distinguished vertex (-1 for
// zero boundary), then parents (negative for an external parent). Output:
// signed count modulo p, the first moments, and one witness if any exists.
// Only the distinguished external parent carries boundary label 1.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>

using Row = std::vector<int>;
using Matrix = std::vector<Row>;

struct Counts {
    int prime;
    Row parents;
    int special;
    Row sums;
    Row witness;

    int mod(int x) const {
        int r = x % prime;
        return r < 0 ? r + prime : r;
    }

    void add_point(const Row& labels, int sign) {
        // All primes in the supplied check are below 64.
        std::uint64_t used = 1;
        for (int x : labels) {
            std::uint64_t bit = std::uint64_t{1} << x;
            if (used & bit) return;
            used |= bit;
        }
        if (witness.empty()) witness = labels;
        sums[0] = mod(sums[0] + sign);
        for (size_t i = 0; i < labels.size(); ++i)
            sums[i + 1] = mod(sums[i + 1] + sign * labels[i]);
    }

    void count_system(Matrix rows, int sign) {
        const int n = parents.size();
        Row free, pivots;
        for (int col = 0; col < n; ++col) {
            int rank = pivots.size();
            int next = rank;
            while (next < int(rows.size()) && mod(rows[next][col]) == 0) ++next;
            if (next == int(rows.size())) {
                free.push_back(col);
                continue;
            }
            std::swap(rows[rank], rows[next]);
            int inverse = 1;
            while (mod(inverse * rows[rank][col]) != 1) ++inverse;
            for (int& x : rows[rank]) x = mod(x * inverse);
            for (int i = 0; i < int(rows.size()); ++i) {
                if (i == rank) continue;
                int factor = rows[i][col];
                for (int j = 0; j <= n; ++j)
                    rows[i][j] = mod(rows[i][j] - factor * rows[rank][j]);
            }
            pivots.push_back(col);
        }
        for (size_t i = pivots.size(); i < rows.size(); ++i)
            if (mod(rows[i][n]) != 0) return;

        Row labels(n);
        auto enumerate = [&](auto& self, size_t j, std::uint64_t used) -> void {
            if (j < free.size()) {
                for (int x = 1; x < prime; ++x) {
                    std::uint64_t bit = std::uint64_t{1} << x;
                    if (!(used & bit)) {
                        labels[free[j]] = x;
                        self(self, j + 1, used | bit);
                    }
                }
                return;
            }
            for (size_t i = 0; i < pivots.size(); ++i) {
                int x = rows[i][n];
                for (int col : free) x -= rows[i][col] * labels[col];
                labels[pivots[i]] = mod(x);
            }
            add_point(labels, sign);
        };
        enumerate(enumerate, 0, 0);
    }

    void run() {
        const int n = parents.size();
        Row moving = {-1};  // dummy source with value 0, mapping to the missing weight
        for (int i = 0; i < n; ++i)
            if (parents[i] >= 0 || i == special) moving.push_back(i);
        Row image = moving;
        do {
            Matrix equations;
            bool fixed = false;
            for (size_t j = 1; j < moving.size(); ++j) {
                int source = moving[j], dest = image[j];
                if (source == dest) {
                    fixed = true;  // the parent contributes a nonzero label
                    break;
                }
                Row row(n + 1);
                if (dest >= 0) ++row[dest];
                --row[source];
                if (parents[source] >= 0) --row[parents[source]];
                row[n] = int(source == special);
                equations.push_back(row);
            }
            if (fixed) continue;
            if (special < 0) {
                Row normalize(n + 1);
                normalize[0] = normalize[n] = 1;
                equations.push_back(normalize);
            }
            int sign = 1;
            for (size_t i = 0; i < image.size(); ++i)
                for (size_t j = 0; j < i; ++j)
                    if (image[j] > image[i]) sign = -sign;
            count_system(equations, sign);
        } while (std::next_permutation(image.begin(), image.end()));
        if (special < 0) {
            // Restore all nonzero dilations. Each has the same permutation sign.
            sums[0] = mod((prime - 1) * sums[0]);
            for (size_t i = 1; i < sums.size(); ++i) sums[i] = 0;
        }
    }
};

int main() {
    int p, n, marked;
    while (std::cin >> p >> n >> marked) {
        if (p < 3 || p >= 64 || n < 1 || n >= p || marked < -1 || marked >= n)
            throw std::runtime_error("invalid parameters");
        for (int d = 2; d * d <= p; ++d)
            if (p % d == 0) throw std::runtime_error("modulus must be prime");
        Row parents(n);
        for (int i = 0; i < n; ++i)
            if (!(std::cin >> parents[i]) || parents[i] < -1 || parents[i] >= i)
                throw std::runtime_error("invalid parent vector");
        if (marked >= 0 && parents[marked] >= 0)
            throw std::runtime_error("the marked vertex must have an external parent");
        Counts count{p, parents, marked, Row(n + 1), {}};
        count.run();
        for (int x : count.sums) std::cout << x << ' ';
        std::cout << '|';
        for (int x : count.witness) std::cout << ' ' << x;
        std::cout << std::endl;
    }
}
