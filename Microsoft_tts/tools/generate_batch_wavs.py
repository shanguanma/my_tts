#!/usr/bin/env python3
# Author: Duo MA
# Email: maduo@cuhk.edu.cn
from pathlib import Path
import os
#from tts2 import transferMsTTSData, get_SSML
from tts import mainSeq
import asyncio
import sys
def get_SSML(path):
    with open(path,'r',encoding='utf-8') as f:
        return f.read()

if __name__=="__main__":
    #input_dir="input_dir"
    #output_dir="output_dir"
    input_xml_dir=sys.argv[1]
    output_audio_dir=sys.argv[2]

    os.makedirs(output_audio_dir, exist_ok = True)
    input_dir = Path(input_xml_dir)
    for path in input_dir.glob("*"):
        path = str(path)
        print(path)
        name = os.path.basename(path).split(".")[0]
        ssml=get_SSML(path)
        asyncio.get_event_loop().run_until_complete(mainSeq(ssml, f"{output_audio_dir}/{name}"))
        #transferMsTTSData(ssml,f"{output_dir}/{name}")
