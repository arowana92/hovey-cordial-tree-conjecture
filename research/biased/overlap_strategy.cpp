// Produce a policy for every next parent color while growing the high vertex and edge bins.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <set>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>

namespace {
using Mask = std::uint32_t;
using Key = std::uint64_t;
constexpr int k = 27;
constexpr Mask all = (1U<<k)-1;
using Row = std::array<unsigned char,k>;

int count(Mask x) { return __builtin_popcount(x); }
Mask shift(Mask x,int by) {
    by=(by+k)%k;
    return ((x<<by)|(x>>(k-by)))&all;
}
Key key(Mask x,Mask w) { return Key(x)|(Key(w)<<k); }

class Strategy {
    int steps, difference, target;
    std::unordered_map<Key,Row> policies;
    std::unordered_set<Key> losses;

    bool enough(Mask x,Mask w) const {
        int first=count(x&w), second=count(shift(x,difference)&w);
        return first>=target && second>=target &&
               (difference==0 || std::max(first,second)>target);
    }

    bool final_matching(Mask x,Mask w) const {
        if (enough(x,w)) return true;
        int first=count(x&w), second=count(shift(x,difference)&w);
        if (!difference || std::min(first,second)<target) return false;
        int desired=k-count(x)-count(w)+target;
        int cycles=std::gcd(k,difference), length=k/cycles;
        int maximum=0, flexible=0, intact=0;
        for (int root=0;root<cycles;++root) {
            std::array<bool,2*k> removed{};
            int last=-1;
            for (int i=0;i<length;++i) {
                int v=(root+i*difference)%k;
                removed[2*i]=w&(1U<<v);
                removed[2*i+1]=x&(1U<<v);
                if (removed[2*i]) last=2*i;
                if (removed[2*i+1]) last=2*i+1;
            }
            if (last<0) { maximum+=length; ++intact; continue; }
            int vertices=0;
            for (int i=1;i<=2*length;++i) {
                if (!removed[(last+i)%(2*length)]) { ++vertices; continue; }
                maximum+=vertices/2;
                if (vertices%2) flexible+=vertices/2;
                vertices=0;
            }
        }
        return maximum>desired || (maximum==desired && (!intact || flexible>=length-1));
    }

    // Which labels gain at least "need" overlaps for this one leaf-parent color?
    Mask gaining(Mask x,Mask w,int parent,int color,int need) const {
        if (need<=0) return all;
        if (parent==color) return need==1 ? all : 0;
        Mask new_weight=shift(x,color-parent), new_vertex=shift(w,-color);
        if (need==1) return new_weight|new_vertex;
        if (need==2) return new_weight&new_vertex;
        return 0;
    }

    int choose(int depth,Mask x,Mask w,int parent) {
        Mask available=all&~(x|shift(w,-parent));
        int first=count(x&w), second=count(shift(x,difference)&w);
        Mask immediate=available&gaining(x,w,parent,0,target-first);
        if (difference) {
            immediate &= gaining(x,w,parent,difference,target-second);
            immediate &= gaining(x,w,parent,0,target+1-first) |
                         gaining(x,w,parent,difference,target+1-second);
        }
        if (immediate) return __builtin_ctz(immediate);
        if (depth+1==steps) {
            Mask left=available&gaining(x,w,parent,0,target-first)&
                      gaining(x,w,parent,difference,target-second);
            for (;left;left&=left-1) {
                int y=__builtin_ctz(left);
                if (final_matching(x|(1U<<y),w|(1U<<((y+parent)%k)))) return y;
            }
            return -1;
        }

        std::array<Mask,64> priorities{};
        for (Mask left=available; left; left&=left-1) {
            int y=__builtin_ctz(left);
            Mask nx=x|(1U<<y), nw=w|(1U<<((y+parent)%k));
            int a=count(nx&nw), b=count(shift(nx,difference)&nw);
            int score=3*(std::min(a,target)+std::min(b,target))+
                      std::min(std::max(a,b),target+1)+std::min(a,b);
            priorities.at(score) |= 1U<<y;
        }
        for (int j=int(priorities.size())-1;j>=0;--j) {
            for (Mask left=priorities[j];left;left&=left-1) {
                int y=__builtin_ctz(left);
                if (solve(depth+1,x|(1U<<y),w|(1U<<((parent+y)%k)))) return y;
            }
        }
        return -1;
    }

    bool solve(int depth,Mask x,Mask w) {
        if (enough(x,w)) return true;
        if (depth==steps) return false;
        Key state=key(x,w);
        if (policies.count(state)) return true;
        if (losses.count(state)) return false;
        Row row{};
        for (int p=0;p<k;++p) {
            int y=choose(depth,x,w,p);
            if (y<0) {
                if (losses.size()>=500000) losses.clear();
                losses.insert(state);
                return false;
            }
            row[p]=y;
        }
        policies.emplace(state,row);
        return true;
    }

public:
    Strategy(int n,int d,int t):steps(n),difference(d),target(t) {}
    bool write(const std::string& path) {
        if (!solve(0,1,0)) return false;
        std::ofstream out(path,std::ios::binary);
        std::set<Key> pending{key(1,0)};
        std::uint64_t states=0;
        while (!pending.empty()) {
            Key state=*pending.begin();
            pending.erase(pending.begin());
            Mask x=state&all,w=state>>k;
            const Row& row=policies.at(state);
            for (Mask word : {x,w})
                for (int i=0;i<32;i+=8) out.put((word>>i)&255);
            out.write(reinterpret_cast<const char*>(row.data()),row.size());
            for (int p=0;p<k;++p) {
                int y=row[p];
                Mask nx=x|(1U<<y),nw=w|(1U<<((p+y)%k));
                if (count(nw)<steps && !enough(nx,nw)) pending.insert(key(nx,nw));
            }
            ++states;
        }
        out.flush();
        if (!out) throw std::runtime_error("strategy write failed");
        std::cout<<states<<" states\n";
        return true;
    }
};
}

int main(int argc,char** argv) {
    if (argc!=5) return 2;
    int steps=std::stoi(argv[1]), delta=std::stoi(argv[2]), target=std::stoi(argv[3]);
    if (steps<1 || steps>7 || delta<0 || delta>=k || target<1 || target>3) return 2;
    return Strategy(steps,delta,target).write(argv[4]) ? 0 : 1;
}
