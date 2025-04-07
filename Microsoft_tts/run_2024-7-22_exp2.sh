#!/bin/bash
stage=0
stop_stage=1000
. path_for_tts.sh
. utils/parse_options.sh


if [ ${stage} -le -1 ] && [ ${stop_stage} -ge -1 ];then
    echo "generate txt format data"
    in_xlsx=data/2024-7-22_exp/text_rawdata_2/words.xlsx
    out_txt=data/2024-7-22_exp/text_rawdata_2/words.txt
    python3 tools/read_xlsx.py $in_xlsx $out_txt
fi
if [ ${stage} -le 0 ] && [ ${stop_stage} -ge 0 ];then
   echo "generate input format data of tts server "
   for name in words prompt;do
    in_txt=data/2024-7-22_exp/text_rawdata_2/$name.txt
    out_xml=data/2024-7-22_exp/exp2/xml/$name
    python3 tools/generate_xml_files.py $in_txt $out_xml
  done
fi

if [ ${stage} -le 1 ] && [ ${stop_stage} -ge 1 ];then
   echo "generate audio via tts server"
   for name in words prompt;do
       in_xml_dir=data/2024-7-22_exp/exp2/xml/$name
       out_audio_dir=data/2024-7-22_exp/exp2/audio/$name
       python3 tools/generate_batch_wavs.py $in_xml_dir $out_audio_dir
   done
fi

if [ ${stage} -le 2 ] && [ ${stop_stage} -ge 2 ];then
   echo "covert mp3 to wav"
   for name in words prompt;do
    in_audio_dir=data/2024-7-22_exp/exp2/audio/$name
    out_audio_dir=exp/2024-7-22_exp/exp2/audio/$name
    python3 tools/mp3_to_wav.py $in_audio_dir $out_audio_dir
  done
fi

if [ ${stage} -le 3 ] && [ ${stop_stage} -ge 3 ];then
   echo "fixed_audio duration lenght in words mode"
   for name in words ;do
      in_audio_dir=exp/2024-7-22_exp/exp2/audio/$name
      out_audio_dir=exp/2024-7-22_exp/exp2/audio/${name}_fix
      required_audio_size_second=2
      python3 tools/fixed_audio_len.py $in_audio_dir $out_audio_dir $required_audio_size_second
   done
fi

if [ ${stage} -le 4 ] && [ ${stop_stage} -ge 4 ];then
   echo "fixed_audio duration lenght in prompt mode"
   for name in prompt ;do
      in_audio_dir=exp/2024-7-22_exp/exp2/audio/$name
      out_audio_dir=exp/2024-7-22_exp/exp2/audio/${name}_fix
      required_audio_size_second=3
      python3 tools/fixed_audio_len.py $in_audio_dir $out_audio_dir $required_audio_size_second
   done
fi

if [ ${stage} -le 6 ] && [ ${stop_stage} -ge 6 ];then

  for name in words ;do
      content_audio_dir=exp/2024-7-22_exp/exp2/audio/${name}_fix
      prompt_dir=exp/2024-7-22_exp/exp2/audio/prompt_fix
      required_silence_audio_len=2
      ding_path=data/2024-7-22_exp/ding_fix/ding_online_fix.wav
      order_random=False
      output_dir=exp/2024-7-22_exp/exp2/audio/${name}_final
      sample_num=5
   python3 tools/concat_audio.py\
       $content_audio_dir \
       $prompt_dir\
       $required_silence_audio_len\
       $ding_path\
       $order_random\
       $output_dir\
       $sample_num

  done
 fi
if [ ${stage} -le 7 ] && [ ${stop_stage} -ge 7 ];then
    in_txt=data/2024-7-22_exp/text_rawdata_2/utts.txt
    out_txt=data/2024-7-22_exp/text_rawdata_2/utts_25_4.txt
    cut_num=25
   python3 tools/prepared_utts.py $in_txt $cut_num $out_txt
fi

if [ ${stage} -le 8 ] && [ ${stop_stage} -ge 8 ];then

  for name in words ;do
      content_audio_dir=exp/2024-7-22_exp/exp2/audio/${name}_fix
      prompt_dir=exp/2024-7-22_exp/exp2/audio/prompt_fix
      required_silence_audio_len=2
      ding_path=data/2024-7-22_exp/ding_fix/ding_online_fix.wav
      order_random=True
      output_dir=exp/2024-7-22_exp/exp2/audio/${name}_final_random
      sample_num=5
   python3 tools/concat_audio.py\
       $content_audio_dir \
       $prompt_dir\
       $required_silence_audio_len\
       $ding_path\
       $order_random\
       $output_dir\
       $sample_num

  done
 fi
