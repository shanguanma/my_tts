#!/usr/bin/env python3
# Author: Duo MA
# Email: maduo@cuhk.edu.cn

import sys

if __name__ == "__main__":
    file_in=sys.argv[1]
    cut_num = sys.argv[2]
    cut_num = int(cut_num)
    raw_list=[]
    with open(file_in,'r')as f:
        for line in f:
            line = line.strip()
            raw_list.append(line)
    print(f"len: {len(raw_list)}")
    import random
    #cut = raw_list[:50]
    cut = raw_list[:-cut_num]
    random.shuffle(cut)
    print(f"after: {len(cut)}")
    with open(sys.argv[3],'w')as fw:
        for a in cut:
            fw.write(f"{a}\n")


