#include <stdint.h>

__attribute__((noinline)) uint64_t probe_target(uint64_t value) {
    return (value ^ UINT64_C(0x5a17)) + UINT64_C(0x31);
}

int main(int argc, char **argv) {
    return (int)probe_target((uint64_t)argc + (argv != 0));
}
