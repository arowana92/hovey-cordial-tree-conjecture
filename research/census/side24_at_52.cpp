// Write witnesses in order of (24-port, left start, 26-port, right start,
// attachment type, attachment site), with exceptional leaf rows immediately after.
#include <array>
#include <cstdint>
#include <cstdio>
#include <stdexcept>
#include <vector>

namespace {
using Mask = std::uint32_t;
using Row = std::array<unsigned char, 5>;
constexpr int k = 27;
constexpr Mask all = (Mask{1} << k) - 1;
Mask bit(int i) { return Mask{1} << i; }
int first(Mask m) { return __builtin_ctz(m); }
Mask rotate(Mask m, int d) { return ((m << d) | (m >> (k-d))) & all; }

struct Room {
    Mask once, twice;  // Residues accepting at least one or two more entries.
    Room(Mask a, Mask b) : once(a | b), twice(a & b) {}
    bool add(int x) {
        Mask b = bit(x);
        if (!(once & b)) return false;
        if (twice & b) twice ^= b;
        else once ^= b;
        return true;
    }
};
struct Map {
    int u, d;
    Mask vertex, edge;
    std::vector<std::array<int, 2>> tails;
    int label(int x) const { return (u*x+d)%k; }
};

std::vector<Map> maps(int f) {
    std::vector<Map> result;
    for (int u=1; u<k; ++u) if (u%3) for (int d=0; d<k; ++d) {
        Map m{u,d,0,0,{}};
        for (int x=24; x<27; ++x) m.vertex |= bit(m.label(x));
        for (int i=23; i<27; ++i) m.edge |= bit((u*(f+i)+2*d)%k);
        Room vertices(m.vertex, bit(26));
        for (Mask s=vertices.once; s; s&=s-1) for (Mask t=vertices.once; t; t&=t-1) {
            int x=first(s), y=first(t);
            Room v=vertices;
            if (v.add(x) && v.add(y) && !v.twice) m.tails.push_back({x,y});
        }
        result.push_back(m);
    }
    return result;
}

Row witness(const Map& m, int x, int y, int v=0) {
    return {static_cast<unsigned char>(m.u), static_cast<unsigned char>(m.d),
            static_cast<unsigned char>(x), static_cast<unsigned char>(y),
            static_cast<unsigned char>(v)};
}

using Batch = std::array<std::array<Row,26>,2>;
Batch direct(const std::vector<Map>& maps, int a, int b, Mask holes) {
    Batch rows{};
    std::array<Mask,2> pending{bit(26)-1, bit(26)-1};
    for (const auto& m : maps) {
        Room weights(m.edge, holes);
        if (!weights.add((m.label(a)+b)%k)) continue;
        for (auto [x,y] : m.tails) for (int path=0; path<=1; ++path) {
            // In both shapes the first tail weight is p+x.
            Mask sites=pending[path] & rotate(weights.once,(k-x)%k);
            if (!path) sites &= rotate(weights.once,(k-y)%k);
            else if (!(weights.once & bit((x+y)%k))) continue;
            for (; sites; sites&=sites-1) {
                int p=first(sites);
                Room e=weights;
                if (e.add((p+x)%k) && e.add(((path?x:p)+y)%k) && !e.twice) {
                    rows[path][p]=witness(m,x,y);
                    pending[path] ^= bit(p);
                }
            }
        }
        if (!(pending[0]|pending[1])) break;
    }
    return rows;
}

Row repair(const std::vector<Map>& maps, int a, int b, Mask holes,
           int path, int p, int z, int parent) {
    for (const auto& m : maps) {
        Room vertices(m.vertex, bit(26)|bit(z));
        Room weights(m.edge, holes|bit((z+parent)%k));
        for (Mask labels=vertices.once; labels; labels&=labels-1) {
            int v=first(labels);
            Room e=weights, available=vertices;
            available.add(v);
            if (!e.add((m.label(a)+(b==z?v:b))%k) || !e.add((v+parent)%k)) continue;
            int site=p==z?v:p;
            for (Mask s=available.once; s; s&=s-1) for (Mask t=available.once; t; t&=t-1) {
                int x=first(s), y=first(t);
                Room leaves=available, tail=e;
                if (leaves.add(x) && leaves.add(y) && !leaves.twice &&
                    tail.add((site+x)%k) && tail.add(((path?x:site)+y)%k) && !tail.twice)
                    return witness(m,x,y,v);
            }
        }
    }
    return {};
}

void write(const Row& row, int size) {
    if (std::fwrite(row.data(),1,size,stdout) != static_cast<std::size_t>(size))
        throw std::runtime_error("cannot write witness");
}
}

int main() {
    for (int a=0; a<24; ++a) for (int f=1; f<24; ++f) {
        auto choices=maps(f);
        for (int b=0; b<26; ++b) for (int g=1; g<26; ++g) {
            Mask holes=rotate(bit(25)|bit(26),g);
            Batch rows=direct(choices,a,b,holes);
            for (int path=0; path<=1; ++path) for (int p=0; p<26; ++p) {
                write(rows[path][p],4);
                if (rows[path][p][0]) continue;
                for (int z=0; z<26; ++z) for (int t=0; t<26; ++t)
                    if (z!=t && g<=z+t && z+t<g+25)
                        write(repair(choices,a,b,holes,path,p,z,t),5);
            }
        }
    }
    return std::fflush(stdout) == 0 ? 0 : 1;
}
