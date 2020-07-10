def xor32(num):
    num = num or 2463534242
    num = num ^ (num << 13 & 0xffffffff)
    num = num ^ (num >> 17 & 0xffffffff)
    num = num ^ (num << 5 & 0xffffffff)
    return num & 0xffffffff
