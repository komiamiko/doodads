#include <iostream>
#include <ctime>
#include <cstdint>
#include <vector>

#include "xoroshiro.cpp"

typedef char byte;

uint64_t symbols;
uint64_t block_size;
uint64_t block_mod;
uint64_t milestone_size;
uint64_t last_milestone = 0;

uint64_t best_length = 0;
std::vector<std::vector<uint64_t>> prev;
std::vector<byte> block;

void print_block() {
    std::cout << "New best with length " << best_length << "\n  ";
    for(uint64_t i=0;i<block.size();++i){
        byte val = block[i];
        if(0<=val && val<=9){
            std::cout << char(val+48);
        }else if(10<=val && val<=35){
            std::cout << char(val+55);
        }else{
            std::cout << "?";
        }
    }
    std::cout << "\n";
}

bool array_all_lt(uint64_t* a, uint64_t* b, uint64_t n){
    for(uint64_t i=0;i<n;++i){
        if(a[i] > b[i])return false;
    }
    return true;
}

void rebuild_cache() {
    while(prev.size()<=symbols){
        prev.push_back(std::vector<uint64_t>());
    }
    uint64_t length = block.size();
    uint64_t tail = length - block_size;
    for(uint64_t s=0;s<symbols;++s){
        std::vector<uint64_t>* sp = &prev[s];
        while(sp->size() > tail){
            sp->pop_back();
        }
        uint64_t index = tail==0?-1:block[tail-1]==s?tail-1:sp->at(tail-1);
        while(sp->size() <= length){
            uint64_t isp = sp->size();
            sp->push_back(index);
            if(block[isp]==s){
                index = isp;
            }
        }
    }
}

bool check_block_subsequence() {
    // check the validity of the newly added block
    // runtime should be O(N) in the length of the string
    uint64_t length = block.size();
    if(length<4)return true;
    uint64_t half = (length-2)/2;
    uint64_t tail = length - block_size;
    if(block_size == 1){
        --tail;
    }
    for(uint64_t i=0;i<half;++i){
        uint64_t istop = i*2+2;
        uint64_t l = istop-1;
        byte c = block[l];
        uint64_t jlast = length-1;
        if(block[jlast]!=c){
            jlast = prev[c][jlast];
        }
        for(;jlast != -1 && jlast >= tail;l=istop-1,c=block[l],jlast=prev[c][jlast]){
            uint64_t jfirst = std::max(i+1, jlast/2);
            uint64_t j = jlast;
            bool reject = false;
            for(--l;l != -1 && l >= i;--l){
                c = block[l];
                j = prev[c][j];
                if(j == -1 || j < jfirst){
                    reject = true;
                    break;
                }
            }
            if(reject)continue;
            return false;
        }
    }
    return true;
}

void extend(){
    // one extension step
    // generally succeeds and takes O(N) time in the current length of the string
    // thus it takes around O(N^2) time to generate up to length N
    // generate random tail
    uint64_t roll = next() % block_mod;
    // roll through all possible tails
    for(uint64_t roll_ofs=0;roll_ofs<block_mod;++roll_ofs){
        uint64_t tail = roll + roll_ofs;
        // add the tail
        for(uint64_t i=0;i<block_size;++i){
            block.push_back(tail % symbols);
            tail /= symbols;
        }
        // did we make a longer string?
        rebuild_cache();
        if(check_block_subsequence()){
            uint64_t length = block.size();
            if(length > best_length){
                best_length = length;
                if(best_length - last_milestone >= milestone_size){
                    last_milestone = best_length;
                    print_block();
                }
            }
            extend();
        }
        // remove the tail
        for(uint64_t i=0;i<block_size;++i){
            block.pop_back();
        }
    }
}

int main(int argc, const char * argv[]) {
    std::cout << "Enter number of symbols\n";
    std::cin >> symbols;
    std::cout << "Enter number of symbols to try at a time\n";
    std::cin >> block_size;
    block_mod = 1;
    for(uint64_t i=0;i<block_size;++i){
        block_mod *= symbols;
    }
    std::cout << "Enter milestone size to print at\n";
    std::cin >> milestone_size;
    std::cout << "Enter random seed\n";
    std::cin >> s[0];
    s[1] = 1;
    std::cout << "Computing sequences...\n";
    extend();
    std::cout << "Exhaustive search completed\n";
    return 0;
}
