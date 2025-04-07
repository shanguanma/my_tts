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


def str2bool(v):
    """Used in argparse.ArgumentParser.add_argument to indicate
    that a type is a bool type and user can enter

        - yes, true, t, y, 1, to represent True
        - no, false, f, n, 0, to represent False

    See https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse  # noqa
    """
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


def read_wav(
    corpus_dir: str,
) -> List:
    wavlist = []
    corpus_dir = Path(corpus_dir)
    assert corpus_dir.is_dir(), f"No such directory: {corpus_dir}"
    for name in corpus_dir.glob("*"):
        print(f"name: {name}")
        wavlist.append(name)

    return wavlist


def concatenate_multi_audio(
    wavlist: List,
    output_dir: str,
    prompt_audio_dir: str = "output_dir_prompt_wav_3s",
    concatente_audio_name="1",
    last_utt=False,
    required_silence_audio_len: int = 2,
    ding_path: str = "data/2024-7-22_exp/ding_fix/ding_online_fix.wav",
    order_random=True,
):
    os.makedirs(output_dir, exist_ok=True)
    target_sr = 16000
    required_silence_audio_len = int(required_silence_audio_len)  # i.e.: 2
    sil_audio = np.zeros(required_silence_audio_len * target_sr)
    # ding_path = "ding_fix/ding_online_fix.wav"
    data_ding, _ = load(ding_path, sr=target_sr, mono=True)

    c = data_ding
    print(f"ding: {c}")
    if order_random:
        import random

        random.shuffle(wavlist)
    print(wavlist)
    ## store sample order
    with open(f"{output_dir}/{concatente_audio_name}_sample_order.txt", "w") as fw1:
        for path in wavlist:
            name = os.path.basename(path).split(".")[0]
            fw1.write(f"{name}\n")

    for path in wavlist:
        content_data, _ = load(str(path), sr=target_sr, mono=True)
        c = np.concatenate((c, content_data, sil_audio), axis=None)

    if last_utt:
        last_prompt_path = f"{prompt_audio_dir}/本组实验结束.wav"
        last_prompt_data, _ = load(last_prompt_path, sr=target_sr, mono=True)
        c = np.concatenate((c, last_prompt_data), axis=None)
    else:
        last_prompt_path = f"{prompt_audio_dir}/请休息一下.wav"
        last_prompt_data, _ = load(last_prompt_path, sr=target_sr, mono=True)
        c = np.concatenate((c, last_prompt_data), axis=None)

    import soundfile as sf

    sf.write(f"{output_dir}/{concatente_audio_name}.wav", c, 16000, "PCM_16")


if __name__ == "__main__":
    # corpus_dir = "output_dir_wav_2s"
    # prompt_dir = "output_dir_prompt_wav_3s"
    content_audio_dir = sys.argv[1]

    wavlist = read_wav(content_audio_dir)
    # output_dir = "output_final_last"
    # for i in range(5):
    #    concatenate_multi_audio(wavlist=wavlist, output_dir=output_dir,  prompt_audio_dir=prompt_dir, concatente_audio_name=f"{int(i)+1}",last_utt=False)
    # concatenate_multi_audio(wavlist=wavlist, output_dir=output_dir,  prompt_audio_dir=prompt_dir, concatente_audio_name="6",last_utt=True)
    prompt_dir = sys.argv[2]
    required_silence_audio_len = sys.argv[3]
    ding_path = sys.argv[4]
    order_random = str2bool(sys.argv[5])
    #concatente_audio_name = sys.argv[6]
    output_dir = sys.argv[6]
    sample_num = sys.argv[7]
    if int(sample_num)>1:
        for i in range(int(sample_num)):
            if i==int(sample_num)-1:
                concatenate_multi_audio(
                    wavlist=wavlist,
                    output_dir=output_dir,
                    prompt_audio_dir=prompt_dir,
                    concatente_audio_name=f"{int(i)+1}",
                    last_utt=True,
                    required_silence_audio_len=required_silence_audio_len,
                    ding_path=ding_path,
                    order_random=order_random,
                )
            else:
                concatenate_multi_audio(
                    wavlist=wavlist,
                    output_dir=output_dir,
                    prompt_audio_dir=prompt_dir,
                    concatente_audio_name=f"{int(i)+1}",
                    last_utt=False,
                    required_silence_audio_len=required_silence_audio_len,
                    ding_path=ding_path,
                    order_random=order_random,
                )
    else:
        concatenate_multi_audio(
                    wavlist=wavlist,
                    output_dir=output_dir,
                    prompt_audio_dir=prompt_dir,
                    concatente_audio_name="1",
                    last_utt=False,
                    required_silence_audio_len=required_silence_audio_len,
                    ding_path=ding_path,
                    order_random=order_random,
                )

