#!/usr/bin/env python3
# Author: Duo MA
# Email: maduo@cuhk.edu.cn
import os
from librosa import load
import numpy as np
from librosa.util import fix_length
from typing import Any, List
import librosa
from pathlib import Path
import sys
def fix_length_md(
    data: np.ndarray, *, size: int, axis: int = -1, pad_left_right= True, pad_right_len=500, **kwargs: Any
) -> np.ndarray:
    """
    reference: https://librosa.org/doc/main/_modules/librosa/util/utils.html#fix_length
    here, i will pad right and fix audio length
    """
    kwargs.setdefault("mode", "constant")

    n = data.shape[axis]

    if n > size:
        slices = [slice(None)] * data.ndim
        slices[axis] = slice(0, size)
        return data[tuple(slices)]

    elif n < size:
        lengths = [(0, 0)] * data.ndim
        if pad_left_right:
            lengths[axis] = (size - n - pad_right_len, pad_right_len)
        elif pad_right:
            lengths[axis] = (0, size - n)

        return np.pad(data, lengths, **kwargs)

    return data

def read_wav(corpus_dir: str, )-> List:
    wavlist = []
    corpus_dir = Path(corpus_dir)
    assert corpus_dir.is_dir(), f"No such directory: {corpus_dir}"
    for name in corpus_dir.glob("*"):
        print(f"name: {name}")
        wavlist.append(name)

    return wavlist

def fixed_audio_length(corpus_dir: str, output_dir: str, pad_right_len=50,required_audio_size_second=2):
    #corpus_dir = "eggs_exp_audiodata/prompt"
    #output_dir = "eggs_exp_audiodata/prompt_2s"
    #os.makedirs(output_dir, exist_ok = True)
    wavlist = read_wav(corpus_dir)
    #sr=22050
    os.makedirs(output_dir, exist_ok = True)
    required_audio_size_second=required_audio_size_second
    for file_path in wavlist:
        #sr=22050
        sr=24000
        wavname =  os.path.basename(file_path).split(".")[0]
        data,sr = load(file_path, sr=sr, mono=True)
        target_sr=16000
        data_16k = librosa.resample(data, orig_sr=sr, target_sr=target_sr)
        data_16k_pad_left = fix_length_md(data_16k, pad_left_right = True, pad_right_len=pad_right_len, size=required_audio_size_second * target_sr)
        #librosa.output.write_wav(f"{output_dir}/{wavname}.wav", data_16k_pad_left, target_sr)
        import soundfile as sf
        sf.write(f"{output_dir}/{wavname}.wav", data_16k_pad_left, 16000, 'PCM_16')


def fix_ding_online_length(corpus_dir: str, output_dir: str,required_audio_size_second=2):
    os.makedirs(output_dir,exist_ok=True)
    file_path = f"{corpus_dir}/ding_online.wav"
    wavname = os.path.basename(file_path).split(".")[0]
    target_sr=16000
    required_audio_size_second=required_audio_size_second
    data,sr = load(file_path, sr=target_sr, mono=True)
    data_16k_pad_left = fix_length_md(data, size=required_audio_size_second * target_sr)
    import soundfile as sf
    sf.write(f"{output_dir}/{wavname}_fix.wav", data_16k_pad_left, target_sr, 'PCM_16')


if __name__ == '__main__':
    ## fixed audio lenght, both left and right are padded.
    ## content
    #corpus_dir = "output_dir_wav"
    #output_dir = "output_dir_wav_2s"
    #os.makedirs(output_dir, exist_ok = True)
    #fixed_audio_length(corpus_dir, output_dir,pad_right_len=500)

    ## prompt
    #corpus_dir = "output_dir_prompt_wav"
    #output_dir = "output_dir_prompt_wav_3s"
    #os.makedirs(output_dir, exist_ok = True)
    #fixed_audio_length(corpus_dir, output_dir,pad_right_len=500,required_audio_size_second=3)

    audio_dir=sys.argv[1]
    audio_dir_fix=sys.argv[2]
    fixed_audio_length(audio_dir,audio_dir_fix,pad_right_len=500,required_audio_size_second=int(sys.argv[3]))
    #prompt_audio_dir=sys.argv[3]
    #prompt_audio_dir_fix=sys.argv[4]
    #fixed_audio_length(prompt_audio_dir,prompt_audio_dir_fix,pad_right_len=500,required_audio_size_second=3)
