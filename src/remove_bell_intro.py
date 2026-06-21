# 功能：去除片头片尾
# 作者：hanjackcom
# 个人主页：https://hanjack.com

import os
import torch
from faster_whisper import WhisperModel
from pydub import AudioSegment
import torch.hub

INPUT_DIR = "."
OUTPUT_DIR = "clean_audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 片头广告关键词
CUT_KEYS = {"第", "lesson", "课", "听力"}

# 1. 加载ASR语音识别模型
asr_model = WhisperModel("tiny", device="cpu", compute_type="int8")

# 2. 新版Silero VAD加载方式
vad_model, utils = torch.hub.load(
    repo_or_dir='snakers4/silero-vad',
    model='silero_vad',
    force_reload=False,
    onnx=False
)
(get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = utils

def process_mp3(filepath, outpath):
    audio = AudioSegment.from_mp3(filepath)
    total_sec = len(audio) / 1000.0
    wav_np = read_audio(filepath)
    speech_ts = get_speech_timestamps(wav_np, vad_model, sampling_rate=16000)

    # ---------- 第一步：裁掉片头广告/叮声 ----------
    seg_iter, _ = asr_model.transcribe(filepath, word_timestamps=True)
    cut_start = 0.0
    for seg in seg_iter:
        txt = seg.text.lower()
        if any(k in txt for k in CUT_KEYS):
            cut_start = seg.end
        else:
            break
    # VAD兜底：无识别文字时，截取到第一段人声开始
    if cut_start < 0.3 and len(speech_ts) > 0:
        cut_start = speech_ts[0]["start"] / 16000

    # ---------- 第二步：裁掉片尾人声后的叮声 ----------
    cut_end = total_sec
    if len(speech_ts) > 0:
        last_speech_end = speech_ts[-1]["end"] / 16000
        cut_end = last_speech_end + 0.5  # 预留0.5秒课文结尾缓冲

    # 截取音频
    start_ms = int(cut_start * 1000)
    end_ms = int(cut_end * 1000)
    clean_audio = audio[start_ms:end_ms]

    clean_audio.export(outpath, format="mp3", bitrate="128k")
    print(f"处理 {os.path.basename(filepath)} | 起点:{cut_start:.2f}s 终点:{cut_end:.2f}s")

# 批量遍历mp3
for fname in os.listdir(INPUT_DIR):
    if fname.lower().endswith(".mp3"):
        src = os.path.join(INPUT_DIR, fname)
        dst = os.path.join(OUTPUT_DIR, fname)
        process_mp3(src, dst)

print("\n全部处理完成，干净音频输出至 clean_audio 文件夹")