#!/usr/bin/env python3
# Author: Duo MA
# Email: maduo@cuhk.edu.cn

from pathlib import Path
import os
import sys

def covert_mp3_to_wav(input_dir: str, output_dir: str):
    os.makedirs(output_dir,exist_ok=True)
    import subprocess
    input_dir=Path(input_dir)
    for path in input_dir.glob("*"):
        name=os.path.basename(path).split(".")[0]
        path = str(path)
        command=f'ffmpeg -i {input_dir}/{name}.mp3 -acodec pcm_s16le -ac 1 -ar 16000 {output_dir}/{name}.wav'
        return_value = subprocess.call(command, shell=True)
        print('###############')
        print('Return value:', return_value)

if __name__ == "__main__":
    audio_in_dir = sys.argv[1]
    aduio_out_dir = sys.argv[2]
    covert_mp3_to_wav(audio_in_dir,aduio_out_dir)
