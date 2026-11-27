// Independent coefficient extraction on three finite-field grids.
// Take the rank-one row multiplicities by finite differences of determinants.
#include <algorithm>
#include <iostream>
#include <stdexcept>
#include <vector>

using Matrix = std::vector<std::vector<int>>;

int residue(long long x, int p) {
    int a = static_cast<int>(x % p);
    return a < 0 ? a+p : a;
}

int power(int a, int n, int p) {
    int out = 1;
    for (; n; n >>= 1, a = a*a % p)
        if (n & 1) out = out*a % p;
    return out;
}

int determinant(Matrix a, int p, const std::vector<int>& inv) {
    int result = 1;
    for (int c = 0; c < static_cast<int>(a.size()); ++c) {
        int pivot = c;
        while (pivot < static_cast<int>(a.size()) && a[pivot][c] == 0) ++pivot;
        if (pivot == static_cast<int>(a.size())) return 0;
        if (pivot != c) {
            std::swap(a[c], a[pivot]);
            result = residue(-result, p);
        }
        result = result*a[c][c] % p;
        for (int i = c+1; i < static_cast<int>(a.size()); ++i) {
            int factor = a[i][c]*inv[a[c][c]] % p;
            for (int j = c+1; j < static_cast<int>(a.size()); ++j)
                a[i][j] = residue(a[i][j]-factor*a[c][j], p);
        }
    }
    return result;
}

int coefficient(int p, int j, int h, int singles, int e) {
    int r = 2+j+h+singles;
    if (p > 127 || p < 2 || std::min({j,h,singles,e}) < 0 || r >= p || r+e > p)
        throw std::invalid_argument("expected r<p<=127 and r+e<=p");
    std::vector<int> inv(p);
    for (int x=1; x<p; ++x) {
        inv[x] = power(x, p-2, p);
        if (x*inv[x] % p != 1) throw std::invalid_argument("expected a prime");
    }
    Matrix bin(p, std::vector<int>(p));
    for (int b=0; b<p; ++b) {
        bin[b][0] = bin[b][b] = 1;
        for (int a=1; a<b; ++a) bin[b][a] = (bin[b-1][a-1]+bin[b-1][a]) % p;
    }
    int total = 0;
    for (int t=1; t<p; ++t) {
        std::vector<int> pos(r), neg(r);
        for (int i=0; i<r; ++i) {
            pos[i] = power(t, i, p);
            neg[i] = power(inv[t], i, p);
        }
        for (int z=1; z<p; ++z) for (int w=1; w<p; ++w) {
            Matrix d(r,std::vector<int>(r));
            for (int a=0; a<r; ++a) for (int b=a; b<r; ++b)
                d[a][b] = ((a==b) + bin[e+b][e+a]*(z+w*pos[b-a])) % p;
            // Each marked letter has rank one. The mixed difference at 0,1
            // equals the coefficient of their product even at singular D.
            int mixed = power((1+z+w) % p, r, p);
            for (int mask=1; mask<4; ++mask) {
                Matrix m = d;
                for (int a=0; a<r; ++a) for (int b=0; b<r; ++b)
                    m[a][b] = (m[a][b] + (mask&1) + ((mask&2) ? neg[a]*pos[b] : 0)) % p;
                mixed += (mask == 3 ? 1 : -1)*determinant(m, p, inv);
            }
            total = residue(total + mixed*power(inv[z],j,p)*power(inv[w],h,p), p);
        }
    }
    // Three averages over p-1 units, the exponent-reversal sign, and
    // orderings of the three sets of indistinguishable row types.
    total = residue((r*(r-1)/2 % 2 == 0 ? -1 : 1)*total, p);
    for (int n : {j,h,singles}) for (int i=2; i<=n; ++i) total = total*i % p;
    return total;
}

int main(int argc, char** argv) {
    if (argc != 6) return 2;
    std::cout << coefficient(std::stoi(argv[1]), std::stoi(argv[2]), std::stoi(argv[3]),
                             std::stoi(argv[4]), std::stoi(argv[5])) << '\n';
}
