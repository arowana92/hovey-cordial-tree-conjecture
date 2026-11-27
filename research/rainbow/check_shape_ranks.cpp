// Exercise the independent rank on named forests and on a differently ordered catalog.
#include "ranked_forest.hpp"
#include "shape_rank.hpp"
#include <cstdint>
#include <atomic>
#include <future>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>

using Word=std::uint64_t;

std::string canonical(const std::vector<int>& parents) {
    int n=parents.size();
    std::vector<std::vector<std::string>> children(n+1);
    for (int i=n-1;i>=0;--i) {
        auto& list=children[i];
        std::sort(list.begin(),list.end());
        std::string word="(";
        for (const auto& w:list) word+=w;
        children[parents[i]>=0 ? parents[i] : n].push_back(word+")");
    }
    auto& roots=children[n];
    std::sort(roots.begin(),roots.end());
    std::string result;
    for (const auto& r:roots) result+=r;
    return result;
}

Word named(int n) {
    ShapeRank rank(n);
    std::map<std::string,Word> found;
    std::vector<int> par;
    Word count=0;
    auto walk=[&](auto&& self,int i)->void {
        if (i==n) {
            Word r=rank(par);
            auto entry=found.emplace(canonical(par),r);
            if (r>=rank.total() || entry.first->second!=r) throw std::runtime_error("named rank conflict");
            ++count;
        } else for (int parent=-1;parent<i;++parent) {
            par.push_back(parent); self(self,i+1); par.pop_back();
        }
    };
    walk(walk,0);
    std::set<Word> ranks;
    for (const auto& kv:found) ranks.insert(kv.second);
    if (ranks.size()!=found.size() || ranks.size()!=rank.total())
        throw std::runtime_error("named catalog mismatch");
    return count;
}

void unpack(Word w,int n,std::vector<int>& parents) {
    parents.clear();
    std::array<int,26> stack{};
    int depth=0;
    for (int bit=2*n-1;bit>=0;--bit) {
        if ((w>>bit)&1) {
            int v=parents.size();
            parents.push_back(depth?stack[depth-1]:-1);
            stack[depth++]=v;
        } else --depth;
    }
}

Word single_mass(int n,int workers) {
    ShapeRank rank(n);
    RankedForests other(n);
    if (other.count()!=rank.total()) throw std::runtime_error("count mismatch");
    std::vector<std::atomic<Word>> seen((rank.total()+63)/64);
    for (auto& v:seen) v.store(0,std::memory_order_relaxed);
    std::vector<std::future<void>> tasks;
    for (int j=0;j<workers;++j) tasks.push_back(std::async(std::launch::async,[&,j] {
        std::vector<int> par;
        par.reserve(n);
        for (Word i=rank.total()*j/workers;i<rank.total()*(j+1)/workers;++i) {
            unpack(other[i],n,par);
            Word id=rank(par);
            if (id>=rank.total()) throw std::runtime_error("rank out of range");
            Word bit=Word(1)<<(id%64);
            if (seen[id/64].fetch_or(bit,std::memory_order_relaxed)&bit)
                throw std::runtime_error("repeated forest rank");
        }
    }));
    for (auto& task:tasks) task.get();
    return rank.total();
}

Word cross(int n,bool complete) {
    ShapeRank rank(n);
    RankedForests other(n);
    if (other.count()!=rank.total()) throw std::runtime_error("count mismatch");
    std::vector<bool> seen(complete?rank.total():0);
    std::set<Word> subset;
    Word count=0, sample_stride=complete?1:std::max<Word>(1,rank.total()/50000);
    for (Word i=0;i<rank.total();i+=sample_stride) {
        std::vector<int> parents;
        unpack(other[i],n,parents);
        Word id=rank(parents);
        if (id>=rank.total() || (complete?seen[id]:!subset.insert(id).second))
            throw std::runtime_error("rank repeated or out of range");
        if (complete) seen[id]=true;
        ++count;
    }
    return count;
}

int main(int argc,char** argv) {
    if (argc==4 && std::string(argv[1])=="--mass") {
        int n=std::stoi(argv[2]),workers=std::stoi(argv[3]);
        if (n<1 || n>25 || workers<1 || workers>256) return 2;
        std::cout<<single_mass(n,workers)<<" unique ranks at forest mass "<<n<<"\n";
        return 0;
    }
    int full=argc==2?std::stoi(argv[1]):17;
    if (full<1 || full>25) return 2;
    Word tuples=0,whole=0,part=0;
    for (int n=1;n<=9;++n) tuples+=named(n);
    for (int n=1;n<=25;++n) {
        if (n<=full) whole+=cross(n,true);
        else part+=cross(n,false);
    }
    std::cout<<tuples<<" named parent arrays, "<<whole<<" full-catalog forests, "<<part<<" sampled forests\n";
}
