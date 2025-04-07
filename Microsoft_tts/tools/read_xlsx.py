#!/usr/bin/env python3
# Author: Duo MA
# Email: maduo@cuhk.edu.cn

import pandas as pd
import sys
def seq_read(in_xlsx: str, out_txt: str):
    # read second and thirds colum ,because first cloume is number of row
    df = pd.read_excel(in_xlsx,header=None,usecols=[1,2])
    data = df.values # it is 2-dimension list,
                     # per elements is a small list i.e.:
                     # [['苹果' 'apple']
                     #  ['书本' 'book']
                     # ['中国' 'China']
                     # ...]
    print(data)
    with open(out_txt,'w')as f:
        for row in data:
            for e in row:
                #if e is not nan:
                if not pd.isnull(e): # filter nan
                    f.write(f'{e}\n')



if __name__ == "__main__":
    # debug
    #file_in = 'data/2024-7-22_exp/text_rawdata/words.xlsx'
    #df = pd.read_excel(file_in,usecols=[1,2])
    #data = df.values
    #print(data)
    #file_out = 'data/2024-7-22_exp/text_rawdata/words.txt'
    #seq_read(file_in,file_out)
    file_in=sys.argv[1]
    file_out=sys.argv[2]
    seq_read(file_in,file_out)


